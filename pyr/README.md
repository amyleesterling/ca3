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

**Ship** it to pyr.ai from a machine with both repos checked out
(`seung-lab/pyr-homepage-static`, main branch deploys):

    sh pyr/mirror.sh ../pyr-homepage-static
    cd ../pyr-homepage-static && git commit -m "Mirror the CA3 renderings site at /gallery" && git push origin main

`mirror.sh` copies `*.html`, `favicon.ico`, `images/`, `video/` and `web/` into
`gallery/`, applies `seunglab.py` to the front page there, and moves pyr's old
FlyWire gallery page aside as `gallery-flywire.html` so the directory index wins
at `/gallery`. It does not touch pyr's navigation: the GALLERY link is commented
out in every page's nav there and wants uncommenting when the mirror lands.
