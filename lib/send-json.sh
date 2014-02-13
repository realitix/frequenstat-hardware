#!/bin/bash

userId=`cat $PATH_SCRIPT/session/userId | tr -d ' '`
userKey=`cat $PATH_SCRIPT/session/userKey | tr -d ' '`

DATA_SEND="{\"datas\": {\"userId\": \"$userId\", \"userKey\": \"$userKey\""

# On parcourt tous les fichiers à envoyer
cd $PATH_SCRIPT/dump/waiting
LIST_JSON=`ls *.json`

for f in $LIST_JSON
do
	CONTENT_JSON=`cat $PATH_SCRIPT/dump/waiting/$f`
	DATA_SEND_LIST="$DATA_SEND, \"captures\": $CONTENT_JSON}}"
	HTTP_STATUS=`curl -X POST -d "$DATA_SEND_LIST" $URL_API --header "Content-Type:application/json" -m 240 -w "%{http_code}" -s -o /dev/null`
	
	# Si le status HTTP n'est pas égal à 200, il faut envoyer une alerte à l'api pour le signaler

	# Si le status est 000 (la connexion internet ne fonctionne pas)
	if [ $HTTP_STATUS -eq 0 ]
	then
		echo "Connection impossible"
	# 404 = Code JSON mal formaté
	elif [ $HTTP_STATUS -eq 404 ]
	then
        echo "JSON mal formate"
    # 403 = Accès interdit, les fichiers de sessions sont faux
	elif [ $HTTP_STATUS -eq 403 ]
	then
        echo "Mauvaise identification"
    # 400 = Clé manquante dans le JSON
    elif [ $HTTP_STATUS -eq 400 ]
	then
        echo "Cles manquantes"
	fi
	

	#rm $PATH_SCRIPT/dump/waiting/$f
done
