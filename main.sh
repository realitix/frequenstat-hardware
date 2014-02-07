#!/bin/bash

# ------------
# Ce script doit toujours etre executé par root
# ------------

# STEP=1 Lance le scan wifi
# STEP=2 Lance la conversion xml to json
# STEP=3 Lance l'envoie vers le serveur
if [ -z $STEP ]
then
        echo "Vous devez fournir un paramètre STEP avant la commande."
        exit
fi

# On assure que le PATH est complet
export PATH="/sbin:/usr/sbin:$PATH"

# Dossier contenant tous les scripts
export PATH_SCRIPT=/home/realitix/git/tracker-hardware


# On appele le bon script en fonction du STEP
if [ $STEP -eq 1 ]
then
        $PATH_SCRIPT/start-new-capture.sh
elif [ $STEP -eq 2 ]
then
        $PATH_SCRIPT/xml-to-json.sh
elif [ $STEP -eq 3 ]
then
        $PATH_SCRIPT/send-ftp.sh
else
        echo "STEP invalide, il doit etre compris entre 1 et 3"
fi