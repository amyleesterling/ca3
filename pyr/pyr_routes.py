#!/usr/bin/env python3
"""Teach pyr.ai's Flask app to serve the mirrored site at /gallery/.

    python3 pyr/pyr_routes.py /path/to/pyr-homepage-static          # patch main.py
    python3 pyr/pyr_routes.py /path/to/pyr-homepage-static --nav    # uncomment the nav link

main.py renders templates for the routes it knows and answers every other path
with the home page, so a folder dropped into the repo is invisible until it is
routed. This swaps the FlyWire gallery route to /gallery-flywire and adds two
routes that serve static/gallery/ at /gallery/. The rule ends in a slash on
purpose: every URL in the mirrored site is relative, and Flask redirects a
bare /gallery to /gallery/ on its own. Both edits are exact-match replacements,
idempotent, and refuse to guess if the source has moved on.
"""
import glob
import os
import sys

pyr = sys.argv[1]

OLD_ROUTE = '''@app.route("/gallery", methods=["GET"])
def gallery():
    return render_template("gallery.html", discover_items=DISCOVER_ITEMS)
'''
NEW_ROUTE = '''@app.route("/gallery-flywire", methods=["GET"])
def gallery_flywire():
    return render_template("gallery.html", discover_items=DISCOVER_ITEMS)


# The CA3 renderings site, mirrored whole into static/gallery/ by
# amyleesterling/ca3's pyr/mirror.sh. Edit it there, not here. Every URL in it
# is relative, so /gallery must carry its trailing slash: Flask redirects
# /gallery to /gallery/ on its own because the rule ends in one.
_GALLERY = os.path.join(app.root_path, "static", "gallery")


@app.route("/gallery/", methods=["GET"])
def gallery():
    return send_from_directory(_GALLERY, "index.html")


@app.route("/gallery/<path:filename>", methods=["GET"])
def gallery_file(filename):
    return send_from_directory(_GALLERY, filename)
'''

OLD_NAV = '<!-- <a href="/gallery" class="w3-bar-item w3-button"> GALLERY</a> -->'
NEW_NAV = '<a href="/gallery" class="w3-bar-item w3-button"> GALLERY</a>'


def patch_routes():
    p = os.path.join(pyr, "main.py")
    s = open(p, encoding="utf-8").read()
    if NEW_ROUTE in s:
        print("main.py: /gallery routes already in place")
    elif OLD_ROUTE in s:
        open(p, "w", encoding="utf-8").write(s.replace(OLD_ROUTE, NEW_ROUTE))
        print("main.py: /gallery now serves static/gallery; FlyWire page moved to /gallery-flywire")
    else:
        sys.exit("main.py: the /gallery route does not look as expected; refusing to guess")


def patch_nav():
    n = 0
    for f in glob.glob(os.path.join(pyr, "templates", "**", "*.html"), recursive=True):
        s = open(f, encoding="utf-8").read()
        if OLD_NAV in s:
            open(f, "w", encoding="utf-8").write(s.replace(OLD_NAV, NEW_NAV))
            n += 1
    print(f"nav: GALLERY link uncommented in {n} template(s)")


if "--nav" in sys.argv:
    patch_nav()
else:
    patch_routes()
