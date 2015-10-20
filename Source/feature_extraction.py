# -*- coding: utf-8 -*-

"""
This module computes the feature from the detected faces by the module of detection.
"""

import file_management as fm

import sys
import argparse
from random import randint
from os.path import join, basename, splitext

import cv2
from numpy import concatenate
from moviepy.video.io.ffmpeg_reader import FFMPEG_VideoReader

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

#Path of the file which cpintains the detected faces in the dataset.
INPUT_PATH = "detection_output.txt"

#Where the features computed by this module will be saved.
OUTPUT_PATH = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Results\\Features1"

"""
This function recieves String representation of a list
and tranforms it into a list of integers.
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
	result = {}
	video = FFMPEG_VideoReader(video_path, False)
	video.initialize()
	video_fps = video.fps
	
	for frame_pos, faces in data_dictionary.iteritems():
		frame = video.get_frame(frame_pos/video_fps)
		frame_dictionary = {}
			
		for rectangle in faces[:1]:
			x, y, w, h = rectangle
			face = frame[y:y+h, x:x+w]
			#histogram = hue_histogram(face, 32)
			histogram = hue_histogram_zone(face, 32)
			#patches = rand_patch(face, 10, 10)
			
			#I convert the rect to str because lists
			#cannot be keys in a dictionary.
			frame_dictionary[str(rectangle)] = histogram
			
		result[frame_pos] = frame_dictionary
	video.close()

	return result

"""
"""
def hue_histogram(image, bins):
	hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	hist = cv2.calcHist([hsv_image], [0], None, [bins], [0,179])
	
	sum_hist = sum(hist)
	hist_normed = hist
	if sum_hist != 0:
		hist_normed = hist/sum(hist)
	
	return hist_normed
	
"""
"""
def hue_histogram_zone(image, bins):
	hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	rows, cols, channels = hsv_image.shape
	
	a = hsv_image[:rows/2, :cols/2]
	b = hsv_image[rows/2:, :cols/2]
	c = hsv_image[:rows/2, cols/2:]
	d = hsv_image[rows/2:, cols/2:]
	
	hist_a = hue_histogram(a, bins)
	hist_b = hue_histogram(a, bins)
	hist_c = hue_histogram(a, bins)
	hist_d = hue_histogram(a, bins)
	full_hist = hue_histogram(hsv_image, bins)
	
	all_hist = (hist_a, hist_b, hist_c, hist_d, full_hist)
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
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input_path",
		help="Path of the text file containing the detected faces", default=INPUT_PATH)
	parser.add_argument("-o", "--output_path",
		help="Directory where all the features will be saved", default=INPUT_PATH)
	argv = parser.parse_args()
	
	input_path = argv.input_path
	output_path = argv.output_path
	
	if input_path == "":
		print("Where is the input file located?")
		input_path = sys.stdin.readline()
		
	if output_path == "":
		print("Where is the output directory located?")
		output_path = sys.stdin.readline()
	
	try:
		print "| Computing features, this will take several minutes... |\n"
		input_file = open(INPUT_PATH, "r")

		file_results = []
		for line in input_file:	
			if line.startswith("ENDFILE"):
				parsed_data = parse_input_file(file_results)
				#We remove the "SOURCE: " tag and the newline character.
				file_path = file_results[0][8:-1]
				
				features = calc_descriptor(parsed_data, file_path)
				
				file_name = basename(file_path)
				feature_file_path = join(OUTPUT_PATH, splitext(file_name)[0] + ".p")
				fm.save_file(features, feature_file_path)
				
				print " - File : " + file_name + " finished and saved."
				
				file_results = []
			else:
				file_results.append(line)
				
		input_file.close()
		
		return 0
		
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
		
	return 1
		
if __name__ == "__main__":
	main()