# -*- coding: utf-8 -*-

"""
"""

import feature_extraction
import sys
from os import listdir, remove
from os.path import isfile, join
from os.path import join, basename, splitext

import cv2

def calc_distance(v1, v2):
	return cv2.compareHist(v1, v2, cv2.cv.CV_COMP_INTERSECT)
	
caras_path = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\DetectorTrainingPositive"

all_caras = [ join(caras_path, data) for data in listdir(caras_path) if isfile(join(caras_path, data)) ]

kashima_path = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\mikorin.png"
kashima = cv2.imread(kashima_path)
b = feature_extraction.hue_histogram_zone(kashima, 32)

kashima_train_path = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\DetectorTrainingPositive\\Screenshot_92.png"
kashima_train = cv2.imread(kashima_train_path)
d = feature_extraction.hue_histogram_zone(kashima_train, 32)

min_distance = sys.maxint
best_match = None

for cara in all_caras:
	imagen = cv2.imread(cara)
	a =feature_extraction.hue_histogram_zone(imagen, 32)

	c = calc_distance(a, b)
	if  min_distance > c:
		min_distance = c
		best_match = imagen

print calc_distance(b, d)
print min_distance		
cv2.imshow('frame',best_match)
cv2.waitKey(0)
cv2.destroyAllWindows()