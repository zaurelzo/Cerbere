#!/usr/bin/env python
# -*- coding: utf-8 -*-

class eval:

	def __init__(self):
		pass

	#renvoi le nombre total de document pertinenets d'un fichier requêtes 
	#OU
	#Renvoie le nombre de documenst sélectionnés par notre recherche
	def parseResIrit(self, chemin_fichier):
		file = open(chemin_fichier, "r+")
 
		res= []
		indice=0
		for line in file:
			list_values=line.split()
			number=list_values[1]
			res.append(int(number))
		return res

	def calculPoidsTotIrit(self, liste_poids_doc):

		res = 0
		for elt in list_poids_doc:
			res=res+elt
		return res

	def calculPoidsPertinentsSelectionnes(self, poids_tot_documents_pertinents, liste_doc_pertinents, liste_doc_selectionnes):
		res=0
		
		taille_listes_doc_selectionnes = len(liste_doc_selectionnes)
		liste_rappel_precision=[]
		nb_pertinents_selectionnes=0
		
		for indice in range(0, taille_listes)
			if liste_doc_pertinents[indice]==1 && liste_doc_selectionnes[indice]==1
				
				nb_pertinents_selectionnes=nb_pertinents_selectionnes+1
				
				rappel=nb_pertinents_selectionnes/poids_tot_documents_pertinents
				precision = nb_pertinents_selectionnes/(indice+1)
				
				liste_rappel_precision.append((rappel, precision))
		return liste_rappel_precision

#if __name__ == '__main__':
	#o1=eval()
	#res=eval.parseRes(o1,"/home/jordy/Bureau/RI/qrels/qrelQ1.txt")
	#res1=eval.calculPoidsTot(o1,res)
	#print res1