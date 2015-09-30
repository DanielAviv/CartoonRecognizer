# -*- coding: utf-8 -*-

"""
This is an almost exact copy of the example found in:
http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
"""

import numpy as np
import cv2

video_path = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\Dataset1\\data0000.mkv"
video = cv2.VideoCapture(video_path)

while(video.isOpened()):
    ret, frame = video.read()

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

print("Finished")