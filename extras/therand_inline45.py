# -*- coding: utf-8 -*-
import json
import re
import sys
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import xbmc
import xbmcgui

LOG = '[TherandInline45] '
HOME = xbmcgui.Window(10000)
ROOT_SENTINEL = '__THERAND_ROOT__'


def log(msg):
    xbmc.log(LOG + msg, xbmc.LOGINFO)


def arg(i, default=''):
    try:
        return sys.argv[i]
    except Exception:
        return default


def info(expr):
    try:
        return xbmc.getInfoLabel(expr) or ''
    except Exception:
        return ''


def item_info(container_id, suffix):
    return info('Container({}).ListItem.{}'.format(container_id, suffix)).strip()


def clean_label(value):
    value = re.sub(r'\[/?COLOR(?: [^\]]+)?\]', '', value or '', flags=re.I)
    value = re.sub(r'\[/?[BI]\]', '', value, flags=re.I)
    return value.strip()


def is_jacktook_url(url):
    return 'plugin.video.jacktook' in (url or '').lower()


def raw_directory(directory):
    request = {
        'jsonrpc': '2.0',
        'method': 'Files.GetDirectory',
        'params': {'directory': directory, 'media': 'files'},
        'id': 45,
    }

    try:
        response = json.loads(xbmc.executeJSONRPC(json.dumps(request)))
    except Exception as exc:
        log('DIR decode error {!r}: {}'.format(directory, exc))
        return []

    if response.get('error'):
        log('DIR error {!r}: {!r}'.format(directory, response.get('error')))
        return []

    rows = response.get('result', {}).get('files', []) or []
    log('DIR {!r} -> {} entries'.format(directory, len(rows)))
    return rows


def pagination_fallback(current_dir, label):
    label = clean_label(label)
    match = re.search(r'\((\d+)\)\s*$', label)
    if not match:
        return '', ''

    if not re.match(
        r'^(next|suivant|previous|précédent|precedent)\b',
        label,
        flags=re.I,
    ):
        return '', ''

    page = match.group(1)

    try:
        parts = urlsplit(current_dir)
        query = parse_qsl(parts.query, keep_blank_values=True)
        new_query = []
        found = False

        for key, value in query:
            if key == 'page':
                new_query.append((key, page))
                found = True
            else:
                new_query.append((key, value))

        if not found:
            new_query.append(('page', page))

        return (
            urlunsplit(
                (
                    parts.scheme,
                    parts.netloc,
                    parts.path,
                    urlencode(new_query),
                    parts.fragment,
                )
            ),
            'directory',
        )
    except Exception as exc:
        log('PAGE fallback error {!r}: {}'.format(current_dir, exc))
        return '', ''


def resolve_target(current_dir, source_id):
    wanted = clean_label(item_info(source_id, 'Label'))
    raw_path = item_info(source_id, 'Path')

    exact = []
    folded = []

    for row in raw_directory(current_dir):
        label = clean_label(row.get('label', ''))
        path = (row.get('file') or '').strip()
        filetype = (row.get('filetype') or '').strip().lower()

        if not path:
            continue

        candidate = (label, path, filetype)

        if label == wanted:
            exact.append(candidate)
        elif label.casefold() == wanted.casefold():
            folded.append(candidate)

    matches = exact or folded

    if matches:
        label, path, filetype = matches[0]
        log('RESOLVE {!r} -> {!r} type={!r}'.format(label, path, filetype))
        return path, filetype, 'jsonrpc'

    fallback, filetype = pagination_fallback(current_dir, wanted)
    if fallback:
        log('RESOLVE page fallback {!r} -> {!r}'.format(wanted, fallback))
        return fallback, filetype, 'page-fallback'

    log(
        'RESOLVE FAILED current={!r} label={!r} raw_path={!r}'.format(
            current_dir, wanted, raw_path
        )
    )
    return '', '', ''


def history_key(original_id):
    return 'TherandInline45.History.{}'.format(original_id)


def load_history(original_id):
    raw = HOME.getProperty(history_key(original_id))
    if not raw:
        return []

    try:
        value = json.loads(raw)
        return value if isinstance(value, list) else []
    except Exception:
        return []


def save_history(original_id, history):
    HOME.setProperty(history_key(original_id), json.dumps(history))


def clear_history(original_id):
    HOME.clearProperty(history_key(original_id))


def num_items(container_id):
    try:
        return int(info('Container({}).NumItems'.format(container_id)) or '0')
    except Exception:
        return 0


def is_updating(container_id):
    try:
        return xbmc.getCondVisibility(
            'Container({}).IsUpdating'.format(container_id)
        )
    except Exception:
        return False


def has_focus(container_id):
    try:
        return xbmc.getCondVisibility(
            'Control.HasFocus({})'.format(container_id)
        )
    except Exception:
        return False


def container_signature(container_id, limit=5):
    labels = []
    for idx in range(limit):
        label = clean_label(
            info(
                'Container({}).ListItemAbsolute({}).Label'.format(
                    container_id, idx
                )
            )
        )
        if label:
            labels.append(label)
    return labels


def nav_locked():
    return HOME.getProperty('TherandInline45.NavBusy') == 'true'


def lock_nav():
    if nav_locked():
        return False
    HOME.setProperty('TherandInline45.NavBusy', 'true')
    return True


def unlock_nav():
    HOME.clearProperty('TherandInline45.NavBusy')


def keep_focus_and_wait(container_id, reason, previous_signature):
    """
    Let Home continue rendering normally. While Kodi's DirectoryProvider changes,
    repeatedly reclaim the inline control and item zero.

    Success is primarily based on Kodi's own IsUpdating cycle. A visible content
    signature change is accepted too for very fast/cached updates where IsUpdating
    can be missed between two 50 ms samples.
    """
    seen_updating = False
    changed_hits = 0
    last_changed = []

    log(
        'WAIT {} id={} previous={!r}'.format(
            reason, container_id, previous_signature
        )
    )

    # Immediate focus claim: important when switching root widget -> inline twin.
    xbmc.executebuiltin('SetFocus({},0,absolute)'.format(container_id))

    # Usually < 1 s. Hard ceiling 5 s, without blocking Home behind a modal.
    for attempt in range(1, 101):
        xbmc.sleep(50)

        # Keep ownership of focus during the swap. This prevents Kodi from
        # settling on FILMS / SERIES / YOUTUBE while the provider is changing.
        xbmc.executebuiltin('SetFocus({},0,absolute)'.format(container_id))

        updating = is_updating(container_id)
        if updating:
            seen_updating = True

        count = num_items(container_id)
        actual = container_signature(container_id, limit=5)

        changed = bool(actual) and actual != previous_signature
        if changed:
            if actual == last_changed:
                changed_hits += 1
            else:
                changed_hits = 1
                last_changed = actual
        else:
            changed_hits = 0
            last_changed = []

        # Preferred completion: we observed Kodi updating and it has now
        # finished with real items.
        update_finished = seen_updating and not updating and count > 0

        # Cached/very fast completion fallback.
        content_changed = count > 0 and changed_hits >= 2

        if update_finished or content_changed:
            # Final absolute selection after the new items exist.
            xbmc.executebuiltin('SetFocus({},0,absolute)'.format(container_id))
            xbmc.sleep(70)
            first = info(
                'Container({}).ListItemAbsolute(0).Label'.format(container_id)
            ).strip()
            log(
                'READY {} id={} attempt={} items={} seen_updating={} '
                'first={!r} signature={!r}'.format(
                    reason,
                    container_id,
                    attempt,
                    count,
                    seen_updating,
                    first,
                    actual,
                )
            )
            return True

    # Do not leave the user without a widget focus even after timeout.
    xbmc.executebuiltin('SetFocus({},0,absolute)'.format(container_id))
    log(
        'READY TIMEOUT {} id={} items={} updating={} focus={} '
        'previous={!r} actual={!r}'.format(
            reason,
            container_id,
            num_items(container_id),
            is_updating(container_id),
            has_focus(container_id),
            previous_signature,
            container_signature(container_id, limit=5),
        )
    )
    return False


def focus_root(original_id):
    # Root provider was only hidden, not destroyed. Reclaim it aggressively
    # for a short period so clearing WidgetId never strands focus on menu 300.
    for attempt in range(1, 21):
        xbmc.executebuiltin('SetFocus({},0,absolute)'.format(original_id))
        xbmc.sleep(50)
        if has_focus(original_id) and num_items(original_id) > 0:
            log(
                'FOCUS ROOT id={} attempt={} first={!r}'.format(
                    original_id,
                    attempt,
                    info(
                        'Container({}).ListItemAbsolute(0).Label'.format(
                            original_id
                        )
                    ).strip(),
                )
            )
            return True

    log(
        'FOCUS ROOT FAILED id={} items={} focus={}'.format(
            original_id, num_items(original_id), has_focus(original_id)
        )
    )
    return False


def clear_inline(original_id):
    for name in ('Path', 'WidgetId', 'InlineId', 'Label'):
        HOME.clearProperty('TherandInline45.' + name)
    clear_history(original_id)


def native_passthrough(source_id):
    # Disable the universal router for the synthetic second Select so Kodi's
    # original DirectoryProvider receives the click.
    HOME.setProperty('TherandInline45.PassThrough', 'true')
    unlock_nav()
    xbmc.sleep(30)
    xbmc.executebuiltin('SetFocus({})'.format(source_id))
    xbmc.sleep(20)
    xbmc.executebuiltin('Action(Select)')
    xbmc.sleep(500)
    HOME.clearProperty('TherandInline45.PassThrough')
    log('PASSTHROUGH source={}'.format(source_id))


mode = arg(1)

try:
    source_id = int(arg(2, '0'))
except Exception:
    source_id = 0

try:
    original_id = int(arg(3, '0'))
except Exception:
    original_id = 0

try:
    inline_id = int(arg(4, '0'))
except Exception:
    inline_id = 0

root_dir = arg(5, '').strip()


if mode == 'route':
    if not lock_nav():
        log(
            'ROUTE IGNORED busy source={} label={!r}'.format(
                source_id, item_info(source_id, 'Label')
            )
        )
        raise SystemExit

    selected_label = item_info(source_id, 'Label')
    current_inline = HOME.getProperty('TherandInline45.Path').strip()

    current_dir = (
        root_dir
        if source_id == original_id or not current_inline
        else current_inline
    )

    log(
        'ROUTE source={} original={} inline={} label={!r} '
        'current={!r} root={!r}'.format(
            source_id,
            original_id,
            inline_id,
            selected_label,
            current_dir,
            root_dir,
        )
    )

    if not is_jacktook_url(current_dir):
        log('ROUTE non-Jacktook -> native')
        native_passthrough(source_id)
        raise SystemExit

    previous_signature = container_signature(source_id, limit=5)
    target, filetype, resolver = resolve_target(current_dir, source_id)

    if not target:
        log('ROUTE unresolved -> native')
        native_passthrough(source_id)
        raise SystemExit

    if filetype != 'directory':
        log('ROUTE playable type={!r} -> native'.format(filetype))
        native_passthrough(source_id)
        raise SystemExit

    # Ignore a stale card that resolves back to the exact directory already
    # displayed. This can happen during a very fast repeated click.
    if current_inline and target == current_inline:
        log(
            'ROUTE stale/self ignored label={!r} current={!r}'.format(
                selected_label, current_inline
            )
        )
        keep_focus_and_wait(inline_id, 'stale', previous_signature)
        unlock_nav()
        raise SystemExit

    history = load_history(original_id)

    if source_id == original_id or not current_inline:
        history = [ROOT_SENTINEL]
    else:
        if not history:
            history = [ROOT_SENTINEL]
        if history[-1] != current_dir:
            history.append(current_dir)

    save_history(original_id, history)

    HOME.setProperty('TherandInline45.Path', target)
    HOME.setProperty('TherandInline45.InlineId', str(inline_id))
    HOME.setProperty('TherandInline45.Label', selected_label)

    # Switch rows only after the target is fully resolved. No modal window is
    # opened; Home remains the active GUI window throughout.
    HOME.setProperty('TherandInline45.WidgetId', str(original_id))

    log(
        'INLINE resolver={} target={!r} history={!r}'.format(
            resolver, target, history
        )
    )

    try:
        keep_focus_and_wait(
            inline_id,
            'open',
            previous_signature,
        )
    finally:
        unlock_nav()


elif mode == 'back':
    if not lock_nav():
        log('BACK IGNORED busy')
        raise SystemExit

    try:
        stored_original = int(
            HOME.getProperty('TherandInline45.WidgetId') or '0'
        )
    except Exception:
        stored_original = 0

    try:
        stored_inline = int(
            HOME.getProperty('TherandInline45.InlineId') or '0'
        )
    except Exception:
        stored_inline = 0

    if stored_original:
        original_id = stored_original
    if stored_inline:
        inline_id = stored_inline

    history = load_history(original_id)
    current = HOME.getProperty('TherandInline45.Path').strip()

    log(
        'BACK original={} inline={} current={!r} history={!r}'.format(
            original_id, inline_id, current, history
        )
    )

    if not history:
        clear_inline(original_id)
        try:
            focus_root(original_id)
        finally:
            unlock_nav()
        raise SystemExit

    previous = history.pop()

    if previous == ROOT_SENTINEL:
        clear_inline(original_id)
        try:
            focus_root(original_id)
        finally:
            unlock_nav()
        log('BACK -> ROOT {}'.format(original_id))
    else:
        previous_signature = container_signature(inline_id, limit=5)
        save_history(original_id, history)
        HOME.setProperty('TherandInline45.Path', previous)

        log('BACK -> {!r}'.format(previous))

        try:
            keep_focus_and_wait(
                inline_id,
                'back',
                previous_signature,
            )
        finally:
            unlock_nav()


else:
    log('Unknown mode {!r}'.format(mode))
