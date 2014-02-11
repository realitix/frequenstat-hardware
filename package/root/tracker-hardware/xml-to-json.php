#!/usr/bin/php

<?php
	// En paramètre, on lui envoie le fichier à modifier
	$filePath = $argv[1];
	// En sortie, on aura un tableau qu'on transformera en JSON
	$result = array();

	$dom = new DOMDocument();
	$dom->load($filePath);

	$clients = $dom->getElementsByTagName('wireless-client');

	foreach( $clients as $c ) {
		$tmp = array();

		$dateBeggin = new DateTime($c->attributes->item(2)->nodeValue);
		$dateEnd    = new DateTime($c->attributes->item(3)->nodeValue);
		$tmp['dateBeggin'] = $dateBeggin->format(DATE_ATOM);
		$tmp['dateEnd']    = $dateEnd->format(DATE_ATOM);

		foreach( $c->childNodes as $node ) {
			switch ($node->nodeName) {
				case 'client-mac':
					$tmp['mac'] = $node->nodeValue;
					break;
				case 'client-manuf':
					$tmp['company'] = $node->nodeValue;
			}
		}

		$result[] = $tmp;
	}

	$infos = pathinfo($filePath);
	$newFile = $infos['dirname'].'/waiting/'.$infos['filename'].'.json';



	file_put_contents($newFile, json_encode($result));

	// On met le fichier xml dans un dossier history
	rename($filePath, $infos['dirname'].'/history/'.$infos['basename']);
?>