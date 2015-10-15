# -*- coding: utf-8 -*-

"""
This executable detects the faces of the characters in the frames in the database.

This process outputs a file with the source name and for each frame with faces
detected it includes a list of tuples (x, y, w, h) which represents a
rectangle with a face in it.
"""

import sys
from os import listdir, remove
from os.path import isfile, join
import argparse

import cv2

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

#This is the location of the dataset. If empty, the console UI will ask for it.
DATA_PATH = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\Dataset2"

#This relates to the amount of frames we are going to get:
#FPS / FRAMESKIP * amount of seconds = amount of frames.
FRAMESKIP = 10

#This constant determines the name of the output file.
OUTPUT_FILE_NAME = "detection_output.txt"

"""
This method does the detection of the faces.
INPUTS:
 - videos: an array with the paths each video in the dataset.
 - classifier: an .xml file with the classifier necessary for
 the detection.
 
 OUTPUT:
 - A text file containing the squares with the detected faces.
"""
def do_detect(videos, classifier):
	face_cascade = cv2.CascadeClassifier(classifier)
	output_file = open(OUTPUT_FILE_NAME, "w")

	print "Detection started, this will take several minutes."
	for video_path in videos[:2]:
		frames_seen = 0
		frames_analized = 0
		frames_with_faces = 0
		face_count = 0
		
		output_file.write("SOURCE: " + video_path + "\n")
		
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
					output_file.write(str(frame_position) + "\n")
					for face in faces:
						output_file.write(str(face) + ";")
					output_file.write("\n")
					
					face_count += len(faces)
					frames_with_faces += 1
				frames_analized += 1
			frames_seen += 1

		output_file.write("ENDFILE\n")
		print "\n" + str(frames_analized) + " frames analized."
		print "From which " + str(frames_with_faces) + " work."
		print "From which " + str(face_count) + " faces has been found."
		video.release()
		
	output_file.close()
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
		videos = [ join(data_path, data) for data in listdir(data_path) if isfile(join(data_path, data)) ][:1]
	
		if detector == "OCV":
			return do_detect(videos, ".\\Data\\haarcascade_frontalface_default.xml")
		elif detector == "IAF":
			print "Detector not supported yet"
			return 1
		else:
			return do_detect(videos, ".\\Data\\LBPcascade_animeface_woo.xml")
			
	except IOError:
		print "You must give the data path."
	
	return 1

if __name__ == "__main__":
	main()