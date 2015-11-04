# -*- coding: utf-8 -*-

"""
"""

import sys
from os import listdir, rename
from os.path import isfile, join, splitext

import cv2

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"


directory_path = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\DetectorTrainingPositive"
only_files = [ join(directory_path, file) for file in listdir(directory_path) if isfile(join(directory_path, file)) ]

sum_height = 0
sum_width = 0
sum_relation = 0

for file in only_files:
	image = cv2.imread(file, 0)
	sum_height = sum_height + image.shape[0]
	sum_width = sum_width + image.shape[1]
	sum_relation = sum_relation + (float(image.shape[1]) / float(image.shape[0]))
	
print "Mean height: " + str(float(sum_height) / len(only_files))
print "Mean width: " + str(float(sum_width) / len(only_files))
print "Mean relation (h/w): 1/" + str(float(sum_relation) / len(only_files))