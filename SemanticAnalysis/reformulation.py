#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON
from sparqlResquest import *

class reformulationRequest:
	"""docstring for sparqlResquest"""
	def __init__(self):
		pass

	#reformulation par ajout des synonymes des mots-clés sans affecter de poids
	def reformulation1(self, listKeyWords):
		result = sparqlResquest()
		listSynonymous = []
		finalListSynonymous = []
		for keyword in listKeyWords:
			listSynonymous = result.searchSynonymous(keyword)
			for synonymous in listSynonymous:
				print synonymous
				finalListSynonymous.append(synonymous)

		for keyword in finalListSynonymous:
			print keyword

	#reformulation par combinaison des synonymes et des mots-clés
	def reformulation2(self):
		result = sparqlResquest()

	def generateCombination(list)
		

if __name__ == '__main__':
	reform = reformulationRequest()

#<<<<<<< HEAD
	#listKeywords=["prix", "Omar Sy"]
	#reform.reformulation1(listKeywords)
#=======
	listKeywords=[["prix", "recompense","award"],["omar","caira"],["super","good","génial"]]
	for elt in reform.reformulation2(listKeywords):
		print elt 
#>>>>>>> 43e0338251ba983c3d4800d4b1d3bf3439f77d69
