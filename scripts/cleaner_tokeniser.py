## python37

import spacy
from spacy.tokenizer import Tokenizer
from nltk import ngrams
import re
import os
from .loader import *


def custom_tokenizer(nlp):
	"""
	compile custom tokeniser that does not split words on punctuation on infix
	which means searcher copes with OCR text better (hopefully)
	"""
	prefix_re = re.compile(r'''^[^a-zA-Z]''')
	suffix_re = re.compile(r'''[^a-zA-Z]$''')
	##infix_re = re.compile(r'''[-~]''')
	simple_url_re = re.compile(r'''^https?://''')

	return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                                suffix_search=suffix_re.search,
                                ##infix_finditer=infix_re.finditer,
                                token_match=simple_url_re.match)


def clean_tokenise(text_in):
	"""
	word tokenizer using custom SpaCy tokeniser. Preserves new line splits
	"""

	nlp = spacy.blank('en')# define blank tokeniser
	nlp.max_length = 5000000 # set max length to more that 100,000 characters

	nlp.tokenizer = custom_tokenizer(nlp) # compile custom tokeniser

	tokenized_class = nlp(text_in)# split text into tokens with spacy

	tokenized_text = [token.text for token in tokenized_class]# get text tokens from class
	# print(tokenized_text)

	just_words = [token.text for token in tokenized_class if not token.is_punct]
	# print(just_words)

	word_count = {}

	for word in just_words:

		if not word.lower().strip() in word_count:

			word_count[word.lower().strip()] = 0 

		word_count[word.lower().strip()] += 1 # increase find counter if more than one  

	
	cleaned_text_tokens = [e.strip().lower() for e in tokenized_text if e != '' and e != '\n']# clean tokens and lower for searching 
	# print(cleaned_tokens)

	

	return cleaned_text_tokens, word_count


def clean_ngrams(text_in, ngram_len):
	"""
	using search list token range created ngram:indexes pairs
	"""

	all_ngram_dict = {}# create unique bigram dictionary of corpus for each ngram length of input search list

	for gram_len in ngram_len:# iterate over ngram lengths to form unique ngram dict

		ngram_dict = {}# create empty ngram dict

		ngramz = [' '.join(ngram) for ngram in ngrams(text_in, gram_len)]# form ngram
		# print(ngramz)
		# print(f'Total words in corpus for ngram len: {gram_len} is: {len(ngramz)}')

		
		for i, ngram in enumerate(ngramz): # iterate over ngrams

			if not ngram in ngram_dict:# if ngram not already a dict key

				ngram_dict[ngram] = [] # make it a dict key

			ngram_dict[ngram].append(i) # add indices to dict key as list value


		all_ngram_dict[gram_len] = ngram_dict # add whole ngram list to main dict with ngram len as key


	return all_ngram_dict

def clean_ngrams_single(text_in, ngram_len):
	"""
	using search list token range created ngram:indexes pairs
	"""

	all_ngram_dict = {}# create unique bigram dict of corpus for each ngram length of input search list


	ngram_dict = {}# create empty ngram dict

	ngramz = [' '.join(ngram) for ngram in ngrams(text_in, ngram_len)]# form ngram
	# print(ngramz)
	# print(f'Total words in corpus for ngram len: {gram_len} is: {len(ngramz)}')

	
	for i, ngram in enumerate(ngramz): # iterate over ngrams

		if not ngram in ngram_dict:# if ngram not already a dict key

			ngram_dict[ngram] = [] # make it a dict key

		ngram_dict[ngram].append(i) # add indices to dict key as list value


	all_ngram_dict[ngram_len] = ngram_dict # add whole ngram list to main dict with ngram len as key

	return all_ngram_dict




def clean_corpus_for_geoparser(file_in):
	"""
	replaces special characters in tcorpus to allow geoparser to run
	"""
	basename = os.path.basename(file_in)
	filename = os.path.splitext(basename)[0]
	# print(filename)

	text = open_single_file_read(file_in)
	# print(text[:1000])

	clean1 = re.sub(r'&', r'&amp;', text)# 
	clean2 = re.sub(r'<', r'&lt;', clean1)# 
	clean3 = re.sub(r'>',r'&gt;', clean2)# 
	# clean4 = re.sub(r"'",r'&#39;', clean3)# 
	# clean5 = re.sub(r'"',r'&#34;', clean4)# 
	# print(clean3[:1000])


	return clean3, filename
		





	