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

	with open(boxVersionPath, "r") as file:
		version = file.read().strip()

	app = importlib.import_module('tracker_v%s.tracker-hypervisor' % version)
	app.main()

if __name__ == '__main__':
	main()
