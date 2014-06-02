Documentation

Nous nommerons cette partie du développement la couche basse.
Cela regroupe l'écoute wifi, la mise en forme du fichier de données et l'envoie sur le serveur.

1 - L'écoute wifi

L'écoute wifi est réalisé en ptyhon à l'aide de la librairie scapy.
Nous écoutons les probes request.
Les probes request sont des données envoyées par les clients wifi afin de signaler leur présence.
Ces paquets contiennent sufisamment d'informations pour nous.
A ce niveau tout repose sur la carte wifi, elle doit être puissante et sensible, pleinement compatible avec linux.
Il faut une carte wifi qui supporte le mode monitoring.

Scapy a été étendu pour supporter les data frame non nativement prises en charge. A tester.
	
2 - La mise en forme du fichier

Une fois l'écoute terminé, un fichier est généré.
Pour simplifier, nous le parsons puis nous le reformatont en json, enfin on le déplace dans le dossier d'attente de transfert.

3 - Envoie sur le serveur

Le serveur est doté d'une api permettant de recevoir les nouvelles captures.
On se connecte au serveur et lui envoie les données en JSON.
Une sécurité a été mise en place et nécessitant l'id de l'utilisateur et sa clé associé.
Sans ca, les données ne sont pas envoyées.
Le script récupère le code HTTP de retour et s'il s'agit d'une erreur, il le transmet à l'API pour signaler l'erreur
Le script peut ausi détecter l'abscence de connexion internet, dans ce cas, le script est stoppé et en attente du retour de la connexion

4 - Prérequis

Les logiciels suivants sont prérequis:
	python
	python-scapy
	python-numpy
	libpcap
	tcpdump
	python-pytz

Il suffit simplement de lancer le fichier main.py en administrateur pour laisser le programme s'éxécuter.


-----------------------------
Informations Générales sur le wifi ou comment capturer toutes les adresses mac des clients
-----------------------------
Il existe trois types de frame wifi: Control, Management et Data
Voir : https://supportforums.cisco.com/docs/DOC-13664

Chaque frame contient une ou plusieurs adresses mac.
Il faut donc trouver celle appartenant à la station.
Pour cela, il existe un flag FromDs et ToDs (voir http://www.commentcamarche.net/contents/1282-les-modes-de-fonctionnement-du-wifi-802-11-ou-wi-fi)
Si toDs=1, alors c'est la station qui envoie la requête.

Les control frame et management frame n'ont pas cette indication, toDs et fromDs seront égal à 0.
C'est seulement pour les datas frame.

Pour les datas frame, il suffit de sélectionner celle contenant toDs=1.
Poues les autres, il faut les connaitres.

De plus, pour les data frame, si ToDs=0 et fromDs=0, c'est une requête adhoc, les deux adresses mac sont deux stations différentes. 
A capturer ?

Les adresses macs contenues dans les controls fields dépendent des paquets précédemment envoyés. 
Nous ne faisons pas d'analyse de paquets, nous ne pourrons donc pas utiliser les controls frames.

Pour conclure,
Nous allons capturer les management frame de type Probe, Asoociation, Reassociation
Nous allons capturer les datas frame avec toDs=1 

