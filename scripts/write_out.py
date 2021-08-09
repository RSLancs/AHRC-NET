## python 37
import json
import pandas as pd



def write_updated_file_out(synonym_out_list, synonym_out_list_FULL, tracking, file_name):

	## write API Species ID output to CSV file 
	my_df1 = pd.DataFrame(synonym_out_list) # transform result list to data frame
	print(my_df1)

	my_df1.to_csv('./Out/' + file_name + '_POWO_lookup_' + str(st) +'.csv', index=False, encoding='utf-8-sig')

	## Write updated LD_corpus file out to pickle 
	pickling_on = open('./Out/' + file_name + '_POWO_lookup_' + str(st) + '.pickle',"wb")
	pickle.dump(synonym_out_list, pickling_on)
	pickling_on.close()

	correct_list = open('./Out/' + file_name + '_POWO_lookup_' + str(st) + '_tracking.txt', 'w')
	for item in tracking:
		correct_list.write("%s\n" % item)
	correct_list.close	



def write_out_list_txt(out_path, out_data):
	"""
	write out list txt file
	"""

	thefile = open(out_path, 'w', encoding='utf8')

	for item in out_data:
	 		thefile.write("%s\n" % item)




def write_out_flat_txt(out_path, out_data):
	"""
	write out flat txt file
	"""

	with open(out_path, 'w', encoding='utf8') as f:
		f.write(out_data)



def write_dict_to_json(out_path, dict_in):
	"""
	take a dict and write out
	"""
	
	with open(out_path, 'w', encoding='utf8') as outfile: 
		json.dump(dict_in, outfile)



def write_dict_exsisting_json(out_path, dict_in, file):
	"""
	take a dict and write out
	"""

	result_dict = {file :dict_in}
	with open(out_path, mode='r+', encoding='utf-8') as f:
	    data = json.load(f)
	    data.update(result_dict)
	    f.seek(0)
	    json.dump(data, f)


def json_initilise(list_in):
	"""
	creates blank files for results
	"""

	for file in list_in:
		with open(file,"w+") as f:
			json.dump({}, f)
			f.close()



def write_updated_file_out_csv(file_name, finds_in):
	"""
	write collocates out to csv
	"""

	dict_to_list = []

	for key, values in finds_in.items():

		for value in values:

			dict_to_list.append([key, key[:4], value[0], value[1], value[2], value[3], value[4], 
								value[5], value[6], value[7], value[8], value[9], value[10], value[11], 
								value[12], value[13], value[14], value[15], value[16], value[17], value[18], value[19]])


	my_df1 = pd.DataFrame(dict_to_list)# transform result list to data frame

	my_df1.columns = ['text', 
					'year',
					'plant_search_term_raw',
					'plant_search_term_cleaned',
					'plant_edit_distance',
					'mapped_accepted_name(s))',
					'plant_start',
					'plant_end',
					'match_type',
					'location_search_term_raw',
					'location_search_term_cleaned',
					'location_edit_distance',
					'location_start',
					'location_end',
					'ner_type',
					'latitude',
					'longitude',
					'location_type',
					'window_text',
					'direction_found',
					'left_span',
					'right_span'
					]# add column labels							

	my_df1.to_csv(file_name, index=True, header=True)# write results out to file