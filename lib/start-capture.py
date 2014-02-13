#!/usr/bin/env python

from scapy.all import *
import scapy_ex
import pprint

# Define the interface name that we will be sniffing from, you can
# change this if needed.
interface = "wlan0"


# The PacketHandler() function is called each time Scapy receives a packet
# (we'll tell Scapy to use this function below with the sniff() function).
# The packet that was sniffed is passed as the function argument, "p".
def PacketHandler(p):

	# Define our tuple (an immutable list) of the 3 management frame
	# subtypes sent exclusively by clients. I got this list from Wireshark.
	stamgmtstypes = (0, 2, 4)

	# Make sure the packet has the Scapy Dot11 layer present
	if p.haslayer(Dot11):

		# Check to make sure this is a management frame (type=0) and that
		# the subtype is one of our management frame subtypes indicating a
		# a wireless client
		if p.type == 0 and p.subtype in stamgmtstypes:
			print p.addr2

			while Dot11Elt in p:
				print "Inside"
				p = p[Dot11Elt]
				if p.ID==1:
					print "SSID: %s" % p.info
				if p.ID==221:
					print "Vendor: %s" % p.info
				p = p.payload

# With the sniffmgmt() function complete, we can invoke the Scapy sniff()
# function, pointing to the monitor mode interface, and telling Scapy to call
# the sniffmgmt() function for each packet received. Easy!
sniff(iface=interface, prn=PacketHandler)