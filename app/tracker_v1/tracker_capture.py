# -*-coding:utf-8 -*

import os
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

fileConfPath = "%s/config.yml" % (os.path.dirname(os.path.realpath(__file__)))

def main():
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
	
	# On intialise la carte wifi
	initInterface(conf['IFACE'])

	# On lance la capture
	params = {
		"iface": conf['IFACE'],
		"db": conf['PATH_DB'],
		"bpfFilter": conf['SCAPY_FILTER']
	}
	capture = Capture(**params)
	print "Démarrage de la capture"
	capture.start()
	print "Fin de la capture"