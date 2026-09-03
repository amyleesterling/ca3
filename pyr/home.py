#!/usr/bin/env python3
"""Build the phone-friendly pyr.ai home page.

    python3 pyr/home.py preview          # fetch https://pyr.ai/, write pyr-home/index.html
    python3 pyr/home.py patch DIR        # patch DIR/templates/index.html in a pyr checkout

Both modes make the same change: pyr/home_mobile.css is inlined after the
pyr.css link. Preview mode also points every root-relative asset at pyr.ai so
the page renders from this site. Patch mode edits the Flask template in place,
replacing an earlier injection if one is there, so it is safe to run again.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, "home_mobile.css"), encoding="utf-8").read()
MARK_A, MARK_B = "<!-- mobile landing: begin -->", "<!-- mobile landing: end -->"
BLOCK = f"{MARK_A}\n<style>\n{CSS}</style>\n{MARK_B}"
# The sheet goes in just before </head>: after pyr.css however the template
# spells that link (the rendered page and the Jinja source differ), and before
# the body's own hero <style>, which the hero selectors outrank by id.
ANCHOR = "</head>"


def inject(html):
    html = re.sub(r"\n?" + re.escape(MARK_A) + r".*?" + re.escape(MARK_B) + r"\n?", "", html, flags=re.S)
    assert html.count(ANCHOR) == 1, "</head> not found exactly once"
    return html.replace(ANCHOR, BLOCK + "\n" + ANCHOR)


mode = sys.argv[1]
if mode == "preview":
    html = subprocess.run(["curl", "-sL", "--max-time", "60", "https://pyr.ai/"],
                          check=True, capture_output=True, text=True).stdout
    html = inject(html)
    html = re.sub(r'(src|href)="/(assets/|pyr\.css|marked\.min\.js)', r'\1="https://pyr.ai/\2', html)
    html = re.sub(r'url\("/assets/', 'url("https://pyr.ai/assets/', html)
    html = html.replace('src="./marked.min.js"', 'src="https://pyr.ai/marked.min.js"')
    # site-relative page links keep working from the preview by pointing home
    html = re.sub(r'href="/(consortium|ca3_access|gallery|principles|tos|about|apps|for_media)"',
                  r'href="https://pyr.ai/\1"', html)
    html = re.sub(r'href="(principles|tos|guidelines)"', r'href="https://pyr.ai/\1"', html)
    out = os.path.join(HERE, "..", "pyr-home", "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    print(f"preview -> {os.path.normpath(out)} ({len(html)} bytes)")
elif mode == "patch":
    p = os.path.join(sys.argv[2], "templates", "index.html")
    html = open(p, encoding="utf-8").read()
    new = inject(html)
    open(p, "w", encoding="utf-8").write(new)
    print(f"patched {p}" if new != html else f"{p} already current")
else:
    sys.exit(__doc__)
