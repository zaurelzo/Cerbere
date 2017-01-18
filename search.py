#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database_Manager.databaseManager import *
#stemming 
from nltk.stem.snowball import FrenchStemmer
#stop words 
from stop_words import get_stop_words

from eval.eval import * 

import math
import sys,os,time
import numpy as np
import matplotlib.pyplot as plt

class search:
	"""docstring for Search"""
	def __init__(self):
		self.db = databaseManager()
		self.eval_obj= eval()

	def runSearch(self, list_keywords,termScoreMethod,documentScoreMethod):
		stemmer = FrenchStemmer()
		stop_words_french = get_stop_words('fr')
		stop_words_french = [stemmer.stem(word.lower()) for word in stop_words_french]

		list_keywords_split=[]

		for word in list_keywords:
			wordList = word.split()
			for w in wordList:
				list_keywords_split.append(w)
		
		list_of_words_request=[]
		for word in list_keywords_split:
			#print word
			if isinstance(word,str):
				word=word.decode("utf-8").lower()
			else:
				word=word.lower()

			if (word in stop_words_french)==False:
				list_of_words_request.append(stemmer.stem(word))
		#for elt in list_of_words_request:
		#	print elt


		# by default, documents score are equal to zero
		scoreNameDoc=[(0, "D"+str(i+1)+".html") for i in range(138)]
		nb_doc_collection = 138;


		#scoring all documents,
		for idDoc in range(138):
			if idDoc+1 != 127:
				score= self.computeDocumentScore(idDoc+1,list_of_words_request,termScoreMethod,documentScoreMethod)
				scoreNameDoc[idDoc]=(score,scoreNameDoc[idDoc][1])
		scoreNameDoc.sort(key=lambda tup: tup[0])
		return scoreNameDoc[::-1]


	def computeDocumentScore(self,indiceDoc,list_of_words_request,termScoreMethod,documentScoreMethod):

		#contains the score of each term
		termScoreVector=[]

		#compute freq vector or IDF vector
		for keyword in list_of_words_request:
			idWord = self.db.getIdByWord(keyword)
			freq = self.db.freqByIdWordIdDoc(idWord, indiceDoc)
			
			if termScoreMethod=="TF":
				termScoreVector.append(freq)
			elif termScoreMethod=="TF_IDF":
				nb_doc_contenant_termes=self.db.countNbAppareancesWord(idWord)
				IDF=0
				if nb_doc_contenant_termes>0:
					IDF = math.log(float(138)/float(nb_doc_contenant_termes))
				termScoreVector.append(IDF*freq)
		
		#security
		if (termScoreVector==[]):
			raise NameError("query terms are not in the database")
		
		#produit scalaire
		if documentScoreMethod==1:
			return sum(termScoreVector)
		#coef de dice
		elif documentScoreMethod==2:
			square_x= [term*term for term in termScoreVector ]
			return 2*sum(termScoreVector)/(sum(square_x)+len(list_of_words_request))
		#mesure du cosinus
		elif documentScoreMethod==3:
			square_x= [term*term for term in termScoreVector ]
			return sum(termScoreVector)/(sum(square_x)*len(list_of_words_request))
		#mesure du jaccard
		elif documentScoreMethod==4:
			square_x= [term*term for term in termScoreVector ]
			return sum(termScoreVector)/(sum(square_x)+len(list_of_words_request)-sum(termScoreVector))

	def evalTotal(self,Liste_requests,listTermScoreMethod,listDocumentScoreMethod,perQueryOrTotal):
		tabAveragePrecisionPerMethod=[]
		tabAverageRappelPerMethod=[]

		for indtermScoreMethod,termScoreMethod in enumerate(listTermScoreMethod):
			for indDocumentScoreMethode,documentScoreMethod in enumerate(listDocumentScoreMethod):

				tab_rappel=[]
				tab_precision=[]
				ListeColor=["b","g","r","c","m","y","k","r","g"]
				for ind,req in enumerate(Liste_requests):
					list_doc_pertinant= self.eval_obj.readFileQrels("RessourcesProjet/qrels/qrelQ"+str(ind+1)+".txt")
					#print "requete en cours " , req
					list_doc_selectionnes=self.runSearch(req,termScoreMethod,documentScoreMethod)

					#permet d'avoir un tableau de rappel et de précision
					for elt in  self.eval_obj.calculRappelAndPrecision(list_doc_pertinant,list_doc_selectionnes):
						
						tab_rappel.append(elt[0])
						tab_precision.append(elt[1])

					if per_Query_or_total=="perQuery":
						#permet de prendre juste un nombre d'éléments restreints pour le rappel et la précision
						x=[value for i,value in enumerate(tab_rappel) if i%7==0]
						y=[value for i,value in enumerate(tab_precision) if i%7==0]
						plt.plot(x,y,ListeColor[ind])
						plt.ylabel('Precision')
						plt.xlabel('Rappel')
						print ">>>>>>> Compute done for request "+ str(ind+1) + " with parameters "+ termScoreMethod + " and " + str(documentScoreMethod)
						print "P@5: "+ str(tab_precision[5]) + "| P@10:"+str(tab_precision[10]) + "| P@25:"+ str(tab_precision[25])
						print "===================================================="
					else:
							tabAveragePrecisionPerMethod.append(tab_precision)
							tabAverageRappelPerMethod.append(tab_rappel)
					tab_rappel=[]
					tab_precision=[]

				#on calcule la précision et le rappel moyen (ie pour toutes les requêtes) pour la méthode total
				#et on met sur le graphe les différentes valeurs à "ploter"
				#print "DEBUG ======== :  taille vecteur rappel " ,len (tabAverageRappelPerMethod)
				#print "DEBUG ======== :  taille vecteur precision ",  len (tabAveragePrecisionPerMethod)

				if per_Query_or_total=="total":
					tabAverageRappel=[]
					for ind,tabRappelPerRequest in enumerate(tabAverageRappelPerMethod):
						if ind==0:
							tabAverageRappel.append(np.array(tabRappelPerRequest))
						else:
							tabAverageRappel[0]=(np.array(tabRappelPerRequest) + tabAverageRappel[0])
					tabAverageRappel[0]=np.array(tabAverageRappel[0])/len(Liste_requests)
					#print "DEBUG ======== taille tableau rappel moyen pour une méthode : ", len (tabAverageRappel)
					#print "DEBUG ========  nombre element tableau rappel moyen pour une méthode ", len (tabAverageRappel[0])

					tabAveragePrecision=[]
					for ind,tabPrecisionPerRequest in enumerate(tabAveragePrecisionPerMethod):
						if ind==0:
							tabAveragePrecision.append(np.array(tabPrecisionPerRequest))
						else:
							tabAveragePrecision[0]=(np.array(tabPrecisionPerRequest)+tabAveragePrecision[0])
					tabAveragePrecision[0]=np.array(tabAveragePrecision[0])/len(Liste_requests)
					#print "DEBUG ======== taille tableau précision moyen pour une méthode : ", len (tabAveragePrecision)
					#print "DEBUG ========  nombre element tableau précision moyen pour une méthode ", len (tabAveragePrecision[0])

					#Quelques valeurs à "ploter dans le graphe
					toPlotRappel=[value for i,value in enumerate(tabAverageRappel[0]) if i%7==0 ]
					toPlotPrecision=[value for i,value in enumerate(tabAveragePrecision[0]) if i%7==0]

					plt.plot(toPlotRappel,toPlotPrecision,ListeColor[indDocumentScoreMethode+indtermScoreMethod-1],linewidth=1.5, linestyle="-",\
					 label="Met "+ termScoreMethod + " " +str(documentScoreMethod ) )
					plt.legend(bbox_to_anchor=(0., 1.05, 1., .105), loc=0,ncol=3, mode="expand", borderaxespad=0.)

					print ">>>>>>> Compute done for method "+ per_Query_or_total + " with parameters "+ termScoreMethod + " and " + str(documentScoreMethod)
					print "P@5 moy : "+ str(tabAveragePrecision[0][5]) + "| P@10 moy :"+str(tabAveragePrecision[0][10]) + "| P@25 moy :"+ str(tabAveragePrecision[0][25])
					print "==============================================================="
					plt.ylabel('Precision moy')
					plt.xlabel('Rappel moy')

				tabAverageRappelPerMethod=[]
				tabAveragePrecisionPerMethod=[]

		#show graph
		plt.show()

if __name__ == '__main__':
	listTermScoreMethod=[]
	listDocumentScoreMethod=[]
	per_Query_or_total=""

	if len(sys.argv) != 4:
		print "[Usage] python search.py <TF|TF_IDF> <1|2|3|4> <perQuery|total>"
		sys.exit(1)
	else:
		per_Query_or_total=sys.argv[3]
		#print "arguement 3 ", sys.argv[3]
		if sys.argv[3]=="perQuery":
			listTermScoreMethod.append(sys.argv[1])
			listDocumentScoreMethod.append(int(sys.argv[2]))
		elif sys.argv[3]=="total":
			listTermScoreMethod.append("TF")
			listTermScoreMethod.append("TF_IDF")
			listDocumentScoreMethod=[v+1 for v in range(4)]
		else:
			print ("3rd argument is not valid")
			sys.exit(1)
	

	List_requests= [["personnes", "Intouchables"], [ "lieu naissance", "Omar Sy"], ["personne récompensée", "Intouchables"],
	["palmarès", "Globes de Cristal 2012"],[ "membre jury", "Globes de Cristal 2012"],
	["prix", "Omar Sy", "Globes de Cristal 2012"],[ "lieu", "Globes Cristal 2012"],
	[ "prix", "Omar Sy"],  ["acteur", "joué avec", "Omar Sy"] ]

	search_obj=search()
	start_time=time.clock()
	#print listTermScoreMethod
	print listDocumentScoreMethod
	search_obj.evalTotal(List_requests,listTermScoreMethod,listDocumentScoreMethod,per_Query_or_total)
	print ">>>>>>> Total process Time : ", time.clock() - start_time, "seconds"
