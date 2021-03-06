# -*- coding: utf-8 -*-

"""
This module is the second step in the process of the project and
it serves the purpuse of computing features for the rectangles found by
the module of detection.
"""

import file_management as fm

import sys
import argparse
from random import randint
from os import listdir
from os.path import join, basename, splitext, isfile

import cv2
from numpy import concatenate

import time

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

#Path of the files which cointains the detected faces in the dataset.
INPUT_PATH = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Results\\ResDetDef"

#Where the features computed by this module will be saved.
OUTPUT_PATH = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Results\\ResFeatDef32"

"""
This function recieves String representation of a list
and tranforms it into a list of integers.
"""
def str_to_array(array_string):
	string_array = array_string.split(";")
	result = [ map(int, array[1:-1].split()) for array in string_array ]
	return result

"""
This receives each line from the input file from the detection 
and return a dictionary representation of each of the files.
"""
def parse_input_file(lines):
	#This extracts the lines in the file in odd and even positions,
	#removes the unnecessary characters and parses them as readable data.
	frames = [ float(line[:-1]) for line in lines[::2] ]
	faces = [ str_to_array(line[:-2]) for line in lines[1::2] ]
	
	file_dictionary = zip(frames, faces)
	return file_dictionary
	
"""
Gets a dictionary representation of the detected rectangles
in the dataset and outputs the computed features as a
dictionary. 
"""
def calc_descriptor(data_dictionary, video_path):
	result = {}
	frame_counter = 0
	dictionary_length = len(data_dictionary)

	video = cv2.VideoCapture(video_path)

	while(video.isOpened()):
		video_continues = video.grab()
			
		if video_continues == False:
			break
		
		target = data_dictionary[frame_counter]
		current_position = video.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
		
		if(current_position == target[0]):
			if(frame_counter >= dictionary_length - 1):
				break
			
			video_continues, frame = video.retrieve()

			for rectangle in target[1]:
				x, y, w, h = rectangle
				face = frame[y:y+h, x:x+w]
				histogram = hue_histogram_zone(face, 32)
				
				#I convert the rect to str because lists
				#cannot be keys in a dictionary.
				dict_key = str(target[0]) + ":" + str(rectangle)
				result[dict_key] = histogram
			
			frame_counter += 1

	video.release()
	return result

"""
"""
def hue_histogram(image, bins):
	hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	hist = cv2.calcHist([hsv_image], [0], None, [bins], [0,255])
	
	sum_hist = sum(hist)
	hist_normed = hist
	if sum_hist != 0:
		hist_normed = hist/sum(hist)
	
	return hist_normed
	
"""
"""
def hue_histogram_zone(image, bins):
	rows, cols, channels = image.shape
	
	a = image[:rows/2, :cols/2]
	b = image[rows/2:, :cols/2]
	c = image[:rows/2, cols/2:]
	d = image[rows/2:, cols/2:]
	
	hist_a = hue_histogram(a, bins)
	hist_b = hue_histogram(a, bins)
	hist_c = hue_histogram(a, bins)
	hist_d = hue_histogram(a, bins)
	full_hist = hue_histogram(image, bins)
	
	all_hist = (hist_a, hist_b, hist_c, hist_d, full_hist)
	return concatenate(all_hist, axis=0)

"""
This was a failed experiment
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
		help="Directory where all the features will be saved", default=OUTPUT_PATH)
	argv = parser.parse_args()
	
	input_path = argv.input_path
	output_path = argv.output_path
	start = time.time()
	
	if input_path == "":
		print("Where is the input file located?")
		input_path = sys.stdin.readline()
		
	if output_path == "":
		print("Where is the output directory located?")
		output_path = sys.stdin.readline()
	
	try:
		print "| Computing features, this will take several minutes... |\n"
		detection_files = [ join(input_path, data) for data in listdir(input_path) if isfile(join(input_path, data)) ]
		
		for file_path in detection_files:
			file = open(file_path, "r")	
			lines = [ line for line in file ][:-1]
			parsed_data = parse_input_file(lines[1:])
			
			#We remove the "SOURCE: " tag and the newline character.
			source_path = lines[0][8:-1]
			
			features = calc_descriptor(parsed_data, source_path)

			file_name = basename(source_path)
			feature_file_path = join(OUTPUT_PATH, splitext(file_name)[0] + ".p")
			fm.save_file(features, feature_file_path)

			print " - File : " + file_name + " finished and saved."
		
		print("---RUNTIME: " + str(time.time() - start) + " seg.---")
		return 0
		
	except IOError as e:
		print "The directory used to store or extract the descriptors does not exists."
		
	return 1
		
if __name__ == "__main__":
	main()