# -*-coding:utf-8 -*


import time
import ntplib

from utils import *

class Synchro(object):
	"""
	 Classe gérant le décalage des heures
	"""
		
	def start(self):
		response = None
		while response is None:
			response = self.execute()
			if response is None:
				time.sleep(10)
		
		offset = int(response - time.time())
		
		# If offset less than 2 seconds, ok
		if abs(offset) <= 2:
			return 0
			
		# We reload ntp service to take the good time
		ex('/etc/init.d/ntp restart')
		
		# We return the offset
		return offset
			
	def execute(self):
		c = ntplib.NTPClient()
		try:
			print "Requete"
			response = c.request('ntp.frequenstat.com')
			response = response.tx_time
			print "Réponse: %s" % time.ctime(response)
		except ntplib.NTPException:
			print "Erreur de connexion"
			response = None
			
		return response
		