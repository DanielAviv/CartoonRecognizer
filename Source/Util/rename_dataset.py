# -*- coding: utf-8 -*-

"""
This executable changes the name of all the files in a directory to dataXXXX.extension,
where XXXX is a number and extension is the original extension of the file.
"""

import sys
from os import listdir, rename
from os.path import isfile, join, splitext

__author__ = "Daniel Aviv"
__credits__ = "Juan Manuel Barrios"
__email__ = "daniel_avivnotario@hotmail.com"
__status__ = "Development"

#Default directory, will be favoured over the one in the arguments.
#If empty, won't be used.
DIRECTORY = "D:\\Mis Documentos\\MaterialU\\Memoria\\CartoonRecognizer\\Data\\Dataset"

"""
This returns the formatted name as described in the header.
"""
def format_name(old_name, index):
	formated_index = "%04d" % index #This formats the index as a 4-digit int
	old_name_extension = splitext(old_name)[1]
	new_file_name = "data" + formated_index + old_name_extension
	
	return new_file_name

def main(argv=None):
	if argv is None:
		argv = sys.argv
	
	try:
		directory_path = DIRECTORY
		if DIRECTORY == "":
			directory_path = str(argv[1])

		only_files = [ file for file in listdir(directory_path) if isfile(join(directory_path, file)) ]
		
		index = 0
		for file in only_files:
			old_name = join(directory_path, file)
			new_name = join(directory_path, format_name(old_name, index))
			rename(old_name, new_name)
			
			index = index + 1
			
		print "Files renamed"
		return 0
		
	except IndexError as e:
		print "ERROR: You must provide the path of the directory to rename"
		
	return 1

if __name__ == "__main__":
	main()