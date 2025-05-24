import cv2
import dlib
import numpy as np
from picamera2 import Picamera2
import time
import math

# Initialize Pi camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (800, 600)})
picam2.configure(config)
picam2.start()
time.sleep(1)

# Load dlib models
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("../model_files/shape_predictor_5_face_landmarks.dat")

# 3D model points (excluding chin)
model_points = np.array([
    (0.0, 0.0, 0.0),             # Nose tip
    (-30.0, 30.0, -30.0),        # Left eye
    (30.0, 30.0, -30.0),         # Right eye
    (-20.0, -30.0, -30.0),       # Left mouth
    (20.0, -30.0, -30.0)         # Right mouth
], dtype="double")

while True:
    frame = picam2.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    faces = detector(gray, 0)
    if len(faces) == 0:
        cv2.putText(frame, "No face detected", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    else:
        face = max(faces, key=lambda r: r.width())  # Use largest face
        shape = predictor(gray, face)
        landmarks = np.array([[p.x, p.y] for p in shape.parts()], dtype="double")

        if landmarks.shape[0] == 5:
            image_points = np.array([
                landmarks[2],  # Nose tip
                landmarks[0],  # Left eye
                landmarks[1],  # Right eye
                landmarks[3],  # Left mouth
                landmarks[4],  # Right mouth
            ], dtype="double")

            # Camera parameters
            height, width = frame.shape[:2]
            focal_length = width
            center = (width / 2, height / 2)
            camera_matrix = np.array([
                [focal_length, 0, center[0]],
                [0, focal_length, center[1]],
                [0, 0, 1]
            ], dtype="double")
            dist_coeffs = np.zeros((4, 1))

            print(f"model_points.shape: {model_points.shape}, image_points.shape: {image_points.shape}")

            success, rvec, tvec = cv2.solvePnP(
                model_points.astype(np.float64),
                image_points.astype(np.float64),
                camera_matrix.astype(np.float64),
                dist_coeffs,
                flags=cv2.SOLVEPNP_EPNP
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

    cv2.imshow("Focus Tracker (5-point)", frame)
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
