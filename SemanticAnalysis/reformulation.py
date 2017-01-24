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
		#on contruit la liste résultat avec les coefs
		finalListSynonymous = []
		for keyword in listKeyWords:
			listSynonymous = self.sparpqlObject.searchSynonymous(keyword)
			
			#transforme listSynonimous en unicode
			listSynonymousUnicode=[]
			for wo in listSynonymous:
				if isinstance(wo,str):
					wo=wo.decode("utf-8")
				listSynonymousUnicode.append(wo)
			
			if not (keyword.decode("utf-8") in listSynonymousUnicode):
				listSynonymousUnicode.append(keyword.decode("utf-8"))

			newCoef=float(1)
			#on construit la liste des résultats avec les coeffs 
			finalListSynonymous=finalListSynonymous+[ (w,newCoef) for w in listSynonymousUnicode]

		return finalListSynonymous

	#reformulation par combinaison des synonymes et des mots-clés
	#Attention,si les mots de la requête n'apparaissent pas dans la liste listOfListofSynonimous
	#après avoir éffectuée la requête, on les rajoutes. Ceci est la cas si les mots de la req 
	#n'appartiennent pas à la base de connaissances.
	def reformulation2(self,listKeyWords):
		listOfListofSynonimous=[]
		for keyword in listKeyWords:
			listOfListofSynonimous.append(self.sparpqlObject.searchSynonymous(keyword))

		#transforme toutes les combinaisons en unicode
		FinalListOfListofSynonimous=[[] for subList in listOfListofSynonimous ]
		for index,subList in enumerate(listOfListofSynonimous):
			for w in subList:
				if isinstance(w,str):
					w=w.decode("utf-8")
				FinalListOfListofSynonimous[index].append(w)
		
		finalListKeyWord=[]
		for keyword in  listKeyWords:
			if isinstance(keyword,str):
				keyword=keyword.decode("utf-8")
			finalListKeyWord.append(keyword)

		#on rajoute les mots de la requête s'ils n'y sont pas 
		for index,keyword in enumerate(finalListKeyWord):
			if not (keyword in FinalListOfListofSynonimous[index]):
				FinalListOfListofSynonimous[index].append(keyword)

		return self.createAllCombinaision(FinalListOfListofSynonimous)


	def tupleBelong(self,elt,listTuple):
		for a,b in listTuple:
			if elt==(a,b):
				return True
		return False


	def createAllCombinaision(self,listOfListofSynonimous):		
		listResultOfRequest=[]
		if len(listOfListofSynonimous)==0:
			return []
		elif len(listOfListofSynonimous)==1:
			for word in listOfListofSynonimous[0]:
				listResultOfRequest.append([[word,1]]) #ajout du poids
			return listResultOfRequest
		else:
			for word in listOfListofSynonimous[0]:
				for i in self.createAllCombinaision(listOfListofSynonimous[1:]):
					listResultOfRequest.append([[word,1]]+i)
			return listResultOfRequest



	#reformulation par ajout des synonymes des mots-clés avec affection des poids affecter de poids
	def reformulation3(self, listKeyWords):
		#on contruit la liste résultat avec les coefs
		finalListSynonymous = []
		for keyword in listKeyWords:
			listSynonymous = self.sparpqlObject.searchSynonymous(keyword)
			
			#transforme listSynonimous en unicode
			listSynonymousUnicode=[]
			for wo in listSynonymous:
				if isinstance(wo,str):
					wo=wo.decode("utf-8")
				listSynonymousUnicode.append(wo)
			
			if not (keyword.decode("utf-8") in listSynonymousUnicode):
				listSynonymousUnicode.append(keyword.decode("utf-8"))

			newCoef=float(1)/float((len(listSynonymousUnicode)))

			#on construit la liste des résultats avec les coeffs 
			finalListSynonymous=finalListSynonymous+[ (w,newCoef) for w in listSynonymousUnicode]

		return finalListSynonymous


	def reformulation4(self,listKeywords):
		resultList=self.sparpqlObject.searchResquestSPARQL(listKeywords)
		#print resultList
		#liste résultat en unicode
		finalList=[]
		for wo in resultList:
			if isinstance(wo,str):
				wo=wo.decode("utf-8")
			finalList.append((wo,1))

		for keyword in listKeywords:
			if not (keyword.decode("utf-8") in finalList):
				finalList.append((keyword.decode("utf-8"),1))
		return finalList

	def reformulation4Plus(self,listKeywords, reformulationOther):
		resultList=self.sparpqlObject.searchResquestSPARQL(listKeywords)
		#print resultList
		#liste résultat en unicode
		finalList=[]
		finalListAux=[]
		for wo in resultList:
			if isinstance(wo,str):
				wo=wo.decode("utf-8")
			finalListAux.append(wo)


		if resultList==[]:
			if reformulationOther=="ref1":
				finalList=self.reformulation1(listKeywords)
			elif reformulationOther=="ref2":
				finalList=self.reformulation2(listKeywords)
			elif reformulationOther=="ref3":
				finalList=self.reformulation3(listKeywords)
		else:
			for keyword in listKeywords:
				if not (keyword.decode("utf-8") in finalListAux):
					finalListAux.append(keyword.decode("utf-8"))
			for word in finalListAux:
				finalList.append([[word, 1]])

		return finalList 



if __name__ == '__main__':
	reform = reformulationRequest()

	#listKeywords=[["prix", "recompense","award"],["omar","caira"],["super","good","génial"]]
	for elt in reform.reformulation1(["personne", "a joué avec", "Omar Sy"]):
		print elt 
