#!/usr/bin/env python
# -*- coding: utf-8 -*-

#htm parser
from bs4 import BeautifulSoup
#stop words 
from stop_words import get_stop_words
#stemming 
from nltk.stem.porter import *


class parser:
	
	def __init__(self):
		pass

	##return a list which contains important words for the given file (stemming and delete stop word)
	def parse(self,file_path):
		file = open(file_path, "r+")
		#print (type(file.read()))
		soup = BeautifulSoup(file.read(),"html.parser")

		#kill all script and style elements
		for script in soup(["script", "style"]):
			script.extract() # rip it out

		text = soup.get_text()

		# break into lines and remove leading and trailing space on each 
		lines = (line.strip() for line in text.splitlines()) 
		# break multi-headlines into a line each 
		chunks = (phrase.strip() for line in lines for phrase in line.split(" ")) 
		# drop blank lines 
		text = '\n'.join(chunk for chunk in chunks if chunk)

		list_of_words = text.split() 
		#get french and english stop words
		stop_words_english = get_stop_words('en')
		stop_words_french = get_stop_words('fr')
		
		#stemmer
		stemmer = PorterStemmer()
		

		#filter list using stop words and apply stemming operation   
		filter_words = set ([ stemmer.stem(word) for word in list_of_words if not (word in stop_words_english or word in stop_words_french)] ) 

		return filter_words
