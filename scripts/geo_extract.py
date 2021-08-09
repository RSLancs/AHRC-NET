##python37

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import glob
from pprint import pprint
from .cleaner_tokeniser import *
from .searcher import *
import itertools
import operator



def just_locations(in_dict):
    """ 
    takes a dict of geolocations and flattens to list
    """

    just_places = []

    for place in in_dict.keys():

        just_places.append(place)

    return list(set(just_places))




def most_common(L):
    # get an iterable of (item, iterable) pairs
    SL = sorted((x, i) for i, x in enumerate(L))
    # print('SL:', SL)
    groups = itertools.groupby(SL, key=operator.itemgetter(0))
    
    # auxiliary function to get "quality" for an item
    def _auxfun(g):
        item, iterable = g
        count = 0
        min_index = len(L)
        for _, where in iterable:
            count += 1
            min_index = min(min_index, where)
            # print('item %r, count %r, minind %r' % (item, count, min_index))
        return count, min_index

    # pick the highest-count/earliest item
    return max(groups, key=_auxfun)[0]




def extract_geoparser_locations(in_file):
    """
    extract locations identified by geoparser for out.xml
    """
         
    locations_counter = {}
    geoparser_finds = {}
    geoparser_finds_generic = {}
    token_len = []

    # for file in files_in_folder_list:# iterate over files in dir
    
    tree = ET.parse(in_file) # open geoparser xml file

    # roots = input_tree.getroot() # get root of xml tag structure

    for ent in tree.iter('ent'):
        # print(ent.attrib)
        name = ent.get('lat')
        # print(name)
        if name:
            # print(ent.attrib)

            for parts in ent: #iterate over elements
                for part in parts:
                    # print(part.text)

                    token_len.append(len(part.text.split())) # get location ngram length for ngram tokenisation

                    place = part.text.lower().strip()

                    if 'st.' in place: # prep 'st.' for searcher format
                        place = re.sub(r'st.', r'st .', place)

                    ## find counter
                    if not place in locations_counter: # if ngram not already a dict key

                        locations_counter[place] = 0 


                    locations_counter[place] += 1 # increase find counter if more than one
                    # print(part.text, locations_counter[part.text.lower().strip()])

                    ## all finds and details
                    if not place in geoparser_finds: # if ngram not already a dict key
    
                        geoparser_finds[place] = []
                        

                    geoparser_finds[place].append([part.text,                                                                   
                                                    ent.get('type'), 
                                                    ent.get('lat'),
                                                    ent.get('long'),
                                                    ent.get('feat-type'),
                                                    part.get('ew')])

                    if not place in geoparser_finds_generic: # if ngram not already a dict key
    
                        geoparser_finds_generic[place] = []


                    geoparser_finds_generic[place].append([part.text,                                                                   
                                                            ent.get('type'), 
                                                            ent.get('lat'),
                                                            ent.get('long'),
                                                            ent.get('feat-type')])
                                                                    
    generic = {} # filter location to unique items
    
    for key, value in geoparser_finds_generic.items():
      
        # pprint(f'all geo finds: {value}')
        # print('\n')
        res = most_common(value)
        # print(res)
        # print('\n\n')

        if len(res) > 5:
            print(f'{res}, is over 1')

        else:
            if not key in generic: # if ngram not already a dict key
                generic[key] = res   

    return geoparser_finds, generic




def locations_counter(in_dict):
    """
    get placename counts of dict
    """
    location_counter = {}

    for key, value in in_dict.items():
        # print(key, value)
        # print(len(value))

        if not key in location_counter: # if ngram not already a dict key

            location_counter[key] = len(value)


    return location_counter




def token_lengths(in_list):
    """
    returns the unique token lengths from list
    """
    token_lengths = []

    for location in in_list:
        token_lengths.append(len(location.split()))
  
    return list(set(token_lengths))

     


def compare_geo_finds(raw_geoparser_results, corpus_find_counts):
    """
    compares the geoparser find number with total in corpus
    """

    for key, value in raw_geoparser_results.items():

        corp_find_number = corpus_find_counts[key]

        print(f'place: {key}, raw_count: {value}, corp_count: {corp_find_number}')



def corpus_counter_adjuster(in_list, corpus_find_counts):
    """
    adjusts counter if overlap in find
    """

    longest_words = []
    updated_counts = corpus_find_counts

    for word, find, ed, start, end in in_list:# iterate over every location found in corpus 
        word_length = end - start
        word_longer = False
        # check the sapn for over laps
        for word_alt, find_alt, ed_alt, start_alt, end_alt in in_list:
        # Exact same word move on
            if start_alt == start and end_alt == end:
                continue
        # word starts after the word we are interested in ends
            if start_alt > end:
                continue
        # word ends before the word we are looking at
            if end_alt < start:
                continue
            word_length_alt = end_alt - start_alt
            if word_length_alt > word_length:
                word_longer = True
        # If not words were added while searching for longer words then 
        if not word_longer:
            longest_words.append([word, find, ed, start, end])
   

        if word_longer: # if word is the shorter overlap
            # print(word, find, ed, start, end)
            # print(updated_counts[word])
            updated_counts[word] -= 1
            # print(updated_counts[word])

    return longest_words, updated_counts




def collect_xml_sentence(in_items, path):
    """
    where a location discrepancy is found try to resolve
    """

    tree = ET.parse(path) # open geoparser xml file

    find_with_sen = []

    for item in in_items: # iterate over finds
        # print(item)
        
        word_id = item[5] # collect word id

        for sen in tree.iter('s'):

            match = [word.attrib for word in sen if word.attrib['id'] == word_id]

            if len(match) == 1:
                # print(match)

                sentence = [word.text for word in sen]

                find_with_sen.append(item + sentence)

    return find_with_sen



def map_locations(raw_geoparser_finds, corpus_find_counts, full_geoparser_results, corpus_find_results, path):
    """
    compares the geoparser find number with total in corpus then tries to get 
    index for each placename in corpus
    """

    locations_indexses = []

    updated_corpus_find_results, updated_corpus_find_counts = corpus_counter_adjuster(corpus_find_results, corpus_find_counts) 
    # pprint(updated_corpus_find_counts)

    
    for key, value in raw_geoparser_finds.items():# iterate over raw results

        corp_find_number = updated_corpus_find_counts[key] # pull corresponding corpus find

        if corp_find_number == value: # if same number of matches then use corpus find indexses
            # print(f'place: {key}, raw_count: {value}, corp_count: {corp_find_number}')

            collect_locations = [find for find in updated_corpus_find_results if find[0].lower().strip() == key.lower().strip()]
           
            for item in collect_locations:
                # print(item)

                collection_location_info = full_geoparser_results[item[0]]
                locations_indexses.append(item[1:] + full_geoparser_results[item[0]])
                # print(f'place: {key}, raw_count: {value}, corp_count: {corp_find_number}')

        elif corp_find_number != value:
            print(f'place: {key}, raw_count: {value}, corp_count: {corp_find_number}')

            # print(full_geoparser_results[key])
           
            # sen_collected = collect_xml_sentence(full_geoparser_results[key], './geoparsed_corpus_test/' + path + '.txt.out.xml')
            # # pprint(sen_collected)

            # text = open_single_file_read('./corpus_test/' + path + '.txt')# load cleaned text

            # tokens_cleaned, _ = clean_tokenise(text)# tokenise text
            # # print(tokens_cleaned)

            
            # for extract in sen_collected:

            #     # len_extract = len(extract[1])
            #     just_extract = extract[6:]
            #     # print(just_extract)
            #     len_extract = len(just_extract)
            #     # print(len_extract)

            #     ngrams = clean_ngrams_single(tokens_cleaned, len_extract) # collect ngrams dict
            #     # print(ngrams)

            #     matches = find_all_match_instances_single(ngrams, just_extract)



    return locations_indexses



def add_coordinates(updated_geoparser_finds_in, corpus_location_matches_name_in):
    """
    puts lat lon to corpus finds
    """

    merged = []

    for find, f, ed, start, end in corpus_location_matches_name_in:

        # print(f'find is {find}')
        # print('\n')

        geo = updated_geoparser_finds_in.get(find)
        # print(f'lookup is: {geo}')
        # print('\n\n')
        
        if geo: # if an xy can be linked to find
            
            merged.append([find, geo[0], ed, start, end, geo[1], geo[2], geo[3], geo[4]])

        else:
            print(f'not coordinates found for {find}')

        
    return merged

        
