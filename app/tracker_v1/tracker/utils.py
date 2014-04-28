# -*-coding:utf-8 -*

import os
import hashlib
import bz2
from tempfile import SpooledTemporaryFile
from subprocess import check_call
from shutil import copyfileobj
from datetime import datetime
from operator import itemgetter, attrgetter

def ex(cmd):
	"""Shell out a subprocess and return what it writes to stdout as a string"""
	in_mem_file = SpooledTemporaryFile(max_size=2048, mode="r+")
	check_call(cmd, shell=True, stdout=in_mem_file)
	in_mem_file.seek(0)
	stdout = in_mem_file.read()
	in_mem_file.close()
	return stdout

def initInterface(iface):
    ex("ifconfig %s down" % (iface))
	ex("iwconfig %s essid any" % (iface))
	ex("iwconfig %s key off" % (iface))
	ex("iwconfig %s mode monitor" % (iface))
	ex("ifconfig %s up" % (iface))
	
"""
 Calcul le hash MD5 d'un fichier
"""
def calculateMd5(filePath):
    m = hashlib.md5()
    
    with open(filePath, 'rb') as fh:
        while data = fh.read(8192):
            m.update(data)
            
    return m.hexdigest()
    

"""
 Compresse un fichier en bz2
"""
def compressBz2(filePath):
    newFilePath = '%s.bz2' % (filePath)
    with open(filePath, 'rb') as input:
        with bz2.BZ2File(newFilePath, 'wb', compresslevel=9) as output:
            copyfileobj(input, output)
    os.remove(filePath)
    

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
def cleanCapturesList(tmpRequests, seconds=25):
	requests = []

	macs = [r['mac'] for r in tmpRequests]
	macs = list(set(macs)) # Uniq mac

	for m in macs:
	    macsTmp = []
	    for r in tmpRequests:
	        if r['mac'] == m:
	            macsTmp.append(r)
	            
	    # macsTmp contient toutes les requetes liées à une adresse mac
	    macsTmp.sort(key=lambda x: x['date'])
	    packets = []
	    packetsIter = -1
	    
	    i1 = 0
	    while i1 < len(macsTmp):
	    	date1 = datetime.strptime(macsTmp[i1]['date'], '%Y-%m-%d %H:%M:%S')
	    	nbShift = 1
	    	i2 = -1
	    	while i2 < len(macsTmp):
	    		if i2 == i1:
	    			packets.append([macsTmp[i1]])
	    			packetsIter += 1
	    			i2 += 1
	    			continue
	    		if i2 < i1:
	    			i2 += 1
	    			continue
	    		
	    		date2 = datetime.strptime(macsTmp[i2]['date'], '%Y-%m-%d %H:%M:%S')
	    		delta = date2 - date1
	    		
	    		if delta.total_seconds() <= seconds:
	    			packets[packetsIter].append(macsTmp[i2])
	    			nbShift += 1
	    		
	    		i2 += 1
	    
	    	i1 += nbShift
	    
	    # On a un tableau multidimensionnelle contenant les paquets regroupés par date similaire
	    # On sélectionne la plus haute intensité par paquet
	    for lot in packets:
	    	lot.sort(key=lambda x: x['power'], reverse=True)
	    	requests.append(lot[0])
	    	
	    return requests
	    	