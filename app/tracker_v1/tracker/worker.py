# -*-coding:utf-8 -*

import os
import sys
import json
import sqlite3
from datetime import datetime
import requests

from utils import *

class Worker(object):
    """
     Classe gérant le déplacement, le formating et l'envoie des données
    """

    def __init__(self, db=None, pathFolderWaitingCompress=None, 
        pathFolderWaitingSend=None, pathFileUserId=None, 
        pathFileUserKey=None, pathFilePlaceId=None, pathFileBoxId=None, urlApi=None):
        
        if pathFolderWaitingCompress == None or \
           pathFolderWaitingSend == None or \
           pathFileUserId == None or \
           pathFileUserKey == None or \
           pathFilePlaceId == None or \
           pathFileBoxId == None or \
           db == None or \
           urlApi == None :
            raise ValueError("Les dossiers ou fichiers sont mals renseignés")

        self.pathFolderWaitingCompress = pathFolderWaitingCompress
        self.pathFolderWaitingSend = pathFolderWaitingSend
        self.urlApi = urlApi

        if not os.path.exists(db):
            print "DB inexistante"
            sys.exit(0)

        self.db = sqlite3.connect(db)

        with open(pathFileUserId, "r") as file:
            self.userId = file.read().strip()
        with open(pathFileUserKey, "r") as file:
            self.userKey = file.read().strip()
        with open(pathFilePlaceId, "r") as file:
            self.placeId = file.read().strip()
        with open(pathFileBoxId, "r") as file:
            self.boxId = file.read().strip()

    def format(self):
        """
         Cette fonction génère le fichier contenant les données
        """
        c = self.db.cursor()
        requests = []
        for r in c.execute('SELECT date, power, mac FROM captures ORDER BY date'):
            requests.append({"date": r[0], "power": r[1], "mac": r[2]})
        self.db.close()

        # On filtre les éléments en trop
        requests = cleanCapturesList(requests)

        fileName = '%d-%d-%d_%s' % (self.userId, self.placeId, self.boxId, fileName)
        fileDest = "%s/%s" % (self.pathFolderWaitingCompress, fileName)
        with open(fileDest, "w") as f:
            json.dump(requests, f)
    
    def compress(self):
        """
         Cette fonction compresse le fichier en bz2 pour l'envoi
         Pour chaque fichier en attente:
          - On le compresse avec la commande système
          - On le déplace dans le dossier d'attente d'envoi
        """
        # On parcourt les fichiers à compresser
        for fileName in os.listdir(self.pathFolderWaitingCompress):
            # On compresse
            compressBz2('%s/%s' % (self.pathFolderWaitingCompress, fileName))
            
            # On déplace
            fileName = '%s.bz2' % (fileName)
            fileSrc  = '%s/%s' % (self.pathFolderWaitingCompress, fileName)
            fileDest = '%s/%s' % (self.pathFolderWaitingSend, fileName)
            os.rename(fileSrc, fileDest)
            
    def send(self):
        """
         Cette fonction envoie les données et supprime les fichiers
         Pour chaque fichier en attente:
          - On l'envoie au serveur avec les identifiants (en http)
            et le hash md5 du fichier
          - Le serveur nous renvoie 1 si c'est bon, 0 sinon
            - Si c'est 1, on supprime le fichier (car c'est bon)
            - Sinon on le renvoie au serveur
        """
        # On parcourt les fichiers a envoyer
        for fileName in os.listdir(self.pathFolderWaitingSend):
            fileSrc = "%s/%s" % (self.pathFolderWaitingSend, fileName)
            status = 0
            md5 = calculateMd5(fileSrc);
            count = 3
            returnContent = 0
            
            while count > 0 or returnContent != 1:
                count = count - 1
                
                with open(fileSrc, "rb") as file:
                    files = {'file': file}
                    datas = {
                        'datas': {
                            'userId': self.userId, 
                            'userKey': self.userKey,
                            'placeId': self.placeId,
                            'boxId': boxId
                        }
                    }
    
                    try:
                        r = requests.post(self.urlApi, data=json.dumps(datas), files=files)
                        status = r.status_code
                        if status == 200 :
                            returnContent = int(r.content)
                    except requests.exceptions.ConnectionError:
                        status = 0

            # On supprime le fichier lu
            if status == 200 and returnContent == 1:
                os.remove(fileSrc)

            """ 
             * 000 = la connexion internet ne fonctionne pas
             * 404 = Code JSON mal formate
             * 403 = Acces interdit, les fichiers de sessions sont faux
             * 400 = Cle manquante dans le JSON
             * 500 = Erreur du serveur
            """
            if status == 0:
                print "Connection impossible"
            elif status == 404:
                print "JSON mal formate"
            elif status == 403:
                print "Mauvaise identification"
            elif status == 400:
                print "Cles manquantes"
            elif status == 500:
                print "Erreur du serveur"

    def start(self):
        self.format()
        self.compress()
        self.send()