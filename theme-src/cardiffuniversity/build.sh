#!/usr/bin/env bash
# Build the Cardiff University theme into its runtime folder, and optionally zip it for release.
#
#   ./build.sh            tokens.json -> scss/_cu-tokens.scss, compile SCSS into
#                         themes/site/cardiffuniversity/cardiffuniversity.css, check the author guide
#   ./build.sh package    the same, then zip the runtime folder into dist/cardiffuniversity.zip
#
# The runtime folder holds only what Xerte loads (.info, .css, .js, .jpg, logo_left.svg).
# Xerte copies the whole theme folder into every project export, so nothing else belongs there.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
NAME=cardiffuniversity
RUNTIME="$REPO/themes/site/$NAME"

python3 "$HERE/tools/build-tokens.py"
npx -y sass@1 --no-source-map "$HERE/$NAME.scss" "$RUNTIME/$NAME.css"
echo "Compiled $RUNTIME/$NAME.css"
# The author guide's utility tables are generated from the CSS; warn (do not fail) when they drift.
python3 "$HERE/tools/build-reference.py" --check || echo "Run: python3 tools/build-reference.py"

if [ "${1:-}" = "package" ]; then
    mkdir -p "$HERE/dist"
    rm -f "$HERE/dist/$NAME.zip"
    (cd "$REPO/themes/site" && zip -rqX "$HERE/dist/$NAME.zip" "$NAME" -x '.*' '*/.*')
    echo "Packaged $HERE/dist/$NAME.zip"
    unzip -l "$HERE/dist/$NAME.zip"
fi
