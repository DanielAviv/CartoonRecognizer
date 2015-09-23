# -*- coding: utf-8 -*-

"""
This is an almost exact copy of the example found in:
http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
"""

import numpy as np
import cv2

def rectanglify(img,x, y, w, h):
	cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

cap = cv2.VideoCapture('D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\Dataset2\\data0000.mkv')


print cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES,30121)


ret, frame = cap.read()
	#asdf = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
	#cap.set(cv2.cv.CV_CAP_PROP_POS_MSEC, asdf*10)

rectanglify(frame, 446 ,214,  66 , 66)


cv2.imshow('frame',frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

cap.release()

print("asasd")