#!/usr/bin/env python
# -*-coding:utf-8 -*

"""
	Point d'entrée permettant d'utiliser la bonne version du logiciel
"""

import importlib
import sys
from datetime import datetime

# On supprime le buffer stdout
class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data.replace("\n"," [%s]\n"% str(datetime.now())))
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)
sys.stdout = Unbuffered(sys.stdout)

def main():
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
