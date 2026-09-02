#!/usr/bin/env sh
# Build the Seung Lab variant into seunglab/ for a live preview on this site.
# The <base href="../"> makes the copy borrow every image, film and page from
# the real site, so the folder holds one HTML file and nothing else.
set -eu
HERE=$(cd "$(dirname "$0")/.." && pwd)
python3 "$HERE/pyr/seunglab.py" "$HERE" "$HERE/seunglab" --base ../
