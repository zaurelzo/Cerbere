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

		list_of_words = text.split()
		
		#get french and english stop words
		#stop_words_english = get_stop_words('en')
		stop_words_french = get_stop_words('fr')
		stemmer = FrenchStemmer()
		Global_stop_words_List=["?",".","!",",","'","|","...",":","–","&","-","€"]+stop_words_french

		#filter list using stop words and apply stemming operation   
		filter_words = [ stemmer.stem(self.cleanWord(word.lower())) for word in list_of_words if  not ((word.lower() in Global_stop_words_List) or self.isUrl(word.lower())==True)] 

		return filter_words

	#delete ... at the end of a word
	def cleanWord(self,word):
		Listind=range(0,len(word))
		Listind=Listind[::-1]
		result=word
		for ind in Listind:
			if word[ind]=='.':
				result=result[0:ind]
			else:
				return result
		return result

	def isUrl(self,url):
		if (re.match('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)):
			return True
		else:
			return False


if __name__ == '__main__':
	o1=parser()
	print o1.cleanWord("tech..nique")
	for elt in o1.parse("../RessourcesProjet/corpus-utf8/D"+str(1)+".html"):
		print elt

