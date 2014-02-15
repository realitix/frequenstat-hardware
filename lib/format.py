#!/usr/bin/env python
import os
import json

# ------------
# Ce script va lire tous les fichiers present dans le dossier temporaire et les formate
# Ensuite, il va le deplacer dans le dossier en attente d'envoie
# ------------

pathTmpFolder = os.environ.get('PATH_DUMP_TMP')
pathWaitingFolder = os.environ.get('PATH_DUMP_WAITING')
separator = os.environ.get('SEPARATOR')

# On parcourt les fichiers
for fileName in os.listdir(pathTmpFolder):
    requests = []
    fileSrc = "%s/%s" % (pathTmpFolder, fileName)
    
    # On parcourt le fichier et on enregistre les elements dans le tableau requests
    with open(fileSrc, "r") as file:
        for oneLine in file:
            if oneLine.strip():
                elems = oneLine.strip().split(separator)
                request = {"mac": elems[0], "power": elems[1], "date": elems[2]}
                requests.append(request)
    
    # On ecrase le fichier avec le json
    with open(fileSrc, "w") as file:
        json.dump(requests, file)
    
    # On le deplace dans le dossier d'attente
    fileDest = "%s/%s" % (pathWaitingFolder, fileName)
    os.rename(fileSrc, fileDest)
