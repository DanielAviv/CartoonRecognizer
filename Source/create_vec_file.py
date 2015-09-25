# -*- coding: utf-8 -*-

"""
This executable detects the faces of the characters in the frames in the database.
"""

from os import listdir
from os.path import isfile, join

import cv2

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

data_path = "D:\\DetectorTraining"
positive_img = [ (join(data_path, img)) for img in listdir(data_path) if isfile(join(data_path, img)) ]

output_file = open("anime_faces.info", "a")

for each_positive in positive_img:
	output_file.write(each_positive)
	output_file.write(" 1 0 0 ")
	
	image = cv2.imread(each_positive)
	
	rows, columns, channels = image.shape
	output_file.write(str(columns) + " " + str(rows) + "\n")

output_file.close()