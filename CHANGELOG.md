# Changelog

Les versions intermédiaires non publiées ne sont listées que lorsqu’elles correspondent à un checkpoint vérifié ou à un ensemble fonctionnel identifiable.

## Unreleased — `develop`

- ajout d’un arrière-plan fixe configurable pour chaque entrée de sous-menu ;
- correction de l’écran noir lors de l’utilisation d’un chemin `/storage`, `special://` ou `image://` : le fond du sous-menu est maintenant rendu comme une texture directe au lieu de passer par le moteur de slideshow global ;
- exclusion du menu d’alimentation, des widgets et du mode `playlistBackground` ;
- réécriture du README pour présenter le fork Therand90 ;
- ajout d’une documentation fonctionnelle des personnalisations ;
- mise à jour de l’URL source de l’extension vers le dépôt du fork.

## 3.19.11+25widgets.10

- changement dynamique de la police et du gras pour chaque section d’accueil ;
- utilisation des véritables variantes grasses de Roboto, Condensed et Noto ;
- conservation des correctifs d’arrière-plan personnalisé, Cinéma, YouTube et replay ;
- checkpoint fonctionnel archivé sous le tag `25widgets.10-working`.

## Fondation du fork 25 widgets

- synchronisation avec Arctic: Zephyr (martian) 3.19.10 pour Kodi 21 Omega ;
- extension de SkinShortcuts jusqu’à 25 widgets ;
- navigation premier/dernier widget fiabilisée ;
- fanart et métadonnées TMDbHelper étendus aux slots supplémentaires ;
- replis d’images adaptés aux contenus de replay ;
- intégration facultative du service de métadonnées Therand.
