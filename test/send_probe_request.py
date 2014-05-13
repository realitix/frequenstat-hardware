#!/usr/bin/env python

from scapy.all import *
import pprint


p = RadioTap()/Dot11(type=0,subtype=4,addr1="ff:ff:ff:ff:ff:ff", addr2="00:11:22:33:44:55",addr3="ff:ff:ff:ff:ff:ff")
p /= Dot11Elt(ID=0,info="ff:ff:ff:ff:ff:ff")
p /= Dot11Elt(ID=1,info="\x82\x84\x8b\x96")
conf.iface="wlp1s0"
sendp(p)