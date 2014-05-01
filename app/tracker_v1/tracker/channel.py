# -*-coding:utf-8 -*

import os
import json
import re
import requests

from datetime import datetime
from time import sleep
from utils import *

class Channel(object):
	"""
	 Classe gérant le channel hopping
	"""
	def __init__(self, iface):
		self.iface = iface
		self.channel = self.getChannel()
	
	def update(self):
		self.channel = ((self.channel + 3) % 14) + 1
		self.setChannel(self.channel)
		
	def setChannel(self, channel):
		ex('iwconfig %s channel %d' % (self.iface, channel))
		
	def getChannel(self):
		stdout = ex('iwgetid -c %s' % self.iface)
		match = re.search('Channel:(\d+)', stdout)
		return int(match.group(1))
		
	def start(self):
		while(True):
			sleep(0.5) #500 ms
			self.update()
			
		