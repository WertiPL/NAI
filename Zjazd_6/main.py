# Jan Szenborn Wiktor Rostkowski , 2024

import cv2
import mediapipe as mp
from videoplayer import Video
import pygame

pygame.init()

WIDTH, HEIGHT = 900, 900

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


def detect_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
    return len(face_rects) > 0


def detect_eyes(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray)
    return len(eyes) > 0


def detect_pose(frame, pose):
    frame.flags.writeable = False
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)
    frame.flags.writeable = True
    return results.pose_landmarks is not None


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
if face_cascade.empty() or eye_cascade.empty():
    raise IOError('Unable to load the cascade classifier xml file')

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# File Path ADS
file_path = 'Volvo_Trucks_Advertisement.mp4'

# Start ADS


detect = 0
cap = cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        _, frame = cap.read()

        face_detected = detect_face(frame)
        eyes_detected = detect_eyes(frame)
        pose_detected = detect_pose(frame, pose)

        # Draw rectangles or landmarks on the frame based on detection results
        if face_detected or eyes_detected and pose_detected:
            if detect == 0:
                video_player = Video(file_path)
                video_player.set_size((900, 900))
                video_player.draw(SCREEN, (0, 0))
                detect = 1

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in face_rects:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 120, 0), 3)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            eyes = eye_cascade.detectMultiScale(gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_drawing.draw_landmarks(
                frame_rgb,
                pose.process(frame_rgb).pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )
            frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

        else:
            if detect == 1:
                print("Pause ...")

                video_player.close()
                detect = 0


        # Display the frame with detection results
        cv2.imshow('Active Ads', frame)

        if cv2.waitKey(5) == 27:
            break

video_player.close()
cap.release()
cv2.destroyAllWindows()
