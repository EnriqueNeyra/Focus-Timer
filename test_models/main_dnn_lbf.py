import cv2
import numpy as np
import math
from picamera2 import Picamera2
import time

# Load OpenCV DNN face detector
net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")

# Load FacemarkLBF landmark model
facemark = cv2.face.createFacemarkLBF()
facemark.loadModel("lbfmodel.yaml")

# Initialize Pi camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (800, 600)})
picam2.configure(config)
picam2.start()
time.sleep(1)

# 3D model points (used with solvePnP)
model_points = np.array([
    (0.0, 0.0, 0.0),             # Nose tip (30)
    (0.0, -63.6, -12.5),         # Chin (8)
    (-43.3, 32.7, -26.0),        # Left eye (36)
    (43.3, 32.7, -26.0),         # Right eye (45)
    (-28.9, -28.9, -24.1),       # Left mouth (48)
    (28.9, -28.9, -24.1)         # Right mouth (54)
], dtype="double")

while True:
    frame = picam2.capture_array()
    height, width = frame.shape[:2]

    # Face detection
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], False, False)
    net.setInput(blob)
    detections = net.forward()

    faces = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.6:
            box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            x1, y1, x2, y2 = box.astype("int")
            faces.append((x1, y1, x2 - x1, y2 - y1))

    if not faces:
        cv2.putText(frame, "No face detected", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    else:
        _, landmarks = facemark.fit(frame, np.array(faces))
        for face, landmark in zip(faces, landmarks):
            shape = landmark[0]  # (68, 2)

            image_points = np.array([
                shape[30],  # Nose tip
                shape[8],   # Chin
                shape[36],  # Left eye
                shape[45],  # Right eye
                shape[48],  # Left mouth
                shape[54],  # Right mouth
            ], dtype="double")

            # Camera calibration matrix
            focal_length = width
            center = (width / 2, height / 2)
            camera_matrix = np.array([
                [focal_length, 0, center[0]],
                [0, focal_length, center[1]],
                [0, 0, 1]
            ], dtype="double")
            dist_coeffs = np.zeros((4, 1))

            if image_points.shape[0] == 6:
                success, rvec, tvec = cv2.solvePnP(
                    model_points, image_points, camera_matrix, dist_coeffs,
                    flags=cv2.SOLVEPNP_ITERATIVE
                )

                if success:
                    yaw = math.degrees(rvec[1][0])
                    pitch = math.degrees(rvec[0][0])
                    focused = abs(yaw) < 25 and abs(pitch) < 20
                    color = (0, 255, 0) if focused else (0, 0, 255)
                    status = "Focused" if focused else "Distracted"

                    cv2.putText(frame, f"Yaw: {int(yaw)}°", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    cv2.putText(frame, f"Pitch: {int(pitch)}°", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    cv2.putText(frame, status, (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

                    for (x, y) in image_points:
                        cv2.circle(frame, (int(x), int(y)), 3, color, -1)

                    x, y, w, h = face
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    cv2.imshow("Focus Tracker (DNN + LBF 6pts)", frame)
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
