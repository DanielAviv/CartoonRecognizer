# -*- coding: utf-8 -*-

"""
This executable creates a both .info file (negative and positive examples)
necessary to the process of detection.
"""

from os import listdir
from os.path import isfile, join
import argparse

import cv2

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

#This is the location of the dataset. If empty, the console UI will ask for it.
DATA_PATH = "D:\\DetectorTrainingNegative"

#Paths where the output files are located.
POS_PATH = ".\\Data\\anime_faces.info"
NEG_PATH = ".\\Data\\not_anime_faces.info"

"""
This function creates the info files
INPUT:
- data_path: Path where the example images are.
- with_size: Boolean that determines if the file contains the size of the image or not.
"""
def write_examples(data_path, with_size):
	positive_img = [ (join(data_path, img)) for img in listdir(data_path) if isfile(join(data_path, img)) ]

	output_file = None
	if with_size == True:
		output_file = open(POS_PATH, "a")
	else
		output_file = open(NEG_PATH, "a")

	for each_positive in positive_img:
		output_file.write(each_positive)
		
		if with_size == True:
			output_file.write(" 1 0 0 ")
			
			image = cv2.imread(each_positive)
			
			rows, columns, channels = image.shape
			output_file.write(str(columns) + " " + str(rows))
			
		output_file.write("\n")

	output_file.close()
	
	return 0

def main(argv=None):
	parser = argparse.ArgumentParser()
	parser.add_argument("-ws", "--sanssize", help="", action="store_true")
	argv = parser.parse_args()
	
	data_path = DATA_PATH
	
	try:
		remove(POS_PATH)
		remove(NEG_PATH)
	except OSError:
		pass
	
	if DATA_PATH == "":
		print("Where is the data located?")
		data_path = sys.stdin.readline()
		
	return write_examples(data_path, not(argv.sanssize))

if __name__ == "__main__":
	main()