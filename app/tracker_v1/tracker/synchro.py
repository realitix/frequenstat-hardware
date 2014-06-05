# -*-coding:utf-8 -*


import time
import ntplib

from utils import *

class Synchro(object):
    """
     Classe gérant le décalage des heures
    """

    def __init__(self):
        
        
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
			response = c.request('ntp.frequenstat.com')
			response = response.tx_time
        except ntplib.NTPException:
            response = None
            
        return reponse
		