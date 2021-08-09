## python37 

import pykew.powo as powo
from pykew.powo_terms import Name
from pykew.powo_terms import Geography

from pprint import pprint
# import pandas as pd
import datetime
import time
from .write_out import *
from .loader import *


ts = time.time()# get time stamp for api POWO lookup query.....................
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')# format time stamp to when POWO was accessed	



###................. kingdom query whole POWO database.............. 

def powo_plantae_mass_look_up():
	"""
	look up all Plantae from POWO and get list of accepted names
	"""
		
	print('lookup started')	

	finds = []

	query = { Name.kingdom: 'Plantae' } # compile query
	
	results = powo.search(query) # use query to search POWO
	
	for r in results:
		finds.append(r)
	
	write_dict_to_json('./media/robertsmail/USB16/powo_plantae_2.0_' + st + '.json', finds) # save results as json

	return finds



def extract_powo_accepted_names(full_powo_lookup):
	"""
	takes raw powo look up and extracts all accepted plant names and unique fqId
	codes for later synonym lookup
	"""
	
	# pprint(full_powo_lookup[500001])
	# keys = ['name', 'kingdom', 'accepted', 'rank', 'fqId', 'synonymOf']
	# pprint(list(map(full_powo_lookup[500001].get, keys)))

	# name, kingdom, accepted, rank, fqId, synonymOf = list(map(full_powo_lookup[500001].get, keys))
	
	# if not accepted:
	# 	print('sysysysn')
	# 	print(synonymOf['name'])


	accepted_list ={}
	
	keys = ['name', 'kingdom', 'accepted', 'rank', 'fqId', 'synonymOf'] # compile lookup keys
	
	
	for i in full_powo_lookup: # iterate over all POWO lookup instances
			
		name, kingdom, accepted, rank, fqId, synonymOf = list(map(i.get, keys))#collect keys


		## if record is a species and accepted
		if kingdom == 'Plantae':
			if accepted == True:
				if rank == 'Species':
					
					if not name in accepted_list: # if species not already a dictionary key

						accepted_list[name] = [] # make species a key

	## once accepted names compiled 
	for i in full_powo_lookup:
			
		syn_name, syn_kingdom, syn_accepted, syn_rank, syn_fqId, syn_synonymOf = list(map(i.get, keys)) #collect all keys... again 

		if syn_kingdom == 'Plantae': # check record is a plant
			if syn_accepted == False: # check its a synonym
				if syn_rank == 'Species': # check its a species	
					if syn_synonymOf != None: # check an accepted name is listed
						# print(syn_name, syn_kingdom, syn_accepted, syn_rank, syn_fqId, syn_synonymOf)
						# pprint(i)
						# print(syn_synonymOf['name'])	

						if syn_synonymOf['name'] in accepted_list: # if 
							accepted_list[syn_synonymOf['name']].append(syn_name)


	for key, value in accepted_list.items():# remove duplicate species names within synonym nests

		accepted_list[key] = list(set(value))
	
	
	return accepted_list, st			




# # # #..............look up small list of plants  in POWO..............

def powo_search(input_clean_list): # load in clean plant list
	"""
	Takes an input search list and checks for synonym names in POWO
	"""
	
	ts = time.time()# get time stamp for api POWO lookup query.....................
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')# format time stamp to when POWO was accessed	
	
	accepted_match =[]	
	syn_match = []
	tracking = []
	synonyms_to_accepted_species = []
	synonyms_to_accepted_species_FULL = []

	tracking.append(['POWO was accessed on: ' , st])
	tracking.append(['Species in: ', input_clean_list])


	## check all plant names in input search list are accepted names
	def search(in_list): # search each input plant names against POWO
		## lookup speciesfrom list in POWO database
		# print(f'Searching for: {in_list} \n') 
		tracking.append(['Searching for: ', in_list])
		
		try:
			query = {Name.full_name: in_list} # transform plant name to search query format
			result = powo.search(query) # search the POWO database using query
						
			for r in result:
				#print(r)
				
				if r['accepted'] == True: # check match is an accepted plant name
					if r['rank'] == 'Species': # check the match is of the rank 'species'
						# print(f'The species {in_list} has matched as an accepted species in the POWO database.\n')
						tracking.append(['The species ' , in_list,  ' has matched as an accepted species in the POWO database.'])
						accepted_match.append([in_list , r['fqId'], r['accepted'], r['rank']])
				
				if r['accepted'] == False: # if match is NOT rank 'accepted' 
					rel = r['synonymOf']['name'] # collect the matches root accepted name
					# print(f'The species {in_list} has matched as a synonym in the POWO database to the accepted species: {rel}.\n')
					tracking.append(['The species ', in_list, ' has matched as a synonym in the POWO database to accepted species: ', rel])
					syn_match.append(r['synonymOf']['name'])
					
		except AttributeError: # find species in my list not in POWO
			print(f'species: {in_list} not listed in POWO database, Soz. \n')
			tracking.append(['species: ', in_list, ' not listed in POWO database, Soz.'])
			pass

	
	straight_matches = [search(in_spec) for in_spec in input_clean_list] # iterate over input plant name input list
	
	synon_root_matches = [search(in_spec) for in_spec in syn_match] # if any input plant names are found to be a synonym, iterate over root accepted name
	


	## now look up accpeted names for synonyms 
	
	
	for species, species_id, _, _ in accepted_match: # iterate over POWO query results and fqId ID's 
		
		try:
			full_result = powo.lookup(species_id) # lookup the database
			# pprint(full_result)
			
			if full_result['synonym'] == False: # check entry is not a synonyms
				if full_result['taxonomicStatus'] == 'Accepted': # check entry has 'accepted' status
					synonyms_to_accepted_species_FULL.append(full_result)
					# print(f'Species: {species} is considered as an accepted name')
					tracking.append(['Species: ', species, ' is considered as an accepted name'])	
					
					try: # collect  synonyms for species
						synonyms = [s['name'] for s in full_result['synonyms'] if s['rank'] == 'SPECIES'] # check there are synonyms
						synonyms.insert(0, species) # add accepted species to beginning of each nest
						
						## just in case found remove var., subsp., f., subf., from synonym list 
						only_species = [i for i in synonyms if not('subf.' in i or 'var.' in i or 'subsp.' in i or 'f.' in i)]
						
						synonyms_to_accepted_species.append(only_species) # add synonyms to nested list				

					except KeyError: # if no synonyms
						# print(f'No synonyms for {species}. \n')
						tracking.append(['No synonyms for: ', species])
						pass
		
		except ValueError:
			tracking.append('species: ', species, ' found for this not found in full POWO lookup') # if no species listed on POWO add to no-list
			pass		
		
	return synonyms_to_accepted_species, synonyms_to_accepted_species_FULL, tracking, st




def get_abbreviation_list(input_list, abbrevation):
	"""
	Takes nested input search list and creates abbreviations 
	"""

	species_list_with_abbreviations	= []
	token_len = []


	if abbrevation: # if abreation is True

		for nest in input_list:

			for i in nest:
				if i != '' and i != ' ':
					ext = i[0] + ' .'
					ext2 = i.split()
					token_len.append(len(ext2))

					if len(ext2) == 2:
						ext3 = ext2[1]	
						ext4 = ext + " " + ext3		
						
						species_list_with_abbreviations.append(i)
						species_list_with_abbreviations.append(ext4)
						token_len.append(len(ext4.split()))

					elif len(ext2) == 3:
						ext3 = ext2[1]	
						ext3b = ext2[2]
						ext4b = ext + " " + ext3	+ " " + ext3b	
						
						species_list_with_abbreviations.append(i)
						species_list_with_abbreviations.append(ext4b)
						token_len.append(len(ext4b.split()))								
						

	elif not abbrevation:

		for nest in input_list:

			for i in nest:
				
				species_list_with_abbreviations.append(i)


	unique_nest = list(set(species_list_with_abbreviations))#remove any duplicates WITHIN nest
	uniqe_token_len = list(set(token_len))
	
	return unique_nest, uniqe_token_len



def get_abbreviation_dict(input_list, abbrevation):
	"""
	Takes nested input search list and creates abbreviation
	"""

	species_list_with_abbreviations	= []
	token_len = []
	mapped = {}



	if abbrevation: # if abbreviation is True

		for key, value in input_list.items():
			# print(key, value)

			join =  value +[key]
			# print(join)
			
			for i in list(join):
				
				if i != '':
					# print(f'full item: {i}')

					ext = i[0] + ' .'
					ext2 = i.split()
					token_len.append(len(ext2))

					
					if len(ext2) == 2:
						ext3 = ext2[1]	
						ext4 = ext + " " + ext3		
						
						species_list_with_abbreviations.append(i)
						species_list_with_abbreviations.append(ext4)
						token_len.append(len(ext4.split()))


						if not ext4 in mapped:
							mapped[ext4] = [key]
						else:
							mapped[ext4].append(key)
						
						if not i in mapped:
							mapped[i] = [key]
						else:
							mapped[i].append(key)
							
						

					elif len(ext2) == 3:
						ext3 = ext2[1]	
						ext3b = ext2[2]
						ext4b = ext + " " + ext3	+ " " + ext3b
						# print(ext4b)	
						
						species_list_with_abbreviations.append(i)
						species_list_with_abbreviations.append(ext4b)
						# print(i)
						# print(ext4b)
						token_len.append(len(ext4b.split()))	

						if not ext4b in mapped:
							mapped[ext4b] = [key]
						else:
							mapped[ext4b].append(key)
						
						if not i in mapped:
							mapped[i] = [key]
						else:
							mapped[i].append(key)	


					# elif len(ext2) == 4:
					# 	ext3 = ext2[1]	
					# 	ext3b = ext2[2]
					# 	ext4b = ext + " " + ext3	+ " " + ext3b	
						
					# 	species_list_with_abbreviations.append(i)
					# 	species_list_with_abbreviations.append(ext4b)
					# 	# print(i)
					# 	# print(ext4b)
					# 	token_len.append(len(ext4b.split()))	

					# 	if not ext4 in mapped:
					# 		mapped[ext4] = [key]
					# 	else:
					# 		mapped[ext4].append(key)
						
					# 	if not i in mapped:
					# 		mapped[i] = [key]
					# 	else:
					# 		mapped[i].append(key)						
						

	elif not abbrevation:

		for key, value in input_list.items():

			join = key(key) + value

			for i in join:
				if i != '':

					species_list_with_abbreviations.append(i)
					
					ext2c = i.split()
					token_len.append(len(ext2c))
						
					if not i in mapped:
						mapped[i] = [key]
					else:
						mapped[i].append(key)	




	unique_nest = list(set(species_list_with_abbreviations))#remove any duplicates WITHIN nest
	uniqe_token_len = list(set(token_len))
	
	return unique_nest, uniqe_token_len, mapped




def synonym_and_abrevation_to_accepted(in_finds, search_list_mapped):
	"""
	This function takes all match instances and links it to any modern accepted name that it
	is linked with
	"""

	mapped_find = []

	for find, f, ed, start, end in in_finds:
		# print(find)

		collet_acc = search_list_mapped.get(find)

		if '.' in find:

			if collet_acc:
				mapped_find.append([find, f, collet_acc, ed, start, end, 'abbrv'])
			else:
				print(f'Issue linking plant name find: {find} with root accepted name(s)')

		else:
			if collet_acc:
				mapped_find.append([find, f, collet_acc, ed, start, end, 'full'])
			else:
				print(f'Issue linking plant name find: {find} with root accepted name(s)')

	return mapped_find


	


def plant_mapper(powo_full, search_list):
	"""
	builds a quick assessable synonym to accepted name
	plant mapper dictionary 
	"""

	print('build map')
	mapped = {}

	for plant_name in search_list: # iterate over all find instances
		# print(plant_name)
		
		ext = plant_name[0] # get first letter
		ext2 = plant_name.split() #split find into tokens

	
		for key, values  in powo_full.items(): # iterate over accepted:synonym nest
			
			join =  values +[key] # join key with synonym

			for name in join:
				# print(name)

				subext = name[0] # get plant letter
				
				subext2 = name.split() #split plant into tokens

				
				if '.' in plant_name: # check if find is an abbrevations

					if ext == subext:

						if ext2[-1:] == subext2[-1:]:
							# print(ext, ext2[-1:], subext, subext2[-1:])

							if not plant_name in mapped:
								# print(plant_name)
								mapped[plant_name] = [key]
								
							else:
								# print(f'name: {plant_name} is duplicate match to {name}')
								mapped[plant_name].append(key)

				elif ext2 == subext2:
					if not plant_name in mapped:
						mapped[plant_name] = [key]

					else:
						# print(f'name: {plant_name} is duplicate match to {name}')
						mapped[plant_name].append(key)


	return mapped
	# pprint(mapped)
