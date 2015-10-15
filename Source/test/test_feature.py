# -*- coding: utf-8 -*-

"""
This test-case tests the module feature_extraction.py.
"""

import feature_extraction

import unittest
from os.path import join

import cv2

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

#
COLOR_SPACE_IMAGE_PATH = join("test", "test_image.png")

class TestFeatures(unittest.TestCase):
	def setUp(self):
		self.color_space_image = cv2.imread(COLOR_SPACE_IMAGE_PATH, 1)
		
	def tearDown(self):
		self.color_space_image = None
	
	def test_hsv(self):
		hsv_image = cv2.cvtColor(self.color_space_image, cv2.COLOR_BGR2HSV)
		hue,sat,val = cv2.split(hsv_image)
		
		for row in hue:
			for value in row:
				self.assertTrue((value >= 0) and (value < 180))
	
	def test_hue_histogram(self):
		histogram = feature_extraction.hue_histogram(self.color_space_image, 16)
		self.assertTrue(len(histogram) == 16)
		image_size = self.color_space_image.size
		
		for bin in histogram:
			self.assertTrue(image_size >= bin)
			
	def test_zone_hue_histogram(self):
		histogram = feature_extraction.hue_histogram_zone(self.color_space_image, 16)
		self.assertTrue(len(histogram) == 80)
		
	def test_rand_patches(self):
		patches = feature_extraction.rand_patch(self.color_space_image, 10, 10)
		self.assertTrue(len(patches) == 10)
		
		for patch in patches:
			self.assertTrue(patch.shape == (15, 15, 3))

if __name__ == "__main__":
	unittest.main()