#!/usr/bin/env bash
# Build the Cardiff University theme into its runtime folder, and optionally zip it for release.
#
#   ./build.sh            tokens.json -> scss/_cu-tokens.scss, compile SCSS into
#                         themes/site/cardiffuniversity/cardiffuniversity.css, check the author guide
#   ./build.sh package    the same, then zip the runtime folder into dist/cardiffuniversity.zip
#   ./build.sh guide      the same, then check and build the author guide into site/
#
# The runtime folder holds only what Xerte loads (.info, .css, .js, .jpg, logo_left.svg).
# Xerte copies the whole theme folder into every project export, so nothing else belongs there.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
NAME=cardiffuniversity
RUNTIME="$REPO/themes/site/$NAME"

python3 "$HERE/tools/build-tokens.py"
# Pinned so CI's compile matches the committed CSS byte for byte. Update both together.
npx -y sass@1.104.1 --no-source-map "$HERE/$NAME.scss" "$RUNTIME/$NAME.css"
echo "Compiled $RUNTIME/$NAME.css"
# Components read the theme names in _allvariables.scss; only the callouts and the logo width may read --cu-* directly.
if grep -rnE '^[^/]*var\(--cu-' "$HERE/scss" --include='*.scss' \
    | grep -vE '_allvariables\.scss|_cu-tokens\.scss|--cu-callout-|--cu-logo-width|--cu-sticky-nav'; then
    echo "Warning: the lines above read --cu-* directly; map the token in _allvariables.scss and use that name."
fi
# The author guide's utility tables are generated from the CSS; warn (do not fail) when they drift.
python3 "$HERE/tools/build-reference.py" --check || echo "Run: python3 tools/build-reference.py"

if [ "${1:-}" = "guide" ]; then
    python3 "$HERE/tools/build-guide.py"
fi

if [ "${1:-}" = "package" ]; then
    mkdir -p "$HERE/dist"
    rm -f "$HERE/dist/$NAME.zip"
    (cd "$REPO/themes/site" && zip -rqX "$HERE/dist/$NAME.zip" "$NAME" -x '.*' '*/.*')
    echo "Packaged $HERE/dist/$NAME.zip"
    unzip -l "$HERE/dist/$NAME.zip"
fi
