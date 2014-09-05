# Readme
Ce fichier va expliquer les concepts et informations sur la partie hardware

# Types d'utilisation

Il existe deux types d'utilisation, l'utilisation classique et l'utilisation 3d

## Utilisation classique
L'utilisation classique représente un magasin qui souscris à un forfait basique contenant un seul boitier.
Dans ce cas, on utilise tracker_v1

## Utilisation 3d
L'utilisation 3d, quant à elle nécessite deux types de boitier:

- Un boitier maître (tracker_v2)
- Des boitiers esclaves (tracker_v3)

### Comment ça marche ?

#### Démarrage
- Le maître créé un réseau portant le nom "frequenstat-{userId}-{placeId}" et comme mot de passe "frequenstat-{userId}-{placeId}-{userKey}".
- L'esclave essaie de se connecter au réseau ci dessus, une fois connecté, il met à jour son horloge interne.

#### Initialisation
- L'esclave lance son serveur http interne
- Le maître compte le nombre de stations connectées et attend qu'elles le soient toutes ("iwlist wlan0 peers" ou "iw dev wlan0 station dump").
- Une fois qu'elles le sont toutes, il leurs envoie un signal pour vérifier que le serveur http répond bien.

#### En cours
- Le maître va chercher régulièrement les captures sur les esclaves et les envoies au serveur


# Architecture

L'architecture est la même pour toutes les versions.

Le fichier tracker.py principal appelle en fonction de la version le tracker-hypervisor de la version.
Quant à lui, le tracker-hypervisor va appeler le tracker avec le bon argument pour lancer le fork.