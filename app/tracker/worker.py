# -*-coding:utf-8 -*

import os
import json
from datetime import datetime
import requests

from tracker.utils import *

class Worker:
    """
     Classe gérant le déplacement, le formating et l'envoie des données
    """

    def __init__(self, pathFileCurrent=None, pathFolderTmp=None, pathFolderWaiting=None, separator="||", 
        pathFileUserId=None, pathFileUserKey=None, pathFilePlaceId=None, urlApi=None):
        
        if pathFileCurrent == None or \
           pathFolderTmp == None or \
           pathFolderWaiting == None or \
           pathFileUserId == None or \
           pathFileUserKey == None or \
           pathFilePlaceId == None or \
           urlApi == None :
            raise ValueError("Les dossiers ou fichiers sont mals renseignés")

        self.pathFileCurrent = pathFileCurrent
        self.pathFolderTmp = pathFolderTmp
        self.pathFolderWaiting = pathFolderWaiting
        self.separator = separator
        self.tmpName = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        self.urlApi = urlApi

        with open(pathFileUserId, "r") as file:
            self.userId = file.read().strip()
        with open(pathFileUserKey, "r") as file:
            self.userKey = file.read().strip()
        with open(pathFilePlaceId, "r") as file:
            self.placeId = file.read().strip()

    def format(self):
        """
         Cette fonction parcourt les fichiers temporaires, les reformate et les déplace
        """
        for fileName in os.listdir(self.pathFolderTmp):
            fileSrc = "%s/%s" % (self.pathFolderTmp, fileName)
            
            # On parcourt le fichier et on enregistre les elements dans le tableau requests
            tmpRequests = []
            with open(fileSrc, "r") as file:
                for oneLine in file:
                    if oneLine.strip():
                        elems = oneLine.strip().split(self.separator)
                        request = {"mac": elems[0], "power": int(elems[1]), "date": elems[2]}
                        tmpRequests.append(request)
                requests.append(val)
                
            # On filtre les éléments en trop
            requests = cleanCapturesList(requests)
        
            # On ecrase le fichier avec le json
            with open(fileSrc, "w") as file:
                json.dump(requests, file)
            
            # On le deplace dans le dossier d'attente
            fileDest = "%s/%s" % (self.pathFolderWaiting, fileName)
            os.rename(fileSrc, fileDest)

    def send(self):
        """
         Cette fonction envoie les données et supprime les fichiers
        """
        # On parcourt les fichiers a envoyer
        for fileName in os.listdir(self.pathFolderWaiting):
            fileSrc = "%s/%s" % (self.pathFolderWaiting, fileName)
            opened = False
            status = 0

            with open(fileSrc, "r") as file:
                opened = True
                datas = {
                    'datas': {
                        'userId': self.userId, 
                        'userKey': self.userKey,
                        'placeId': self.placeId,
                        'captures': json.load(file)
                    }
                }

                try:
                    r = requests.post(self.urlApi, data=json.dumps(datas))
                    status = r.status_code
                except requests.exceptions.ConnectionError:
                    status = 0

            # On supprime le fichier lu
            if opened == True and status == 200:
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

    def start(self):
        self.format()
        self.send()