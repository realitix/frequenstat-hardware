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

Le serveur est doté d'une api permettant de recevoir les nouvelles captures.
On utilise curl pour se connecter au serveur et lui envoyer les données en JSON.
Une sécurité a été mise en place et nécessitant l'id de l'utilisateur et sa clé associé.
Sans ca, les données ne sont pas envoyées.
Le script récupère le code HTTP de retour et s'il s'agit d'une erreur, il le transmet à l'API pour signaler l'erreur
Le script peut ausi détecter l'abscence de connexion internet, dans ce cas, le script est stoppé et en attente du retour de la connexion

Le fichier send-json.sh gère cette partie.

4 - Processus d'exécution

Les logiciels suivants sont prérequis:
	aircrack-ng (contenant airodump-ng)
	lftp
	php5-cli
	curl

Afin que tout se passe bien, il va falloir crééer trois taches cron décaler de cinq minutes chacunes, 
un fichier main.sh a été créé pour simplifier l'appel:
	1: 'STEP=1 main.sh'
	2: 'STEP=2 main.sh'
	3: 'STEP=3 main.sh'

ATTENTION: Toutes ces taches doivent être exécuté en cron administrateur (root)

En fonction du rafrachissement désiré pour le client, ces taches cron peuvent être exécuté toutes les heures ou tous les jours.
Attention cependant, plus le temps est court, meilleur est la précision.
