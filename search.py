#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database_Manager.databaseManager import *
#stemming 
from nltk.stem.snowball import FrenchStemmer
#stop words 
from stop_words import get_stop_words

from eval.eval import * 

import math

import matplotlib.pyplot as plt

class search:
	"""docstring for Search"""
	def __init__(self):
		self.db = databaseManager()

	def runSearch(self, list_keywords):
		stemmer = FrenchStemmer()
		stop_words_french = get_stop_words('fr')
		stop_words_french = [stemmer.stem(word.lower()) for word in stop_words_french]

		
		list_of_words_request=[]
		for word in list_keywords:
			#print word
			if isinstance(word,str):
				word=word.decode("utf-8").lower()
			else:
				word=word.lower()

			if (word in stop_words_french)==False:
				list_of_words_request.append(stemmer.stem(word))
		#for elt in list_of_words_request:
		#	print elt



		scoreNameDoc=[(0, "D"+str(i+1)+".html") for i in range(138)]
		nb_doc_collection = 138;
		#tab_avec_IDF = []
		#tab_sans_IDF = []


		#for elt in list_of_words_request:
		#	print elt

		#print len(scoreNameDoc)
		for idDoc in range(138):
			indiceDoc=idDoc+1;
			if indiceDoc != 127:

				for keyword in list_of_words_request:

					idWord = self.db.getIdByWord(keyword)
					freq = self.db.freqByIdWordIdDoc(idWord, indiceDoc)
					nb_doc_contenant_termes=self.db.countNbAppareancesWord(idWord)
					#if nb_doc_contenant_termes>0:
					#	IDF = math.log(float(nb_doc_collection)/float(nb_doc_contenant_termes))
					if freq!= -1:
						sCourant= scoreNameDoc[idDoc][0]
	#<<<<<<< HEAD
	#						sCourant_avec_IDF=sCourant+(freq * IDF)
	#=======
						#sCourant_avec_IDF=sCourant+(freq * IDF)
	#>>>>>>> ed90f6794413b247ef95ee35f4eb84d22af14c9c
						sCourant_sans_IDF=sCourant+freq 
						scoreNameDoc[idDoc]=(sCourant_sans_IDF,scoreNameDoc[idDoc][1])
		scoreNameDoc.sort(key=lambda tup: tup[0])
		return scoreNameDoc[::-1]

if __name__ == '__main__':
	search_obj=search()
	eval_obj= eval()

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

			# limiter i à 5, 10, 25.
		#x=[value for i,value in enumerate(tab_rappel) if i%7==0]
		#y=[value for i,value in enumerate(tab_precision) if i%7==0]
		#plt.plot(x,y,ListeColor[ind])

		x5=[value for i,value in enumerate(tab_rappel) if i<5]
		y5=[value for i,value in enumerate(tab_precision) if i<5]
		plt.plot(x5,y5,ListeColor[ind])

		print "valeurs des rappels pour la requête numéro"+str(ind)
		for rappel in x5:
			print "---------"+str(rappel)
		print "valeurs des précision pour la requête numéro"+str(ind)
		for rappel in y5:
			print "---------"+str(rappel)
		#x10=[value for i,value in enumerate(tab_rappel) if i<10]
		#y10=[value for i,value in enumerate(tab_precision) if i<10]
		#plt.plot(x10,y10,ListeColor[ind])

		#x25=[value for i,value in enumerate(tab_rappel) if i<25]
		#y25=[value for i,value in enumerate(tab_precision) if i<25]
		#plt.plot(x25,y25,ListeColor[ind])

		tab_rappel=[]
		tab_precision=[]
	plt.show()

	







		
