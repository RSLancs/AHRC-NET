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


## run corpus searchers
search_corpus = True
if_geoparsed = False # if you want to include geoparsed texts in lookup to get indexes



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
		
		clean_files_in_folder_list = glob.glob('./cleaned_corpus/*.txt') # collect cleaned files in directory
		# print(f'length of texts in corpus: {len(clean_files_in_folder_list)}')

		for cleaned_file in clean_files_in_folder_list:# iterate over files in dir

			check_if_geoparsed = check_exsisting_geoparsed(cleaned_file, './geoparsed_corpus/*.xml')# check if file already geoparsed
			

			if not check_if_geoparsed:# if not already geoparsed geoparse
				print(os.path.basename(cleaned_file))

				geoparse = subprocess.run('cat ' + cleaned_file + ' | ./geoparser-1.2/scripts/run -t plain -g os -o ./geoparsed_corpus ' + os.path.basename(cleaned_file), shell=True)
				
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
	if search_corpus:
		print('---Searching corpus---')

		# all_plant_finds = {}
		# all_plant_find_counts = {}
		# all_location_finds = {}
		# all_location_find_counts = {}
		# all_word_counts = {}
		# all_edinburgh_geo_counts = {}
		# all_edinburgh_geo_finds = {}
		# all_ngrams = {}


		powo_list = load_json_as_dict('./data/accepted_synonyms_search_list_dict_2021-08-03.json') # load nested plant list	

		plant_search_list, search_token_lenghts = get_abbreviation_dict(powo_list, abbreavtion) # compile abbreviations and flat plant search list
		# print(plant_search_list)


		files_in_folder_list = glob.glob('./corpus/*.txt') # collect files in directory
		# print(f'length of texts in corpus: {files_in_folder_list}')
		
		for file in files_in_folder_list:# iterate over cleaned corpus in folder
			basename = os.path.basename(file)
			filename = os.path.splitext(basename)[0]# get file name without path ot extension
			print(filename)

			
			if if_geoparsed:
				
				location_counts, all_edin_loc, loc_ngram_len = location_find_counts('./geoparsed_corpus_test/' + filename + '.txt.out.xml')# extract loactions from geoparsed.xml
				# all_edinburgh_geo_counts[filename] = location_counts # add finds to tracking dict
				# all_edinburgh_geo_finds[filename] = all_edin_loc # add finds to tracking dict
				# print(all_edin_loc)
				
				just_edin_geo_place_names = just_locations(location_counts)# get unique location names
				
				search_token_lenghts = list(set(search_token_lenghts + loc_ngram_len))# update token lengths with geoparser results
				# print(just_edin_geo_place_names)
			
			
			text = open_single_file_read(file)# load cleaned text
		# 	# print(text)

			tokens_cleaned, word_count = clean_tokenise(text)# tokenise text
			# all_word_counts[filename] = word_count # add finds to tracking dict
			# print(word_count)

			ngrams = clean_ngrams(tokens_cleaned, search_token_lenghts) # collect ngrams dict
			# all_ngrams[filename] = ngrams
			# print(ngrams)
			
			plant_matches_indexes, plant_matches_name, plant_match_count = find_all_match_instances(ngrams, plant_search_list, edit_dist)
			# all_plant_find_counts[filename] = plant_match_count # add find counts to tracking dict
			# all_plant_finds[filename] = plant_matches_name # add finds from text to tracking dict
			print(f'number of finds: {len(plant_matches_indexes)}')
			
			# text = None
			# tokens_cleaned = None
			# word_count = None
			# ngrams = None
			# plant_matches_indexes = None
			# plant_matches_name = None



			# map_to_accepted = synonym_and_abrevation_to_accepted(plant_matches_name, powo_list)# map finds to their root accepted names
			# all_plant_finds[filename] = map_to_accepted # add finds from text to tracking dictionary 
			# pprint(map_to_accepted)

			
			# look up place names
			# place_matches, place_matches_name, place_count = find_all_match_instances(ngrams, just_edin_geo_place_names, edit_dist)
			# all_location_finds[filename] = place_matches_name # add finds from text to tracking dictionary
			# all_location_find_counts[filename] = place_count # add find counts to tracking dictionary
			# print(location_counts)

			# geo_compare = compare_geo_finds(location_counts, place_count)# compare the SpaCy finds count with the geoparser finds counts

			# map_placename_to_index = map_locations(location_counts, place_count, all_edin_loc, place_matches_name)
			# pprint(map_placename_to_index)



			
			## geoparse text
			# check_if_geoparsed = check_exsisting_geoparsed(filename)
			
			# if not check_if_geoparsed:

			# 	geoparse = subprocess.run('cat ' + file + ' | ./geoparser-1.2/scripts/run -t plain -g os -o ./geoparsed_corpus ' + os.path.basename(filename), shell=True)
				
			# 	assert geoparse.returncode == 0 # check geoparser ran and outputted results
				
			

			# tree = ET.parse('./data/' + os.path.basename(file) + '.out.xml')# open geoparser xml file


			# geoparser_results, geo_token_lenghts = get_geoparser_results(tree)
			# # pprint(geoparser_results)
			# # print(geo_token_lenghts)

			# unique_locations = just_locations(geoparser_results)
			# # print(unique_locations)

			# ngrams = clean_ngrams(tokens_cleaned, geo_token_lenghts)
			# # print(ngrams)
			
			# place_matches, place_matches_name, place_count = find_all_match_instances(ngrams, unique_locations, edit_dist)
			# # print(place_count)

			# geo_compare = compare_geo_finds(geoparser_results, place_count)
			# 
