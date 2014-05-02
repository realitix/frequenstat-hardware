#!/usr/bin/env python
# -*-coding:utf-8 -*

"""
	Permet de mettre à jour le code
	On commence par checker l'url vide pour le code
"""

import sys
import requests
import random
import tarfile

sessionPath = "../session/"
urlVersion = 'http://dev2.bevi.fr/api/getAppVersion/'
urlApp = 'http://dev2.bevi.fr/api/getApp/'

def main():
	with open("%s%s" % (sessionPath, 'boxVersion'), "r") as file:
		boxVersion = file.read().strip()
	with open("%s%s" % (sessionPath, 'appVersion'), "r") as file:
		appVersion = file.read().strip()
	
	r = requests.get('%s%s' % (urlVersion, boxVersion))
	if r.status_code != 200:
	    print('Code http != 200')
	    sys.exit(1)
	
	infos = r.json()
	if infos['appVersion'] <= appVersion:
	    sys.exit(0)
	
    r = requests.get('%s%s' % (urlApp, boxVersion), stream=True)
    if r.status_code != 200:
        print('Code http != 200')
	    sys.exit(2)
	
	tmpFile = '/tmp/%d' % random.randint(1,100000)
    with open(tmpFile, 'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)
	
	tar = tarfile.open(tmpfile, 'r:bz2')
	tmpFile2 = '/tmp/%d' % random.randint(1,100000)
	tar.extractall(tmpFile2)
	
	#TODO Stopper les services
	#TODO Ecraser le dossier de la version de la boxe
    

if __name__ == '__main__':
    main()
