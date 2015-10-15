# -*- coding: utf-8 -*-

"""
"""

import cPickle as pickle

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

"""
"""
def save_file(data, file_path):
	new_file = open(file_path, "wb")
	pickle.dump(data, 2)

"""
"""
def load_file(file_path):
	file = open(file_path, "wb")
	pickle.load(file_path)