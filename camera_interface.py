import cv2
from picamera2 import Picamera2
import time

class CameraInterface:
    def __init__(self, resolution=(800, 600)):
        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration(
            main={"format": "RGB888", "size": resolution}
            )
        self.picam2.configure(config)
        self.picam2.start()
        time.sleep(1)

    def get_frame(self):
        frame = self.picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        return frame, gray
