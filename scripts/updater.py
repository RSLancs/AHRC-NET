##python37....

import re
import pandas as pd




##..........load csv gazetteer LD_update as data frame and split into update types delete, add update etc.....................

update = pd.read_csv('./data/LD_Updates_P4.csv', encoding='utf8') # load text as .csv format 
update = update.drop_duplicates()# remove any duplicate rows

manual_loc= update.loc[update['conf']=='Manual']# make data frame of just Manual updated
manual_loc = manual_loc.values.tolist()
#pprint(manual_loc[:5])

add_loc=update.loc[update['conf'] =='Add']# make data frame of just Add updated
add_loc = add_loc.values.tolist()
#pprint(add_loc[:5])


del_loc = update.loc[update['conf'] =='DEL']# make data frame of just DEL updated
del_loc = del_loc.values.tolist()
#pprint(del_loc[:5])

man_add_loc = update[update.conf.isin(['Manual', 'Add'])]# make data frame of ADD and MANUAL updated
man_add_loc = man_add_loc.values.tolist()
#print(man_add_loc)

##..............delete wrong entries.......................



def delete_places(geoparser_finds_in): 
	deletes_record = [] # record what changes have been made
	all_after_delete = {}

	for text, finds in geoparser_finds_in.items():
		# print(len(finds))
		after_deletes = finds
		
		for i, find in enumerate(after_deletes):# iterate over each row in spatial relations file
			# print(key)

			for dl in del_loc: # iterate over LD_updates deletes list - ie list of places to be deleted
				if dl[0].strip().lower() == find[0].strip().lower(): # check if LD_updates. Deletes location of matches LD_corpsu 
					# print(f'DELETED - location: {key} was deleted')
					
					#update record
					deletes_record.append(['DELETED - location: ', find])
					# print(f'{find} to be deleted')
					
					# update file
					del(after_deletes[i])

		# print(len(finds), len(after_deletes))
		all_after_delete[text] = after_deletes
				

	return all_after_delete, deletes_record

##....................... update lat, lons....................

def updated_places(geoparser_finds_in): 
	updates_record = [] # record what changes have been made
	all_exsisting_updated = {} #updated list

	
	for text, finds in geoparser_finds_in.items():

		after_update = finds
		
		for i, find in enumerate(after_update):# iterate over each row in spatial relations file
			# print(key)
					
		# for existing place names update lat, lon
			for ml in manual_loc: 
				#print(i[0], loc[0])				
				if ml[0].strip().lower() == find[0].strip().lower():
					# print(find[6], find[7], '-->')
					
					updates_record.append(['UPDATED - location: ', str(find[2]), str(find[3]), 'updated to: ', [ml[2], ml[1]]])

					## update file
					after_update[i][6], after_update[i][7] = ml[2], ml[1]
					# print('->', ml[2], ml[1])
					
		all_exsisting_updated[text] = after_update

	return all_exsisting_updated, updates_record


##......................add standardised location if varation detected...

# def standardised_loc(geoparser_finds_in):
# 	standardised_record = []
# 	standardised = geoparser_finds_in

# 	for key, value in standardised.items(): # iterate over spatial relations rows

# 			# standardise location name using LD_update list
# 			for sl in man_add_loc: # iterate over LD_update list items 'add' and 'manual'
								
# 				if sl[0].strip().lower() == key.strip().lower(): # if LD update location matches LD_corpus location, update corpus file
# 					print(f'STANDARDISED - location: {key} matched {sl[0]} therefore {key} updated to: {sl[5]}')
					
# 					## update record list
# 					standardised_record.append(['STANDARDISED - LD_update location: ', str(key), 'matched corpus location: ', str(sl[0]), 
# 						' - therefore location: ', str(key),  'updated to: ', str(sl[5])])

# 					for find in value:
# 						find[0] == [sl[0]]
# 					##  update file
# 					key = sl[5].strip().lower()	# update standadised place name in locations_with_geo column
					
	

# 	return standardised, standardised_record
			

##........... run all LD_corpus location updates...................

def full_update_pipe(input_text):
	after_deletes = delete_places(input_text)
	# print(after_deletes[0])

	after_updates = updated_places(after_deletes[0])	
	# # print(after_updates[0])

	# # after_standardised = standardised_loc(after_updates[0])
	
	all_updates_record = after_deletes[1] + after_updates[1]# merge all update records 

	return after_updates[0], all_updates_record 


