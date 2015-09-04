# -*- coding: utf-8 -*-

"""
This executable changes the name of all the files in a directory to dataXXXX,
where XXXX is a number.
"""
import sys
from os import listdir, rename
from os.path import isfile, join

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

#Default directory, will be favoured over the one in the arguments.
#If empty, won't be used.
DIRECTORY = "D:\\Mis Documentos\\MaterialU\\CC69E-Intro a Trabajo de Titulo\\CartoonRecognizer\\Data\\Dataset1"

def main(argv=None):
	if argv is None:
		argv = sys.argv
	
	try:
		directory_path = DIRECTORY
		if DIRECTORY == "":
			directory_path = str(argv[1])
		
		only_files = [ file for file in listdir(directory_path) if isfile(join(directory_path, file)) ]
		
		#["%04d" % x for x in range(10000)]
		index = 0
		for file in only_files:
			rename(file, "caca" + str(index))
		
	except IndexError as e:
		print "ERROR: You must provide the path of the directory"
		
	return 1

if __name__ == "__main__":
	main()