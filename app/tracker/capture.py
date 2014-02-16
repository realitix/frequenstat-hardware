# -*-coding:utf-8 -*

import os
from datetime import datetime
from scapy.all import *
import scapy_ex

class Capture:
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
        stationMac = p.getlayer(Dot11).sta_bssid()
        dateNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        power = str(p.dBm_AntSignal)

        strFile = "%s%s%s%s%s\n" % (stationMac, self.separator, power, self.separator, dateNow)
        self.file.write(strFile)

    def start(self):
        sniff(iface=self.iface, prn=self.packetHandler, timeout=self.timeout, filter=self.bpfFilter)
