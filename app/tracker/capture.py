# -*-coding:utf-8 -*

import os
from datetime import datetime
from scapy.all import *
from scapy_extension import scapy_ex
from scapy_extension import ieee80211

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
        """
         Management frame
         Association, reassociation, probe request
        """
        if p.type == 0 and p.subtype in [0, 2, 4]:
            stationMac = p.addr2
            dateNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            power = str(p.dBm_AntSignal)

            strFile = "%s%s%s%s%s\n" % (stationMac, self.separator, power, self.separator, dateNow)
            self.file.write(strFile)

        """
         Controle frame
         Association, reassociation, probe request
        """
        if p.type == 1 and p.subtype in []:

    def start(self):
        sniff(iface=self.iface, prn=self.packetHandler, timeout=self.timeout, filter=self.bpfFilter)
