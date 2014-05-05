# -*-coding:utf-8 -*

import os
import sys
from datetime import datetime
from scapy.all import *
import time
import scapy_ex
import sqlite3
import pcapy as pcap

# Permet d'utiliser libpcap https://stackoverflow.com/questions/18994242/why-isnt-scapy-capturing-vlan-tag-information
#TODO comparer les performance entre libpcacp et RawSocket!
# Seul libpcap permet d'utiliser les filtres
conf.use_pcap=True
import scapy.arch.pcapdnet 

class Capture(object):
    """
     Classe gérant la capture des paquets par scapy
    """

    def __init__(self, iface=None, db=None, dbTimeout=120, bpfFilter=None):
        if iface == None or db == None:
            raise ValueError("L'interface ou le fichier sont mal renseignés")

        self.iface = str(iface) # Corrige une erreur de type unicode
        self.bpfFilter = bpfFilter
        self.pkts = []
        self.nbPackets = 0
        self.nbMaxPackets = 10
        self.maxStoptime = 120
        self.dbTimeout = dbTimeout
        self.stoptime = time.time() + self.dbTimeout
        self.db = db
        self.createSchema()


    def createSchema(self):
        db = sqlite3.connect(self.db)
        c = db.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS captures (date TEXT, power INTEGER, mac text)''')
        db.commit()
        db.close()

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
        
        if (
            ( p.type == 0 and p.subtype in [0, 2, 4] ) or
            ( p.type == 2 and p.hasflag('FCfield', 'to-DS') and not p.hasflag('FCfield', 'from-DS') ) or
            ( p.type == 2 and not p.hasflag('FCfield', 'to-DS') and not p.hasflag('FCfield', 'from-DS') )
        ):
            stationMac = p.addr2
        """
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
        sniff(
            iface=self.iface, 
            prn=self.packetHandler,
            store=False, 
            filter=self.bpfFilter)
