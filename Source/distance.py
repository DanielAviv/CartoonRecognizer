# -*- coding: utf-8 -*-

"""
"""

from numpy import linalg

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

def euclidean_distance(v1, v2):
	return linalg.norm(v1 - v2)