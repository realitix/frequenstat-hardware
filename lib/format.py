#!/usr/bin/env python
import os
import json

# ------------
# Ce script va lire tous les fichiers présent dans le dossier temporaire et les formaté
# Ensuite, il vales déplacer dans le dossier en attente d'envoie
# ------------

pathTmpFolder = os.environ.get('PATH_DUMP_TMP')
pathWaitingFolder = os.environ.get('PATH_DUMP_WAITING')
separator = os.environ.get('SEPARATOR')

# On parcourt les fichiers
for fileName in os.listdir(pathTmpFolder):
    requests = []
    fileSrc = "%s/%s" % (pathTmpFolder, fileName)
    
    # On parcourt le fichier et on enregistre les éléments dans le tableau requests
    with open(fileSrc, "r") as file:
        for oneLine in file:
            if oneLine.strip():
                elems = oneLine.strip().split(separator)
                request = {"mac": elems[0], "date": elems[1], "power": elems[2]}
                requests.append(request)
    
    # On écrase le fichier avec le json
    json.dump(requests, filePath)
    
    # On le déplace dans le dossier d'attente
    fileDest = "%s/%s" % (pathWaitingFolder, fileName)
    os.rename(fileSrc, fileDest)
