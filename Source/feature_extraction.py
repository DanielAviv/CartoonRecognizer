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
	print data_dictionary
	return None

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
				calc_descriptor(parsed_data, file_results[0])
				
				file_results = []
			else:
				file_results.append(line)
				
		input_file.close()
		
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
		
if __name__ == "__main__":
	main()