#!/usr/bin/env python
# -*- coding: utf-8 -*-

import BeautifulSoup 

class parser:
	
	def __init__(self, file_path):

		self.file = open(file_path, "r+")
		print self.file.read()



if __name__ == '__main__':
	o1=parser("../RessourcesProjet/corpus-utf8/D1.html")