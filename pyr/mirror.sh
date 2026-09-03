#!/usr/bin/env sh
# Mirror this site into the pyr.ai repository as /gallery/.
#
#   sh pyr/mirror.sh /path/to/pyr-homepage-static
#
# pyr.ai is a Flask app (main.py), not a static host: it renders templates for
# the routes it knows and answers every other path with the home page. So the
# site is copied into <pyr>/static/gallery/, the Seung Lab variant
# (pyr/seunglab.py) is applied to the front page there, and main.py learns two
# routes that serve the folder at /gallery/ (pyr/pyr_routes.py). Every URL in
# the site is relative, so nothing else is rewritten. A preview of the variant
# is built into seunglab/ in this repo: sh pyr/preview.sh
#
# Run it again after any change here and commit the result on pyr's main branch,
# which is the branch that deploys pyr.ai. The GitHub Action in
# .github/workflows/mirror-pyr.yml does exactly this on every change to main.
set -eu
PYR=${1:?usage: sh pyr/mirror.sh /path/to/pyr-homepage-static}
HERE=$(cd "$(dirname "$0")/.." && pwd)
[ -d "$PYR/.git" ] || { echo "not a git checkout: $PYR" >&2; exit 1; }

DEST="$PYR/static/gallery"

# an earlier run put the folder at the top level, where Flask never looks
if [ -d "$PYR/gallery" ]; then
  git -C "$PYR" rm -rq gallery 2>/dev/null || rm -rf "$PYR/gallery"
  echo "removed the stray top-level gallery/"
fi

# a clean copy every time, so a file deleted here is deleted there too
rm -rf "$DEST"
mkdir -p "$DEST"
cp "$HERE"/*.html "$HERE/favicon.ico" "$DEST/"
cp -R "$HERE/images" "$HERE/video" "$HERE/web" "$DEST/"

# the Seung Lab version differs from this site in a few deliberate places;
# seunglab.py holds every one of them
python3 "$HERE/pyr/seunglab.py" "$DEST" "$DEST"

# teach the Flask app the /gallery/ routes, and keep the old FlyWire gallery
# page reachable at /gallery-flywire. Idempotent; refuses to guess if main.py
# no longer looks as expected.
python3 "$HERE/pyr/pyr_routes.py" "$PYR"

# the GALLERY link is commented out in the nav of every template. Uncomment it,
# exactly that markup and nothing else. A no-op once it has been done.
python3 "$HERE/pyr/pyr_routes.py" "$PYR" --nav

git -C "$PYR" add -A
echo "staged in $PYR: $(git -C "$PYR" diff --cached --stat | tail -1)"
echo "next: cd $PYR && git commit -m 'Mirror the CA3 renderings site at /gallery' && git push origin main"
