# -*- coding: utf-8 -*-

"""

"""

import numpy as np
import cv2

def rectanglify(img,x, y, w, h):
	cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

cap = cv2.VideoCapture('D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\Dataset2\\data0000.mkv')


print cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES,22731)

asdf = [[1562 ,  69 ,  76   ,88],
 [ 794 , 374 , 310 , 361]]

ret, frame = cap.read()
	#asdf = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
	#cap.set(cv2.cv.CV_CAP_PROP_POS_MSEC, asdf*10)

for wea in asdf:
	rectanglify(frame, wea[0], wea[1], wea[2], wea[3])

#resized_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
cv2.imshow('frame',frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

cap.release()

print("asasd")