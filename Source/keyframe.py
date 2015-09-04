# -*- coding: utf-8 -*-

"""
This executable computes frames from a video dataset at a constant rate.
"""

import sys
from os import listdir
from os.path import isfile, join

import cv2

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

#Default directory for the database and for the results, will be favoured over the ones in 
#the arguments.
DATA_DIRECTORY = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\Dataset1"
RESULT_DIRECTORY = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Results\\Results1"

"""
This function receives the path of a video and saves frames at a constant rate defined by RATE in
RESULT_DIRECTORY.
"""
def compute_frames(video_path):
	video = cv2.VideoCapture(video_path)
	frameCount = 0
	
	while(video.isOpened()):
		pass
		
	video.release()

def main(argv=None):
	if argv is None:
		argv = sys.argv
	
	try:
		data_path = DATA_DIRECTORY
		result_path = RESULT_DIRECTORY
		
		if DATA_DIRECTORY == "" or RESULT_DIRECTORY == "":
			data_path = argv[1]
			result_path = argv[2]
			
		video_paths = [ join(data_path, data) for data in listdir(data_path) if isfile(join(data_path, data)) ]
		
		for video_path in video_paths:
			compute_frames(video_path)
			
		return 0
		
	except IndexError as e:
		print "ERROR: You must provide both the path of the data directory and the result directory"
		
	return 1

if __name__ == "__main__":
	main()