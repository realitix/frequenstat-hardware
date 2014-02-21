#!/usr/bin/env python
# -*-coding:utf-8 -*

import os
import yaml
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

fileConfPath = "./config.yml"

def main():
	# On charge la conf
	with open(fileConfPath, "r") as file:
		conf = yaml.load(file)
		conf = conf['main']
	
	# On intialise la carte wifi
	execSystem("ifconfig %s down" % (conf['IFACE']))
	execSystem("iwconfig %s essid any" % (conf['IFACE']))
	execSystem("iwconfig %s key off" % (conf['IFACE']))
	execSystem("iwconfig %s mode monitor" % (conf['IFACE']))
	execSystem("ifconfig %s up" % (conf['IFACE']))

	while(True):
		# On lance la capture
		with open(conf['FILE_CURRENT'], "w") as file:
			params = {
				"iface": conf['IFACE'],
				"file": file,
				"timeout": conf['LISTEN_TIMEOUT'],
				"bpfFilter": conf['SCAPY_FILTER']
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
