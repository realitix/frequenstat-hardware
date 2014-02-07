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

	#rm $PATH_SCRIPT/dump/waiting/$f
done
