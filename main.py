#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time 
from parser.parser import * 
from database_Manager.databaseManager import *
from collections import Counter

if __name__ == '__main__':
	#global Variables, chnages for a specific action (1 : do the action , 0 : don't do the action)
	DELETE_TABLES=0
	CREATE_TABLE=0


	myParser=parser()
	myDatabaseManager=databaseManager()

	if (DELETE_TABLES):
		myDatabaseManager.deleteTables()
	elif(CREATE_TABLE):
		myDatabaseManager.createTables()
	else:
		start_time=time.clock()

		#words to add in the database (to not have duplicates words)
		addWordsList=[]

		#List wchich contains parsing list result for each file
		list_Of_Result_ParsingDocument=[]

		for num in range (139):
			#pas de fichier commençant avec le numéro 0 et 127
			if num !=0 and num!=127:

				#add documents titles in the database
				#myDatabaseManager.addElementDocumentsTable("D"+str(num)+".html")
				
				path = "RessourcesProjet/corpus-utf8/D"+str(num)+".html"
				resultList=myParser.parse(path)
				#print type (resultList)

				#maintain a list of all parsing list result
				list_Of_Result_ParsingDocument.append(resultList)

				#to know wich words has been found in a previous file
				addWordsList= list(set(addWordsList+resultList))#list union
				print ("done for : ", path)

		addWordsList.sort()
		#print addWordsList

		#=========================================================================
		#Delete words with one occurences
		#ListWordsWithMultipleOccurences=[]
		#for word,occurence in (Counter(resultList)).iteritems():
		#	if occurence==1:
		#		ListWordsWithMultipleOccurences.append(word)
		#print ListWordsWithMultipleOccurences
		#=========================================================================
		print ("Number of words :", len(addWordsList))


		#create a global dict of frenquencies and add (idWord,idDoc,freq) in IndexDocumentsCorrespondences
		globalDictWithFrequencies={}
		for idDoc ,subList in enumerate(list_Of_Result_ParsingDocument):
			print ("traitment dic  doc ", idDoc)
			dicSubList=Counter(subList)

			for word,freq in dicSubList.iteritems():
				idWord=addWordsList.index(word)
				globalDictWithFrequencies[(idWord,idDoc)]=freq
		print "len dic : ",len(globalDictWithFrequencies)

		#add word in the database 
		#for i,word in enumerate (addWordsList):
		#	print ("adding word :", i)
		#	myDatabaseManager.addElementsIndexTable(word)

		print "=============: ", time.clock() - start_time, "seconds"