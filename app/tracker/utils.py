# -*-coding:utf-8 -*

import os
from datetime import datetime

def execSystem(cmd):
	pipe = os.popen(cmd)

	# On bloque le script jusqu'à la fin de la commande
	pipe.read()

"""
 On fabrique une nouvelle liste supprimant les doublons ( - de trente seconde entre 2 requetes)
 Algo:
 - On créé une liste contenant toutes les adresses mac uniques
 - Pour chaque adresses mac
 --- En reparcourant la liste, on créé une liste de tous les elems de l'adresse mac
 --- On trie la liste par date
 --- Pour chaque élement
 ------ On créer une nouvelle liste contenant tous les éléments suivant le filtre
 ------ On saute la quantité qu'on a ajoué à la liste précédente
 ------ Pour chaque paquet, on prend l'éléments ayant le signal le plus fort et on ajoute à la liste finale
"""
def cleanCapturesList(tmpRequest):
	requests = []

	macs = [r['mac'] for r in tmpRequests]
	macs = list(set(macs)) # Uniq mac

	# Fonction de comparaison utilisé par sort()
	def comp(v1, v2):
		v1 = datetime(v1)
		v2 = datetime(v2)
	    if v1[1]<v2[1]:
	        return -1
	    elif v1[1]>v2[1]:
	        return 1
	    else:
	        return 0

	for m in macs:
	    macsTmp = []
	    for r in tmpRequests:
	        if r['mac'] == m:
	            macsTmp.append(r)