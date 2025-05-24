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

# Load Haar face detector
face_cascade = cv2.CascadeClassifier("../model_files/haarcascade_frontalface_alt2.xml")

while True:
    # Capture and convert frame
    frame = picam2.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        # Assume focused if at least one frontal face is detected
        focused = True
        status = "Focused"
        color = (0, 255, 0)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    else:
        focused = False
        status = "Distracted"
        color = (0, 0, 255)

    # Overlay status
    cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # Show frame
    cv2.imshow("Focus Detection (Haar Only)", frame)
    if cv2.waitKey(1) == 27:  # ESC to quit
        break

cv2.destroyAllWindows()
