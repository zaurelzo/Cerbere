#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON

class sparqlResquest:
	"""docstring for sparqlResquest"""
	def __init__(self):
		pass

	def searchSynonymous(self, word):
		sparql = SPARQLWrapper("http://localhost:3030/Base_de_connaissances")
		query = """
		    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		SELECT ?label
		WHERE {
		  ?subject rdfs:label \"""" + word +"""\"@fr.
		  ?subject rdfs:label ?label
		}"""
  		
		print query

  		sparql.setQuery(query)
	

		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()

		listResults=[]
		for result in results["results"]["bindings"]:
			listResults.append(result["label"]["value"])
		return listResults

	def searchWithProperty(self, property, word):
		sparql = SPARQLWrapper("http://localhost:3030/Base_de_connaissances")


if __name__ == '__main__':
	req = sparqlResquest()

	for elt in req.searchSynonymous("prix"):
		print elt


