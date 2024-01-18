# Jan Szenborn Wiktor Rostkowski , 2024
import cv2
import mediapipe as mp

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
if face_cascade.empty() or eye_cascade.empty():
    raise IOError('Unable to load the cascade classifier xml file')

cap = cv2.VideoCapture(0)

while cap.isOpened():
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in face_rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 120, 0), 3)
        eye_gray = gray[y:y + h, x:x + w]
        eye_color = frame[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(eye_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(eye_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('Face dector', frame)
    if cv2.waitKey(5) == 27:
        break

cap.release()
