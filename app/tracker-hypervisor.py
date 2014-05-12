#!/usr/bin/env python
# -*-coding:utf-8 -*

"""
	Hyperviseur gérant le bon déroulement du programme
	On lance dans l'ordre le channel hopping, le sniffer et le worker
	On test qu'ils tournent bien et si un s'arrete on le relance
"""

import subprocess
import time
import os

def main():
	d = os.getcwd()+'/'
	
	types = ['3','1','2']
	procs = dict()
	for t in types:
		procs[t] = subprocess.Popen([d+'tracker.py', t])
	
	while 1:
		for t, proc in procs.iteritems():
			if proc.poll() is not None:
				procs[t] = subprocess.Popen([d+'tracker.py', t])
		time.sleep(10)
				

if __name__ == '__main__':
    main()
