#!/bin/bash

# On charge les variables
source ./tracker.conf

ifconfig wlan0 down
iwconfig wlan0 essid any
iwconfig wlan0 mode monitor
ifconfig wlan0 up