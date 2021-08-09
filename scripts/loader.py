## python 37
import re
import glob
import os
import json

##.........load species look up list........

def species_input_list(input_list):
	"""
	function to load and clean a plant list ready for POWO lookup
	"""

	with open(input_list, 'r') as f: # open species lookup list
		species = f.readlines() # split list on new lines

	strip_species = [s.strip() for s in species]# strip out white space
	remove_blanks = [s for s in strip_species if len(s) > 3] # remove any blank rows
	unique_species = list(set(remove_blanks)) # remove duplicate species

	print(f'Plant list read in. \nEmpty rows removed. \nExtra white space or punctuation removed. \nDuplicate species removed.')
	print(f'Imported and cleaned Plant list length: {len(unique_species)}')
	# print(unique_species, '\n\n')
	
	return unique_species



def open_single_file_read(file): 
	"""
	read in text from file and preform basic processing - join words split over two lines,
	add white space after fullstops, remove excessive white space 
	"""
	with open(file, 'r', encoding='utf-8', errors='ignore') as f:
		# print(file)
		raw_data = f.read() # read and lower text
		word_join1 = re.sub(r'-\s+\n+(\w+ *)', r'\1\n', raw_data)# join words split over 2 lines
		word_join2 = re.sub(r'-\n+(\w+ *)', r'\1\n', word_join1)# join words split over 2 lines
		word_join3 = re.sub(r'\n\n\n+',r'\n\n', word_join2)# remove excessive new lines
		# fullstop_standard = re.sub(r'\.(?![\s])',r'. ', word_join3) # add a \s after '.' to help tokenization
		# print(len(fullstop_standard))

	return word_join3
	#return 'UNIQUETEXTIDENT' + file[28:-4] +'\n\n' + fullstop_standard + '\n\n' #28 for Linux path, 39 for win




def check_exsisting_geoparsed(root_filename_in, out_folder):
	"""
	takes a file name and makes sure it has not already been geoarsed
	"""
	exsisting = False

	# print(root_filename_in[-3:])
	root_basename = os.path.basename(root_filename_in)# getfilename without path
	root_filename = os.path.splitext(root_basename)[0] # remove extension from filename
				
	in_folder_list = glob.glob(out_folder) # collect files in destination directory

	if out_folder[-3:] == 'xml': # check if this is a geoparser file with multiple extensions - eg .txt.out.xml

		for file in in_folder_list: # iterate over files in folder
			basename = os.path.basename(file)
			before_first_period = basename.partition('.') # get filename without extension
			# print(f'checking if already geoparsed: {root_filename}, {before_first_period[0]}')

			if root_filename == before_first_period[0]:
				exsisting = True

	if out_folder[-3:] == 'txt':

		for file in in_folder_list:
			basename = os.path.basename(file)
			filename = os.path.splitext(basename)[0]
			# print(f'checking if already cleaned: {root_filename}, {filename[:-8]}')

			if root_filename == filename[:-8]:
				exsisting = True

	return exsisting




def load_json_as_dict(file_in):
	"""
	load json as dict
	"""
	with open(file_in) as json_file:
		data = json.load(json_file)

	return data