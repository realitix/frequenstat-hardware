# -*-coding:utf-8 -*

import os
import sys
from datetime import datetime
from scapy.all import *
import time
import scapy_ex
import sqlite3
import pcapy as pcap

conf.use_pcap=True

class Capture(object):
    """
     Classe gérant la capture des paquets par scapy
    """

    def __init__(self, iface=None, db=None, dbTimeout=120, timeout=3600, bpfFilter=None):
        if iface == None or db == None:
            raise ValueError("L'interface ou le fichier sont mal renseignés")

        self.iface = str(iface) # Corrige une erreur de type unicode
        self.timeout = timeout
        self.bpfFilter = bpfFilter
        self.pkts = []
        self.nbPackets = 0
        self.nbMaxPackets = 200
        self.maxStoptime = 120
        self.dbTimeout = dbTimeout
        self.stoptime = time.time() + self.dbTimeout

        if not os.path.exists(db):
            self.db = sqlite3.connect(db)
            self.createSchema()
        else
            self.db = sqlite3.connect(db)

    def createSchema():
        c = self.db.cursor()
        c.execute('''CREATE TABLE captures (date TEXT, power INTEGER, mac text)''')
        self.db.commit()
        self.db.close()

    def commit():
        c = self.db.cursor()
        for p in self.pkts:
            c.execute("INSERT INTO captures VALUES ('%s', %d, '%s')" % (p['date'], p['power'], p['mac']))

        self.db.commit()
        self.db.close()

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
	        power = int(str(p.dBm_AntSignal))
            self.pkts.append({'date': dateNow, 'mac': stationMac, 'power': power })

            self.nbPackets = self.nbPackets + 1
            remain = self.stoptime - time.time()

            if self.nbPackets > self.nbMaxPackets or remain <= 0:
                self.commit()
                self.stoptime = time.time() + self.dbTimeout
                self.nbPackets = 0
        	

    def start(self):
        self.bpfFilter = None
        sniff(
        	iface=self.iface, 
        	prn=self.packetHandler,
        	store=False,
        	timeout=self.timeout, 
        	filter=self.bpfFilter)
