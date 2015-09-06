# -*- coding: utf-8 -*-

"""
This is an almost exact copy of the example found in:
http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
"""

import numpy as np
import cv2

cap = cv2.VideoCapture('D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\Dataset1\\data0000.mkv')

# Dont know wtf is happening here 
# print cap.set(0,1000000)
# print cap.set(5,60)

while(cap.isOpened()):
    ret, frame = cap.read()

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("asasd")