# -*-coding:utf-8 -*

import os
import sys
import logging
from datetime import datetime
from scapy.all import *
import time
import scapy_ex
import sqlite3

# Permet d'utiliser libpcap https://stackoverflow.com/questions/18994242/why-isnt-scapy-capturing-vlan-tag-information
#TODO comparer les performance entre libpcacp et RawSocket!
# Seul libpcap permet d'utiliser les filtres
#import pcapy as pcap
#conf.use_pcap=True
#import scapy.arch.pcapdnet 

class Capture(object):
    """
     Classe gérant la capture des paquets par scapy
    """

    def __init__(self, iface=None, db=None, dbTimeout=120, nbMaxPackets=100, bpfFilter=None):
        self.log = logging.getLogger()
        
        if iface == None or db == None:
            self.log.critical("L'interface ou le fichier sont mal renseignés")
            raise ValueError("L'interface ou le fichier sont mal renseignés")

        self.iface = str(iface) # Corrige une erreur de type unicode
        self.bpfFilter = bpfFilter
        self.pkts = []
        self.nbPackets = 0
        self.nbMaxPackets = nbMaxPackets
        self.dbTimeout = dbTimeout
        self.stoptime = time.time() + self.dbTimeout
        self.db = db

    def commit(self):
        db = sqlite3.connect(self.db)
        c = db.cursor()
        inserts = []
        for p in self.pkts:
            inserts.append((p['date'], p['power'], p['mac']))
        c.executemany('INSERT INTO captures VALUES (?,?,?)', inserts)
        db.commit()
        db.close()

        # Empty the list
        self.pkts = []

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
        	# Date en milliseconds
            dateNow = round(time.time()*1000)
            power = int(str(p.dBm_AntSignal))
            self.pkts.append({'date': dateNow, 'mac': stationMac, 'power': power })

            self.nbPackets = self.nbPackets + 1
            remain = self.stoptime - time.time() 

            if self.nbPackets > self.nbMaxPackets or remain <= 0:
                self.commit()
                self.stoptime = time.time() + self.dbTimeout
                self.nbPackets = 0
            

    def start(self):
        sniff(
            iface=self.iface, 
            prn=self.packetHandler,
            store=False, 
            filter=self.bpfFilter)
