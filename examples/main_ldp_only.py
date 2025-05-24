from picamera2 import Picamera2
import cv2
import numpy as np
import time

# Initialize camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (800, 600)})
picam2.configure(config)
picam2.start()
time.sleep(1)

# Load LBP face detector (frontal only)
face_cascade = cv2.CascadeClassifier("../model_files/lbpcascade_frontalface.xml")

while True:
    frame = picam2.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        status = "Focused"
        color = (0, 255, 0)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    else:
        status = "Distracted"
        color = (0, 0, 255)

    # Display status
    cv2.putText(frame, f"Status: {status}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("LBP Focus Tracker", frame)
    if cv2.waitKey(1) == 27:  # ESC to quit
        break

cv2.destroyAllWindows()
