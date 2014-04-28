# -*-coding:utf-8 -*

import os
from datetime import datetime
from scapy.all import *
from scapy_extension import scapy_ex

class Capture(object):
    """
     Classe gérant la capture des paquets par scapy
    """

    def __init__(self, iface=None, separator="||", file=None, timeout=3600, bpfFilter=None):
        if iface == None or file == None:
            raise ValueError("L'interface ou le fichier sont mal renseignés")

        self.iface = str(iface) # Corrige une erreur de type unicode
        self.separator = separator
        self.file = file
        self.timeout = timeout
        self.bpfFilter = bpfFilter

    def packetHandler(self, p):
    	stationMac = None
    	
        """
         - Management frame
           -> Association, reassociation, probe request
         - Data frame
           -> Ce qui contient toDs=1 et fromDs=0
           -> Ce qui contient toDs=0 et fromDs=0
        """
        if (
        	( p.type == 0 and p.subtype in [0, 2, 4] ) or
        	( p.type == 2 and p.hasflag('FCfield', 'to-DS') and not p.hasflag('FCfield', 'from-DS') ) or
        	( p.type == 2 and not p.hasflag('FCfield', 'to-DS') and not p.hasflag('FCfield', 'from-DS') )
        ):
        	stationMac = p.addr2
        
        if stationMac is not None:
	        dateNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	        power = str(p.dBm_AntSignal)
	        strFile = "%s%s%s%s%s\n" % (stationMac, self.separator, power, self.separator, dateNow)
	        self.file.write(strFile)
        	

    def start(self):
        sniff(
        	iface=self.iface, 
        	prn=self.packetHandler,
        	store=False,
        	timeout=self.timeout, 
        	filter=self.bpfFilter)
