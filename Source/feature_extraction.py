# -*- coding: utf-8 -*-

"""
"""

import sys
import argparse

import cv2

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

#
INPUT_PATH = "detection_output.txt"

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
			
		for face in faces[0:1]:
			x, y, w, h = face
			histogram = hue_histogram(frame[y:y+h, x:x+w])
			
		video.release()
		break

	return 0

"""
"""
def hue_histogram(image):
	cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	cv2.calcHist([image], [0], None, [256], [0,179])

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