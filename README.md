# Arctic: Zephyr (martian) + 25 widgets

Fork personnel maintenu par **Therand90**, conçu pour une installation Kodi / LibreELEC orientée widgets, télévision, replay et cinéma.

Ce projet part de **Arctic: Zephyr (martian)**, lui-même issu du travail de **jurialmunkey**, **beatmasterrs** et **martian89**. Le fork conserve leur identité visuelle, mais son fonctionnement d’accueil s’est progressivement éloigné de l’original afin de mieux répondre à notre usage quotidien.

> Version stable actuelle : `3.19.11+25widgets.10` — Kodi 21 Omega.

## Ce que ce fork apporte

- jusqu’à **25 widgets configurables** par section d’accueil ;
- navigation retravaillée entre le menu et les listes de widgets ;
- titres de section personnalisables : taille, couleur, police et gras ;
- meilleure gestion des arrière-plans personnalisés, Cinéma, YouTube et replay ;
- arrière-plan fixe configurable pour chaque entrée de sous-menu sur `develop` ;
- repli intelligent sur les vignettes lorsque le fanart est absent ou générique ;
- affichage adapté aux vignettes paysage, portrait et carrées ;
- intégration facultative avec `service.therand.replaymetadata` pour enrichir les résumés de replay ;
- filtrage des faux résumés identiques au titre ;
- ressources et traductions supplémentaires nécessaires aux options propres au fork.

Le détail des différences fonctionnelles est conservé dans [`docs/THERAND_CUSTOMIZATIONS.md`](docs/THERAND_CUSTOMIZATIONS.md). L’historique des checkpoints importants se trouve dans [`CHANGELOG.md`](CHANGELOG.md).

## Branches

| Branche | Rôle |
|---|---|
| `master` | version stable, testée sur Kodi avant publication |
| `develop` | prochaine version et améliorations en cours |

Le tag `25widgets.10-working` désigne la copie exacte du checkpoint fonctionnel actuellement installé sur Kodi.

## Installation

1. Télécharger le ZIP d’une version publiée dans les **Releases** GitHub.
2. Dans Kodi, activer **Sources inconnues** dans `Paramètres > Système > Extensions`.
3. Ouvrir `Extensions > Installer depuis un fichier ZIP`.
4. Sélectionner l’archive du skin.
5. Conserver une sauvegarde de `userdata/addon_data/skin.arctic.zephyr.martian.25widgets` avant une mise à jour importante.

Les builds provenant de `develop` sont destinés aux tests et peuvent nécessiter un rechargement du skin ou une reconstruction de certains widgets SkinShortcuts.

## Services compagnons

Le skin fonctionne seul. Certaines fonctions de replay sont toutefois prévues pour coopérer avec le service facultatif :

- `service.therand.replaymetadata` — résumés et métadonnées de replay mis en cache par widget.

L’absence du service ne doit pas empêcher le skin de démarrer : les métadonnées Kodi classiques restent utilisées en repli.

## Méthode de développement

Toute modification suit désormais ce cycle :

1. travail sur `develop` ;
2. validation XML et contrôle du diff ;
3. test réel sur Kodi / LibreELEC ;
4. commit et push du checkpoint validé ;
5. tag de sauvegarde avant l’amélioration suivante ;
6. fusion dans `master` uniquement après validation.

## Crédits et licence

Merci à **jurialmunkey**, **beatmasterrs** et **martian89** pour les fondations du skin et les années de travail qui rendent ce fork possible.

Le projet reste distribué sous **Creative Commons Attribution-NonCommercial-ShareAlike 3.0**. Les éléments provenant d’Arctic Fuse 2 conservent leur licence **CC BY-NC-SA 4.0** respective. Consultez [`LICENSE.txt`](LICENSE.txt) et les licences incluses avec les ressources concernées.

Ce dépôt est un fork communautaire indépendant. Les problèmes propres à cette version doivent être signalés sur le dépôt Therand90, pas auprès des auteurs d’origine.
