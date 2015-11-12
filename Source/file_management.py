# -*- coding: utf-8 -*-

"""
This module helps the managment of data into files
and viceversa.
"""

import cPickle as pickle

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

"""
This recieves almost any object and a path
and creates a .p file containing the information
from the object.
"""
def save_file(data, file_path):
	new_file = open(file_path, "wb")
	pickle.dump(data, new_file, 2)

"""
This retrieves the original object stored 
by the method save_file.
"""
def load_file(file_path):
	file = open(file_path, "rb")
	return pickle.load(file)