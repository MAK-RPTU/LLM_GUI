# flask_camera.py
import cv2
import io
import datetime
import pytz
import threading
from flask import Flask, Response
from PIL import Image, ImageDraw, ImageFont

class FlaskCameraServer:
    def __init__(self, host="0.0.0.0", port=8000, camera_index=0):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.camera = cv2.VideoCapture(camera_index)
        if not self.camera.isOpened():
            raise RuntimeError("❌ Could not open webcam. Try another index.")

        # Routes
        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule("/video_feed", "video_feed", self.video_feed)

    def generate_frames(self):
        font_path = "C:/Windows/Fonts/arial.ttf"
        font = ImageFont.truetype(font_path, size=30)
        while True:
            success, frame = self.camera.read()
            if not success:
                break
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)

            # Timestamp overlay
            draw = ImageDraw.Draw(img)
            local_timezone = pytz.timezone("Europe/Berlin")
            # local_timezone = pytz.timezone("Asia/Karachi")
            timestamp = datetime.datetime.now(local_timezone).strftime('%d-%m-%Y %H:%M:%S')
            draw.text((5, 5), f"Cam - {timestamp}", fill="black", font=font)

            # Convert to JPEG
            stream = io.BytesIO()
            img.save(stream, format="JPEG")
            stream.seek(0)
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + stream.read() + b"\r\n")
            stream.close()

    def video_feed(self):
        return Response(self.generate_frames(),
                        mimetype="multipart/x-mixed-replace; boundary=frame")

    def index(self):
        return "<html><body><h1>Webcam Stream</h1><img src='/video_feed'></body></html>"

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False)

    def run_in_background(self):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()
