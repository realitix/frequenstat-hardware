# -*-coding:utf-8 -*

import os
import json
from datetime import datetime
from time import sleep
import requests

from tracker.utils import *

class Channel(object):
    """
     Classe gérant le channel hopping
    """
    def __init__(self, iface):
        self.channel = self.getChannel()
        self.iface = iface
    
    def update(self):
        self.channel = ((self.channel + 3) % 14) + 1
        self.setChannel(self.channel)
        
    def setChannel(self, channel):
        ex('iwconfig {0} channel {1}'.format(self.iface, channel))
        
    def getChannel(self):
        stdout = ex('iwgetid -c {0}'.format(self.iface))
		match = re.search('Channel:(\d+)', stdout)
		return int(match.group(1))
		
	def start(self):
	    while(True):
	        sleep(0.5) #500 ms
	        self.update()
	        
        