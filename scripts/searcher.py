## python 37
import re


def find_all_match_instances(ngram_dict, flat_search_list, edit_dist):
	"""
	functions takes an ngram input dictionary and looks
	for all matches and returns their indexes
	"""
	
	matches = []	
	matches_with_name = []
	matches_count = {}

	for search_item in flat_search_list: #iterate over search_item list					
		search_item_ready = search_item.lower().strip() # lower and strip white space
		
		if '\u00d7' in search_item: # special character in plant name \u00d7, replace with 'x'
			search_item_ready = re.sub(r'\u00d7', r'x', search_item_ready)
		# 	print(f'raw plant name: {search_item}. Clean plant name: {search_item_ready}')
		

		############### not set up ###############
		if edit_dist >= 1: # of fuzzy matching
			for i, ngram_dict in enumerate(bigrams): #iterate over all bigrams in text
				edit_distance = nltk.edit_distance(bigram, search_item_ready, substitution_cost=1, transpositions=False)#check edit-distance
				if edit_distance <= edit_dist: #is edit-distance size is less than selected edit distance
					matches.append([i,bigram, edit_distance, search_item_ready])# add to list with index
		############################################

		
		elif edit_dist == 0: # look for exact matches
					
			finds = ngram_dict[len(search_item_ready.split())].get(search_item_ready) # check plant name matches any bigram in corpus dict
	
			if finds:# if plabt name matches any bigram in corpus dictionary
				for find in finds:
					matches.append((find, find+len(search_item_ready.split())))
					matches_with_name.append([search_item, search_item_ready, edit_dist, find, find+len(search_item_ready.split())])
					
					if not search_item in matches_count: # if ngram not already a dictionary key

						matches_count[search_item] = 0 

					matches_count[search_item] += 1 # increase find counter if more than one   
			else:

				if not search_item in matches_count: # if ngram not already a dictionary key

					matches_count[search_item] = 0 

	return matches, matches_with_name, matches_count
				



def find_all_match_instances_single(ngram_dict, extract):
	"""
	functions takes an ngram input dictionary and looks
	for all matches and returns their indexes
	"""
	
	matches = []	
	matches_with_name = []
	# matches_count = {}

	join_extract = ' '.join(extract)
	search_item_ready = join_extract.lower().strip() # lower amd strip white space
	print(search_item_ready)
		
		# if '\u00d7' in search_item: # special character in plant name \u00d7, replace with 'x'
		# 	search_item_ready = re.sub(r'\u00d7', r'x', search_item_ready)
		# # 	print(f'raw plant name: {search_item}. Clean plant name: {search_item_ready}')

					
	# finds = ngram_dict[len(search_item_ready.split())].get(search_item_ready) # check plant name matches any bigram in corpus dict
	finds = ngram_dict.get(search_item_ready)
	
	if finds:# if plabt name matches any bigram in corpus dict
		for find in finds:
			print(find)
	# 		matches.append((find, find+len(search_item_ready.split())))
	# 		matches_with_name.append([search_item, search_item_ready, edit_dist, find, find+len(search_item_ready.split())])
			
	# 		if not search_item in matches_count: # if ngram not already a dict key

	# 				matches_count[search_item] = 0 

	# 			matches_count[search_item] += 1 # increase find counter if more than one   
	# 	else:

	# 		if not search_item in matches_count: # if ngram not already a dict key

	# 			matches_count[search_item] = 'nan' 

	return matches_with_name
