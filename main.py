import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import mediapipe as mp

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)


# Define a function to check posture
def check_posture(landmarks):
    if landmarks is None:
        return False  # No landmarks detected

    # Get relevant landmark coordinates
    neck = landmarks[mp_pose.PoseLandmark.NOSE.value]
    mid_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    back = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

    # Check if the neck and shoulders form a straight line
    neck_y = neck.y
    mid_shoulder_y = mid_shoulder.y
    back_y = back.y

    # Simple check for posture: if neck is above shoulder points, posture is correct
    if neck_y < mid_shoulder_y and neck_y < back_y:
        return True  # Posture is correct
    return False  # Posture is incorrect


# Function to process video stream
def process_video():
    ret, frame = cap.read()
    if ret:
        # Convert the frame to RGB for MediaPipe processing
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(image_rgb)

        # Draw landmarks and check posture
        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark
            cv2.circle(frame, (int(landmarks[mp_pose.PoseLandmark.NOSE.value].x * frame.shape[1]),
                               int(landmarks[mp_pose.PoseLandmark.NOSE.value].y * frame.shape[0])), 5, (0, 255, 0), -1)
            cv2.circle(frame, (int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * frame.shape[1]),
                               int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * frame.shape[0])), 5,
                       (0, 255, 0), -1)
            cv2.circle(frame, (int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * frame.shape[1]),
                               int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * frame.shape[0])), 5,
                       (0, 255, 0), -1)

            # Check posture
            if check_posture(landmarks):
                cv2.putText(frame, "Posture: Correct", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Posture: Incorrect", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Convert the frame to an ImageTk format
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)

    label.after(10, process_video)


# Initialize the main Tkinter window
root = tk.Tk()
root.title("Posture Checker")

# Set up video capture
cap = cv2.VideoCapture(0)

# Create a label to display video frames
label = tk.Label(root)
label.pack()

# Start video processing
process_video()

# Run the Tkinter event loop
root.mainloop()

# Release the video capture when done
cap.release()
cv2.destroyAllWindows()

