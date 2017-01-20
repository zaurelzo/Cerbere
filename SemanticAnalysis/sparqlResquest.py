#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON

class sparqlResquest:
	"""docstring for sparqlResquest"""
	def __init__(self):
		pass

	def searchSynonymous(self, word):
		sparql = SPARQLWrapper("http://localhost:3030/ontologies_omar_sy")
		query = """
		    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		SELECT ?label
		WHERE {
		  ?subject rdfs:label \"""" + word +"""\"@fr.
		  ?subject rdfs:label ?label
		}"""  		

  		sparql.setQuery(query)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()

		listResults=[]
		for result in results["results"]["bindings"]:
			listResults.append(result["label"]["value"])
		return listResults

	#permet de savoir si un des mots est une propriété de la base de connaissances
	def searchProperty(self, word):
		isProperty=False

		sparql = SPARQLWrapper("http://localhost:3030/Base_de_connaissances")
		query = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
				PREFIX owl: <http://www.w3.org/2002/07/owl#>
				PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
				PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
				SELECT ?type
				WHERE {
				  	?type a owl:ObjectProperty.
				  	?type rdfs:label \"""" + word +"""\"@fr
				}"""
		sparql.setQuery(query)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()

		listResults=[]
		for result in results["results"]["bindings"]:
			listResults.append(result)

		if listResults!=[]:
			isProperty=True
		return isProperty


	def searchWithProperty(self, propertyReq, word):
		sparql = SPARQLWrapper("http://localhost:3030/Base_de_connaissances")
		query = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		SELECT ?label
		WHERE {
		    ?subject ?property ?object.
		  	?property rdfs:label  \"""" + propertyReq +"""\"@fr.
		  	?subject rdfs:label \"""" + word +"""\"@fr.
			?object rdfs:label ?label
		}"""

		sparql.setQuery(query)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()

		listResults=[]
		for result in results["results"]["bindings"]:
			listResults.append(result["label"]["value"])
		return listResults


	#1 correspond au requête de type 1 (synonyme), 3 correspond au requête de type 3 (avec propriété)
	def whichSearchMethod(self, listKeywords):
		requestType=1
		nameProperty=""
		for elt in listKeywords:
			if self.searchProperty(elt)!=False:
				requestType=3;
				nameProperty=elt;
		result=[requestType, nameProperty]
		return result

	def searchResquestSPARQL(self, listKeywords):
		listResults=[]

		methodChoice=self.whichSearchMethod(listKeywords)
		sizeListKeywords = len(listKeywords)
		#if methodChoice[0]==1:
		#	for word in listKeywords:
		#			listResults.append(self.searchSynonymous(word))
		if methodChoice[0]==3 and sizeListKeywords==2: 
			for word in listKeywords:
				if word != methodChoice[1]:
					word_request=word
			listResults= self.searchWithProperty(methodChoice[1], word_request)	
		return listResults



if __name__ == '__main__':
	req = sparqlResquest()

	res = req.searchResquestSPARQL(["personnes", "Intouchables"])
	print res


