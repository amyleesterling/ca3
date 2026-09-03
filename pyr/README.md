# The Seung Lab version, at pyr.ai/gallery

pyr.ai/gallery is this site, mirrored whole, with a few deliberate differences
for the lab's audience. Every difference is one literal replacement in
`seunglab.py`, asserted against the source, so a change here that moves an
anchor fails the build loudly instead of shipping the unmodified page.

What differs, today:

- the header's triangle count gives way to the mossy fibers traced, and the
  wordmark, top hairline and eyebrow rail take after the scifi-ui masthead
- "Overnight renders" is "Renders", the making-of paragraph is gone, and each
  caption in that section reads as a title with its explainer under it
- on the single cell, the triangle count becomes synapses per fiber

**Preview** the variant on this site, built by `sh pyr/preview.sh` into
`seunglab/` (one HTML file that borrows all media from the real site):
https://amyleesterling.github.io/ca3/seunglab/

**Ship** it to pyr.ai without a terminal: the GitHub Action
`.github/workflows/mirror-pyr.yml` runs the mirror on every change to this
site's main branch, and on demand from the Actions tab ("Mirror to pyr.ai" >
"Run workflow"). It needs one secret, `PYR_TOKEN`: a GitHub token from an
account that can push to `seung-lab/pyr-homepage-static`, added under this
repo's Settings > Secrets and variables > Actions. Until that secret exists
the job stops with a note instead of failing.

A fine-grained token for an organisation repo is not usable until an owner of
that organisation approves it: the button reads "Generate token and request
access", and until approval every clone fails with "Write access to repository
not granted", even for reads. Owners approve under the org's Settings > Personal
access tokens > Pending requests. The one in use expires after 30 days; a fresh
token in the same secret restarts the mirror.

Or from a machine with both repos checked out
(`seung-lab/pyr-homepage-static`, main branch deploys):

    sh pyr/mirror.sh ../pyr-homepage-static
    cd ../pyr-homepage-static && git commit -m "Mirror the CA3 renderings site at /gallery" && git push origin main

## The home page on a phone

pyr.ai's front page was composed for a wide screen. `home_mobile.css` is a
phone-only layout for it (everything under one `max-width: 600px` query, so
desktop is untouched): the hero keeps the desktop composition turned upright,
text at the top over a veil, the cells filling the lower half, the same white
fade at the foot; the rows below stack picture over text instead of squeezing
both into half a phone. `home.py preview` fetches the live page, inlines that
sheet and writes `pyr-home/index.html` for a live preview at
https://amyleesterling.github.io/ca3/pyr-home/. `home.py patch DIR` inlines the
same sheet into `templates/index.html` of a pyr checkout, and the Action
`.github/workflows/pyr-home-branch.yml` does that on every change here and
pushes the result to the branch `ca3/mobile-landing` of pyr's repo. Nothing
touches pyr's main: opening the pull request from that branch is a person's
call, at https://github.com/seung-lab/pyr-homepage-static/compare/main...ca3/mobile-landing.

## How the mirror works

pyr.ai is a Flask app, not a static host: `main.py` renders a template for each
route it knows and answers every other path with the home page, so a folder
dropped into the repo is invisible until it is routed. `mirror.sh` therefore
copies `*.html`, `favicon.ico`, `images/`, `video/` and `web/` into
`static/gallery/`, applies `seunglab.py` to the front page there, and runs
`pyr_routes.py`, which moves the old FlyWire gallery route to `/gallery-flywire`,
adds two routes serving the folder at `/gallery/` (Flask redirects a bare
`/gallery` to the slash on its own, which matters because every URL in the site
is relative), and uncomments the GALLERY link in the nav of every template. Both
edits are exact-match and idempotent; if `main.py` no longer looks as expected
the script stops rather than guess. Checked against a stub of the app: `/gallery`
308s to `/gallery/`, pages and media serve with the right types, a film answers a
range request with 206, and the catch-all still serves the home page.
