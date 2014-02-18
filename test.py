#!/usr/bin/env python

from scapy.all import *
import tracker.scapy_extension.ieee80211

import pprint

def packetHandler(p):
    pprint.pprint(p)
    print "\n\n"

sniff(iface="wlan0", prn=packetHandler)