#!/usr/bin/env python3
"""Build the pyr.ai (Seung Lab) variant of this site from the source pages.

    python3 pyr/seunglab.py SRC_DIR OUT_DIR [--base ../]

The variant is this site with a handful of deliberate differences, each one a
literal replacement below. Every anchor is asserted, so if the source drifts
the build fails here rather than silently shipping the unmodified page.
--base inserts a <base href> so a preview build can live in a subfolder and
still pull media from the real site; the pyr mirror does not use it.
"""
import re, sys, os

src_dir, out_dir = sys.argv[1], sys.argv[2]
base = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else None
s = open(os.path.join(src_dir, "index.html"), encoding="utf-8").read()

def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, f"anchor found {n}x, expected {count}: {a[:70]!r}"
    s = s.replace(a, b)

# -- the link card: this copy lives at pyr.ai/gallery, so the card says so and the image
#    is served from there (mirror.sh copies og.jpg alongside the pages) ----------------------
rep('<meta property="og:url" content="https://amyleesterling.github.io/ca3/">',
    '<meta property="og:url" content="https://pyr.ai/gallery/">')
rep('content="https://amyleesterling.github.io/ca3/og.jpg"',
    'content="https://pyr.ai/gallery/og.jpg"', count=2)

# -- Renders: a title, no making-of paragraph, captions as title + explainer ------------
rep('''  <h2>Overnight renders</h2>
  <p>Rendered on one workstation in a single night, 103 minutes of GPU time for
  the four pieces below. The two widescreen masters also replace their vertical
  cuts further down this page when you are on a wide screen.</p>
''', '''  <h2>Renders</h2>
''')
head, sect, tail = re.split(r'(?=<h2>Renders</h2>)|(?=  <h2>Watch it assemble</h2>)', s, maxsplit=2)
def caption(m):
    title, body = m.group(1).rstrip('.'), m.group(2).strip()
    # a leading "Eighteen seconds." becomes a duration mark beside the title
    d = re.match(r'((?:[A-Z][a-z]+ ){1,2}seconds)\.\s+', body)
    if d:
        title += f' <em class="fd">{d.group(1).lower()}</em>'
        body = body[d.end():]
    return f'<figcaption><span class="ft">{title}</span><span class="fx">{body}</span></figcaption>'
sect, n = re.subn(r'<figcaption><b>([^<]+)</b>\s*(.*?)</figcaption>', caption, sect, flags=re.S)
assert n == 6, f"expected 6 captions in the Renders section, rewrote {n}"
s = head + sect + tail

# -- the single cell: a scientific stat where the triangle count was ---------------------
rep('''        <p class="d">mossy fiber synapses, and they arrive from only <b>6</b> fibers.
        A single terminal makes dozens of contacts on one thorn.</p>''',
    '''        <p class="d">mossy fiber synapses, and they arrive from only <b>6</b> fibers.</p>''')
rep('''        <p class="k">reconstructed at</p>
        <p class="v">4.5M</p>
        <p class="d">triangles, with no simplification applied, which is why the
        thorny excrescences hold their shape this close up.</p>''',
    '''        <p class="k">per fiber, on average</p>
        <p class="v">27</p>
        <p class="d">synapses. A mossy fiber does not touch a cell once: its terminal
        wraps a single thorn and makes dozens of contacts there.</p>''')
rep('data-hud="4.5M triangles"', 'data-hud="182 thorny cells"')
# the header's stats row now carries the volume's cell counts on both versions, so
# only the figure mark keeps a triangle count to swap
rep('data-hud="982 cells · 124M triangles"', 'data-hud="982 cells · 25,723 synapses"')

# -- the header, after the scifi-ui masthead: a lit wordmark, a hairline that runs wider
#    on hover, and an eyebrow rail that starts to travel -----------------------------------
rep('''</style>''', '''
  /* ---- seung lab variant ------------------------------------------------- */
  .ft { display: block; color: var(--ink); font-weight: 500; font-size: 17px;
        letter-spacing: -.012em; line-height: 1.3; margin: 0 0 6px; }
  .ft .fd { font-style: normal; font-weight: 400; font-size: 10.5px; letter-spacing: .14em;
            text-transform: uppercase; color: var(--faint); margin-left: 8px;
            vertical-align: 2px; white-space: nowrap; }
  .fx { display: block; }
  .heropanel h1 {
    background: linear-gradient(100deg, #6FB0FF 0%, #EAF4FF 26%, #BBDBFF 46%,
      #64A6EE 68%, #A6D2FF 100%);
    background-size: 220% 100%;
    -webkit-background-clip: text; background-clip: text;
    color: transparent; -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 2px 14px rgba(74,150,240,.38));
    animation: wordmark-sheen 9s ease-in-out infinite;
  }
  @keyframes wordmark-sheen { 0%, 100% { background-position: 0% 0; } 50% { background-position: 100% 0; } }
  .heropanel::before {
    transition: left 620ms cubic-bezier(.16,1,.3,1), right 620ms cubic-bezier(.16,1,.3,1),
                box-shadow 420ms ease;
  }
  .heropanel:hover::before, .heropanel:focus-within::before {
    left: 2%; right: 2%; box-shadow: 0 0 14px rgba(150,212,255,.85);
  }
  .heropanel:hover .heroeyebrow u, .heropanel:focus-within .heroeyebrow u {
    animation: holo-eyebrow-run 900ms linear infinite;
  }
  .heropanel:hover .heroeyebrow s, .heropanel:focus-within .heroeyebrow s {
    animation: holo-eyebrow-blip 1400ms ease-in-out infinite;
  }
  @keyframes holo-eyebrow-run { to { background-position: -7px 0; } }
  @keyframes holo-eyebrow-blip {
    0%, 100% { box-shadow: 0 0 8px rgba(120,205,255,.9); }
    50%      { box-shadow: 0 0 15px rgba(150,225,255,1); }
  }
  @media (prefers-reduced-motion: reduce) {
    .heropanel h1 { animation: none; background-position: 0 0; }
    .heropanel::before { transition: none; }
    .heropanel:hover .heroeyebrow u, .heropanel:hover .heroeyebrow s,
    .heropanel:focus-within .heroeyebrow u, .heropanel:focus-within .heroeyebrow s { animation: none; }
  }
</style>''')

if base:
    assert 'href="#' not in s, "in-page anchors break under <base>; rewrite them first"
    rep('<head>', f'<head>\n<base href="{base}">')

os.makedirs(out_dir, exist_ok=True)
open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(s)
print(f"seung lab variant -> {os.path.join(out_dir, 'index.html')} ({len(s)} bytes)")
