## python 37



def add_window(in_finds, all_tokens, left, right):
	"""
	inserts text windows for each find for each text
	"""

	all_finds_with_window = {}


	for text, text_finds in in_finds.items():

		tokens = all_tokens.get(text) # get tokens for relevant text

		finds_with_tokens = []

		for find, f, ed, acc, start, end, mtype in text_finds: # iterate over finds

			# print(tokens[start-left: end+right])

			window = tokens[start-left: end+right] # collect tokens around match indexes
			
			finds_with_tokens.append([find, f, acc, ed, start, end, mtype, window])

		all_finds_with_window[text] = finds_with_tokens


	return all_finds_with_window




def static_collocates(plant_finds_in, location_find_in, left, right):
	"""
	takes plant and location finds and forms collocates based on input parameters
	"""

	collocates = {}

	for text, plant_finds in plant_finds_in.items():# iterate over texts for plant finds
		
		locations = location_find_in.get(text) # collect location finds for corresponding text
		

		collocate_in_text = []
		
		for plant, plt, ed, acc, pstart, pend, mtype, window in plant_finds: # iterate over plant finds WITHIN text
			
			for location, loc, ed,  lstart, lend, ft ,lat, lon, loc_type  in locations: # iterate over location finds WITHIN same text
				# print(location, loc, ed, ft , lstart, lend, lat, lon, loc_type)
			
				left_diff = pstart - lend # check if plant of location find is within left span
				right_diff = pend - lstart #  check if plant of location find is within right span
		
				if left_diff in range(0, left):
					collocate_in_text.append([plant, plt, ed, acc, pstart, pend, mtype, location, loc, ed, lstart, lend, ft, lat, lon, loc_type, window, 'found_left', left, right])

				elif right_diff in range(0, right): # if within span match as collocate
					collocate_in_text.append([plant, plt, ed, acc, pstart, pend, mtype, location, loc, ed, lstart, lend, ft, lat, lon, loc_type, window, ' found_right', left, right])

		collocates[text] = collocate_in_text	

	return collocates	

				



