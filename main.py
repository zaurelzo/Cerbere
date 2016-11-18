#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time 
from parser.parser import * 

if __name__ == '__main__':
	o1=parser()
	start_time = time.clock()
	for i in range (139):
		#pas de fichier commençant avec le numéro 0 et 127
		if i !=0 and i!=127:
			path = "RessourcesProjet/corpus-utf8/D"+str(i)+".html"
			o1.parse(path)
			print ("done for : ", path)
	print "=============: ", time.clock() - start_time, "seconds"