#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database_Manager.databaseManager import *

class search:
	"""docstring for Search"""
	def __init__(self):
		self.db = databaseManager()

	def runSearch(self, list_keywords):
		list_keywords=[word.lower() for word in list_keywords]
		scoreNameDoc=[(0, "D"+str(i+1)+"html") for i in range(138)]
		for idDoc in range(138):
			indiceDoc=idDoc+1;
			if indiceDoc != 127:
				for keyword in list_keywords:

					idWord = self.db.getIdByWord(keyword)
					freq = self.db.freqByIdWordIdDoc(idWord, indiceDoc)
					if freq!= -1:
						sCourant= scoreNameDoc[idDoc][0]
						sCourant=sCourant+freq
						scoreNameDoc[idDoc]=(sCourant,scoreNameDoc[idDoc][1])
		scoreNameDoc.sort(key=lambda tup: tup[0])
		return scoreNameDoc[::-1]

if __name__ == '__main__':
	s=search()
	for elt in s.runSearch(["omar", "sy", "intouchables"]):
		if elt[0]!=0:
			print elt







		
