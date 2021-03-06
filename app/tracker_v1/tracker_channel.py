# -*-coding:utf-8 -*

import os
import logging
import yaml
from datetime import datetime

from tracker.utils import *
from tracker.channel import *

"""
	Ce script gère le channel hopping
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
	createLogger('/tmp/tracker_channel.log', conf['LOG_LEVEL'])
	log = logging.getLogger()

	if conf['WAIT_CHANNEL']:
		time.sleep(int(conf['WAIT_CHANNEL']))
	
	# On intialise la carte wifi
	initInterface(conf['IFACE'])
	
	# On créer le processus effectuant le channel hopping
	params = {
		"iface": conf['IFACE'],
		"channel": conf['CHANNEL']
	}
	channel = Channel(**params)
	log.info("Démarrage du channel hopping")
	channel.start()