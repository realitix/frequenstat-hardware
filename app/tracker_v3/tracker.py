#!/usr/bin/env python
# -*-coding:utf-8 -*

"""
	Point d'entrée permettant d'utiliser la bonne version du logiciel
"""

import importlib
import sys
import pytz
import signal
from datetime import datetime

import tracker_server
import tracker_capture
import tracker_worker
import tracker_channel
import tracker_connector

def handler(signum, frame):
	sys.exit("Fin du script")

def main():
	signal.signal(signal.SIGTERM, handler)

	argc = len(sys.argv)
	if argc == 1:
		print "1=Capture app, 2=Worker app, 3=Channel app, 4=Serveur HTTP, 5=Connecteur"
		sys.exit(0)
	
	if int(sys.argv[1]) == 1:	
		app = tracker_capture
	elif int(sys.argv[1]) == 2:
		app = tracker_worker
	elif int(sys.argv[1]) == 3:
		app = tracker_channel
	elif int(sys.argv[1]) == 4:	
		app = tracker_server
	elif int(sys.argv[1]) == 5:	
		app = tracker_connector
	else:
		print "Argument invalide"
		
	app.main()

if __name__ == '__main__':
	main()
