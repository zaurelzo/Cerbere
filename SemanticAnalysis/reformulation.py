#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from SPARQLWrapper import SPARQLWrapper, JSON
#from sparqlResquest import *

class reformulationRequest:
	"""docstring for sparqlResquest"""
	def __init__(self):
		pass

	# #reformulation par ajout des synonymes des mots-clés sans affecter de poids
	# def reformulation1(self, listKeyWords):
	# 	result = sparqlResquest()
	# 	listSynonymous = []
	# 	finalListSynonymous = []
	# 	for keyword in listKeyWords:
	# 		listSynonymous = result.searchSynonymous(keyword)
	# 		for synonymous in listSynonymous:
	# 			print synonymous
	# 			finalListSynonymous.append(synonymous)

	# 	for keyword in finalListSynonymous:
	# 		print keyword

	#reformulation par combinaison des synonymes et des mots-clés
	def reformulation2(self,listOfListofSynonimous):
		
		listResultOfRequest=[]
		if len(listOfListofSynonimous)==0:
			return []
		elif len(listOfListofSynonimous)==1:
			subListResult=[]
			for word in listOfListofSynonimous[0]:
				subListResult.append([word])
			return subListResult
		else:
			for word in listOfListofSynonimous[0]:
				for i in self.reformulation2(listOfListofSynonimous[1:]):
					listResultOfRequest.append([word]+i)
			return listResultOfRequest

if __name__ == '__main__':
	reform = reformulationRequest()

	listKeywords=[["prix", "recompense","award"],["omar","caira"],["super","good","génial"]]
	for elt in reform.reformulation2(listKeywords):
		print elt 