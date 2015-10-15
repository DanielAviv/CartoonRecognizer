# -*- coding: utf-8 -*-

"""
This module computes the feature from the detected faces by the module of detection.
"""

import sys
import argparse
from random import randint

import cv2
from numpy import concatenate

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

#
INPUT_PATH = "detection_output.txt"

#
OUTPUT_PATH = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Results\\Features1"

"""
"""
def str_to_array(array_string):
	string_array = array_string.split(";")
	result = [ map(int, array[1:-1].split()) for array in string_array ]
	return result

"""
"""
def parse_input_file(lines):
	data_lines = lines[1:]
	
	#This extracts the lines in the file in odd and even positions,
	#removes the unnecessary characters and parses them as readable data.
	frames = [ float(lines[:-1]) for lines in data_lines[::2] ]
	faces = [ str_to_array(lines[:-2]) for lines in data_lines[1::2] ]
	
	file_dictionary = dict(zip(frames, faces))
	return file_dictionary
	
"""
"""
def calc_descriptor(data_dictionary, video_path):
	result = []
	
	for frame_pos, faces in data_dictionary.iteritems():
		video = cv2.VideoCapture(video_path)
		video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frame_pos)
		ret, frame = video.read()
			
		for face in faces:
			x, y, w, h = face
			#histogram = hue_histogram(frame[y:y+h, x:x+w], 32)
			#histogram = hue_histogram_zone(frame[y:y+h, x:x+w], 32)
			patches = rand_patch(frame[y:y+h, x:x+w], 10, )
			
		video.release()
		break

	return 0

"""
"""
def hue_histogram(image, bins):
	cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	hist = cv2.calcHist([image], [0], None, [bins], [0,179])
	hist_normed = hist/sum(hist)
	
	return hist_normed
	
"""
"""
def hue_histogram_zone(image, bins):
	cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	rows, cols, channels = image.shape
	
	a = image[:rows/2, :cols/2]
	b = image[rows/2:, :cols/2]
	c = image[:rows/2, cols/2:]
	d = image[rows/2:, cols/2:]
	
	hist_a = cv2.calcHist([a], [0], None, [bins], [0,179])
	hist_b = cv2.calcHist([b], [0], None, [bins], [0,179])
	hist_c = cv2.calcHist([c], [0], None, [bins], [0,179])
	hist_d = cv2.calcHist([d], [0], None, [bins], [0,179])
	full_hist = hue_histogram(image, bins)
	
	hist_a_normed = hist_a/sum(hist_a)
	hist_b_normed = hist_b/sum(hist_b)
	hist_c_normed = hist_c/sum(hist_c)
	hist_d_normed = hist_d/sum(hist_d)
	full_hist_normed = full_hist/sum(full_hist)
	
	all_hist = (hist_a_normed, hist_b_normed, hist_c_normed, hist_d_normed, full_hist_normed)
	return concatenate(all_hist, axis=0)

"""
"""
def rand_patch(image, amount, size):
	rows, cols, channels = image.shape
	#I arbitrarly defined the patch size as a fraction of the height.
	patch_size = image.shape[0]/size
	patches = []
	
	for i in range(0, amount):
		rand_row = randint(0, rows - patch_size)
		rand_col = randint(0, cols - patch_size)
		
		patch = image[rand_row:rand_row + patch_size, rand_col:rand_col + patch_size]
		#Another arbitrary desition.
		resized_patch = cv2.resize(patch, (15, 15))
		
		patches.append(resized_patch)
		
	return patches
		

def main(argv=None):
	input_path = INPUT_PATH
	
	if INPUT_PATH == "":
		print("Where is the input file located?")
		input_path = sys.stdin.readline()
	
	input_file = None
	
	try:
		input_file = open(INPUT_PATH, "r")

		file_results = []
		for line in input_file:	
			if line.startswith("ENDFILE"):
				parsed_data = parse_input_file(file_results)
				#We remove the "SOURCE: " tag and the newline character.
				calc_descriptor(parsed_data, file_results[0][8:-1])

				file_results = []
				break
			else:
				file_results.append(line)
				
		input_file.close()
		
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
		
if __name__ == "__main__":
	main()