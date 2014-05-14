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
import datetime

logPath = "../logs/"

def main():
	if not os.path.isdir(logPath):
		print "Repertoire des logs inexistant"
		return
		
	d = os.getcwd()+'/'
	types = ['3','1','2']
	procs = dict()
	logs = dict()
	for t in types:
		logs[t] = open(logPath+t, 'w+')
		procs[t] = subprocess.Popen([d+'tracker.py', t], stdout=logs[t], stderr=subprocess.STDOUT)
	
	while 1:
		for t, proc in procs.iteritems():
			if proc.poll() is not None:
				logs[t].write('\n\n%s - Redemarrage du processus!\n\n' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
				procs[t] = subprocess.Popen([d+'tracker.py', t], stdout=logs[t], stderr=subprocess.STDOUT)
		time.sleep(10)
				

if __name__ == '__main__':
    main()
