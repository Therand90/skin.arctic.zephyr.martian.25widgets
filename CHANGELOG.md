# Changelog

Les versions intermédiaires non publiées ne sont listées que lorsqu’elles correspondent à un checkpoint vérifié ou à un ensemble fonctionnel identifiable.

## Unreleased — `develop`

- personnalisation du titre de chaque entrée de sous-menu : taille, couleur, police et gras.

## 3.19.11+25widgets.12

- ajout d’un arrière-plan fixe configurable pour chaque entrée de sous-menu ;
- correction de l’écran noir avec les chemins `/storage`, `special://`, URL ou `image://` grâce à un rendu direct de la texture ;
- exclusion du menu d’alimentation, de l’éditeur de widgets et du mode `playlistBackground` ;
- réécriture du README pour présenter le fork Therand90 ;
- ajout d’une documentation fonctionnelle des personnalisations ;
- mise à jour de l’URL source de l’extension vers le dépôt du fork ;
- checkpoint testé sur Kodi / LibreELEC avant fusion dans `master`.

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
