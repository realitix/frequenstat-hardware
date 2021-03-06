# -*-coding:utf-8 -*

import os
import sys
import json
import logging
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
        pathFileUserKey=None, pathFilePlaceId=None, pathFileBoxId=None,
        urlApi=None, offset=0):
        
        self.log = logging.getLogger()
        
        if pathFolderWaitingCompress == None or \
           pathFolderWaitingSend == None or \
           pathFileUserId == None or \
           pathFileUserKey == None or \
           pathFilePlaceId == None or \
           pathFileBoxId == None or \
           db == None or \
           urlApi == None :
            self.log.critical("Les paramètres du worker sont mauvais")
            raise ValueError("Les paramètres du worker sont mauvais")

        self.pathFolderWaitingCompress = pathFolderWaitingCompress
        self.pathFolderWaitingSend = pathFolderWaitingSend
        self.urlApi = urlApi
        self.lastDate = None
        self.db = db
        self.hasDatas = None
        self.offset = offset

        with open(pathFileUserId, "r") as file:
            self.userId = int(file.read().strip())
        with open(pathFileUserKey, "r") as file:
            self.userKey = str(file.read().strip())
        with open(pathFilePlaceId, "r") as file:
            self.placeId = int(file.read().strip())
        with open(pathFileBoxId, "r") as file:
            self.boxId = int(file.read().strip())

    def format(self):
        """
         Cette fonction génère le fichier contenant les données
         La requete sql évite les doublons et sélectionne la plus grande puissance
        """
        sql = '''
            SELECT c.date, c.power, c.mac
            FROM
            captures c,
            (
                SELECT rowid, mac, date
                        FROM captures
                        GROUP BY mac, date
                    HAVING MAX(power)
            ) t
            WHERE t.rowid = c.rowid
            ORDER BY c.date ASC
            '''

        db = sqlite3.connect(self.db)
        c = db.cursor()
        requests = []
        self.hasDatas = False
        for r in c.execute(sql):
            self.hasDatas = True
            self.lastDate = r[0]
            
            # Convert date in millisecond into classic format
            dateClassic = datetime.fromtimestamp(round(r[0]/1000)).strftime('%Y-%m-%d %H:%M:%S')
            
            requests.append({"date": dateClassic, "power": r[1], "mac": r[2]})
        db.close()

        if self.hasDatas:
            fileName = '%d-%d-%d_%s' % (self.userId, self.placeId, self.boxId, datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
            fileDest = "%s/%s" % (self.pathFolderWaitingCompress, fileName)
            with open(fileDest, "w") as f:
                json.dump(requests, f)

    def cleanDb(self):
        """
         Cette fonction supprime toutes les captures inférieur à la date enregistré
         On efface pas toutes les captures dans le cas ou il y a eu une insertion depuis le format
        """
        sql = "DELETE FROM captures WHERE date <= "+str(self.lastDate)+";"
        db = sqlite3.connect(self.db)
        c = db.cursor()
        c.execute(sql)
        db.commit()
        db.close()
        
    def offsetDb(self):
        """
         Cette fonction décale toutes les dates de capture de offset secondes
         La date est exprimée en milliseconde
        """
        sql = "UPDATE captures SET date = date + "+self.offset*1000+";"
        db = sqlite3.connect(self.db)
        c = db.cursor()
        c.execute(sql)
        db.commit()
        db.close()
    
    def compress(self):
        """
         Cette fonction compresse le fichier en bz2 pour l'envoi
         Pour chaque fichier en attente:
          - On le compresse avec la commande système
          - On le déplace dans le dossier d'attente d'envoi
        """
        # On parcourt les fichiers à compresser
        for fileName in os.listdir(self.pathFolderWaitingCompress):
            if 'gitignore' in fileName:
                continue
            # On compresse
            compressBz2('%s/%s' % (self.pathFolderWaitingCompress, fileName))
            
            # On déplace
            fileName = '%s.bz2' % (fileName)
            fileSrc  = '%s/%s' % (self.pathFolderWaitingCompress, fileName)
            fileDest = '%s/%s' % (self.pathFolderWaitingSend, fileName)
            os.rename(fileSrc, fileDest)
            
        # Le fichier est bien créé, on vide la bdd
        if self.hasDatas:
            self.cleanDb()
            
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
        self.log.info("Envoie des fichiers")
        # On parcourt les fichiers a envoyer
        for fileName in os.listdir(self.pathFolderWaitingSend):
            if 'gitignore' in fileName:
                continue
            fileSrc = "%s/%s" % (self.pathFolderWaitingSend, fileName)
            status = 0
            md5 = calculateMd5(fileSrc);
            count = 3
            returnContent = 0

            self.log.info("Envoie de %s" % fileSrc)
            
            while count > 0:
                count = count - 1
                self.log.info("Essaie a %s" % self.urlApi)
                with open(fileSrc, "rb") as file:
                    files = {'file': file}
                    datas = {
                        'userId': self.userId, 
                        'userKey': self.userKey,
                        'placeId': self.placeId,
                        'boxId': self.boxId,
                        'md5': md5
                    }
    
                    try:
                        r = requests.post(self.urlApi, data=datas, files=files, verify=False)
                        status = r.status_code
                        if status == 200 :
                            returnContent = int(r.content)
                            count = 0
                    except requests.exceptions.ConnectionError:
                        status = 0

            # On supprime le fichier lu
            if status == 200 and returnContent == 1:
                os.remove(fileSrc)
                self.log.info("Le fichier %s a été supprimé" % fileSrc)

            """ 
             * 000 = la connexion internet ne fonctionne pas
             * 404 = Code JSON mal formate
             * 403 = Acces interdit, les fichiers de sessions sont faux
             * 400 = Cle manquante dans le JSON
             * 500 = Erreur du serveur
            """
            if status == 200 and returnContent == 1:
                self.log.info("Le fichier a bien été transféré")
            elif status == 200 and returnContent == -1:
                self.log.info("Nom du fichier non conforme")
            elif status == 200 and returnContent == -2:
                self.log.info("Hash MD5 invalide")
            elif status == 200 and returnContent == -3:
                self.log.info("Erreur de décompression")
            elif status == 0:
                self.log.info("Connection impossible")
            elif status == 404:
                self.log.info("JSON mal formate")
            elif status == 403:
                self.log.info("Mauvaise identification")
            elif status == 400:
                self.log.info("Cles manquantes")
            elif status == 500:
                self.log.info("Erreur du serveur")
            else:
                self.log.info("Status inconnu: %d" % status)
        
    def start(self):
        if self.offset != 0:
            self.offsetDb()
            
        self.format()
        self.compress()
        self.send()
