# pyr.ai gallery, staged

`gallery.html` is a drop-in for the **main** branch of `seung-lab/pyr-homepage-static`
(the branch that deploys pyr.ai), replacing the existing `/gallery` page. It keeps
that page's FlyWire sections and adds a CA3 section on top: the Nature Neuroscience
September 2026 cover, the citation, the live 3D block, and the renders and films
from this repo, all loaded from `amyleesterling.github.io/ca3` so no media needs
copying. It also re-enables the GALLERY link in both navs, which was commented out.

Preview: https://amyleesterling.github.io/ca3/pyr/gallery.html

To ship: copy `gallery.html` over the pyr repo's gallery page, and add the cover
scan at `assets/natneuro-2026-09-cover.jpg` (until it exists the cover artwork
stands in). Asset URLs are absolute (`https://pyr.ai/assets/...`) so the file
renders identically from either host.

This folder can be deleted once the page is live on pyr.ai.
