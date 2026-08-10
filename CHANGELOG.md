# Changelog

Les versions intermédiaires non publiées ne sont listées que lorsqu’elles correspondent à un checkpoint vérifié ou à un ensemble fonctionnel identifiable.

## Unreleased — `develop`

Aucune modification en attente : `develop` est alignée sur la dernière version stable.

## 3.19.11+25widgets.45

Version stable validée sur Kodi / LibreELEC le 10 août 2026.

### Navigation inline Jacktook

- navigation des dossiers directement dans les widgets de Home sans ouverture de la fenêtre de liste Jacktook ;
- pagination multi-pages `Next (N)` ;
- série → saisons → épisodes ;
- résolution des vraies URLs et du `filetype` via `Files.GetDirectory` ;
- passthrough natif pour les médias réellement jouables et pour les addons non Jacktook ;
- historique par widget pour Back/Esc ;
- focus maintenu dans la ligne et sélection absolue du premier élément après transition ;
- verrou `NavBusy` contre les doubles clics et absorption des clics concurrents ;
- spinner de chargement non modal rendu dans Home, sans bloquer le `DirectoryProvider`.

### PVR / télévision

- cartes compactes dédiées aux groupes `pvr://channels/tv/` ;
- illustrations facultatives `/storage/pictures/tvgroups/<libellé>.png|jpg` ;
- utilisation de l’illustration personnalisée comme arrière-plan plein écran au focus ;
- suppression du fallback de mosaïque/logos PVR quand aucune image personnalisée n’existe ;
- restauration du background normal de la section Chaînes ;
- image programme PVR améliorée : fanart TMDb HD en priorité, vignette EPG nette centrée avec fond agrandi en repli.

### Personnalisation conservée

- titres de section et de sous-menu : taille, couleur, police et gras ;
- arrière-plan fixe par entrée de sous-menu ;
- arrière-plans Cinéma/YouTube/replay et fallback d’images conservés ;
- compatibilité 25 widgets et service facultatif `service.therand.replaymetadata` conservées.

### Checkpoints de développement `.17` → `.45`

- `.45-develop` : retour à la base `.41` et suppression complète du DialogBusy modal introduit ensuite. Le chargement est maintenant un spinner non-modal dessiné directement dans Home, afin de laisser le DirectoryProvider du widget continuer son cycle normal. `NavBusy` bloque les doubles clics et un onclick no-op les absorbe sans fallback natif. Pendant le refresh, le helper réclame le focus de l'overlay toutes les 50 ms et attend en priorité le cycle Kodi `Container(id).IsUpdating`; changement de signature = secours pour les réponses mises en cache. Focus final = item 0 absolu. Back reçoit la même logique et le retour racine récupère agressivement le widget original ;

- `.41-develop` : suppression de toutes les conditions XML fragiles sur le routage inline. Chaque widget généré reçoit désormais un onclick universel protégé uniquement par `TherandInline41.PassThrough`; le helper décide lui-même à partir du `widgetPath` s'il s'agit de Jacktook, puis utilise `Files.GetDirectory` pour distinguer `directory` (inline) des éléments jouables (clic natif). Le deadlock de visibilité du container inline est également supprimé. Base `.39`, architecture générique pour tous les widgets actuels et futurs ;

- `.39-develop` : reprise de la `.37` après la régression `.38`. La condition Next/Previous connue fonctionnelle est conservée à l'identique. Le helper reçoit maintenant le chemin racine généré du widget et résout le véritable champ `file` de l'élément via `Files.GetDirectory`, avec fallback `page=N`. Une seconde action indépendante intercepte les vrais dossiers des sections FILMS/SÉRIES (série, saison, etc.) sans pouvoir casser la pagination. Historique et focus absolu conservés ;

- `.37-develop` : corrections de navigation du prototype inline `.36`. Le helper suit désormais `ListItem.Property(node.target_url)` avant le Path (comportement identique au DirectoryProvider Kodi), maintient une pile d'historique par widget, restaure la page précédente avec Back/Esc, et réessaie le focus jusqu'au chargement du container inline en sélectionnant toujours son premier élément via `SetFocus(id,0,absolute)`. Le mécanisme reste générique pour tous les widgets générés du mode Moderne Multi-Widgets Netflix ;

- `.36-develop` : pagination inline générique pour le vrai mode Moderne Multi-Widgets Netflix. Chaque widget dynamique généré conserve son container original et reçoit automatiquement un overlay inline à ID distinct (8100+slot), évitant le conflit d'ID de `.35`. Next/Previous est intercepté dans le vrai container, le chemin est chargé dans l'overlay, et Back restaure le widget original. Les overlays d'info/titre et les variables TMDb/fanart suivent le container inline. Tous les futurs widgets héritent du mécanisme via le template; base `.28-develop` validée, flèches inchangées ;

- `.28-develop` : pour l'encart programme de la liste des chaînes PVR, les fanarts TMDb HD remplissent de nouveau tout le cadre ; quand seul `EpgEventIcon` existe, le cadre est rempli par une version agrandie et assombrie de la vignette avec l'image originale nette centrée par-dessus, afin d'éviter les bandes vides ;

- `.27-develop` : corrige l'image du programme dans la liste des chaînes PVR : priorité au fanart TMDb haute résolution quand disponible, et passage de `aspectratio=scale` à `keep` pour empêcher le zoom/crop et la pixelisation des petites vignettes EPG ;

- `.26-develop` : rétablit le background normal de la section Chaînes (`Container(300).ListItem.Property(background)`) qui avait été masqué en `.24`, tout en conservant la correction `.25` qui supprime les mosaïques/logos PVR dans les cartes Groupes TV sans image personnalisée ;

- `.25-develop` : supprime le fallback `$VAR[PosterImage]` des cartes Groupes TV. Sans image personnalisée `/storage/pictures/tvgroups/<groupe>.png/.jpg`, la carte reste en verre sombre avec son libellé, sans mosaïque/logos de chaînes PVR ;

- `.24-develop` : masque le background propre de la section Chaînes (`Container(300).ListItem.Property(background)`, actuellement `/storage/pictures/menus/chaines.png`) tant que le widget Groupes TV est actif, afin de supprimer définitivement les logos de chaînes visibles au repos ;

- `.23-develop` : détection persistante du widget Groupes TV via `Container(300).ListItem.Property(widgetPath) = pvr://channels/tv/`, au lieu d'une propriété transitoire liée au focus ;

- `.22-develop` : masque le Global Fanart et les anciens blocs d’infos pendant tout l’état actif du widget Groupes TV afin d’éliminer l’art PVR résiduel lorsque les cartes n’ont plus le focus ;

- masque aussi le ClearArt/logos PVR lorsque le widget des groupes TV est actif mais qu’aucune carte n’a le focus ;
- groupes TV : suppression du fanart/logo PVR historique derrière l’image personnalisée ;
- fond personnalisé plus lumineux ;
- titre du groupe centré avec le même style que le grand titre de la section ;
- masquage du petit titre/résumé à gauche pendant le focus.

- images thématiques facultatives pour les groupes TV depuis `/storage/pictures/tvgroups` ;
- nom de fichier = libellé exact du groupe PVR, avec prise en charge `.jpg` et `.png` ;
- fallback automatique vers l’illustration/logos PVR existants si aucun fichier personnalisé n’est présent ;
- cartes TV conservées en style vitré compact avec focus actuel ;
- la même image personnalisée devient l’arrière-plan plein écran lorsque le groupe TV est focus, avec la luminosité/fondu habituels du skin ;
- sans image personnalisée, le fond normal de la section reste utilisé.

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
