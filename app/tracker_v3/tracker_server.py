# -*-coding:utf-8 -*

import os
import logging
import time
import yaml
from datetime import datetime

from tracker.utils import *
from tracker.server import *

"""
	Ce script gère le serveur http.
	Il va charger la conf.
	Ensuite il va lancer l'écoute.
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
	createLogger('/tmp/tracker_server.log', conf['LOG_LEVEL'])
	log = logging.getLogger()

	
	# Attente avant le démarrage
	if conf['WAIT_SERVER']:
		time.sleep(int(conf['WAIT_SERVER']))

	# On lance le server
	params = {
		"port": conf['SERVER_PORT'],
		"pathFolderWaitingSend": conf['PATH_DUMP_WAITING_SEND']
	}
	server = Server(**params)
	log.info("Démarrage du serveur")
	server.start()
	log.info("Fin du serveur")