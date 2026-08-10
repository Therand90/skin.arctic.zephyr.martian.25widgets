# Arctic: Zephyr (martian) + 25 widgets

Fork personnel maintenu par **Therand90**, conçu pour une installation Kodi / LibreELEC orientée widgets, télévision, replay et cinéma.

Ce projet part de **Arctic: Zephyr (martian)**, lui-même issu du travail de **jurialmunkey**, **beatmasterrs** et **martian89**. Le fork conserve leur identité visuelle, mais son accueil a été étendu pour un usage très orienté widgets et navigation directe depuis Home.

> Version stable actuelle : `3.19.11+25widgets.45` — Kodi 21 Omega / LibreELEC 12.x.

## Ce que ce fork apporte

- jusqu’à **25 widgets configurables** par section d’accueil ;
- navigation retravaillée entre le menu et les listes de widgets ;
- titres des sections principales **et des entrées de sous-menu** personnalisables : taille, couleur, police et gras ;
- arrière-plan fixe configurable par entrée de sous-menu, y compris les chemins `/storage`, `special://`, URL et `image://` ;
- meilleure gestion des arrière-plans personnalisés, Cinéma, YouTube et replay ;
- replis d’images adaptés aux contenus paysage, portrait et carré ;
- intégration facultative avec `service.therand.replaymetadata` pour enrichir les résumés de replay ;
- widgets **Groupes TV PVR** en cartes compactes, avec illustrations personnalisées facultatives dans `/storage/pictures/tvgroups` ;
- amélioration de l’image du programme PVR : priorité au fanart TMDb HD, puis vignette EPG nette avec fond agrandi ;
- navigation **inline Jacktook** directement dans les widgets de Home : pagination `Next`, séries, saisons et épisodes sans ouvrir les fenêtres de liste classiques ;
- historique `Back/Esc`, verrou anti-double-clic, focus conservé dans la ligne et retour automatique au premier élément après changement de niveau ;
- spinner de chargement **non modal**, dessiné dans Home pour ne pas bloquer le `DirectoryProvider` Kodi.

Le détail des différences fonctionnelles est conservé dans [`docs/THERAND_CUSTOMIZATIONS.md`](docs/THERAND_CUSTOMIZATIONS.md). L’architecture de la navigation inline est documentée séparément dans [`docs/INLINE_NAVIGATION.md`](docs/INLINE_NAVIGATION.md). L’historique des checkpoints importants se trouve dans [`CHANGELOG.md`](CHANGELOG.md).

## Navigation inline Jacktook

La version `.45` transforme les widgets Jacktook en petits navigateurs hiérarchiques sans quitter l’accueil :

`Trending → Next (2) → Next (3) → …`

et pour les séries :

`Trending → Série → Saison → Épisodes`

Les éléments de type dossier restent inline. Les éléments réellement jouables repassent automatiquement vers le clic natif de Kodi/Jacktook. `Backspace` / `Esc` remonte l’historique inline et revient au widget racine au dernier niveau.

Le système est injecté dans le template générique des widgets du mode **Moderne Multi-Widgets Netflix** : un nouveau widget généré par SkinShortcuts hérite donc de la mécanique sans duplication manuelle par slot. Le routeur n’active actuellement le drill-down que pour les chemins `plugin.video.jacktook`; les autres addons conservent leur comportement natif.

## Groupes TV PVR

Pour un widget dont le chemin est `pvr://channels/tv/`, le skin utilise un rendu compact dédié. Une image thématique peut être fournie par groupe :

```text
/storage/pictures/tvgroups/<nom exact du groupe>.png
/storage/pictures/tvgroups/<nom exact du groupe>.jpg
```

Exemples : `Toutes les chaînes.png`, `Cinéma.png`, `Crime.png`, `Jeunesse.png`.

Quand une image personnalisée existe, elle est utilisée dans la carte et comme arrière-plan plein écran au focus. Sans image personnalisée, la carte reste propre et sombre, sans mosaïque parasite de logos PVR.

## Branches

| Branche | Rôle |
|---|---|
| `master` | version stable, testée sur Kodi avant publication |
| `develop` | prochaine version et améliorations en cours |

À la publication de `.45`, `master` et `develop` sont réalignées sur le même checkpoint validé. Les anciens tags `25widgets.10-working`, `25widgets.12-working` et `25widgets.13-working` restent des points de restauration historiques.

## Installation

1. Télécharger le ZIP d’une version publiée dans les **Releases** GitHub ou générer l’archive depuis `master`.
2. Dans Kodi, activer **Sources inconnues** dans `Paramètres > Système > Extensions`.
3. Ouvrir `Extensions > Installer depuis un fichier ZIP`.
4. Sélectionner l’archive du skin.
5. Conserver une sauvegarde de `userdata/addon_data/skin.arctic.zephyr.martian.25widgets` avant une mise à jour importante.

Les builds provenant de `develop` sont destinés aux tests et peuvent nécessiter un redémarrage de Kodi ou une reconstruction de certains widgets SkinShortcuts.

## Services compagnons

Le skin fonctionne seul. Certaines fonctions de replay sont toutefois prévues pour coopérer avec le service facultatif :

- `service.therand.replaymetadata` — résumés et métadonnées de replay mis en cache par widget.

L’absence du service ne doit pas empêcher le skin de démarrer : les métadonnées Kodi classiques restent utilisées en repli.

## Méthode de développement

Toute modification suit ce cycle :

1. travail sur `develop` ou sur un build de test local ;
2. validation XML et contrôle du diff ;
3. test réel sur Kodi / LibreELEC ;
4. conservation d’un checkpoint fonctionnel ;
5. documentation des changements ;
6. promotion dans `master` uniquement après validation utilisateur.

La navigation inline `.45` a été développée par itérations locales `.36` à `.45`; `.41` a constitué le premier moteur complet fonctionnel et `.45` la stabilisation validée sans bug constaté lors des tests immédiats.

## Crédits et licence

Merci à **jurialmunkey**, **beatmasterrs** et **martian89** pour les fondations du skin et les années de travail qui rendent ce fork possible.

Le projet reste distribué sous **Creative Commons Attribution-NonCommercial-ShareAlike 3.0**. Les éléments provenant d’Arctic Fuse 2 conservent leur licence **CC BY-NC-SA 4.0** respective. Consultez [`LICENSE.txt`](LICENSE.txt) et les licences incluses avec les ressources concernées.

Ce dépôt est un fork communautaire indépendant. Les problèmes propres à cette version doivent être signalés sur le dépôt Therand90, pas auprès des auteurs d’origine.
