import subprocess
import os
import signal
import time
import threading

class CameraStream:
    """
    Streams local webcam via FFmpeg over UDP
    """

    def __init__(self, device_name="HD Web Camera", resolution="640x320", framerate=30, udp_ip="127.0.0.1", udp_port=12345):
        self.device_name = device_name
        self.resolution = resolution
        self.framerate = framerate
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.process = None

    def start(self):
        if self.process is not None:
            print("Camera stream already running.")
            return

        ffmpeg_cmd = [
            "ffmpeg",
            "-f", "dshow",
            "-video_size", self.resolution,
            "-framerate", str(self.framerate),
            "-i", f'video={self.device_name}',
            "-preset", "ultrafast",
            "-tune", "zerolatency",
            "-c:v", "libx264",
            "-f", "mpegts",
            f"udp://{self.udp_ip}:{self.udp_port}"
        ]

        # Start FFmpeg in a separate thread
        def run_ffmpeg():
            self.process = subprocess.Popen(
                ffmpeg_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP  # Windows safe
            )
            # Do NOT call wait() here

        thread = threading.Thread(target=run_ffmpeg, daemon=True)
        thread.start()
        print(f"[CameraStream] Started streaming to udp://{self.udp_ip}:{self.udp_port}")


    def stop(self):
        """
        Stop the streaming process
        """
        if self.process:
            os.kill(self.process.pid, signal.SIGTERM)
            self.process = None
            print("[CameraStream] Stream stopped.")

    def get_stream_url(self):
        """
        Return the URL for the stream
        """
        return f"udp://@{self.udp_ip}:{self.udp_port}"
