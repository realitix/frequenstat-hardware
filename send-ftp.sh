#!/bin/bash
PATH="/sbin:/usr/sbin:$PATH"
PATH_SCRIPT=/home/realitix/Projets/WifiListener

# Doit être lancé par root

# On doit envoyer tous les fichiers json présent dans dump/waiting/
lftp ftp://test:test@ftp.bevi.fr -e "mirror -R $PATH_SCRIPT/dump/waiting/ / ; quit"

# On supprime les fichiers car ils viennent d'etre envoyé
rm $PATH_SCRIPT/dump/waiting/*.json
