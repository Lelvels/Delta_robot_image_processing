from ctypes import sizeof
from math import sqrt
import cv2
import numpy as np

import time
import math

cap = cv2.VideoCapture(0)  # gán cam
start_time = time.time()
xMax, yMax, wMax, hMax = 0, 0, 0, 0
xNext, yNext = 0, 0
xNext_new, yNext_new = 0, 0
x_old, y_old = 0, 0
v, v_x, v_y = 0, 0, 0

t = 1.5
step = 5
while True:
    _, frame = cap.read()  # đọc
    # print( frame.shape) 480 640
    # Belt
    y_start = 210
    y_stop = 338
    x_start = 50
    x_stop = 534
    belt = frame[y_start:y_stop,x_start:x_stop]  # cắt
    gray_belt = cv2.cvtColor(belt, cv2.COLOR_BGR2GRAY)  # đổi qua xám
    _, threshold = cv2.threshold(gray_belt, 120, 255, cv2.THRESH_BINARY)  # từ xám lấy nhị phân

    # Detect the Nuts
    contours, _ = cv2.findContours(
        threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # tìm đường bao

    areaMax = 0

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)  # khoanh vùng nhị phân

        # Calculate area
        area = cv2.contourArea(cnt)

        # Distinguish small and big nuts
        if (area > areaMax) & (area > 2000):
            areaMax = area
            xMax, yMax, wMax, hMax, = x, y, w, h

    cv2.rectangle(belt, (xMax, yMax),
                  (xMax + wMax, yMax + hMax), (0, 0, 255), 2)

    xNext = int(xMax + v_x*t)
    yNext = int(yMax + v_y*t)
    cv2.rectangle(belt, (xNext, yNext),
                  (xNext + wMax, yNext + hMax), (255, 0, 0), 2)
    cv2.putText(belt, str(areaMax), (xMax, yMax), 1, 1, (0, 255, 0))

    x_new, y_new = ((xMax + wMax)/2.0), ((yMax + hMax)/2.0)
    xNext_new, yNext_new = ((xNext + wMax)/2.0), ((yNext + hMax)/2.0)

    end_time = time.time()

    if end_time-start_time >= 1.0/step:
        s = sqrt((x_new-x_old)**2 + (y_new-y_old) ** 2)
        v = int(s/(1.0/step))
        v_x = int((x_new-x_old)/(1.0/step))
        v_y = int((y_new-y_old)/(1.0/step))
        x_old, y_old = x_new, y_new
        # cv2.putText(belt, str(v), (x_new, y_new), 1, 1, (0, 255, 0))

        start_time = time.time()
        print(" x= " + str(x_new) + " y= " + str(y_new) + " v= " + str(v)+" v_x= " +
              str(v_x)+" v_y= " + str(v_y) + " xNext= " + str(xNext_new) + " yNext= " + str(yNext_new))

    cv2.imshow("Frame", frame)
    cv2.imshow("belt", belt)
    cv2.imshow("threshold", threshold)  

    key = cv2.waitKey(1)
    if key == 27:
        break
    # stop = ctrl+[
cap.release()
cv2.destroyAllWindows()
