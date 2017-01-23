#!/usr/bin/env python
# -*- coding: utf-8 -*-

#stemming 
from nltk.stem.snowball import FrenchStemmer

class stopWords:
	
	def __init__(self):
		self.path="/Users/jordycabannes/Desktop/Bureau/Cerbere/stopwords"

	def getListStopwords(self):
		stemmer = FrenchStemmer()
		file = open(self.path, "r+")
		list_words= []
		res=[]
		indice=0
		#Il n'y q'une seule ligne dans le fichier
		for line in file:
			list_words = line.split(',')

		for word in list_words:
			if isinstance(word,str):
				word=stemmer.stem(word.decode("utf-8").lower())
			else:
				word=stemmer.stem(word.lower())
			res.append(word)
		return res

if __name__ == '__main__':
	o1=stopWords()
	res = o1.getListStopwords()

	for elt in res:
		print elt