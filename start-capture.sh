#!/bin/bash
PATH="/sbin:/usr/sbin:$PATH"
PATH_SCRIPT=/home/realitix/Projets/WifiListener


# Doit être lancé par root

# On configure l'interface wifi
service network-manager stop
service avahi-daemon stop
ifconfig wlan0 down

iwconfig wlan0 essid any
iwconfig wlan0 mode monitor

airodump-ng --write=$PATH_SCRIPT/dump/current/dump --output-format=netxml --berlin 30 wlan0 > /dev/null 2>&1
