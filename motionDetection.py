import threading
import winsound

import cv2
import imutils
import numpy as np
import objectDetection as od

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, 500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (5, 5), 0.5)

alarm = False
alarm_mode = False
alarm_counter = 0


def beep_alarm():
    global alarm
    for _ in range(1):
        if not alarm_mode:
            break
        print("Alarm")
        winsound.Beep(2500, 1000)
    alarm = False


while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, 500)
    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0.5)

        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]

        start_frame = frame_bw

        if threshold.sum() > 300:
            alarm_counter += 1
            dilated = cv2.dilate(threshold, None, iterations=3)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                if cv2.contourArea(contour) > 300:
                    (x, y, h, w) = cv2.boundingRect(contour)
                    cropped_img = frame[y:y + h, x:x + w]
                    cv2.imshow("img", cropped_img)
                    print("img type is ",type(cropped_img))
                    for i in od.detect_object(cropped_img):
                        print(i[:2])
        else:
            if alarm_counter > 0:
                alarm_counter -= 1

        cv2.imshow("cam", threshold)
    else:
        cv2.imshow("cam", frame)

    if alarm_counter > 10:
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm).start()

    key_pressed = cv2.waitKey(20)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord("q"):
        alarm_mode = False
        break

cap.release()
cv2.destroyAllWindows()
