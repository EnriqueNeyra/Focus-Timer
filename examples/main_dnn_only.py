from picamera2 import Picamera2
import cv2
import numpy as np
import time

# Load OpenCV DNN face detector
net = cv2.dnn.readNetFromCaffe("../model_files/deploy.prototxt", "../model_files/res10_300x300_ssd_iter_140000.caffemodel")

# Initialize camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (800, 600)})
picam2.configure(config)
picam2.start()
time.sleep(1)

# Confidence threshold for attention detection
FOCUS_THRESHOLD = 0.8

while True:
    frame = picam2.capture_array()
    height, width = frame.shape[:2]

    # DNN face detection
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], False, False)
    net.setInput(blob)
    detections = net.forward()

    status = "Distracted"
    color = (0, 0, 255)

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > FOCUS_THRESHOLD:
            box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            x1, y1, x2, y2 = box.astype("int")

            # Draw detection box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Mark as focused
            status = "Focused"
            color = (0, 255, 0)

            # Only use the first confident face
            break

    # Overlay status
    cv2.putText(frame, f"Status: {status}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Focus Detection (DNN Confidence)", frame)
    if cv2.waitKey(1) == 27:  # ESC to quit
        break

cv2.destroyAllWindows()
