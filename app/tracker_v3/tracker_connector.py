# -*-coding:utf-8 -*

import os
import logging
import yaml
from datetime import datetime

from tracker.utils import *
from tracker.connector import *

"""
	Ce script gère la connexion au réseau
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
	createLogger('/tmp/tracker_connector.log', conf['LOG_LEVEL'])
	log = logging.getLogger()

	if conf['WAIT_CONNECTOR']:
		time.sleep(int(conf['WAIT_CONNECTOR']))
	
	# On créer le processus effectuant la connexion
	params = {
		"iface": conf['CONNECTOR_IFACE'],
		"channel": conf['CONNECTOR_CHANNEL'],
		"pathFileUserId": conf['FILE_USER_ID'],
		"pathFileUserKey": conf['FILE_USER_KEY'],
		"pathFilePlaceId": conf['FILE_PLACE_ID']
	}
	connector = Connector(**params)
	log.info("Démarrage du connecteur")
	connector.start()