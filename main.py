import time

import cv2
import imutils

# import motionDetection as md
import objectDetection as od
import messageTrigger as mt
import myUtils as util
from firebase.firebase import stop_listener, update_status

import firebase.settings as s
# required Global variables
MINIMUM_FRAME_PERCENTAGE = 2
MAXIMUM_FRAME_PERCENTAGE = 20
OBJECT_ACCURACY_PERCENTAGE = 50
_UNKNOWN_OBJECT_ACCURACY_ = 65
# s.ALARM_MODE = True

HIGH_PRIORITY_OBJECTS = ['person',
                         'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
                         'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'zebra']

# Setting camera properties and taking inputs...
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

_, frame1 = cap.read()

print("Starting Application....\nOptions: \n 1. Press 't' for Toggle Alarm Mode. \n 2. Press 'q' for stop execution. ")
update_status(1 if s.ALARM_MODE else 0)


# Resizing the image
frame1 = imutils.resize(frame1, width=300)

# Image pre-processing
img1 = util.image_preprocess(frame1)

# calculating the no of pixels
h, w = frame1.shape[:2]
MINIMUM_FRAME_PERCENTAGE = h * w * MINIMUM_FRAME_PERCENTAGE / 100
MAXIMUM_FRAME_PERCENTAGE = h * w * MAXIMUM_FRAME_PERCENTAGE / 100

while True:
    _, frame2 = cap.read()
    frame2 = imutils.resize(frame2, width=300)
    cam = frame2
    if s.ALARM_MODE:
        img2 = util.image_preprocess(frame2)
        difference = cv2.absdiff(img1, img2)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]

        frame1 = frame2
        img1 = img2
        cam = difference
        # cv2.imshow("threshold", cam)
        # cv2.waitKey(1)

        if threshold.sum() > MINIMUM_FRAME_PERCENTAGE:

            dilated = cv2.dilate(threshold, None, iterations=3)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                (x, y, h, w) = cv2.boundingRect(contour)
                cropped_img = frame2[y:y + h, x:x + w]
                # cv2.imshow("img", cropped_img)

                for i in od.detect_object(cropped_img):
                    name, accuracy = i[:2]
                    # finding the difference between high priority and low priority
                    #  notification type and send the data to the methods which handle
                    #  the data insertion and triggering messages.
                    if name in HIGH_PRIORITY_OBJECTS and accuracy >= OBJECT_ACCURACY_PERCENTAGE or threshold.sum() > MAXIMUM_FRAME_PERCENTAGE:
                        if name not in HIGH_PRIORITY_OBJECTS and accuracy < _UNKNOWN_OBJECT_ACCURACY_:
                            name = 'unknown'
                        # todo: pass the objects to a method
                        # mt.send_high_alert(name, i[1], i[2]) # edited on 2/6/23
                        mt.send_high_alert(name, i[1], frame1)
                    else:
                        pass

                        if name not in HIGH_PRIORITY_OBJECTS and accuracy < _UNKNOWN_OBJECT_ACCURACY_:
                            name = 'unknown'
                        mt.send_low_alert(name, i[1], i[2])
    # time.sleep(0.5)
    cv2.imshow("threshold", cam)
    key_pressed = cv2.waitKey(1)
    if key_pressed == ord("t"):
        s.ALARM_MODE = not s.ALARM_MODE
        print(f"-------> Toggle Alarm Mode... : {s.ALARM_MODE} <--------")
    if key_pressed == ord("q"):
        s.ALARM_MODE = False
        update_status(-1)
        stop_listener()
        print("--------> Ending Process... <--------")
        break


h, w = frame1.shape[:2]
print(f" h = {h}, w = {w}")
print(f'ratio 20% is {h * w * 20 / 100}')
print('Closing Application...')


