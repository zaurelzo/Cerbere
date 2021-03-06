#!/usr/bin/env python
# -*- coding: utf-8 -*-

#htm parser
from bs4 import BeautifulSoup
#stop words 
from stop_words import get_stop_words
#stemming 
from nltk.stem.snowball import FrenchStemmer
import re

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

		text = soup.get_text(separator=" ")

		# break into lines and remove leading and trailing space on each 
		lines = (line.strip() for line in text.splitlines()) 
		# break multi-headlines into a line each 
		chunks = (phrase.strip() for line in lines for phrase in line.split(" ")) 
		# drop blank lines 
		text = '\n'.join(chunk for chunk in chunks if chunk) 

		#convert all str objects to unicode objects (usefull when search words which are not stop words)
		list_of_words=[]
		for word in text.split():
			if isinstance(word,str):
				list_of_words.append(word.decode("utf-8").lower())
			else:
				list_of_words.append(word.lower())

		#get french stop words
		stop_words_french = get_stop_words('fr')
		stemmer = FrenchStemmer()
		
		#meilleure heuristique : au lien d'enlever les caractères 1 à 1, on se débarasse de ceux ayant une taille de 1 
		#Global_stop_words_List=["?",".","!",",","'","|","...",":","–","&","-","€"]+stop_words_french
		Global_stop_words_List=[word for word in list_of_words if len(word)==1] + stop_words_french

		#convert all str objects to unicode objects (usefull when search words which are not stop words)
		filter_stop_words_list=[]
		for word in Global_stop_words_List:
			if isinstance(word,str):
				filter_stop_words_list.append(stemmer.stem(word.decode("utf-8").lower()))
			else:
				filter_stop_words_list.append(stemmer.stem(word.lower()))


		#filter list using stop words and apply stemming operation 
		filter_words = []
		for word in list_of_words:
			word = word.lower()
			if not self.isUrl(word):
				list_clean_words = self.cleanWord(word)
				#list_clean_words=[stemmer.stem(cword) for cword in list_of_words]
				for clean_word in list_clean_words:
					if not (stemmer.stem(clean_word) in filter_stop_words_list):
						filter_words.append(stemmer.stem(clean_word))

		return filter_words

	#delete stupid caracters
	def cleanWord(self,word):
		return re.findall(r"[a-z0-9]+", word)

	def isUrl(self,url):
		if (re.match('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)):
			return True
		else:
			return False


if __name__ == '__main__':
	o1=parser()
	l=  o1.parse("../RessourcesProjet/corpus-utf8/D"+str(1)+".html")
	print l
	 