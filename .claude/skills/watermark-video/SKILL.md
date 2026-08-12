---
name: watermark-video
description: Burn a small text watermark (a domain or handle) into the bottom corner of video files, without changing their file size or resolution. Use when asked to watermark, brand, or add a credit to videos, or to protect clips from being reposted uncredited.
---

# Watermarking video

Burns a text mark into every frame of a set of clips. Written from doing it to
the sixteen clips in this repo; every number here is one that was measured
rather than guessed, and the failures are recorded next to the fixes so they
are not repeated.

## Before touching anything, ask

**Never assume the mark's text.** Ask the user to confirm, and wait for an
answer:

1. **What the mark says** — a domain (`pyr.ai`), a handle (`@amyneurons`), or a
   name. Do not infer it from the repo name, the CNAME, or the site's own
   branding. A repo can serve one domain and credit another, and this repo does
   exactly that: the site is `amyleesterling.github.io/ca3` and the mark reads
   `pyr.ai`.
2. **How loud** — see the opacity table below. The difference between 11% and
   50% is the difference between a credit and a caption, and it is not
   recoverable without a full re-encode, so it is worth one question.

Also confirm, if there is any doubt, that **the footage is the user's to mark**.
Watermarking someone else's clip with your own domain is a false claim of
authorship. Stock footage, collaborators' renders and dataset-supplied video
are all cases to ask about rather than assume.

## Opacity

White text, measured off a real H.264 encode against a black background:

| opacity | peak luma | reads as |
|---|---|---|
| 0.11 | ~38/255 | nearly invisible; attribution only, will not deter anyone |
| 0.18 | ~63/255 | faint but findable |
| 0.35 | ~90/255 | clearly present, still quiet |
| 0.50 | ~128/255 | unmistakable; what this repo uses |

Anything below about 0.10 risks being crushed entirely by the encoder in dark
scenes. Whatever the opacity, put a dark shadow under the text at `opacity *
0.65` with blur `fontSize * 0.22`: white alone disappears against bright frames,
and the shadow leaves a readable ghost there instead.

## Placement

Bottom-right, sized as a **fraction of frame height**, never a pixel count:

- mark image height: `round(frameHeight * 0.045)`
- margin from the right and bottom edges: `round(frameHeight * 0.02)`

A set of clips usually mixes aspect ratios — this one has 1920×1080, 720×1280
and 1080×1920 — and a fixed pixel size looks wrong on the portrait cuts.

Use **one corner for every clip**. Sampling peak brightness in all four corners
across all sixteen clips here found that every corner is bright in at least one
clip, so collision is unavoidable; a fixed position reads as deliberate where a
per-clip position reads as an accident. Bottom-left is the worst choice, as
burned-in titles tend to live there.

To check the corners of a new set:

```bash
# peak luma in one corner across a whole clip; run per corner, per clip
ffmpeg -v error -i clip.mp4 \
  -vf "select='not(mod(n,6))',crop=iw*0.18:ih*0.09:iw*0.80:ih*0.89,scale=60:30" \
  -vsync 0 -f rawvideo -pix_fmt gray - | python3 -c \
  "import sys; d=sys.stdin.buffer.read(); print('peak', max(d))"
```

## The font must be a real file

**Do not pass a CSS font stack to a renderer.** A stack like
`ui-sans-serif, -apple-system, "Segoe UI", Roboto, sans-serif` is correct in a
stylesheet, where the reader's own machine supplies the font, and wrong here,
where the font must exist on the machine drawing the frame. On Linux none of
those exist and it falls silently through to DejaVu Sans — no warning, just the
wrong typeface. That happened here and shipped before it was caught.

Fetch the font explicitly and **assert it loaded** by comparing metrics against
the fallback:

```bash
css=$(curl -s -A "Mozilla/5.0" "https://fonts.googleapis.com/css2?family=Roboto:wght@500")
curl -sL -o Roboto.ttf "$(echo "$css" | grep -o 'https://fonts.gstatic.com/[^)]*' | head -1)"
```

Roboto is Apache 2.0, so embedding it in rendered output is fine. Check any
other font's licence before shipping frames that contain it.

Render the mark to a transparent PNG once, then scale it per clip. Serve the
font over `http://localhost` rather than `file://`, which Chromium blocks:

```js
await page.addStyleTag({ content:
  `@font-face{font-family:'M';src:url('/fonts/Roboto.ttf') format('truetype');font-weight:500;}` });
await page.evaluate(() => document.fonts.load("500 160px M"));
// assert: a different width from the fallback proves the font actually loaded
const ok = await page.evaluate(() => {
  const c = document.createElement('canvas').getContext('2d');
  c.font = '500 160px M';             const a = c.measureText('pyr.ai').width;
  c.font = '500 160px "DejaVu Sans"'; return a !== c.measureText('pyr.ai').width;
});
if (!ok) throw new Error('font fell back — do not encode');
```

Draw at a large size (160px) and let ffmpeg scale down; letter-space by about
`fontSize * 0.06`, applied per character, since canvas has no `letterSpacing`.

## Encode: match the bitrate, do not pick a quality

This is the part that costs money if you get it wrong. A CRF encode targets a
quality level, and re-encoding already-lossy video at high quality **inflates
it** — the largest clip here went from 17 MB to 24–29 MB at CRF 17–19, which is
real data on a phone.

Two-pass at each clip's own average bitrate holds the size instead:

```bash
BR=$(python3 -c "print(int($(stat -c%s in.mp4) * 8 / $DURATION / 1000))")
MH=$(python3 -c "print(round($H * 0.045))")
M=$(python3 -c "print(round($H * 0.02))")
FC="[1:v]scale=-1:$MH:flags=lanczos[wm];[0:v][wm]overlay=W-w-$M:H-h-$M"

ffmpeg -i in.mp4 -i mark.png -filter_complex "$FC" \
  -c:v libx264 -b:v ${BR}k -preset medium -pix_fmt yuv420p \
  -pass 1 -passlogfile pl -an -f null /dev/null -y
ffmpeg -i in.mp4 -i mark.png -filter_complex "$FC" \
  -c:v libx264 -b:v ${BR}k -preset medium -pix_fmt yuv420p \
  -pass 2 -passlogfile pl -movflags +faststart -an out.mp4 -y
```

Drop `-an` if the clip has audio, and add `-c:a copy` instead. For VP9/WebM
sources, swap `libx264` for `libvpx-vp9` and keep the same two-pass structure.

Result on this repo: 100.1 MB in, 99.9 MB out, SSIM 0.976–0.999.

## Never re-encode an already-marked file

Once a mark has shipped, the files in the tree are the marked ones. Encoding
from those stacks a second mark on the first and puts every clip through
another generation of lossy compression. Recover the originals from git and
encode from those:

```bash
git log --oneline -- video/            # find the commit before the mark landed
git show <commit>:video/clip.mp4 > /tmp/orig/clip.mp4
```

Then prove they are bare before using them — peak luma in the mark's own box
should be near zero on a clip with a dark corner:

```bash
ffmpeg -v error -ss 5 -i /tmp/orig/clip.mp4 -frames:v 1 \
  -vf "crop=$MW:$MH:$X:$Y" -f rawvideo -pix_fmt gray - | python3 -c \
  "import sys; d=sys.stdin.buffer.read(); print('peak', max(d))"
```

## Verify before shipping

Check every clip, not a sample. Four things:

1. **The mark is there.** Mean luma inside the mark's box, marked vs original,
   must rise. Expect roughly +8 at opacity 0.50, +1.7 at 0.11. Do **not** test
   with peak brightness — on a clip whose corner already holds bright content
   the peak does not move, and it will read as a failure when the mark is fine.
2. **Nothing else moved.** Resolution, frame rate and duration identical.
3. **Size held.** Total within a couple of percent; no clip over +10%.
4. **It is legible.** Extract the mark box from each clip and look at all of
   them together. At low opacity, amplify with
   `format=gray,lut=y='min(255,val*6)'` — `eq=brightness=` is unreliable for
   this. A clip whose corner sits on bright content will look blown out under
   amplification even though the mark is correctly applied; trust the numeric
   check there.

```bash
ffmpeg -v error -i marked.mp4 \
  -vf "select='not(mod(n,5))',crop=$MW:$MH:$X:$Y" -vsync 0 \
  -f rawvideo -pix_fmt gray - | python3 -c \
  "import sys; d=sys.stdin.buffer.read(); print('mean', sum(d)/len(d))"
```

## Two things this does not do

A burned-in mark is **attribution, not protection**. It travels with a reposted
file, which is its whole value. It will not stop anyone who wants it gone —
cropping it takes seconds. Say so plainly rather than implying the clips are now
safe.

And it does nothing for the **stills**, which are a separate job — no re-encode
needed, so it is much quicker. Check them too: in this repo three images carry a
PYR logo and thirty-five carry nothing, which is the kind of inconsistency worth
surfacing.
