# -*-coding:utf-8 -*

import os
import json
import logging
import re
import requests

from datetime import datetime
from time import sleep
from utils import *

class Connector(object):
	"""
	 Classe gérant la connexion
	"""
	def __init__(self, iface=None, channel=None, pathFileUserId=None, pathFileUserKey=None, pathFilePlaceId=None):
		self.log = logging.getLogger()
		
		if iface == None or \
		   channel == None or \
           pathFileUserId == None or \
           pathFileUserKey == None or \
           pathFilePlaceId == None :
			self.log.critical("Paramètres manquants")
			raise ValueError("Paramètres manquants")
		
		self.iface = iface
		self.channel = channel
		
		with open(pathFileUserId, "r") as file:
            self.userId = int(file.read().strip())
        with open(pathFileUserKey, "r") as file:
            self.userKey = str(file.read().strip())
        with open(pathFilePlaceId, "r") as file:
            self.placeId = int(file.read().strip())
            
        self.essid = None
        self.password = None
		
	def initIdentification(self):
	    self.essid = 'frequenstat-%d-%d' % (self.userId, self.placeId)
	    self.password = 'frequenstat-%d-%d-%s' % (self.userId, self.placeId, self.userKey)
	
	def initWifi(self):
	    ex('iwconfig %s channel %d' % (self.iface, channel))
	    ex('iwconfig %s essid %s' % (self.iface, self.essid))
	    ex('iwconfig %s mode Managed' % (self.iface))
	    ex('iwconfig %s key s:%s' % (self.iface, self.password))
	    ex('iwconfig %s commit' % (self.iface))
		
	def start(self):
	    self.initIdentification()
	    self.initWifi()
		while(True):
			sleep(3600)
			
		