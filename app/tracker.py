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

def handler(signum, frame):
	sys.exit("Fin du script")

def main():
	signal.signal(signal.SIGTERM, handler)

	# CONFIGURATION
	boxVersionPath = "/home/realitix/git/tracker-hardware/session/boxVersion"

	argc = len(sys.argv)
	if argc == 1:
		print "1=Capture app, 2=Worker app, 3=Channel app"
		sys.exit(0)

	with open(boxVersionPath, "r") as file:
		version = file.read().strip()
	
	if int(sys.argv[1]) == 1:	
		app = importlib.import_module('tracker_v%s.tracker_capture' % version)
		app.main()
	elif int(sys.argv[1]) == 2:
		app = importlib.import_module('tracker_v%s.tracker_worker' % version)
		app.main()
	elif int(sys.argv[1]) == 3:
		app = importlib.import_module('tracker_v%s.tracker_channel' % version)
		app.main()
	else:
		print "Argument invalide"

if __name__ == '__main__':
	main()
