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
		print ("delete tables...")
		myDatabaseManager.deleteTables()
	elif(CREATE_TABLE):
		print "create tables..."
		myDatabaseManager.createTables()
	else:
		start_time=time.clock()
		#words to add in the database (to not have duplicates words)
		addWordsList=[]
		#List wchich contains parsing list result for each file
		list_Of_Result_ParsingDocument=[]
		List_Title_Documents=[]

		for num in range (139):
			#pas de fichier commençant avec le numéro 0 et 127
			if num !=0 and num!=127:

				#add documents titles 
				List_Title_Documents.append("D"+str(num)+".html")
				
				path = "RessourcesProjet/corpus-utf8/D"+str(num)+".html"
				resultList=myParser.parse(path)
				#print type (resultList)

				#maintain a list of all parsing list result
				list_Of_Result_ParsingDocument.append(resultList)

				#contain words which apppears once in all files
				addWordsList= list(set(addWordsList+resultList))#list union
				print "parsing done for : "+ path

		addWordsList.sort()
		#file = open("save_file", "r+")
		#for elt in addWordsList:
		#	file.write(elt+"\n")
		#for word in addWordsList:
		#	print "===> " +  word
		print ">>>>>>> Number of words :" + str(len(addWordsList))

		#create a global dict of  where key is(idWord,idDoc) and value is freq 
		globalDictWithFrequencies={}
		for idDoc ,subList in enumerate(list_Of_Result_ParsingDocument):
			print "traitment doc : " + str(idDoc+1)
			dicSubList=Counter(subList)

			for word,freq in dicSubList.iteritems():
				idWord=addWordsList.index(word)
				globalDictWithFrequencies[(idWord+1,idDoc+1)]=freq		
		print ">>>>>>> length global dic : " + str(len(globalDictWithFrequencies))

		print ">>>>>>> adding block of elements in the database"
		#add elements in the database
		myDatabaseManager.addElementDocumentsTable(List_Title_Documents)
		myDatabaseManager.addElementsIndexTable(addWordsList)
		myDatabaseManager.addElementIndexDocumentsCorrespondences(globalDictWithFrequencies)
		print ">>>>>>> Total process Time : ", time.clock() - start_time, "seconds"