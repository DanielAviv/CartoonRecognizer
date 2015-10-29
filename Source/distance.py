# -*- coding: utf-8 -*-

"""
"""

import feature_extraction as fe
import file_management as fm

from os import listdir
from os.path import isfile, join, basename
import argparse

import cv2
import numpy as np
from sklearn.neighbors import NearestNeighbors

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

#
FEATURE_DIRECTORY = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Results\\FeaturesD1F"

#
INPUT_DIRECTORY = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\input"

#
MATCHES = 5

"""
"""
def kNN_FLANN(input_features, feature_files, desired_matches):
	FLANN_INDEX_KDTREE = 0
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks = 100)
	
	input_as_array = np.asarray(input_features, np.float32)
	flann = cv2.flann_Index(input_as_array, index_params)
	
	candidates = []
	
	for file_path in feature_files:
		dataset_features_dict = fm.load_file(file_path)
		dataset_features = dataset_features_dict.values()
		
		#input_as_array = np.asarray(input_features, np.float32)
		data_as_array = np.asarray(dataset_features, np.float32)
		print "k: " + str(desired_matches)
		matches, dist = flann.knnSearch(data_as_array, 5, params=search_params)
		print len(matches)
		#print input_as_array
		break
	
	return 0
	
"""
"""
def kNN_scikit(input_features, feature_files, desired_matches):
	pass
	
"""
"""
def kNN_OCV(input_features, data_features, desired_matches):
	result = []
	responses = np.asarray(range(0, len(data_features)), np.float32)

	knn = cv2.KNearest()
	knn.train(data_features, responses)
	ret, results, neighbours, dist = knn.find_nearest(input_features, desired_matches)
	
	candidates_position_array = []
	
	for neighbour_array in neighbours:
		candidates_position_array.extend(neighbour_array)
		
	result = [ data_features[position] for position in candidates_position_array ]
	
	return result
	
"""
"""
def compute_input_features(input_paths):
	result = []

	for image_path in input_paths:
		image = cv2.imread(image_path, 1)
		image_features = fe.hue_histogram_zone(image, 32)
		
		result.append(image_features)
		
	return result
		
def main(argv=None):
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument("feature_directory", help="")
	parser.add_argument("input_images", help="")
	argv = parser.parse_args()
	"""
	feature_directory = FEATURE_DIRECTORY
	input_images_path = INPUT_DIRECTORY

	try:
		feature_files = [ join(feature_directory, data)
			for data in listdir(feature_directory) if isfile(join(feature_directory, data)) ]

		input_images = [ join(input_images_path, data)
			for data in listdir(input_images_path) if isfile(join(input_images_path, data)) ]
			
		input_features = compute_input_features(input_images)
		input_as_array = np.asarray(input_features, np.float32)
		
		candidates = {}
		
		for file_path in feature_files:
			dataset_features_dict = fm.load_file(file_path)
			dataset_features = dataset_features_dict.values()
			data_as_array = np.asarray(dataset_features, np.float32)
			
			selected_features = kNN_OCV(input_as_array, data_as_array, MATCHES)
			print len(selected_features)

			for key, value in dataset_features_dict.items():
				for feature in selected_features:
					if np.array_equal(feature, value):
						new_key = basename(file_path) + ":" + key
						candidates[new_key] = value
						break

		print len(candidates.keys()) == len(set(candidates.keys()))

	except IOError:
		print "ERROR: The path provided does not exist"

	return 1
	
if __name__ == "__main__":
	main()