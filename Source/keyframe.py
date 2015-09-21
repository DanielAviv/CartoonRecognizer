# -*- coding: utf-8 -*-

"""
This executable computes frames from a video dataset at a constant rate.
"""

import sys
from os import listdir, remove
from os.path import isfile, join, splitext
import argparse

import cv2
from numpy import arange

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

#Default directory for the database and for the results, will be favoured over the ones in 
#the arguments. The results will only be stored if the option -s is active.
DATA_DIRECTORY = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\Dataset1"
RESULT_DIRECTORY = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Results\\Results5"

#This is the factor by which the images will be resized.
#Original_width/height * RESIZE_FACTOR = New_width/height 
RESIZE_FACTOR = 0.3

#This relates to the amount of frames we are going to get:
#FPS / FRAMESKIP * amount of seconds = amount of frames. 
FRAMESKIP = 6

#This constant determines if the frames are saved along with the output position file.
SAVE_FRAMES = False

#This constant determines the name of the output file. It CANNOT be changed via call arguments.
OUTPUT_FILE_NAME = "output.txt"

"""
This compute the output file which is a file with all the videos in the dataset
with each respective array of millisecond position which will be
processed.
"""
def compute_output(video_path, video_name, result_path):
	video = cv2.VideoCapture(video_path)
	video_fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
	video_total_msec = 1000 * video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT) / video_fps
	msec_skip = (1000 / video_fps) * FRAMESKIP

	output_file_path = join(result_path, OUTPUT_FILE_NAME)
	output_file = open(output_file_path, "a")
	
	output_file.write("VIDEO: " + video_name + "\n")
	
	msec_array = arange(0, video_total_msec, msec_skip)
	for msec in msec_array:
		output_file.write(str(msec) + ",")

	output_file.write("\n")
	video.release()
	output_file.close()
	
	return msec_array

"""
This function just calls compute_output. But, if save_frames = True it also
receives the path of the video and saves frames at a constant rate defined by RATE in
result_path. The frames are named video_name_frameX.jpg where X is an int. 
The frames will be resized from it's original source file by the factor resize.
"""	
def compute_frames(video_path, video_name, result_path, resize, save_frames):
	video = cv2.VideoCapture(video_path)
	frames_retrieved = 0

	msec_array = compute_output(video_path, video_name, result_path)
	
	if save_frames:
		for msec in msec_array:
			video.set(cv2.cv.CV_CAP_PROP_POS_MSEC, msec)
			video_continues = video.grab()
			
			if video_continues == False:
				break
				
			video_continues, frame = video.retrieve()
			
			frame_name = splitext(video_name)[0] + "_" + str(frames_retrieved) + ".jpg"
			frame_path = join(result_path, frame_name)
			
			resized_frame = cv2.resize(frame, (0,0), fx=resize, fy=resize)
			cv2.imwrite(frame_path, resized_frame)
			
			frames_retrieved += 1
		
		print str(frames_retrieved) + " frames retrieved and saved."
		video.release()
	
	return 0

def main(argv=None):
	data_path = DATA_DIRECTORY
	result_path = RESULT_DIRECTORY
	resize = RESIZE_FACTOR
	save_frames = SAVE_FRAMES
	
	if DATA_DIRECTORY == "" or RESULT_DIRECTORY == "":
		parser = argparse.ArgumentParser()
		parser.add_argument("data_directory", help="directory where the data is located")
		parser.add_argument("result_directory", help="directory where the frames will be stored")
		parser.add_argument("-r", "--resize", help="factor by which the image will be resized", type=float, default=1)
		parser.add_argument("-s", "--saveframes", help="if this is specified, the frames will be saved along with the position file", action="store_true")
		argv = parser.parse_args()
		
		data_path = argv.data_directory
		result_path = argv.result_directory
		resize = argv.resize
		save_frames = argv.saveframes
		
	videos = [ data for data in listdir(data_path) if isfile(join(data_path, data)) ]
	
	try:
		output_file_path = join(result_path, OUTPUT_FILE_NAME)
		remove(output_file_path)
	except OSError:
		pass

	for video in videos:
		video_path = join(data_path, video)
		compute_frames(video_path, video, result_path, resize, save_frames)
		
	return 0

if __name__ == "__main__":
	main()