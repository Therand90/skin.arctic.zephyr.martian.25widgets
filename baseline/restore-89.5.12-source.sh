#!/bin/sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
BASE="$ROOT/baseline"
OUT="${1:-$ROOT/skin-89.5.12-source-subset.zip}"
EXPECTED="c6106ae3e296a1bf7768934fe215bfcb87e684798c3a0068c3979621dc4bb014"

cat \
  "$BASE/89.5.12-source-subset.zip.b64.part00" \
  "$BASE/89.5.12-source-subset.zip.b64.part01a" \
  "$BASE/89.5.12-source-subset.zip.b64.part01b" \
  "$BASE/89.5.12-source-subset.zip.b64.part01c" \
  "$BASE/89.5.12-source-subset.zip.b64.part01d" \
  "$BASE/89.5.12-source-subset.zip.b64.part02" \
  "$BASE/89.5.12-source-subset.zip.b64.part03" \
  "$BASE/89.5.12-source-subset.zip.b64.part04" \
  "$BASE/89.5.12-source-subset.zip.b64.part05" \
  "$BASE/89.5.12-source-subset.zip.b64.part06" \
  "$BASE/89.5.12-source-subset.zip.b64.part07" \
  | base64 -d > "$OUT"

ACTUAL="$(sha256sum "$OUT" | awk '{print $1}')"
if [ "$ACTUAL" != "$EXPECTED" ]; then
    echo "ERROR: SHA256 mismatch" >&2
    echo "expected: $EXPECTED" >&2
    echo "actual:   $ACTUAL" >&2
    rm -f "$OUT"
    exit 1
fi

unzip -t "$OUT" >/dev/null
printf 'OK: restored %s\nSHA256: %s\n' "$OUT" "$ACTUAL"
