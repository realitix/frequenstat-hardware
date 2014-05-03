# -*-coding:utf-8 -*

import os
import yaml
from datetime import datetime

from tracker.utils import *
from tracker.capture import *
from tracker.worker import *
from tracker.channel import *

"""
	Ce script gère tout le programme.
	Il va charger la conf
	Il va initialiser la carte wifi.
	Ensuite il va lancer l'écoute.
	Enfin, il va régulièrement relancer l'écoute et envoyer les données sur l'api
"""

fileConfPath = "%s/config.yml" % (os.path.dirname(os.path.realpath(__file__)))

def main():
	# On charge la conf
	with open(fileConfPath, "r") as file:
		conf = yaml.load(file)
		conf = conf['main']
	
	# On surcharge avec la conf personnelle
	with open(conf['PATH_CONFIG_PERSO'], "r") as file:
		conf2 = yaml.load(file)
		if conf2:
			conf2 = conf2.get('main')
			conf.update(conf2)
	
	# On intialise la carte wifi
	initInterface(conf['IFACE'])

	while(True):
		# On lance la capture
		with open(conf['FILE_CURRENT'], "w") as file:
			params = {
				"iface": conf['IFACE'],
				"db": conf['PATH_DB'],
				"timeout": conf['LISTEN_TIMEOUT'],
				"bpfFilter": conf['SCAPY_FILTER']
			}
			capture = Capture(**params)
			print "Démarrage de la capture"
			capture.start()
			print "Fin de la capture"

		# On lance le worker en forkant pour relancer instantément l'écoute
		pid = os.fork()
		if pid == 0:
			# Child
			params = {
				"pathFileCurrent": conf['FILE_CURRENT'],
				"pathFolderTmp": conf['PATH_DUMP_TMP'],
				"pathFolderWaitingCompress": conf['PATH_DUMP_WAITING_COMPRESS'],
				"pathFolderWaitingSend": conf['PATH_DUMP_WAITING_SEND'],
				"pathFileUserId": conf['FILE_USER_ID'],
				"pathFileUserKey": conf['FILE_USER_KEY'],
				"pathFilePlaceId": conf['FILE_PLACE_ID'],
				"pathFileBoxId": conf['FILE_BOX_ID'],
				"urlApi": conf['URL_API'],
				"bd": conf['PATH_DB']
			}
			worker = Worker(**params)
			print "Démarrage du worker"
			worker.start()
			os._exit(0)