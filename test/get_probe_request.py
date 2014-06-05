#!/usr/bin/env python

from scapy.all import *
import pprint


def packetHandler(p):
	#if p.haslayer(Dot11WEP):
	if p.type == 0 and p.subtype == 4:
		print "Paquet recu"


sniff(iface="alpha1", prn=packetHandler)