#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON
from sparqlResquest import *

class reformulationRequest:
	"""docstring for sparqlResquest"""
	def __init__(self):
		self.sparpqlObject = sparqlResquest()

	#reformulation par ajout des synonymes des mots-clés sans affecter de poids
	def reformulation1(self, listKeyWords):
		listSynonymous = []
		finalListSynonymous = []
		for keyword in listKeyWords:
			listSynonymous = self.sparpqlObject.searchSynonymous(keyword)
			for synonymous in listSynonymous:
				#print synonymous
				finalListSynonymous.append(synonymous)
		return finalListSynonymous


	#reformulation par combinaison des synonymes et des mots-clés
	#Attention,si les mots de la requête n'apparaissent pas dans la liste listOfListofSynonimous
	#après avoir éffectuée la requête, on les rajoutes. Ceci est la cas si les mots de la req 
	#n'appartiennent pas à la base de connaissances.
	def reformulation2(self,listKeyWords):
		listOfListofSynonimous=[]
		for keyword in listKeyWords:
			listOfListofSynonimous.append(self.sparpqlObject.searchSynonymous(keyword))

		#on rajoute les mots de la requête s'ils n'y sont pas 
		for index,keyword in enumerate(listKeyWords):
			if not (keyword in listOfListofSynonimous[index]):
				listOfListofSynonimous[index].append(keyword)

		return self.createAllCombinaision(listOfListofSynonimous)

	
	def createAllCombinaision(self,listOfListofSynonimous):		
		listResultOfRequest=[]
		if len(listOfListofSynonimous)==0:
			return []
		elif len(listOfListofSynonimous)==1:
			for word in listOfListofSynonimous[0]:
				listResultOfRequest.append([word])
			return listResultOfRequest
		else:
			for word in listOfListofSynonimous[0]:
				for i in self.createAllCombinaision(listOfListofSynonimous[1:]):
					listResultOfRequest.append([word]+i)
			return listResultOfRequest

if __name__ == '__main__':
	reform = reformulationRequest()

	#listKeywords=[["prix", "recompense","award"],["omar","caira"],["super","good","génial"]]
	for elt in reform.reformulation2(["personnes", "Intouchables"]):
		print elt 
