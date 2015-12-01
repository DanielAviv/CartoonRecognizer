# -*- coding: utf-8 -*-

"""
"""

from feature_extraction import str_to_array

import sys
from os import listdir, remove
from os.path import isfile, join, basename
import argparse

import cv2
import numpy as np
import time

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

#
GROUND_TRUTH_PATH = "..\\Data\\test\\ground_truth.txt"

#
DATA_PATH = "..\\Data\\test\\data"

#
DETECTOR_PATH = "D:\\TrainImages\\eLBP22.xml"

"""
"""
def get_intersection(r1, r2):
	return 100.0*INTERSECT(r1, r2)/UNION(r1, r2)
	
"""
"""
def INTERSECT(r1, r2):
	left = max(r1[0], r2[0])
	right = min(r1[2], r2[2])
	top = max(r1[1], r2[1])
	bottom = min(r1[3], r2[3])

	return AREA([left, top, right, bottom])

"""
"""
def UNION(r1, r2):
	return AREA(r1) + AREA(r2) - INTERSECT(r1, r2)
	
"""
"""
def AREA(r):
	if (r[0] < r[2] and r[1] < r[3]):
		return (r[2] - r[0])*(r[3] - r[1])
	return 0

"""
"""
def create_ground_truth_dict(file_path):
	ground_truth_file = open(file_path)
	ground_truth_dict = {}
	
	for line in ground_truth_file:
		key, value_str = line.split("#")
		value = None
		if value_str[2:-1] != "":
			value = str_to_array(value_str[2:-1])
		else:
			value = []
			
		ground_truth_dict[key] = value
		
	return ground_truth_dict

def main(argv=None):
	true_pos = 0
	false_pos = 0
	false_neg = 0
	amount_of_faces = 0
	exec_time = 0
	
	image_path_coll = [ join(DATA_PATH, image_name) for image_name in listdir(DATA_PATH) if isfile(join(DATA_PATH, image_name)) ]
	classifier = cv2.CascadeClassifier(DETECTOR_PATH)
	
	ground_truth_dict = create_ground_truth_dict(GROUND_TRUTH_PATH)
	
	min_neigh_iter = np.arange(3, 30, 3)
	scale_factor_iter = np.arange(1.1, 1.55, 0.05)
	
	for scale_factor in scale_factor_iter:
		for min_neigh in min_neigh_iter:
			start = time.time()
			for image_path in image_path_coll:
				image = cv2.imread(image_path)
				detected_faces = classifier.detectMultiScale(image, scale_factor, min_neigh, flags=0, minSize=(70, 70))
				
				detected_faces = [(x,y,x+w,y+h) for (x,y,w,h) in detected_faces]
				
				image_name = basename(image_path)
				ground_truth_faces = ground_truth_dict[image_name]
				
				amount_of_faces += len(ground_truth_faces)
				
				match = 0
				"""
				for (x,y,w,h) in detected_faces:
					cv2.rectangle(image,(x,y),(w,h),(255,0,0),2) #AZUL

				for (x,y,w,h) in ground_truth_faces:
					cv2.rectangle(image,(x,y),(w,h),(0,0,255),2) #ROJO
					
				cv2.imshow(basename(image_path),image)
				
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
				"""
				for true_face in ground_truth_faces:
					best_match = None
					best_percentage = 0
					
					for detected_face in detected_faces:
						percentage = get_intersection(detected_face, true_face)

						if (percentage > best_percentage) and (percentage > 50):
							best_match = detected_face
							best_percentage = percentage
							
							if cv2.waitKey(0) & 0xFF == ord('q'):
								break
								
					if (best_percentage == 0):
						false_neg += 1
					else:
						true_pos += 1
						match += 1
						
				false_pos += (len(detected_faces) - match)

			total_pos = (true_pos + false_pos)
				
			if total_pos == 0:
				total_pos = 1
			
			end = time.time()
			precision = float(true_pos)*100/total_pos
			recall = float(true_pos)*100/amount_of_faces
			print "SF=" + str(scale_factor) + ", MN=" + str(min_neigh) + "|| Presicion: " + round(precision, 4) + "%, " + "Recall: " + round(recall, 4) + "%, Exec. time: " + str(end - start) + "sec."

	return 0

if __name__ == "__main__":
	main()