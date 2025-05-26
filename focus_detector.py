import cv2
from picamera2 import Picamera2
import time

class FocusDetector:
    def __init__(self, cascade_path=None):
        if cascade_path is None:
            cascade_path = "./model_files/haarcascade_frontalface_alt2.xml"
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

    def is_focused(self, frame_gray):
        faces = self.face_cascade.detectMultiScale(frame_gray, scaleFactor=1.05, minNeighbors=5)
        return len(faces) > 0, faces