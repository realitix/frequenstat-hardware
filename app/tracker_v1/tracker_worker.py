# -*-coding:utf-8 -*

import os
import yaml
from datetime import datetime
import time
import random

from tracker.utils import *
from tracker.worker import *

"""
	Ce script gère le worker.
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

	while(True):
		params = {
			"pathFolderWaitingCompress": conf['PATH_DUMP_WAITING_COMPRESS'],
			"pathFolderWaitingSend": conf['PATH_DUMP_WAITING_SEND'],
			"pathFileUserId": conf['FILE_USER_ID'],
			"pathFileUserKey": conf['FILE_USER_KEY'],
			"pathFilePlaceId": conf['FILE_PLACE_ID'],
			"pathFileBoxId": conf['FILE_BOX_ID'],
			"urlApi": conf['URL_API'],
			"db": conf['PATH_DB']
		}
		worker = Worker(**params)
		print "Démarrage du worker"
		worker.start()

		# On attend le prochain envoie
		time.sleep(random.randint(conf['WORKER_MIN_TIME'], conf['WORKER_MAX_TIME']))