#!/usr/bin/env python
# -*-coding:utf-8 -*

"""
	Point d'entrée permettant d'utiliser la bonne version du logiciel
"""

import importlib
import sys

boxVersionPath = "../session/boxVersion"

def main():
	argc = len(sys.argv)
	if argc == 1:
		print "1=Main app, 2=Channel hopping"
		sys.exit(0)

	with open(boxVersionPath, "r") as file:
		version = file.read().strip()
	
	if int(sys.argv[1]) == 1:	
		app = importlib.import_module('tracker_v%s.main' % version)
		app.main()
	elif int(sys.argv[1]) == 2:
		app = importlib.import_module('tracker_v%s.channel_hopping' % version)
		app.main()
	else:
		print "Argument invalide"

if __name__ == '__main__':
    main()
