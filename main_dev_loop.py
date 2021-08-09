## python37

from scripts import *
import glob
import subprocess
import os


## set parameters 

## geoparse corpus - RUN ONCE
clean_for_geoparser = False
geoparse_corpus = False



## compile plant list - RUN ONCE
get_powo_plant_names = False


## run corpus searchers - Might need to run over if gazetteer updater modified
plant_list_compile = False
search_corpus = False
if_geoparsed = False 
geoparser_map = False
if_collocate = True


## model parameters
look_up = True
edit_dist = 0 # 
collocate_left = 10
collocate_right = 10
abbreavtion = True # True/False - Do you want to search for abbreviated names to? (recommended)


## unique save codes
accepted_plant_filename = '_powo_accpeted_names'
acc_sys_plant_filename = '_powo_nested_list'

if __name__ =='__main__':

	## a fault finder for geoparser
	# test_geo_fault('./cleaned_corpus/1777_Nicholson_and_Burns_Volume_1_History_and_Antiquities_of_the_Counties_of_Westmorland_and_Cumberlandcleaned.txt')
	

	##clean corpus ready for geoparser
	if clean_for_geoparser:
		print('---Cleaning corpus---')
		
		corpus_files_in_folder = glob.glob('./corpus/*.txt')# collect raw corpus filenames from folder
		# print(f'length of texts in corpus: {len(files_in_folder)}')
		
		for corpus_file in corpus_files_in_folder:# iterate over files in dir 
			# basename = os.path.basename(file)
			# filename = os.path.splitext(basename)[0] # get file name without path ot extension

			check_if_cleaned = check_exsisting_geoparsed(corpus_file, './cleaned_corpus/*.txt') # check in text has not already been cleaned

			if not check_if_cleaned:# if not already cleaned
				
				clean, 	text = clean_corpus_for_geoparser(corpus_file)# clean special characters &, <, > to allow geoparser to work
				# print(clean[:1000])

				write_out = write_out_flat_txt('./cleaned_corpus/' + text + '_cleaned.txt', clean)# write cleaned file out to new folder

			else:
				print(f'{corpus_file} is already clean')
	


	## geoparse_cleaned corpus
	if geoparse_corpus:
		print('---Geoparsing corpus---')	
		
		clean_files_in_folder_list = glob.glob('./corpus_test/*.txt') # collect cleaned files in directory
		# print(f'length of texts in corpus: {len(clean_files_in_folder_list)}')

		for cleaned_file in clean_files_in_folder_list:# iterate over files in dir
		
			check_if_geoparsed = check_exsisting_geoparsed(cleaned_file, './geoparsed_corpus/*.xml')# check if file already geoparsed

			if not check_if_geoparsed:# if not already geoparsed geoparse
				print(os.path.basename(cleaned_file))

				geoparse = subprocess.run('cat ' + cleaned_file + ' | ./geoparser-1.2/scripts/run -t plain -g os -o ./geoparsed_corpus_test ' + os.path.basename(cleaned_file), shell=True)
				
				assert geoparse.returncode == 0 # check geoparser ran without error and outputted results

			else:
				print(f'{cleaned_file} is already geoparsed')




	## collect all accepted plant names from POWO
	if get_powo_plant_names:
		print('---getting all POWO plant names---')
		
		# full_powo_lookup = powo_plantae_mass_look_up() # collect all accepted names from powo write to ./data file
		full_powo_lookup = load_json_as_dict('/media/robertsmail/USB16/powo_plantae_2021-07-27.json')# load full lookup if not in pipe
		
		all_powo_accepted, lookup_date = extract_powo_accepted_names(full_powo_lookup)		
		write_dict_to_json('/media/robertsmail/USB16/accepted_synonyms_search_list_dict_' + st + '.json', all_powo_accepted) # save results as json

		


	## load search list and search corpus
	if plant_list_compile:
		print('---compiling plant names lists and maps---')

		powo_list = load_json_as_dict('./data/accepted_synonyms_search_list_dict_2021-08-03.json') # load nested plant list
		# powo_list = load_json_as_dict('./data_test/test_plant_list.json') # load nested plant list		
	
		plant_search_list, search_token_lenghts, quick_map_plants = get_abbreviation_dict(powo_list, abbreavtion) # compile abbreviations and flat plant search list
		write_dict_to_json('./data/mapped_synonym_accepted_quick_look_up.json', quick_map_plants)
		# print(plant_search_list)

		

	## load search list and search corpus
	if search_corpus:
		print('---Searching corpus---')

		
		powo_list = load_json_as_dict('./data/accepted_synonyms_search_list_dict_2021-08-03.json') # load nested plant list
		
		plant_search_list, search_token_lenghts, quick_map_plants = get_abbreviation_dict(powo_list, abbreavtion) # compile abbreviations and flat plant search list
		# print(plant_search_list[:100])

		files_in_folder_list = glob.glob('./corpus/*.txt') # collect files in directory
		# print(f'length of texts in corpus: {files_in_folder_list}')
	
		text_tracking = {}

		for file in files_in_folder_list:# iterate over cleaned corpus in folder
			basename = os.path.basename(file)
			filename = os.path.splitext(basename)[0]# get file name without path ot extension
			print(filename)

			text = open_single_file_read(file)# load cleaned text
			# print(text)

			tokens_cleaned, word_count = clean_tokenise(text)# tokenise text
			# print(word_count)
			# write_dict_exsisting_json('./data/all_corpus_word_counts.json', word_count, file)  
			

			ngrams = clean_ngrams(tokens_cleaned, search_token_lenghts) # collect ngrams dict
			# all_ngrams_plants[filename] = ngrams
			# print(ngrams)
			# write_dict_exsisting_json('./data/all_ngrams_for_plant_names.json', ngrams, file) 
			

			plant_matches_indexes, plant_matches_name, plant_match_count = find_all_match_instances(ngrams, plant_search_list, edit_dist)
			# print(plant_matches_name)
			
			map_to_accepted = synonym_and_abrevation_to_accepted(plant_matches_name, quick_map_plants)# map finds to thier root accepted names
			text_tracking[filename] = map_to_accepted # add find counts to tracking dict
			# pprint(map_to_accepted)
		
	
		write_dict_to_json('./data/all_plant_matches_finds.json', text_tracking) 
	


	## collect locations from corpus using geoparser outputs - collect location indeses
	if if_geoparsed:

		raw_corpus_location_counts = {}
		raw_corpus_location_finds = {}
		

		files_in_folder_list = glob.glob('./corpus/*.txt') # collect files in directory
		# print(f'length of texts in corpus: {files_in_folder_list}')
		
		for file in files_in_folder_list:# iterate over cleaned corpus in folder
			basename = os.path.basename(file)
			filename = os.path.splitext(basename)[0]# get file name without path ot extension
			print(filename)

			text = open_single_file_read(file)# load cleaned text

			tokens_cleaned, _ = clean_tokenise(text)# tokenise text
			# print(tokens_cleaned)

			# raw_geoparser_matches, raw_generic_geoparser_matches = extract_geoparser_locations('./geoparsed_corpus_test/' + filename + '.txt.out.xml')# extract loactions from geoparsed.xml
			raw_all_geoparser_matches, raw_generic_geoparser_matches = extract_geoparser_locations('/media/robertsmail/USB16/geoparsed_corpus/' + filename + '_cleaned.txt.out.xml')# extract loactions from geoparsed.xml
			# pprint(raw_generic_geoparser_matches)
			
			just_edin_geo_place_names = just_locations(raw_generic_geoparser_matches)# get unique location names to search corpus with
			# print(just_edin_geo_place_names)

			ngrams = clean_ngrams(tokens_cleaned, token_lengths(just_edin_geo_place_names)) # collect ngrams dict
			# print(ngrams)

			## look up place names
			corpus_location_indeses, raw_corpus_location_matches_name, corpus_location_counts = find_all_match_instances(ngrams, just_edin_geo_place_names, edit_dist)
			raw_corpus_location_counts[filename] = corpus_location_counts # add finds from text to tracking dict
			# print(corpus_location_matches_name)
			# print(corpus_location_counts)


			add_lat_log = add_coordinates(raw_generic_geoparser_matches, raw_corpus_location_matches_name)
			raw_corpus_location_finds[filename] = add_lat_log # add finds from text to tracking dict
			# pprint(add_lat_log)
		 
		write_dict_to_json('./data/raw_corpus_location_counts.json', raw_corpus_location_counts) 
		write_dict_to_json('./data/raw_corpus_location_finds.json', raw_corpus_location_finds)
	
	

	# ## if you want to merge corpus location finds with geoparser finds - CURRENTLY NOT WORKING
	# if geoparser_map:
	# 		geo_compare = compare_geo_finds(location_counts, place_count)# compare the spacy finds count with the geoparser finds counts

	# 		map_placename_to_index = map_locations(updated_geoparser_location_counts, corpus_location_counts, updated_geoparser_finds, corpus_location_matches_name,  filename)
			# pprint(map_placename_to_index)
	
	

	## builds collocates from raw outputs
	if if_collocate:
		print('---forming collocates---')


		plant_finds = load_json_as_dict('./data/all_plant_matches_finds.json') # load all plant finds	

		location_finds = load_json_as_dict('./data/raw_corpus_location_finds.json') # load all location finds

		tokenised_texts = load_json_as_dict('./data/all_tokenised_texts.json') # corpus tokens
		  
		updated_location_finds, tracker = full_update_pipe(location_finds)
		# pprint(updated_geoparser_finds)
		# print(tracker)

		add_collocate_window = add_window(plant_finds, tokenised_texts, collocate_left, collocate_right)
		# print(add_collocate_window)

		static_collocate = static_collocates(add_collocate_window, location_finds, collocate_left, collocate_right)
		# print(static_collocate)
		# print(static_collocate[0][0])

		write_updated_file_out_csv('./data/static_collocates_1l0_r10.csv', static_collocate) 


# 

	# updated_geoparser_location_counts = locations_counter(updated_geoparser_matched_generic)# change geoparser find counts after gazetteer updated
			# print(updated_location_counts)


			# 		updated_corpus_location_matches_name, updated_corpus_location_counts = corpus_counter_adjuster(corpus_location_matches_name, corpus_location_counts)
	# 		all_corpus_location_find_counts[filename] = updated_corpus_location_counts # add finds from text to tracking dict
	# 		# print(updated_corpus_location_matches_name)
	# 		# print(updated_corpus_location_counts)










			