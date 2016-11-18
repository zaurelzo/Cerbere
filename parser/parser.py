#!/usr/bin/env python
# -*- coding: utf-8 -*-

#htm parser
from bs4 import BeautifulSoup
#stop words 
from stop_words import get_stop_words
#stemming 
from nltk.stem.porter import *
import time 

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
		

		#filter list using stop words and delete duplicates  
		filter_words = set ([ word for word in list_of_words if not (word in stop_words_english or word in stop_words_french)] ) 

		#apply stemming operation  
		filter_word_stemming = [stemmer.stem(word) for word in filter_words ] 

		return filter_word_stemming

if __name__ == '__main__':
	o1=parser()
	start_time = time.clock()
	for i in range (139):
		#pas de fichier commençant avec le numéro 0 et 127
		if i !=0 and i!=127:
			path = "../RessourcesProjet/corpus-utf8/D"+str(i)+".html"
			o1.parse(path)
			print ("done for : ", path)
	print "=============: ", time.clock() - start_time, "seconds"