#!/usr/bin/env python
# -*-coding:utf-8 -*

"""
	Permet de télécharger les éléments de session
"""

import requests
import sys
import os

def getSerial():
    cpuserial = None
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if 'Serial' in line:
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = None
    
    return cpuserial

def main():
	# CONFIGURATION
	url = 'http://dev2.bevi.fr/api/v1/session/'
	sessionPath = "/home/realitix/git/tracker-hardware/session"

	sn = getSerial();
	if not sn:
	    print "Impossible de lire le numero de serie"
	    sys.exit(1)
	
	url = "%s%s" % (url, sn)
	r = requests.get(url, verify=False)
	
	if r.status_code != 200:
	    print "Le serveur n'a pas repondu 200"
	    sys.exit(2)
	
	infos = r.json()
	
	if not os.path.isdir(sessionPath):
	    print "Le dossier de session n'existe pas"
	    sys.exit(3)
	
	# Par defaut, la version de l'application est à 1
	infos['appVersion'] = 1
	keys = ['boxId', 'boxVersion', 'placeId', 'userId', 'userKey']
	
	for v in keys:
	    with open("%s/%s" % (sessionPath, v), "w") as f:
		    f.write(infos[v])
		    print "%s a bien ete mis a jour"
	


if __name__ == '__main__':
    main()
