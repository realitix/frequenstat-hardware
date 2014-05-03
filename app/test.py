#!/usr/bin/env python

from scapy.all import *

"""
import pcappy as pcap
conf.use_pcap=True
import scapy.arch.pcapdnet 
"""
import pprint


def packetHandler(p):
	#if p.haslayer(Dot11WEP):
	if p.type == 2 and p.subtype == 0:
		pprint.pprint(p)
		print "\n\n"


sniff(iface="mon0", prn=packetHandler)