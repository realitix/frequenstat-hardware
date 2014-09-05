#!/usr/bin/env python
# -*-coding:utf-8 -*

"""
	Hyperviseur gérant le bon déroulement du programme
	On lance dans l'ordre le channel hopping, le sniffer et le worker
	On test qu'ils tournent bien et si un s'arrete on le relance
"""

import subprocess
import signal
import sys
import time
import os
from datetime import datetime

procs = dict()

def handler(signum, frame):
	for t, proc in procs.iteritems():
		if proc.poll() is None:
			proc.send_signal(signal.SIGTERM)
	sys.exit("Fin de l'hypervision")


def main():
	signal.signal(signal.SIGTERM, handler)

	# CONFIGURATION
	logPath = "/home/realitix/git/tracker-hardware/logs/"
	appPath = "/home/realitix/git/tracker-hardware/app/tracker_v1/tracker.py"

	if not os.path.isdir(logPath):
		print "Repertoire des logs inexistant"
		return
		
	types = ['3','1','2']
	logs = dict()
	for t in types:
		logs[t] = open(logPath+t, 'a', 0)
		procs[t] = subprocess.Popen([appPath, t], stdout=logs[t], stderr=subprocess.STDOUT)
	
	while 1:
		for t, proc in procs.iteritems():
			if proc.poll() is not None:
				logs[t].write('\n\nRedemarrage du processus! [%s]\n\n' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
				procs[t] = subprocess.Popen([appPath, t], stdout=logs[t], stderr=subprocess.STDOUT)
		time.sleep(10)
				

if __name__ == '__main__':
	main()
