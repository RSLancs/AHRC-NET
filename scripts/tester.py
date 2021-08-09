##python 37

import re
from pprint import pprint
import glob
import subprocess


def test_geo_fault(file): 
	"""
	read in text from file and preform basic processing - join words split over two lines,
	add whitespace after fullstops, remove excessibe whitespace - then split on newline
	and feed each line into geoparser to see where it breaks - WARNING - very slow on big docs
	"""

	with open(file, 'r', encoding='utf-8', errors='ignore') as f:
		# print(file)
		raw_data = f.read() # read and lower text
		word_join1 = re.sub(r'-\s+\n+(\w+ *)', r'\1\n', raw_data)# join words split over 2 lines
		word_join2 = re.sub(r'-\n+(\w+ *)', r'\1\n', word_join1)# join words split over 2 lines
		word_join3 = re.sub(r'\n\n\n+',r'\n\n', word_join2)# remove excessive new lines
		# fullstop_standard = re.sub(r'\.(?![\s])',r'. ', word_join3) # add a \s after '.' to help tokenization
		# print(len(fullstop_standard))
		clean1 = re.sub(r'&', r'&amp;', word_join3)# 
		clean2 = re.sub(r'<', r'&lt;', clean1)# 
		clean3 = re.sub(r'>',r'&gt;', clean2)# 
		
		split_by_line = list(filter(bool, clean3.splitlines()))
		# pprint(split_by_line)

		for i, line in enumerate(split_by_line):
			with open('./geo_fault_find/' + str(i) + '.txt', 'w', encoding='utf8') as f:
				f.write(line)
				f.close()
	

		files_in_folder_list = glob.glob('./geo_fault_find/*.txt') # collect files in directory
		print(f'length of texts in corpus: {len(files_in_folder_list)}')

		for file in files_in_folder_list:# iterate over files in dir
			# basename = os.path.basename(file)
			# filename = os.path.splitext(basename)[0]
			print(file)

			geoparse = subprocess.run('cat ' + file + ' | ./geoparser-1.2/scripts/run -t plain -g os', shell=True)
				
			assert geoparse.returncode == 0 # check geoparser ran and outputted results
		