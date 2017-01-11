#!/usr/bin/env python
# -*- coding: utf-8 -*-


class eval:

	def __init__(self):
		pass

	#Renvoi la liste des documents pertinents pour un fichier txt d'une requête
	def readFileQrels(self, chemin_fichier):
		file = open(chemin_fichier, "r+")
 
		res= []
		indice=0
		#On récupère chaque ligne des fichiers txt
		for line in file:
			#On parse chaque ligne suivan le caractère espace
			list_values=line.split()
			number=list_values[1]
			res.append((int(number),list_values[0]))
		return res
		#On renvoi le tableau à 2 colonnes : poids|nom document 

	#calcule le nombre total de documents pertinents dans la liste renvoyée par la fonction précédente
	def calculTotalPertinents(self, liste_poids_doc):
		res = 0
		for elt in liste_poids_doc:
			res=res+elt[0]
		return res

	#Permet de retrouver dans la liste des documents pertinents un couple. On va rechercher dans la liste des documents pertinents un tuple
	#ayant pour second élément le même que celui de tuple_elt (ce second élément est le nom du fichier).
	#On renvoi ce tuple issu de la liste des documents pertinent si on l'a trouvé.
	def findindexInList(self,tuple_elt, liste_doc_pertinents ):
		for ind,elt  in enumerate(liste_doc_pertinents):
			if (elt[1]==tuple_elt[1]):
				return liste_doc_pertinents[ind]


	def calculRappelAndPrecision(self,liste_doc_pertinents, liste_doc_selectionnes):
		
		list_Qrels_sort=[]

		#on crée la nouvelle liste à partir des docs selectionnés, on trier la liste des documents pertinents selon 
		#le même ordre que celui de la liste des documents sélectionnés
		for (freq,nameDoc) in liste_doc_selectionnes:
			elt = self.findindexInList((freq,nameDoc),liste_doc_pertinents)
			list_Qrels_sort.append(elt)

		#On récupère le nombre d'éléments sélectionnées ayant une fréquence supérieure à 0
		taille_listes_doc_selectionnes = len ([elt for elt in liste_doc_selectionnes if elt[0]>0])
		
		#On ininitialise la liste des tuples (rappel, précision) avec des tuples (-1,-1)
		#et on limite sa taille à celle de la liste des documents pertinents
		liste_rappel_precision=[(-1,-1) for elt in range (len(liste_doc_pertinents))]
		
		#Variable du nombre total de documents sélecionnés et pertinents, utile pour calculer la précision et le rappel
		nb_pertinents_selectionnes=0

		#On calcule le nombre total de documents pertinents
		poids_tot_documents_pertinents= self.calculTotalPertinents(liste_doc_pertinents)

		rappel=0.0
		precision=0.0
		#print "---------------------"
		for indice in range(len(liste_doc_selectionnes)):
			#On parcourt l'ensemble de la liste des documents electionnés et la liste des documents pertinents
			#Si un fichier est sélectionné (freq>0) et pertinent (poids=1) alors on calcule son rappel et sa précision
			#On ajoute ensuite le tuple (rappel, précision) de ce document dans la liste liste_rappel_precision qui sera retournée
			
			#if indice<5:
			#	print list_Qrels_sort[indice]
			if list_Qrels_sort[indice][0]==1:
			 #and liste_doc_selectionnes[indice][0]>0:
				
				nb_pertinents_selectionnes=nb_pertinents_selectionnes+1
				
			rappel=float(nb_pertinents_selectionnes)/float(poids_tot_documents_pertinents)

			#indice est utilisé comme nombre total de documents sélectionnés
			precision = float(nb_pertinents_selectionnes)/float(indice+1)
			
			liste_rappel_precision[indice]=(rappel, precision)			
			
			#print "nb_pertinents_selectionnes "+str(nb_pertinents_selectionnes)

		return liste_rappel_precision

if __name__ == '__main__':
	o1=eval()
	#print o1.readFileQrels("../RessourcesProjet/qrels/qrelQ4.txt")
	#res1=eval.calculPoidsTot(o1,res)
	#print res1

