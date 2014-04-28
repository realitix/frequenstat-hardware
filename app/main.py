#!/usr/bin/env python
# -*-coding:utf-8 -*

"""
	Point d'entrée permettant d'utiliser la bonne version du logiciel
"""

versionPath = "../session/version"

def main():
	with open(versionPath, "r") as file:
		version = file.read().strip()
	
	app = __import__('tracker_v%s' % version)
	app.main()

if __name__ == '__main__':
    main()
