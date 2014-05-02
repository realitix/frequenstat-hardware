#!/usr/bin/env python
# -*-coding:utf-8 -*

"""
	Permet de télécharger les éléments de session
"""

import requests
import sys
import os

url = 'http://dev2.bevi.fr/api/getSession/'
sessionPath = "../session"

def getSerial():
    cpuserial = None
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
                f.close()
    except:
        cpuserial = None
    
    return cpuserial

def main():
	sn = getSerial();
	if not sn:
	    print "Impossible de lire le numero de serie"
	    sys.exit(1)
	
	url = "%s%s" % (url, sn)
	r = requests.get(url)
	
	if r.status_code != 200:
	    print "Le serveur n'a pas repondu 200"
	    sys.exit(2)
	
	infos = r.json()
	
	if not os.path.isdir(sessionPath):
	    print "Le dossier de session n'existe pas"
	    sys.exit(3)
	    
	keys = ['boxId', 'boxVersion', 'placeId', 'userId', 'userKey']
	
	for v in keys:
	    with open("%s/%s" % (sessionPath, v), "w") as f:
		    f.write(infos[v])
		    print "%s a bien ete mis a jour"
	


if __name__ == '__main__':
    main()