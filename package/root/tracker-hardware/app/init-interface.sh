#!/bin/bash

service network-manager stop
service avahi-daemon stop
ifconfig wlan0 down

iwconfig wlan0 essid any
iwconfig wlan0 mode monitor

ifconfig wlan0 up