# -*- coding: utf-8 -*-

"""
This executable computes frames from a video dataset at a constant rate.
"""

import sys
from os import listdir
from os.path import isfile, join, splitext

import cv2

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

#Default directory for the database and for the results, will be favoured over the ones in 
#the arguments.
DATA_DIRECTORY = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\Dataset1"
RESULT_DIRECTORY = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Results\\Results1"

# This relates to the amount of frames we are going to get:
# FPS / FRAMESKIP * amount of seconds = amount of frames. 
FRAMESKIP = 1800
	
"""
This function receives the path of a video and saves frames at a constant rate defined by RATE in
RESULT_DIRECTORY.
"""
def compute_frames(video_path, video_name):
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
		frame_path = join(RESULT_DIRECTORY, frame_name)
		cv2.imwrite(frame_path, frame)
		
		current_position = video.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
		video.set(cv2.cv.CV_CAP_PROP_POS_MSEC, current_position + msec_skip)
		
		frames_retrieved += 1
	
	print str(frames_retrieved) + " frames retrieved and saved."
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
			
		videos = [ data for data in listdir(data_path) if isfile(join(data_path, data)) ]
		
		for video in videos[0:1]:
			video_name = splitext(video)[0]
			video_path = join(data_path, video)
			compute_frames(video_path, video_name)
			
		return 0
		
	except IndexError as e:
		print "ERROR: You must provide both the path of the data directory and the result directory"
		
	return 1

if __name__ == "__main__":
	main()