# Personnalisations du fork Therand90

Ce document inventorie les écarts fonctionnels principaux entre ce fork et Arctic: Zephyr (martian) 3.19.10. Il décrit le comportement voulu plutôt qu’un simple diff de fichiers.

## Base et compatibilité

- Base graphique : Arctic: Zephyr (martian) 3.19.10.
- Cible principale : Kodi 21 Omega, notamment LibreELEC 12.x.
- Identifiant séparé : `skin.arctic.zephyr.martian.25widgets` afin de ne pas écraser le skin d’origine.
- Version stable actuelle : `3.19.11+25widgets.45`.

## Accueil et widgets

### 25 widgets

Le système SkinShortcuts a été étendu au-delà des slots d’origine pour prendre en charge les widgets 1 à 25 : activation, source, tri, format, ratio, défilement automatique, navigation, informations et fanart.

### Navigation classique

- calcul dynamique du premier et du dernier widget configuré ;
- suppression des anciens replis codés en dur sur un numéro de widget ;
- entrée cohérente depuis le menu principal vers les widgets ;
- bouclage interne plus fiable sans perte involontaire du focus vers la tuile de section ;
- conservation du dernier conteneur actif quand les listes sont reconstruites.

### Navigation inline Jacktook — stable `.45`

Les widgets Jacktook peuvent désormais naviguer dans leurs dossiers **sans quitter Home** :

- pagination `Next (N)` sur plusieurs pages ;
- série → saisons → épisodes ;
- historique par widget pour `Backspace` / `Esc` ;
- retour au widget racine au dernier niveau ;
- focus réclamé pendant le refresh puis forcé sur le premier élément du nouveau dossier ;
- éléments jouables renvoyés automatiquement au clic natif Kodi/Jacktook ;
- verrou `NavBusy` pour absorber les doubles clics pendant la transition ;
- spinner non modal rendu dans `Home.xml` afin de ne jamais bloquer la mise à jour du `DirectoryProvider`.

Le routage est injecté dans le template générique du mode **Moderne Multi-Widgets Netflix**. Les IDs originaux des widgets restent inchangés; chaque widget reçoit un conteneur inline distinct afin d’éviter les collisions d’ID. La navigation inline est actuellement activée uniquement pour `plugin.video.jacktook`; les autres fournisseurs repassent immédiatement vers leur clic natif.

L’implémentation technique détaillée se trouve dans [`INLINE_NAVIGATION.md`](INLINE_NAVIGATION.md).

### Titres par section et sous-menu

Chaque entrée du menu principal et chaque entrée de sous-menu peut définir :

- la taille du titre ;
- sa couleur ;
- sa famille de police ;
- l’utilisation réelle d’une variante grasse.

Les polices Roboto, Condensed, Mono et Noto utilisent les ressources adaptées au choix effectué.

## Arrière-plans

### Sections principales

- priorité donnée à l’arrière-plan explicitement choisi pour une section ;
- restauration de l’arrière-plan d’accueil personnalisé ;
- comportement spécifique pour les sections Cinéma et YouTube ;
- image YouTube fixe incluse comme repli lorsqu’aucun fond personnalisé n’existe.

### Sous-menus

Le bouton **Arrière-plan** est également proposé lors de l’édition d’une entrée de sous-menu, sauf pour le menu d’alimentation et l’éditeur de widgets. Quand le sous-menu possède le focus, son image fixe remplace temporairement le fond de la section parente. La valeur spéciale `playlistBackground` reste exclue pour préserver son fonctionnement dynamique.

Le chemin choisi est rendu directement par un contrôle `image`, comme pour les arrière-plans explicites du menu principal. Il ne passe pas par la variable globale utilisée pour les dossiers de slideshow. Cela évite qu’une image unique provenant d’un chemin `/storage`, `special://`, URL ou `image://` soit interprétée comme un dossier et produise un écran noir.

### Replay et fanart

- détection des faux fanarts provenant de Catch-up TV & More ;
- rejet des fanarts identiques à la vignette ou à l’image paysage ;
- repli sur `landscape`, `thumb` ou `poster` lorsque le vrai fanart manque ;
- rendu compact en haut à droite avec fondu progressif vers le fond ;
- traitement séparé des vignettes paysage et portrait/carrées ;
- prise en charge des chemins Kodi encapsulés sous la forme `image://`.

## PVR / télévision

### Cartes Groupes TV

Un widget `pvr://channels/tv/` reçoit un rendu compact spécifique. Les groupes peuvent utiliser une illustration facultative située dans :

```text
/storage/pictures/tvgroups/<libellé exact>.png
/storage/pictures/tvgroups/<libellé exact>.jpg
```

L’image personnalisée est utilisée dans la carte et devient l’arrière-plan plein écran lorsque le groupe est focus. Sans image personnalisée, le skin n’utilise plus le fallback `$VAR[PosterImage]` responsable des mosaïques/logos de chaînes : la carte reste en verre sombre avec son libellé.

Le background normal de la section **Chaînes** reste disponible derrière le widget lorsqu’aucune carte personnalisée n’est focus.

### Image du programme PVR

Dans la liste des chaînes :

1. fanart TMDb HD en priorité lorsqu’il existe ;
2. sinon, vignette `EpgEventIcon` agrandie et atténuée en arrière-plan ;
3. la même vignette originale est superposée nette et centrée avec `aspectratio=keep` ;
4. l’icône de chaîne reste le dernier fallback lorsqu’aucune image de programme n’est disponible.

Cette stratégie évite à la fois le crop excessif des petites images EPG et les bandes vides autour des visuels verticaux.

## Métadonnées de replay

Le skin sait lire les propriétés écrites par `service.therand.replaymetadata` pour chaque conteneur de widget :

- résumé enrichi isolé par widget ;
- repli immédiat sur les métadonnées Kodi quand le service est absent ;
- protection contre l’affichage du résumé appartenant à l’élément précédent ;
- masquage des descriptions strictement identiques au titre ou au libellé.

## Nettoyage visuel

Les informations liées au widget sont conditionnées par le focus afin d’éviter que des titres, dates ou résumés restent affichés lorsqu’aucun élément de widget n’est réellement sélectionné.

## Traductions et ressources

Le fork ajoute les libellés français et anglais requis pour ses options, ainsi que les ressources d’image et de police nécessaires aux arrière-plans et aux titres personnalisés.

## Règle de stabilité

`master` représente une version réellement testée sur Kodi. Les essais restent sur `develop` ou sous forme de builds locaux jusqu’à validation. À la promotion `.45`, `master` et `develop` sont réalignées sur le même checkpoint.
