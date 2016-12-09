#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database_Manager.databaseManager import *
#stemming 
from nltk.stem.snowball import FrenchStemmer
#stop words 
from stop_words import get_stop_words

from eval.eval import * 

#afficher graphique
import matplotlib.pyplot as plt

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


		scoreNameDoc=[(0, "D"+str(i+1)+".html") for i in range(138)]
		print len(scoreNameDoc)
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
	#for elt in list_doc_selectionnes:
	#	print elt
	Liste_requests= [["personnes", "Intouchables"], ["lieu", "naissance", "Omar" ,"Sy"], ["personne", "récompensée", "Intouchables"],
	["palmarès", "Globes" ,"de", "Cristal", "2012"],["membre", "jury", "Globes", "de" ,"Cristal" ,"2012"],
	["prix", "Omar", "Sy", "Globes" ,"de" ,"Cristal", "2012"],["lieu", "Globes", "Cristal" ,"2012"],
	["prix", "Omar" ,"Sy"],  ["acteur", "joué" ,"avec", "Omar" , "Sy"] ]

	ListeColor=["b","g","r","c","m","y","k","b","g"]
	

	tab_rappel=[]
	tab_precision=[]
	for ind,req in enumerate(Liste_requests):
		list_doc_pertinant= eval_obj.readFileQrels("RessourcesProjet/qrels/qrelQ"+str(ind+1)+".txt")
		#print "requete en cours " , req
		list_doc_selectionnes=search_obj.runSearch(req)
		for elt in  eval_obj.calculRappelAndPrecision(list_doc_pertinant,list_doc_selectionnes):
			#print (elt)
			tab_rappel.append(elt[0])
			tab_precision.append(elt[1])
		plt.plot(tab_rappel,tab_precision,ListeColor[ind])
		tab_rappel=[]
		tab_precision=[]
	plt.show()

	






		
