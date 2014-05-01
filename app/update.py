#!/usr/bin/env python
# -*-coding:utf-8 -*

"""
	Permet de mettre à jour le code
"""

boxVersionPath = "../session/boxVersion"
appVersionPath = "../session/appVersion"

def main():
	with open(boxVersionPath, "r") as file:
		boxVersion = file.read().strip()
	with open(appVersionPath, "r") as file:
		appVersion = file.read().strip()


if __name__ == '__main__':
    main()
