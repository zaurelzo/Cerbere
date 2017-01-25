#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database_Manager.databaseManager import *
#stemming 
from nltk.stem.snowball import FrenchStemmer
#stop words 
from stop_words import get_stop_words
from eval.eval import * 

import math
from math import *
import sys,os,time
import numpy as np
import matplotlib.pyplot as plt
from SemanticAnalysis.reformulation import *

class search:
	"""docstring for Search"""

	def __init__(self):
		self.db = databaseManager()
		self.eval_obj= eval()
		self.reformulationObject = reformulationRequest()

	#retourne liste ordonnée documents pertinents
	def runSearch(self, list_keywords,termScoreMethod,documentScoreMethod):
		stemmer = FrenchStemmer()
		stop_words_french = get_stop_words('fr')
		stop_words_french = [stemmer.stem(word.lower()) for word in stop_words_french]

		list_keywords_split=[]

		for word,coef in list_keywords:
			wordList = word.split()
			for w in wordList:
				#on redivise le coef, par le nombre de mots trouvé en splitant.
				#Comme ça on re répartie le "coef" sur les nouveaux mots
				newCoef=float(coef)/float(len(wordList))
				list_keywords_split.append((w,newCoef))
		

		list_of_words_request=[]
		for word,coef in list_keywords_split:
			#print word
			if isinstance(word,str):
				word=word.decode("utf-8").lower()
			else:
				word=word.lower()
			#print "*************",stemmer.stem(word)
			#if (word in stop_words_french)==False:
			list_of_words_request.append((stemmer.stem(word),coef))
		
		#for elt in stop_words_french:
		#	print "******************",elt


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



	#retourne liste ordonnée documents pertinents
	def computeDocumentScore(self,indiceDoc,list_of_words_request,termScoreMethod,documentScoreMethod):
		#contains the score of each term
		termScoreVector=[]
		queryVector=[]

		#compute freq vector or IDF vector
		for keyword,coef in list_of_words_request:
			freq=0
			idWord = self.db.getIdByWord(keyword)
			if idWord!=-1:
				freq = self.db.freqByIdWordIdDoc(idWord, indiceDoc)
			#else:#debug
			#	print "------------------idWord vaut -1 pour le mot ", keyword

			if termScoreMethod=="TF":
			  	termScoreVector.append(float(freq))
			elif termScoreMethod=="TF_IDF":
				IDF=0
			  	nb_doc_contenant_termes=self.db.countNbAppareancesWord(idWord)
			  	if nb_doc_contenant_termes>0:
			  		IDF = float(math.log(float(138))/float(nb_doc_contenant_termes))
			  	termScoreVector.append(float(IDF)*float(freq))
			queryVector.append(float(coef))

		
		#security
		if (termScoreVector==[]):
			raise NameError("query terms are not in the database")

		# # #produit scalaire
	 	if documentScoreMethod==1:
	 		#print "*************",queryVector[0]
	 		arrayMul=[ float(v)*float(queryVector[i]) for i,v in enumerate(termScoreVector) ]
	 		return float(sum(arrayMul))
		   	#return float(sum(np.array(termScoreVector)*np.array(queryVector)))

		 # #coef de dice
		elif documentScoreMethod==2:
		   	#Numérateur
		   	arrayMul=[ float(v)*float(queryVector[i]) for i,v in enumerate(termScoreVector) ]
		   	numerateur=float(sum(arrayMul))
		   	#numerateur = float(sum(np.array(termScoreVector)*np.array(queryVector)))

			#Dénominateur
			square_x= [float(term)*float(term) for term in termScoreVector ]
			square_y= [float(coef)*float(coef) for coef in queryVector ]
			denominateur = float(sum(square_x))+float(sum(square_y))
			if denominateur==0.0:
				return 0
			else:
				return float(2)*float(numerateur)/float(denominateur)

		##mesure du cosinus
		elif documentScoreMethod==3:
			#Numérateur
			arrayMul=[ float(v)*float(queryVector[i]) for i,v in enumerate(termScoreVector) ]
		   	numerateur=float(sum(arrayMul))
		   	#for inp,va in enumerate(termScoreVector):
		   	#	print str(float(va)*float(queryVector[inp]))
			#numerateur = float(sum(np.array(termScoreVector)*np.array(queryVector)))

			#Dénominateur
			square_x= [float(term)*float(term) for term in termScoreVector ]
			square_y= [float(coef)*float(coef) for coef in queryVector ]
			denominateur = float(sqrt(float(sum(square_x))*float(sum(square_y))))
			if denominateur==0.0:
				return 0
			else:
				return float(numerateur)/float(denominateur)

		#mesure du jaccard
		elif documentScoreMethod==4:
		   	#Numérateur 
		   	arrayMul=[ float(v)*float(queryVector[i]) for i,v in enumerate(termScoreVector) ]
		   	numerateur=float(sum(arrayMul))
		   	#numerateur = float(sum(np.array(termScoreVector)*np.array(queryVector)))

		   	#Dénominateur
		   	square_x= [float(term)*float(term) for term in termScoreVector ]
		   	square_y= [float(coef)*float(coef) for coef in queryVector ]
		   	denominateur = float(sum(square_x))+float(sum(square_y))-float(numerateur)
		   	if denominateur==0.0:
		   		return 0
		   	else:
		   		return float(numerateur)/float(denominateur)



	def evalTotal(self,Liste_requests,listTermScoreMethod,listDocumentScoreMethod,perQueryOrTotal,sortMethod,reformulationType, subReformulationType):
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

					#DONE : au lieu d'appeler runSearch, on appel notre superbe fonction qui se charge de faire de la 
					#reformulation.
					list_doc_selectionnes=self.preTreatementforSemanticSearch(sortMethod,req,termScoreMethod,\
						documentScoreMethod,reformulationType, subReformulationType)

					#permet d'avoir un tableau de rappel et de précision
					for elt in  self.eval_obj.calculRappelAndPrecision(list_doc_pertinant,list_doc_selectionnes):
						
						tab_rappel.append(elt[0])
						tab_precision.append(elt[1])

					if per_Query_or_total=="perQuery":
						#permet de prendre juste un nombre d'éléments restreints pour le rappel et la précision
						x=[value for i,value in enumerate(tab_rappel) if i%7==0]
						y=[value for i,value in enumerate(tab_precision) if i%7==0]
						plt.plot(x,y,ListeColor[ind])
						plt.ylabel('Precision (semantic)')
						plt.xlabel('Rappel (semantic)')
						print ">>>>>>> Compute done for request "+ str(ind+1) + " with parameters "+ termScoreMethod + " and " + str(documentScoreMethod)
						print "P@5: "+ str(tab_precision[5]) + "| P@10:"+str(tab_precision[10]) + "| P@25:"+ \
						str(tab_precision[25])
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
					plt.legend(shadow=True, fancybox=True)

					print ">>>>>>> Compute done for method "+ per_Query_or_total + " with parameters "+ termScoreMethod + " and " + str(documentScoreMethod)
					averP=(float(tabAveragePrecision[0][5])+float(tabAveragePrecision[0][10])+float(tabAveragePrecision[0][25]))/float(3)
					print "P@5 moy : "+ str(tabAveragePrecision[0][5]) + "| P@10 moy :"+str(tabAveragePrecision[0][10]) +\
					"| P@25 moy :"+ str(tabAveragePrecision[0][25]) +" | (P@5,10,25)/3 : "+ str(averP)+"|Total average: "+str(np.average(tabAveragePrecision[0]))
					print "==============================================================="
					plt.ylabel('Precision moy(semantic)')
					plt.xlabel('Rappel moy(semantic)')

				tabAverageRappelPerMethod=[]
				tabAveragePrecisionPerMethod=[]
		#show graph
		plt.show()



	def preTreatementforSemanticSearch(self,sortMethod,Liste_requests,termScoreMethod,documentScoreMethod,reformulationType, subReformulationType):
		listDocumentSelectionnes=[]
		if reformulationType=="ref1":
			list_keywords_synonimous =self.reformulationObject.reformulation1(Liste_requests)
			return self.runSearch(list_keywords_synonimous,termScoreMethod,documentScoreMethod)
			
		elif reformulationType=="ref2":
			list_All_Combinaisons=self.reformulationObject.reformulation2(Liste_requests)
			list_All_documents_selections=[]
			for listOneCombinaison in list_All_Combinaisons:
				v=self.runSearch( listOneCombinaison,termScoreMethod,documentScoreMethod)
				#on trie les documents en fonction de leur nom
				v.sort(key=lambda tup: tup[1])
				list_All_documents_selections.append(v)
			return self.heuristiqueSortDocuments(sortMethod,list_All_documents_selections)

		elif reformulationType=="ref3":
			list_keywords_synonimous =self.reformulationObject.reformulation3(Liste_requests)
			return self.runSearch(list_keywords_synonimous,termScoreMethod,documentScoreMethod)

		elif reformulationType=="ref4":
			list_keywords_synonimous =self.reformulationObject.reformulation4(Liste_requests)
			return self.runSearch(list_keywords_synonimous,termScoreMethod,documentScoreMethod)
		elif reformulationType=="ref4+":
			list_keywords_synonimous =self.reformulationObject.reformulation4Plus(Liste_requests, subReformulationType)
			if subReformulationType=="ref2":
				list_All_documents_selectionsBis=[]
				for listOneCombinaisonBis in list_keywords_synonimous:
					v=self.runSearch( listOneCombinaisonBis,termScoreMethod,documentScoreMethod)
					#on trie les documents en fonction de leur nom
					v.sort(key=lambda tup: tup[1])
					list_All_documents_selectionsBis.append(v)
				return self.heuristiqueSortDocuments(sortMethod,list_All_documents_selectionsBis)
			else:
				return self.runSearch(list_keywords_synonimous,termScoreMethod,documentScoreMethod)


	#TODO finir cette fonction qui permet à partir de des listes des résultats de touutes les combinaisons (pour une requete)
	#de renvoyer une liste résultat (qui correspond à la liste des docs selectionnée) 
	def heuristiqueSortDocuments(self,sortMethod,list_All_documents_selections):
		#on va contruire une liste qui ne contient que des "np array" des scores pour chaque liste de 
		#list_All_documents_selections
		ListVectorScoresubListSynonimous=[ [] for nbElt in range(len(list_All_documents_selections)) ]
		for index, subList in enumerate(list_All_documents_selections):
			for score,nameDoc in subList:
				ListVectorScoresubListSynonimous[index].append(float(score)) 
		
		#on transfore les listes remplies ci-dessus en np array et on construit la liste résultat 
		#en fonction de si on fait une somme ou si on cherche le max
		if sortMethod=="sum":
			finalListResult=[]
			for index,subList in enumerate(ListVectorScoresubListSynonimous):
				if index==0:
					finalListResult.append(np.array(subList))
				else:
					finalListResult[0]=finalListResult[0]+np.array(subList)
			finalListResult[0]=finalListResult[0]/float(len(list_All_documents_selections))
			
			#on réassocie à chaque document à son nouveau score et retourne cette nouvelle liste triée par score décroissant
			#haha :) , cet écriture de merde "[0][i][1]", [0] première liste de list_All_documents_selections
			#[i], on accède au i ème élément de la liste récupérée avec [0]
			#[1] enfin on récupère le nom du document
			finalListResult[0]= [ (score,list_All_documents_selections[0][i][1]) for i,score in enumerate(finalListResult[0])]
			finalListResult[0].sort(key=lambda tup: tup[0])
			#print finalListResult[0][::-1]
			return finalListResult[0][::-1]

		elif sortMethod=="max":
			finalListResult=[]
			for index,subList in enumerate(ListVectorScoresubListSynonimous):
				if index==0:
					finalListResult.append(np.array(subList))
				else:
					finalListResult[0]=np.maximum(finalListResult[0],np.array(subList))
			finalListResult[0]= [ (score,list_All_documents_selections[0][i][1]) for i,score in enumerate(finalListResult[0])]
			finalListResult[0].sort(key=lambda tup: tup[0])
			return finalListResult[0][::-1]

if __name__ == '__main__':
	listTermScoreMethod=[]
	listDocumentScoreMethod=[]
	per_Query_or_total=""
	reformulationType=""
	subReformulationType=""
	sortMethod=""
	if len(sys.argv) != 7:
		print "[Usage] python searchSemantic.py <TF|TF_IDF> <1|2|3|4> <perQuery|total> \
		<ref1(list syn)|ref2(combinaisons)|ref3(list syn avec poids) | ref4(list en utilisant la propriété) | ref4+ > \
		<ref1(list syn)|ref2(combinaisons)|ref3(list syn avec poids)> <sum|max>"
		sys.exit(1)
	else:

		if sys.argv[6]=="sum" or sys.argv[6]=="max":
			sortMethod=sys.argv[6]
		else:
			print ("6th paramater is wrong")
			sys.exit(1) 

		if sys.argv[5]=="ref1" or sys.argv[5]=="ref2" or sys.argv[5]=="ref3":
			subReformulationType=sys.argv[5]
		else:
			print ("5th paramater is wrong")
			sys.exit(1)

		if sys.argv[4]=="ref1" or sys.argv[4]=="ref2" or sys.argv[4]=="ref3" or sys.argv[4]=="ref4" or sys.argv[4]=="ref4+":
			reformulationType=sys.argv[4]
		else:
			print ("4th paramater is wrong")
			sys.exit(1)

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
	 [ "prix", "Omar Sy"], ["acteur", "a joué avec", "Omar Sy"],["prix", "enfant de Trappes"],["personne", "a joué avec", "Omar Sy"]]
	#["acteur", "joué avec", "Omar Sy"]
	#List_requests= [["personnes", "Intouchables"]]

	search_obj=search()
	start_time=time.clock()
	#print listTermScoreMethod
	#print listDocumentScoreMethod
	search_obj.evalTotal(List_requests,listTermScoreMethod,listDocumentScoreMethod,per_Query_or_total,sortMethod,reformulationType, subReformulationType)
	print ">>>>>>> Total process Time : ", time.clock() - start_time, "seconds"
