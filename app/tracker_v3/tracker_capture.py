# -*-coding:utf-8 -*

import os
import logging
import time
import yaml
from datetime import datetime

from tracker.utils import *
from tracker.capture import *

"""
	Ce script gère la capture.
	Il va charger la conf
	Il va initialiser la carte wifi.
	Ensuite il va lancer l'écoute.
	Enfin, il va régulièrement relancer l'écoute et envoyer les données sur l'api
"""

def main():
	# CONFIGURATION
	fileConfPath = "%s/config.yml" % (os.path.dirname(os.path.realpath(__file__)))

	# On charge la conf
	with open(fileConfPath, "r") as file:
		conf = yaml.load(file)
		conf = conf['main']
	
	# On surcharge avec la conf personnelle
	if os.path.exists(conf['PATH_CONFIG_PERSO']):
		with open(conf['PATH_CONFIG_PERSO'], "r") as file:
			conf2 = yaml.load(file)
			if conf2:
				conf2 = conf2.get('main')
				conf.update(conf2)
				
	# Configuration des logs
	createLogger('/tmp/tracker_capture.log', conf['LOG_LEVEL'])
	log = logging.getLogger()

	# Création du schema
	log.info('Création du schema de la base')
	createSchema(conf['PATH_DB'])
	
	# Attente avant le démarrage
	if conf['WAIT_CAPTURE']:
		time.sleep(int(conf['WAIT_CAPTURE']))
		
	# Temps réel on compresse les temps avant envoie
	if conf['REALTIME']:
 		conf['CAPTURE_BUFFER_TIME'] = 2
 		
	# On lance la capture
	params = {
		"iface": conf['IFACE'],
		"db": conf['PATH_DB'],
		"bpfFilter": conf['SCAPY_FILTER'],
		"dbTimeout": conf['CAPTURE_BUFFER_TIME'],
		"nbMaxPackets": conf['CAPTURE_BUFFER_PACKETS']
	}
	capture = Capture(**params)
	log.info("Démarrage de la capture")
	capture.start()
	log.info("Fin de la capture")