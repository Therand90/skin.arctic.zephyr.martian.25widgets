# Navigation inline des widgets

## Objectif

La navigation inline permet d’ouvrir les dossiers d’un widget Jacktook directement dans la ligne du widget sur **Home**, sans basculer vers la fenêtre de liste standard de l’addon.

Comportements couverts par la version stable `3.19.11+25widgets.45` :

- pagination : `Next (2)`, `Next (3)`, etc. ;
- séries : série → saisons → épisodes ;
- historique `Backspace` / `Esc` ;
- maintien du focus dans la ligne ;
- sélection du premier élément après changement de dossier ;
- retour au clic natif pour les éléments réellement jouables ;
- blocage des doubles clics pendant une transition ;
- feedback de chargement non modal.

## Architecture

### Injection générique SkinShortcuts

Le mécanisme est généré dans l’`items template` des widgets. Il n’est donc pas ajouté manuellement à `FILMS`, `SÉRIES` ou à un numéro de widget précis.

Pour chaque widget généré :

- le conteneur original conserve son ID `mainmenuid*10000 + 3100 + slot` ;
- un conteneur inline distinct utilise `mainmenuid*10000 + 8100 + slot` ;
- des groupes d’informations/titre correspondants suivent le conteneur inline ;
- les variables fanart/TMDb incluent également les IDs inline.

L’utilisation d’un ID distinct est obligatoire : les essais avec deux contrôles possédant le même ID ont fait disparaître les widgets.

### Routeur universel

Chaque conteneur reçoit un `<onclick>` universel. La seule garde XML importante est `PassThrough`; aucune décision métier ne dépend de `ListItem.IsFolder`, du libellé de la section ou d’une condition fragile évaluée avant le contexte de l’item.

Le helper `extras/therand_inline45.py` décide ensuite :

1. si le `widgetPath` n’appartient pas à `plugin.video.jacktook`, il déclenche un second clic protégé par `PassThrough` afin de rendre immédiatement la main au comportement natif ;
2. pour Jacktook, il interroge le dossier courant avec `Files.GetDirectory` ;
3. il retrouve l’entrée sélectionnée par son libellé et récupère son vrai champ `file` et son `filetype` ;
4. `filetype=directory` → navigation inline ;
5. autre type → clic natif.

Cette résolution est nécessaire car, dans un widget dynamique, `ListItem.Path` peut être aplati en simple `plugin://plugin.video.jacktook/` alors que le champ `file` retourné par Kodi contient l’URL complète avec `action`, `page`, `mode`, IDs TMDb, saison, etc.

### Pagination

Jacktook génère ses boutons `Next (N)` avec une URL complète. Le routeur récupère cette URL via `Files.GetDirectory`. Un fallback peut reconstruire le paramètre `page=N` depuis le dossier courant si l’entrée n’est momentanément pas retrouvée.

Un garde rejette une cible identique au dossier déjà affiché afin qu’un vieux bouton `Next (N)` encore présent pendant un refresh ne puisse pas ajouter la même page à l’historique.

## Historique et Back

L’historique est stocké par widget dans des propriétés `Window(Home)` :

```text
TherandInline45.History.<original_widget_id>
```

Le premier niveau contient un sentinel racine. Chaque dossier quitté est ensuite empilé. `Back` dépile :

- dossier profond → dossier parent dans le même conteneur inline ;
- premier dossier inline → restauration du widget original.

Le widget original n’est pas détruit; il est seulement masqué pendant l’état inline. Le retour racine peut donc reprendre son focus directement.

## Focus et refresh

Le point délicat est le caractère asynchrone de `CDirectoryProvider` dans Kodi : un changement d’URL déclenche un job de dossier, puis les items du contrôle sont remplacés plus tard.

La version `.45` ne crée **aucun dialog modal** pendant cette phase. Les essais avec `busydialognocancel` rendaient le chargement excessivement long et provoquaient davantage de pertes de focus, car Home cessait d’être la fenêtre active utile au widget.

À la place :

- `NavBusy=true` verrouille temporairement la navigation ;
- un spinner purement visuel est rendu directement dans `Home.xml` ;
- les clics concurrents sont absorbés par un onclick no-op afin qu’ils ne retombent pas sur `DirectoryProvider::OnClick()` ;
- le helper exécute régulièrement `SetFocus(inline_id,0,absolute)` pendant le refresh ;
- `Container(id).IsUpdating` est surveillé comme signal principal ;
- un changement stable de signature des premiers labels sert de repli pour les mises à jour très rapides/mises en cache ;
- une dernière commande `SetFocus(...,0,absolute)` garantit la sélection du premier élément.

## Propriétés runtime

La version `.45` utilise notamment :

```text
TherandInline45.Path
TherandInline45.WidgetId
TherandInline45.InlineId
TherandInline45.Label
TherandInline45.PassThrough
TherandInline45.NavBusy
TherandInline45.History.<widget_id>
```

Les propriétés globales sont nettoyées lors du déchargement de Home. L’historique du widget est supprimé lorsqu’on revient à la racine.

## Compatibilité et extension à d’autres addons

La couche de génération est générique, mais le drill-down `.45` est volontairement limité à Jacktook. Les autres addons suivent le passthrough natif.

Pour ajouter un autre addon, il faut d’abord vérifier que `Files.GetDirectory` expose de manière stable :

- le chemin complet de chaque dossier dans `file` ;
- un `filetype` permettant de distinguer dossier et média jouable ;
- une navigation sans effets de bord nécessitant une fenêtre addon spécifique.

YouTube n’est pas activé dans `.45`. L’intégration doit être faite au moment du fork prévu de l’addon YouTube afin d’adapter proprement les deux côtés plutôt que d’ajouter des exceptions au skin.

## Checkpoints de développement utiles

- `.36` : premier overlay à ID distinct généré pour chaque widget ;
- `.39` : récupération fiable des vraies URLs Jacktook via `Files.GetDirectory` ;
- `.41` : premier moteur complet validé : pagination + séries/saisons + focus ;
- `.45` : stabilisation finale : spinner non modal, verrou anti-double-clic et focus fiable, validée sans bug constaté lors des tests immédiats.
