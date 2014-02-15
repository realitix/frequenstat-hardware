#!/usr/bin/env python

import os
from datetime import datetime
from scapy.all import *
import scapy_ex


iface = os.environ.get('IFACE')
separator = os.environ.get('SEPARATOR')

interface = iface if iface else exit("Aucune interface dans la variable d'environnement IFACE")
subtypes = (0, 2, 4)

def PacketHandler(p):
    # Initialisation des variables
    stationMac = None
    dateNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    power = None
    
	if p.haslayer(Dot11):
		if p.type == 0 and p.subtype in subtypes:
			stationMac = p.getlayer(Dot11).sta_bssid()
			power = str(p.dBm_AntSignal)
	
	# Si l'adresse mac existe, on affiche
	if stationMac != None:
	    print "%s%s%s%s%s" % (stationMac, separator, power, separator, dateNow)
	

sniff(iface=interface, prn=PacketHandler)