#!/bin/bash

# On charge les variables
source ./tracker.conf
NOW=`date '+%Y_%m_%d_%H_%M'`

# On déplace le fichier courant dans le répertoire temporaire
mv $FILE_CURRENT $PATH_DUMP_TMP/$NOW.tmp

# On reformatte en JSON tous les fichiers temporaires
$PATH_SCRIPT/format.py

# On envoie au serveur
$PATH_SCRIPT/send.py