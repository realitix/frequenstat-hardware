#!/bin/bash

# ------------
# Ce script va lire tous les fichiers présent dans dump et les envoyer à php pour traitement
# ------------

cd $PATH_SCRIPT/dump
LIST_XML=`ls *.xml`

for f in $LIST_XML
do
   $PATH_SCRIPT/xml-to-json.php $PATH_SCRIPT/dump/$f
done