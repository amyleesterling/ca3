#!/usr/bin/env sh
# Mirror this site into the pyr.ai repository as /gallery/.
#
#   sh pyr/mirror.sh /path/to/pyr-homepage-static
#
# Copies the site (pages, images, video, the 3D assets) into <pyr>/gallery/,
# then applies the Seung Lab variant (pyr/seunglab.py) to the front page. Every
# URL in the site is relative, so nothing else is rewritten. A preview of the
# variant is built into seunglab/ in this repo: sh pyr/preview.sh
# Run it again after any change here and commit the result on pyr's main branch,
# which is the branch that deploys pyr.ai. The GitHub Action in
# .github/workflows/mirror-pyr.yml does exactly this on every change to main.
set -eu
PYR=${1:?usage: sh pyr/mirror.sh /path/to/pyr-homepage-static}
HERE=$(cd "$(dirname "$0")/.." && pwd)
[ -d "$PYR/.git" ] || { echo "not a git checkout: $PYR" >&2; exit 1; }

# The old /gallery page (FlyWire renders) would shadow the directory index on a
# host that serves gallery.html for /gallery. Keep it, one name over.
if [ -f "$PYR/gallery.html" ]; then
  git -C "$PYR" mv -k gallery.html gallery-flywire.html 2>/dev/null || mv "$PYR/gallery.html" "$PYR/gallery-flywire.html"
  echo "moved gallery.html -> gallery-flywire.html"
fi

# a clean copy every time, so a file deleted here is deleted there too
rm -rf "$PYR/gallery"
mkdir -p "$PYR/gallery"
cp "$HERE"/*.html "$HERE/favicon.ico" "$PYR/gallery/"
cp -R "$HERE/images" "$HERE/video" "$HERE/web" "$PYR/gallery/"
# the Seung Lab version differs from this site in a few deliberate places;
# seunglab.py holds every one of them
python3 "$HERE/pyr/seunglab.py" "$PYR/gallery" "$PYR/gallery"

# The GALLERY link is commented out in every page's nav on pyr.ai. Uncomment it,
# exactly that markup and nothing else, so the mirror is reachable. A no-op once
# it has been done.
python3 - "$PYR" <<'PY'
import glob, os, sys
old = '<!-- <a href="/gallery" class="w3-bar-item w3-button"> GALLERY</a> -->'
new = '<a href="/gallery" class="w3-bar-item w3-button"> GALLERY</a>'
n = 0
for f in glob.glob(os.path.join(sys.argv[1], '*.html')):
    s = open(f, encoding='utf-8').read()
    if old in s:
        open(f, 'w', encoding='utf-8').write(s.replace(old, new)); n += 1
print(f"nav: GALLERY link uncommented in {n} page(s)")
PY

git -C "$PYR" add -A
echo "staged in $PYR: $(git -C "$PYR" diff --cached --stat | tail -1)"
echo "next: cd $PYR && git commit -m 'Mirror the CA3 renderings site at /gallery' && git push origin main"
