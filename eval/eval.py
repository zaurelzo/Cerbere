#!/usr/bin/env python
# -*- coding: utf-8 -*-

class eval:

	def __init__(self):
		pass

	#renvoi le nombre total de document pertinenets d'un fichier requêtes 
	#OU
	#Renvoie le nombre de documenst sélectionnés par notre recherche
	def readFileQrels(self, chemin_fichier):
		file = open(chemin_fichier, "r+")
 
		res= []
		indice=0
		for line in file:
			list_values=line.split()
			number=list_values[1]
			res.append((int(number),list_values[0]))
		return res

	def calculTotalPertinents(self, liste_poids_doc):
		res = 0
		cpt=0;
		for elt in liste_poids_doc:
			if cpt!=126:
				res=res+elt[0]
			cpt=cpt+1
		return res

	def findindexInList(self,tuple_elt, liste_doc_pertinents ):
		for ind,elt  in enumerate(liste_doc_pertinents):
			if (elt[1]==tuple_elt[1]):
				return liste_doc_pertinents[ind]


	def calculRappelAndPrecision(self,liste_doc_pertinents, liste_doc_selectionnes):
		
		list_Qrels_sort=[]

		#on crée la nouvelle liste à partir des docs selectionnés
		for (freq,nameDoc) in liste_doc_selectionnes:
			elt = self.findindexInList((freq,nameDoc),liste_doc_pertinents)
			list_Qrels_sort.append(elt)

		
		taille_listes_doc_selectionnes = len ([elt for elt in liste_doc_selectionnes if elt[0]>0])
		liste_rappel_precision=[(-1,-1) for elt in range (len(liste_doc_pertinents))]
		nb_pertinents_selectionnes=0

		poids_tot_documents_pertinents= self.calculTotalPertinents(liste_doc_pertinents)
		rappel=0.0
		precision=0.0
		#print "range list doc select ", len(liste_doc_selectionnes)
		for indice in range(len(liste_doc_selectionnes)):
			#print "indice : ", indice, "nom du doc ", liste_doc_selectionnes[indice][1]
			if list_Qrels_sort[indice][0]==1 and liste_doc_selectionnes[indice][0]>0:
				
				nb_pertinents_selectionnes=nb_pertinents_selectionnes+1
				
				rappel=float(nb_pertinents_selectionnes)/float(poids_tot_documents_pertinents)
				precision = float(nb_pertinents_selectionnes)/float(indice+1)
			else:	
				precision = float(nb_pertinents_selectionnes)/float(indice+1)
			
			liste_rappel_precision[indice]=(rappel, precision)			
			

		return liste_rappel_precision

if __name__ == '__main__':
	o1=eval()
	#print o1.readFileQrels("../RessourcesProjet/qrels/qrelQ4.txt")
	#res1=eval.calculPoidsTot(o1,res)
	#print res1