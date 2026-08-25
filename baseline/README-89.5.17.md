# Baseline validée — 89.5.17

Validation réelle sur Kodi 21.3 / LibreELEC le 25 août 2026.

## Stack de référence

- Skin : `3.19.11+25widgets.89.5.17`
- AutoTrailer : `0.27.33`
- YouTube fork : `7.4.4+therand.1.0.9`
- Baseline parente : `stable/89.5.12-pagination-backspace-baseline`

## État validé

Cette version conserve toute la logique de pagination/focus validée en 89.5.12 et ajoute uniquement la finition visuelle et le cloisonnement d'historique nécessaires.

Comportements validés :

- pagination JackTook inline stable ;
- focus guard/path rearm 89.5.12 conservés ;
- le décor théâtre `therand-next-focus.png` reste visible pendant `NavBusy` ;
- le texte `Vers page n°X` reste visible pendant le chargement, y compris lors d'un retour vers une page précédente ;
- l'historique `TherandInline45` appartient strictement au widget vertical qui l'a créé ;
- lorsqu'un autre widget vertical prend le focus, l'ancien historique inline est abandonné immédiatement, sans déplacer le focus ;
- séquence Backspace attendue et validée sur un widget paginé : `page N -> ... -> page 2 -> page 1 -> menu Home` ;
- après changement de widget vertical, Backspace ne remonte jamais dans les anciennes pages du widget quitté ;
- AutoTrailer 0.27.33 reste inchangé.

## Intégrité du ZIP testé

Archive réellement testée :

`skin.arctic.zephyr.martian.25widgets-3.19.11+25widgets.89.5.17-widget-scoped-history-transition-title.zip`

SHA-256 :

`9ff2c47fda30fca7f8588683fa3a7d580d8f1e0812aad9bfb8da0fe4dda07fd8`

## Delta exact depuis 89.5.12

Le fichier `baseline/89.5.12-to-89.5.17.patch` contient le delta textuel exact entre le ZIP 89.5.12 validé et le ZIP 89.5.17 validé.

Les seuls fichiers modifiés sont :

- `addon.xml`
- `1080i/Home.xml`
- `1080i/Includes.xml`
- `1080i/Includes_Widgets.xml`
- `CHANGELOG.md`
- `extras/therand_inline45.py`

Le fichier `baseline/89.5.17-files.sha256` contient les SHA-256 exacts de ces six fichiers dans l'état validé.

## Points techniques

### Transition visuelle

`TherandInline45.TransitionVisual` et `TherandInline45.TransitionTitle` sont des propriétés purement visuelles. Elles ne participent pas au choix du provider ni au focus guard. Elles sont effacées avec `unlock_nav()` et à la fermeture du Home.

### Historique limité au widget actif

Lorsqu'un container vertical différent prend le focus, `Includes_Widgets.xml` appelle :

`RunScript(special://skin/extras/therand_inline45.py,abandon,<nouveau_container>)`

Le mode `abandon` supprime l'historique et les propriétés inline de l'ancien widget sans toucher au nouveau focus. Il est ignoré pendant `NavBusy` afin de ne pas casser un handoff en cours.

## Essais abandonnés à ne pas réintroduire

- 89.5.13 : tentative de gel via `GlobalFanart`, avec régression de descente de widget ;
- 89.5.14 : overlay de fond, inefficace ;
- 89.5.15 : maintien du fallback pendant `IsUpdating`, inefficace ;
- 89.5.16 : maintien correct du décor théâtre mais texte absent et historique Backspace non cloisonné.

## Règle de reprise

Toute nouvelle modification du Home/pagination doit partir de **89.5.17**. Conserver 89.5.12 comme checkpoint précédent indépendant et ne pas modifier les branches `stable/...` existantes.