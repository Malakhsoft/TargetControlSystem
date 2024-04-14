import cv2
import numpy as np
import time

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

explosion_img = cv2.imread('explosion.png', cv2.IMREAD_UNCHANGED)

cap = cv2.VideoCapture(0)

KNOWN_DISTANCE = 5.0

KNOWN_FACE_WIDTH = 0.4583  # Average face width in feet

target_style = 'square'

target_locked = False
eliminate_target = False

blink_count = 0
show_message = True

explosion_start_time = None
explosion_duration = 3  # in seconds

def draw_f14_target(img, center, radius, color, thickness):
    for i in range(5):
        cv2.circle(img, center, int(radius*(1-i*0.1)), color, thickness)

def draw_submarine_target(img, x, y, w, h, color, thickness):
    cv2.line(img, (x, y), (x + w, y + h), color, thickness)
    cv2.line(img, (x, y + h), (x + w, y), color, thickness)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (800, 600))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face_center = (x + w // 2, y + h // 2)
        face_radius = (w + h) // 4

        if target_style == 'f14':
            draw_f14_target(frame, face_center, face_radius, (0, 255, 0), 2)
        elif target_style == 'square':
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        elif target_style == 'submarine':
            draw_submarine_target(frame, x, y, w, h, (0, 255, 0), 2)

        face_width_in_frame = w
        distance = (KNOWN_FACE_WIDTH * KNOWN_DISTANCE) / face_width_in_frame
        distance_feet = distance * 3.28084

        cv2.putText(frame, f'{distance_feet:.2f} ft', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        target_locked = True
        cv2.putText(frame, "Target Locked", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        blink_count += 1
        if blink_count % 30 == 0:
            show_message = not show_message
        if show_message:
            text_size = cv2.getTextSize("Press Spacebar to Eliminate", cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = (frame.shape[1] - text_size[0]) // 2
            text_y = (frame.shape[0] + text_size[1]) // 2
            cv2.putText(frame, "Press Spacebar to Eliminate", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        if eliminate_target:
            explosion_resized = cv2.resize(explosion_img, (w, h))
            overlay = explosion_resized[:, :, 0:3]
            alpha = explosion_resized[:, :, 3] / 255.0
            added_image = cv2.addWeighted(frame[y:y+h, x:x+w], 1, overlay, 0.7, 0)
            frame[y:y+h, x:x+w] = added_image

            explosion_start_time = time.time()
            eliminate_target = False

    if explosion_start_time is not None and time.time() - explosion_start_time > explosion_duration:
        explosion_start_time = None

    for i, (key, note) in enumerate(notes.items()):
        cv2.putText(frame, f'{key}: {note}', (10, 20 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow('Face Detection', frame)

    key = cv2.waitKey(1)
    if key == ord('1'):
        target_style = 'f14'
    elif key == ord('2'):
        target_style = 'square'
    elif key == ord('3'):
        target_style = 'submarine'
    elif key == ord(' '):
        eliminate_target = True
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
