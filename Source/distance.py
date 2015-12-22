# -*- coding: utf-8 -*-

"""
"""

import feature_extraction as fe
import file_management as fm

from os import listdir
from os.path import isfile, join, basename
import argparse
from operator import itemgetter

import cv2
import numpy as np
from sklearn.neighbors import NearestNeighbors

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

ARCH = "q9"
#The output
FEATURE_DIRECTORY = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\ResFeat16"

#
INPUT_DIRECTORY = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\FeatureEvaluation\\" + ARCH

#
MATCHES = 32

#
FINALISTS = 32

"""
"""
def kNN_FLANN(input_features, feature_files, desired_matches):
	return None
	
"""
"""
def kNN_scikit(input_features, feature_files, desired_matches):
	return None
	
"""
"""
def kNN_OCV(input_features, data_features, desired_matches):
	data_features_value = [ data[1] for data in data_features ]
	data_as_array = np.asarray(data_features_value, np.float32)
	responses = np.asarray(range(0, len(data_features)), np.float32)
	
	knn = cv2.KNearest()
	knn.train(data_as_array, responses)
	ret, results, neighbours, dist = knn.find_nearest(input_features, desired_matches)
	
	candidates_position_array = []
	candidates_distance_array = []
	
	for neighbour_array in neighbours:
		candidates_position_array.extend(neighbour_array)
		
	for distance_array in dist:
		candidates_distance_array.extend(distance_array)
	
	result = [ data_features[int(position)] for position in candidates_position_array ]
	
	return result, candidates_distance_array
	
"""
"""
def vote(candidates, nb_of_finalists):
	votes = {}
	
	for candidate in candidates:
		face_key = candidate[0][0]
		votes[face_key] = 0
	
	for candidate in candidates:
		face_key = candidate[0][0]
		votes[face_key] = votes[face_key] + (10/candidate[1])
	
	real_nb = min(nb_of_finalists, len(candidates))
	best = dict(sorted(votes.iteritems(), key=itemgetter(1), reverse=True)[:nb_of_finalists])

	return best
	
"""
"""
def compute_input_features(input_paths):
	result = []

	for image_path in input_paths:
		image = cv2.imread(image_path, 1)
		image_features = fe.hue_histogram_zone(image, 16)
		
		result.append(image_features)
		
	return result
		
def main(argv=None):
	feature_directory = FEATURE_DIRECTORY
	input_images_path = INPUT_DIRECTORY
	
	output_file = open(ARCH + ".txt", "w")

	try:
		feature_files = [ join(feature_directory, data)
			for data in listdir(feature_directory) if isfile(join(feature_directory, data)) ]

		input_images = [ join(input_images_path, data)
			for data in listdir(input_images_path) if isfile(join(input_images_path, data)) ]
			
		input_features = compute_input_features(input_images)
		input_as_array = np.asarray(input_features, np.float32)
		
		candidates = []
		
		for file_path in feature_files:
			dataset_features_dict = fm.load_file(file_path)
			dataset_features = dataset_features_dict.items()
			
			selected_features, distances = kNN_OCV(input_as_array, dataset_features, MATCHES)
			
			for feature in selected_features:
				new_key = basename(file_path) + ":" + feature[0]
				candidates.append([new_key, feature[1]])
				
		final_candidates, distance = kNN_OCV(input_as_array, candidates, MATCHES)
		matches = zip(final_candidates, distance)

		final_results = vote(matches, FINALISTS)
		
		print("Done! Output File generated")
		for result in final_results:
			output_file.write(result + "\n")

	except IOError:
		print "ERROR: The path provided does not exist"

	return 1
	
if __name__ == "__main__":
	main()