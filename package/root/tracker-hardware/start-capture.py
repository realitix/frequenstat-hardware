#!/usr/bin/env python

from scapy.all import *

def PacketHandler(pkt) :
    if pkt.haslayer(Dot11) :
        if pkt.type == 0 and pkt.subtype == 4 :
            print "%s" % pkt.addr2

sniff(iface="wlan0", prn = PacketHandler)