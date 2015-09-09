# -*- coding: utf-8 -*-

"""
This executable computes frames from a video dataset at a constant rate.
"""

import sys
from os import listdir
from os.path import isfile, join, splitext
import argparse

import cv2

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

#Default directory for the database and for the results, will be favoured over the ones in 
#the arguments.
DATA_DIRECTORY = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\Dataset1"
RESULT_DIRECTORY = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Results\\Results4"

#This is the factor by which the images will be resized.
#Original_width/height * RESIZE_FACTOR = New_width/height 
RESIZE_FACTOR = 0.3

# This relates to the amount of frames we are going to get:
# FPS / FRAMESKIP * amount of seconds = amount of frames. 
FRAMESKIP = 10

"""
This function receives the path of a video and saves frames at a constant rate defined by RATE in
result_path. The frames are named video_name_frameX.jpg where X is an int. The frames will be
resized from it's original source file by the factor resize.
"""
def compute_frames(video_path, video_name, result_path, resize):
	video = cv2.VideoCapture(video_path)
	
	video_fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
	msec_skip =  (1000 / video_fps) * FRAMESKIP
	frames_retrieved = 0
	
	while(video.isOpened()):
		video_continues = video.grab()
		
		if video_continues == False:
			break
			
		video_continues, frame = video.retrieve()
		
		frame_name = video_name + "_" + str(frames_retrieved) + ".jpg"
		frame_path = join(result_path, frame_name)
		
		resized_frame = cv2.resize(frame, (0,0), fx=resize, fy=resize)
		cv2.imwrite(frame_path, resized_frame)
		
		current_position = video.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
		video.set(cv2.cv.CV_CAP_PROP_POS_MSEC, current_position + msec_skip)
		
		frames_retrieved += 1
	
	print str(frames_retrieved) + " frames retrieved and saved."
	video.release()

def main(argv=None):
	data_path = DATA_DIRECTORY
	result_path = RESULT_DIRECTORY
	resize = RESIZE_FACTOR
	
	if DATA_DIRECTORY == "" or RESULT_DIRECTORY == "":
		parser = argparse.ArgumentParser()
		parser.add_argument("data_directory", help="directory where the data is located")
		parser.add_argument("result_directory", help="directory where the frames will be stored")
		parser.add_argument("-r", "--resize", help="factor by which the image will be resized", type=float, default=1)
		argv = parser.parse_args()
		
		data_path = argv.data_directory
		result_path = argv.result_directory
		resize = argv.resize
		
	videos = [ data for data in listdir(data_path) if isfile(join(data_path, data)) ]

	for video in videos[0:1]:
		video_name = splitext(video)[0]
		video_path = join(data_path, video)
		compute_frames(video_path, video_name, result_path, resize)
		
	return 0

if __name__ == "__main__":
	main()