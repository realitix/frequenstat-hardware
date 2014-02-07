#!/bin/bash

# On stoppe l'ancien processus de capture
#pid_status=`ps -ef | grep airodump-ng | grep -v grep | awk '{print $2}' | xargs`
pkill -9 airodump-ng

# On déplace le fichier généré dans le dossier dump et on le renomme de maniere agreable
name_date=`date '+%Y_%m_%d_%H_%M'`
mv $PATH_SCRIPT/dump/current/dump* $PATH_SCRIPT/dump/$name_date.xml

# On le relance
$PATH_SCRIPT/start-capture.sh
