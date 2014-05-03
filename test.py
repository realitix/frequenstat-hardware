#!/usr/bin/env python

from scapy.all import *

import pprint

def packetHandler(p):
    pprint.pprint(p)
    print "\n\n"

sniff(iface="wlp0s20u2", prn=packetHandler)