# Baseline validée — 89.5.12 / AutoTrailer 0.27.33

Validation réelle sur Kodi 21.3 / LibreELEC le 25 août 2026.

## Stack de référence

- Skin : `3.19.11+25widgets.89.5.12`
- AutoTrailer : `0.27.33`
- YouTube fork : `7.4.4+therand.1.0.9`

## Comportements validés

- pagination JackTook inline rapide et fiable ;
- un seul clic suffit pour passer à la page suivante ;
- garde de focus pendant le remplacement du `DirectoryProvider`, sans saut vers le widget du dessus/dessous ;
- retour Backspace hiérarchique : poster courant -> début de ligne, début de page N -> page N-1, début de page 1 -> menu Home ;
- une preview active est arrêtée sans promotion FullScreenVideo ;
- aucune ouverture parasite du dossier YouTube durant le stress-test final ;
- AutoTrailer n'utilise pas `Action(Back,Home)` pour cette route Home ;
- le keymap Home est réellement rechargé via `Action(ReloadKeymaps)`.

## Pagination 89.5.12

La version 89.5.12 conserve le routage direct introduit dans 89.5.11 : les cartes `Next (N)` sont résolues directement par leur numéro de page, sans `Files.GetDirectory` du répertoire courant et sans `Container.Refresh`.

Pendant le swap, le focus est garé sur un contrôle neutre afin que Kodi ne choisisse pas un widget voisin lorsque le container inline est momentanément vide. En cas de provider bloqué, le helper garde son timeout de sécurité et restaure proprement le widget racine.

## Intégrité du ZIP complet testé

`skin.arctic.zephyr.martian.25widgets-3.19.11+25widgets.89.5.12-focus-anchor-path-rearm.zip`

SHA-256 : `b1476bca58c600cc28e37804d0d180ba725fd3850df0bcf8cbd20cf12fa516d9`

Ce hash désigne exactement l'archive complète testée avant la promotion de cette baseline.

## Snapshot source archivé dans GitHub

Le ZIP complet contient beaucoup d'assets inchangés et n'est pas stocké en entier dans Git. À la place, la branche conserve un snapshot ZIP des fichiers source concernés par le développement 89.5.12 (XML Home/widgets/vidéo, template de widgets et helpers Python).

SHA-256 du snapshot source : `c6106ae3e296a1bf7768934fe215bfcb87e684798c3a0068c3979621dc4bb014`

Restauration :

```sh
sh baseline/restore-89.5.12-source.sh
```

Le script concatène les morceaux Base64 archivés, vérifie le SHA-256 puis exécute `unzip -t`. Le morceau `part01` est volontairement découpé en `part01a` à `part01d` pour éviter toute troncature lors de l'archivage via l'API GitHub.

## Règle de reprise

Toute amélioration suivante doit partir de cette baseline. Ne pas réintroduire les expériences abandonnées : `Container.Refresh` forcé, martèlement de `SetFocus`, AutoTrailer 0.27.24/0.27.25, ou `Action(Back,Home)` pour le Backspace Home.
