#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database_Manager.databaseManager import *
#stemming 
from nltk.stem.snowball import FrenchStemmer
#stop words 
from stop_words import get_stop_words

from eval.eval import * 

class search:
	"""docstring for Search"""
	def __init__(self):
		self.db = databaseManager()

	def runSearch(self, list_keywords):
		stemmer = FrenchStemmer()
		stop_words_french = get_stop_words('fr')
		stop_words_french = [word.lower() for word in stop_words_french]

		
		list_of_words_request=[]
		for word in list_keywords:
			if isinstance(word,str):
				word=word.decode("utf-8").lower()
			else:
				word=word.lower()

			if (word in stop_words_french)==False:
				list_of_words_request.append(stemmer.stem(word.lower()))

		#list_of_words_request =[stemmer.stem(word.lower()) for word in list_of_words_request if not (word.lower() in stop_words_french)]
		scoreNameDoc=[(0, "D"+str(i+1)+".html") for i in range(138)]

		for idDoc in range(138):
			indiceDoc=idDoc+1;
			if indiceDoc != 127:
				for keyword in list_of_words_request:

					idWord = self.db.getIdByWord(keyword)
					freq = self.db.freqByIdWordIdDoc(idWord, indiceDoc)
					if freq!= -1:
						sCourant= scoreNameDoc[idDoc][0]
						sCourant=sCourant+freq
						scoreNameDoc[idDoc]=(sCourant,scoreNameDoc[idDoc][1])
		scoreNameDoc.sort(key=lambda tup: tup[0])
		return scoreNameDoc[::-1]

if __name__ == '__main__':
	search_obj=search()
	eval_obj= eval()
	list_doc_pertinant= eval_obj.readFileQrels("RessourcesProjet/qrels/qrelQ3.txt")
	list_doc_selectionnes=search_obj.runSearch(["personne", "récompensée", "Intouchables"])
	#for elt in list_doc_selectionnes:
	#	print elt
	print eval_obj.calculRappelAndPrecision(list_doc_pertinant,list_doc_selectionnes)
	






		
