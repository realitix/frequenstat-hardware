Documentation

Nous nommerons cette partie du développement la couche basse.
Cela regroupe l'écoute wifi, la mise en forme du fichier de données et l'envoie sur le serveur.

1 - L'écoute wifi

L'écoute wifi est réalisé via le logiciel airodump-ng qui permet d'écouter les probes request.
Les probes request sont des données envoyées par les clients wifi afin de signaler leur présence.
Ces paquets contiennent sufisamment d'informations pour nous.
A ce niveau tout repose sur la carte wifi, elle doit être puissante et sensible, pleinement compatible avec linux.
Sur le site de aircrack-ng, des modèles sont recommandés.
Il faut une carte wifi qui supporte le mode monitoring.

2 scripts gèrent cette partie, start-capture.sh et start-new-capture.sh
	start-capture.sh va configurer la carte wifi puis lancer airodump-ng
	start-new-capture.sh va stopper la capture, déplacer le fichier puis relancer la capture (appelle start-capture).
	
2 - La mise en forme du fichier

Une fois l'écoute terminé, un fichier xml est généré par airodump-ng et contient trop d'information et mal présenté.
Pour simplifier, nous le parsons puis nous le reformatont en json, enfin on le déplace dans le dossier d'attente de transfert.
Le fichier xml-to-json.php gère cette partie.

3 - Envoie sur le serveur

Un serveur ftp doit être configuré en pré requis de ce script.
Ce script va aller lire tous les nouveaux fichier json et les envoyer sur le serveur ftp.
Le fichier send-ftp.sh gère cette partie.

4 - Processus d'exécution

Les logiciels suivants sont prérequis:
	aircrack-ng (contenant airodump-ng)
	lftp
	php5-cli

Afin que tout se passe bien, il va falloir crééer trois taches cron décaler de deux minutes chacunes:
	1: Appeler le fichier start-new-capture.sh
	2: Appeler le fichier xml-to-json.php
	3: Appeler le fichier send-ftp.sh

ATTENTION: Toutes ces taches doivent être exécuté en cron administrateur (root)

En fonction du rafrachissement désiré pour le client, ces taches cron peuvent être exécuté toutes les heures ou tous les jours.
Attention cependant, plus le temps est court, meilleur est la précision.

5 - Amélioration

Créer un seul fichier prenant en paramètre l'étape et contenant toutes les variables de configuration car ici, il y a quatres fichiers à configurer, c'est mauvais pour l'industrialisation de processus.

