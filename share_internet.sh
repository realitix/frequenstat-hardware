#!/bin/bash

ip=`arp -a | grep -oE '((1?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\.){2}(42\.)(1?[0-9][0-9]?|2[0-4][0-9]|25[0-5])'`
route add default gw $ip usb0
service ntp restart