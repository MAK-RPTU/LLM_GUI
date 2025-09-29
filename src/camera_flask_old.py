import cv2
import io
import datetime
import pytz
from flask import Flask, Response
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

# Initialize webcam (0 = default camera; you can try 1,2,... if multiple webcams)
camera = cv2.VideoCapture(0)

# Check if camera opened successfully
if not camera.isOpened():
    raise RuntimeError("Could not open webcam. Try changing cv2.VideoCapture(0) to cv2.VideoCapture(1).")

def generate_frames():
    # Path to a .ttf font file (change path if not available on Windows)
    font_path = "C:/Windows/Fonts/arial.ttf"
    font = ImageFont.truetype(font_path, size=30)

    while True:
        # Capture frame from webcam
        success, frame = camera.read()
        if not success:
            break

        # Convert OpenCV frame (BGR) → PIL Image (RGB)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)

        # Add timestamp overlay
        draw = ImageDraw.Draw(img)
        local_timezone = pytz.timezone("Europe/Berlin")
        # local_timezone = pytz.timezone("Asia/Karachi")
        timestamp = datetime.datetime.now(local_timezone).strftime('%d-%m-%Y %H:%M:%S')
        draw.text((5, 5), f"Cam - {timestamp}", fill="black", font=font)

        # Convert back to JPEG
        stream = io.BytesIO()
        img.save(stream, format="JPEG")
        stream.seek(0)

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + stream.read() + b"\r\n")
        stream.close()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route('/')
def index():
    return "<html><body><h1>Webcam Stream</h1><img src='/video_feed'></body></html>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
