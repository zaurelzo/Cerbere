#!/usr/bin/env python
# -*- coding: utf-8 -*-


import mysql.connector 

class databaseManager:

	def __init__(self):
		self.conn = mysql.connector.connect(host="localhost",user="root",password="mamaya", database="cerbere_db")
		self.cursor = self.conn.cursor()
	
	def createTables(self):
		self.cursor.execute(""" CREATE TABLE IF NOT EXISTS IndexTable (\
    	idIndex int NOT NULL AUTO_INCREMENT, \
    	word varchar(250) NOT NULL, \
    	PRIMARY KEY(idIndex) \
		);""")

		self.cursor.execute(""" CREATE TABLE IF NOT EXISTS Documents(\
    	idDocuments int NOT NULL AUTO_INCREMENT, \
    	title varchar(250) NOT NULL, \
    	PRIMARY KEY(idDocuments) \
		);""")

		self.cursor.execute(""" CREATE TABLE IF NOT EXISTS IndexDocumentsCorrespondences(\
		idIndex int NOT NULL, \
    	idDocuments int NOT NULL, \
    	frequence int NOT NULL, \
    	FOREIGN KEY (idIndex) REFERENCES IndexTable(idIndex), \
    	FOREIGN KEY (idDocuments) REFERENCES  Documents(idDocuments) \
		);""")



	def addElementsIndexTable(self,Listword):
		try:
			for word in Listword:
				self.cursor.execute("""INSERT INTO IndexTable (word) VALUES (%s)""", [word])
			self.conn.commit()
		except:
			print("ERROR WHEN ADD ELEMENT IN IndexTable")
			self.conn.rollback()


	def addElementDocumentsTable(self,ListTitle):
		try:
			for title in ListTitle:
				self.cursor.execute("""INSERT INTO Documents (title) VALUES (%s)""", [title])
			self.conn.commit()
		except:
			print("ERROR WHEN ADD ELEMENT IN Documents")
			self.conn.rollback()


	def addElementIndexDocumentsCorrespondences(self,dic_idWord_IdDoc_Freq):
		try:
			for (idWord,idDoc),freq in dic_idWord_IdDoc_Freq.iteritems():
				#print idWord,idDoc,freq
				self.cursor.execute('INSERT INTO IndexDocumentsCorrespondences (idIndex,idDocuments,frequence) VALUES ("%s","%s","%s")' % \
					(str(idWord),str(idDoc),str(freq)))
			self.conn.commit()
		except:
			print("ERROR WHEN ADD ELEMENT IN IndexDocumentsCorrespondences")
			self.conn.rollback()


	def deleteTables(self):
		self.cursor.execute(""" DROP TABLE IndexDocumentsCorrespondences ;""")
		self.cursor.execute(""" DROP TABLE IndexTable ;""")
		self.cursor.execute(""" DROP TABLE Documents ;""")


	def getIdByWord(self, word):
		self.cursor.execute("""SELECT idIndex FROM IndexTable WHERE word = '%s'""" % (word))
		result = self.cursor.fetchone()
		if result is not None:
			return result[0]
		else:
			return -1


	def freqByIdWordIdDoc(self, idWord, idDocumentsReq):
		self.cursor.execute("""SELECT frequence FROM IndexDocumentsCorrespondences WHERE idIndex ='%s' AND idDocuments='%s'""" % (str(idWord), str(idDocumentsReq)))
		result = self.cursor.fetchone()
		if result is not None:
			return result[0]
		else:
			return -1


	def countNbAppareancesWord(self, idWord):
		self.cursor.execute("""SELECT COUNT(idIndex) FROM IndexDocumentsCorrespondences WHERE idIndex ='%s'""" % (str(idWord)))
		result = self.cursor.fetchone()
		if result is not None:
			return result[0]
		else:
			return 0

if __name__ == '__main__':
	d1= databaseManager()
	#d1.deleteTables()

	# d1.createTables()
	# d1.addElementsIndexTable(["madad"])
	# d1.addElementsIndexTable(["bonjour"])
	# d1.addElementDocumentsTable(["la vie est belle"])
	# d1.addElementDocumentsTable(["gg"])
	# d1.addElementDocumentsTable(["gg1"])
	# d1.addElementDocumentsTable(["gg2"])
	d1.addElementIndexDocumentsCorrespondences({(1,1):23})
	d1.addElementIndexDocumentsCorrespondences({(1,2):20})
	d1.addElementIndexDocumentsCorrespondences({(2,3):23})
	#a={}
	#a[(1,25)]=78
	#d1.addElementIndexDocumentsCorrespondences(a)
	#d1.addElementsIndexTable("dfsd")
	print d1.countNbAppareancesWord(1)
