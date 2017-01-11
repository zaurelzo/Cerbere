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
		pass

if __name__ == '__main__':
	reform = reformulationRequest()

	listKeywords=["prix", "Omar Sy"]
	reform.reformulation1(listKeywords)