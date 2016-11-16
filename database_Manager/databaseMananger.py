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

	def deleteTables(self):
		self.cursor.execute(""" DROP TABLE IndexDocumentsCorrespondences ;""")
		self.cursor.execute(""" DROP TABLE IndexTable ;""")
		self.cursor.execute(""" DROP TABLE Documents ;""")

if __name__ == '__main__':
	d1= databaseManager()
	d1.deleteTables()
	#d1.createTables()