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

# import cv2
# import numpy as np

# class FocusDetector:
#     def __init__(self, model_path="./model_files/res10_300x300_ssd_iter_140000.caffemodel",
#                  config_path="./model_files/deploy.prototxt", confidence_threshold=0.9):
#         self.net = cv2.dnn.readNetFromCaffe(config_path, model_path)
#         self.confidence_threshold = confidence_threshold

#     def is_focused(self, frame):
#         height, width = frame.shape[:2]

#         # Resize + normalize image
#         blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
#                                      (104.0, 177.0, 123.0), False, False)
#         self.net.setInput(blob)
#         detections = self.net.forward()

#         faces = []
#         for i in range(detections.shape[2]):
#             confidence = detections[0, 0, i, 2]
#             print(f"Confidence: {confidence}")
#             if confidence >= self.confidence_threshold:
#                 box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
#                 x1, y1, x2, y2 = box.astype("int")
#                 faces.append((x1, y1, x2 - x1, y2 - y1))

#         is_focused = len(faces) > 0
#         return is_focused, faces
