#!/usr/bin/env python
# -*-coding:utf-8 -*

import os
import json
from datetime import datetime

from tracker.utils import *
from tracker.capture import *
from tracker.worker import *

"""
	Ce script gère tout le programme.
	Il va charger la conf
	Il va initialiser la carte wifi.
	Ensuite il va lancer l'écoute.
	Enfin, il va régulièrement relancer l'écoute et envoyer les données sur l'api
"""

fileConfPath = "./tracker.json"

"""
	La configuration contient les éléments suivants:
	PATH: On assure que le PATH est complet
	PATH_SCRIPT: Dossier contenant tous les scripts
	URL_API: Url de l'api rest recevant les données
	IFACE: Interface d'écoute des paquets
	PATH_DUMP: Dossier de sauvegarde des dumps
	PATH_SESSION: Dossier contenant la session
	PATH_DUMP_CURRENT: Dossier de sauvegarde de l'écoute en cours
	PATH_DUMP_TMP: Dossier de sauvegarde de fichiers temporaires
	PATH_DUMP_WAITING: Dossier de sauvegarde de fichiers en attente d'être envoyé sur serveur
	FILE_CURRENT: Fichier de lecture courant
	SEPARATOR: Séparateur de champs
	FILE_USER_ID: Fichier contenant l'id de l'utilisateur
	FILE_USER_KEY: Fichier contenant la clé de l'utilisateur
"""

def main():
	# On charge la conf
	with open(fileConfPath, "r") as file:
		conf = json.load(file)
	
	# On intialise la carte wifi
	execSystem("ifconfig %s down" % (conf['IFACE']))
	execSystem("iwconfig %s essid any" % (conf['IFACE']))
	execSystem("iwconfig %s mode monitor" % (conf['IFACE']))
	execSystem("ifconfig %s up" % (conf['IFACE']))

	while(True):
		# On lance la capture
		with open(conf['FILE_CURRENT'], "w") as file:
			params = {
				"iface": conf['IFACE'],
				"file": file,
				"timeout": 60,
				"bpfFilter": "type mgt and (subtype probe-req or subtype assoc-req or subtype reassoc-req)"
			}
			capture = Capture(**params)
			print "Démarrage de la capture"
			capture.start()
			print "Fin de la capture"

		# On déplace le fichier
		tmpName = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
		os.rename(conf['FILE_CURRENT'], "%s/%s" % (conf['PATH_DUMP_TMP'], tmpName))

		# On lance le worker en forkant pour relancer instantément l'écoute
		pid = os.fork()
		if pid == 0:
			# Child
			params = {
				"pathFileCurrent": conf['FILE_CURRENT'],
				"pathFolderTmp": conf['PATH_DUMP_TMP'],
				"pathFolderWaiting": conf['PATH_DUMP_WAITING'],
		        "pathFileUserId": conf['FILE_USER_ID'],
		        "pathFileUserKey": conf['FILE_USER_KEY'],
		        "urlApi": conf['URL_API']
			}
			worker = Worker(**params)
			print "Démarrage du worker"
			worker.start()
			os._exit(0)

if __name__ == '__main__':
    main()
