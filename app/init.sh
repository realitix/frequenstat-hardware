#!/bin/bash

# On charge les variables
source ./tracker.conf

ifconfig $IFACE down
iwconfig $IFACE essid any
iwconfig $IFACE mode monitor
ifconfig $IFACE up

# On lance le script et on écrit la ou il faut
$PATH_SCRIPT/capture.py >> $FILE_CURRENT