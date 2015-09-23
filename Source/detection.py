# -*- coding: utf-8 -*-

"""
This executable detects the faces of the characters in the frames in the database.
"""

import sys
from os import listdir, remove
from os.path import isfile, join #, splitext
import argparse

import cv2

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

#
DATA_PATH = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\Dataset2"

#This relates to the amount of frames we are going to get:
#FPS / FRAMESKIP * amount of seconds = amount of frames.
FRAMESKIP = 10

#This constant determines the name of the output file.
OUTPUT_FILE_NAME = "faces.txt"

"""
"""
def OCV_detector(videos):
	face_cascade = cv2.CascadeClassifier('D:\\Archivos de Programa\\OpenCV249\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_default.xml')
	output_file = open(OUTPUT_FILE_NAME, "a")

	for video_path in videos[:1]:
		frames_seen = 0
		frames_analized = 0
		frames_with_faces = 0
		
		output_file.write("SOURCE: " + video_path + "\n")
		print "a"
	
		video = cv2.VideoCapture(video_path)	
		while(video.isOpened()):
			video_continues = video.grab()
			
			if video_continues == False:
				break
			
			if (frames_seen % FRAMESKIP) == 0:
				video_continues, frame = video.retrieve()
				faces = face_cascade.detectMultiScale(frame, 1.3, 5)

				if len(faces) != 0:
					frame_position = video.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
					output_file.write(str(frame_position) + ":")
					output_file.write(str(faces) + "\n")
					print "b"
					
					frames_with_faces += 1
				frames_analized += 1
			frames_seen += 1
			
		output_file.write("\n")
		print str(frames_analized) + " frames analized, from which " + str(frames_with_faces) + " work."
		video.release()
		
	output_file.close()
	return 0

"""
"""	
def IAF_detector(video_dictionary):
	return 0

"""
"""
def DAN_detector(video_dictionary):
	return 0

def main(argv=None):
	parser = argparse.ArgumentParser()
	parser.add_argument("detector", help="Type of detector to use", choices=["OCV", "IAF", "DAN"])
	argv = parser.parse_args()
	
	data_path = DATA_PATH
	detector = argv.detector
	
	if DATA_PATH == "":
		print("Where is the data located?")
		data_path = sys.stdin.readline()
		
	try:
		remove(OUTPUT_FILE_NAME)
	except OSError:
		pass
	
	try:
		videos = [ join(data_path, data) for data in listdir(data_path) if isfile(join(data_path, data)) ]
	
		if detector == "OCV":
			return OCV_detector(videos)
		elif detector == "IAF":
			return IAF_detector(videos)
		else:
			return DAN_detector(videos)
			
	except IOError:
		print "You must give the data path."
	
	return 1

if __name__ == "__main__":
	main()