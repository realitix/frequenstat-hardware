#!/usr/bin/env python
import os
import json
import requests
import pprint
# ------------
# Ce script va lire tous les fichiers present dans le dossier waiting et les envoye au serveur
# Chaque fichier envoye est supprime
# ------------

pathFileUserId = os.environ.get('FILE_USER_ID')
pathFileUserKey = os.environ.get('FILE_USER_KEY')
pathWaitingFolder = os.environ.get('PATH_DUMP_WAITING')
urlApi = os.environ.get('URL_API')

userId = 0
userKey = 0

with open(pathFileUserId, "r") as file:
    userId = file.read().strip()
with open(pathFileUserKey, "r") as file:
    userKey = file.read().strip()

# On parcourt les fichiers a envoyer
for fileName in os.listdir(pathWaitingFolder):
    fileSrc = "%s/%s" % (pathWaitingFolder, fileName)
    opened = False
    status = 0

    with open(fileSrc, "r") as file:
        opened = True
        datas = {'datas': {'userId': userId, 'userKey': userKey, 'captures': json.load(file)}}
        r = requests.post(urlApi, data=json.dumps(datas))
        status = r.status_code
        pprint.pprint(status)

    # On supprime le fichier lu
    if opened == True and status == 200:
        os.remove(fileSrc)

    """ 
     * 000 = la connexion internet ne fonctionne pas
     * 404 = Code JSON mal formaté
     * 403 = Accès interdit, les fichiers de sessions sont faux
     * 400 = Clé manquante dans le JSON
     * 500 = Erreur du serveur
    """
    if status == 0:
        echo "Connection impossible"
    elif status == 404:
        echo "JSON mal formate"
    elif status == 403:
        echo "Mauvaise identification"
    elif status == 400:
        echo "Cles manquantes"