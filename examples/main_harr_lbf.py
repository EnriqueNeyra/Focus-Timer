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

# Load face detector and landmark model
face_cascade = cv2.CascadeClassifier("../model_files/haarcascade_frontalface_default.xml")
facemark = cv2.face.createFacemarkLBF()
facemark.loadModel("../model_files/lbfmodel.yaml")  # Ensure this file is in your project directory

# 3D model points for head pose estimation
model_points = np.array([
    (0.0, 0.0, 0.0),             # Nose tip
    (0.0, -63.6, -12.5),         # Chin
    (-43.3, 32.7, -26.0),        # Left eye corner
    (43.3, 32.7, -26.0),         # Right eye corner
    (-28.9, -28.9, -24.1),       # Left mouth
    (28.9, -28.9, -24.1)         # Right mouth
], dtype="double")

while True:
    # Capture frame and convert to grayscale
    frame = picam2.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        # Ensure correct format for facemark
        faces_for_fit = np.array(faces, dtype=np.int32)

        for (x, y, w, h) in faces_for_fit:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        ok, landmarks = facemark.fit(gray, faces_for_fit)
        print(f"[DEBUG] facemark.fit() success: {ok}, landmarks: {len(landmarks) if landmarks else 0}")

        if ok and len(landmarks) > 0 and landmarks[0].shape == (1, 68, 2):
            shape = landmarks[0][0]

            # Draw landmark points
            for (x, y) in shape:
                cv2.circle(frame, (int(x), int(y)), 2, (0, 255, 0), -1)

            image_points = np.array([
                shape[30],  # Nose tip
                shape[8],   # Chin
                shape[36],  # Left eye
                shape[45],  # Right eye
                shape[48],  # Left mouth
                shape[54]   # Right mouth
            ], dtype="double")

            # Camera internals
            height, width = frame.shape[:2]
            focal_length = width
            center = (width / 2, height / 2)
            camera_matrix = np.array([
                [focal_length, 0, center[0]],
                [0, focal_length, center[1]],
                [0, 0, 1]
            ], dtype="double")
            dist_coeffs = np.zeros((4, 1))  # No lens distortion

            success, rotation_vector, translation_vector = cv2.solvePnP(
                model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
            )
            print(f"[DEBUG] solvePnP() success: {success}, rotation_vector: {rotation_vector}, translation_vector: {translation_vector}")

            if success:
                yaw = rotation_vector[1] * 180.0 / np.pi
                pitch = rotation_vector[0] * 180.0 / np.pi

                focused = abs(yaw) < 25 and abs(pitch) < 20
                color = (0, 255, 0) if focused else (0, 0, 255)
                status = "Focused" if focused else "Distracted"

                cv2.putText(frame, f"Pitch: {int(pitch)}°", (20, 0), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                cv2.putText(frame, f"Yaw: {int(yaw)}°", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                cv2.putText(frame, status, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # Show the frame
    cv2.imshow("Head Pose Tracker", frame)
    if cv2.waitKey(1) == 27:  # ESC to quit
        break

cv2.destroyAllWindows()
