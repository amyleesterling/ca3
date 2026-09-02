# pyr.ai/gallery is this site

The gallery page on pyr.ai is a verbatim mirror of this repository: the same
pages, images, films and 3D block, served from `pyr.ai/gallery/`. Nothing is
adapted, because every URL here is relative.

`mirror.sh` does the copy into a checkout of `seung-lab/pyr-homepage-static`
(its **main** branch deploys pyr.ai):

    sh pyr/mirror.sh ../pyr-homepage-static
    cd ../pyr-homepage-static && git commit -m "Mirror the CA3 renderings site at /gallery" && git push origin main

It moves the old FlyWire gallery page aside as `gallery-flywire.html` so the
directory index wins at `/gallery`, then rsyncs `*.html`, `favicon.ico`,
`images/`, `video/` and `web/` into `gallery/`. Re-run it after any change here.

Two things it does not do, on purpose: it does not touch pyr's navigation (the
GALLERY link there is commented out in every page's nav; uncomment it when the
mirror lands), and it does not copy `.claude/`, `pyr/` or the git history.
