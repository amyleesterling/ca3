#!/usr/bin/env python3
"""Pack the patch's meshes into one small file for an interactive viewer.

    python3 eyewire2/pack_viewer.py MESHDIR OUTDIR [--faces 2000]

Reads MESHDIR/index.json and the GLBs fetch_meshes.py wrote, leaves out the same
strays col3d.html does (a soma far outside the patch, or branches reaching well past
it), decimates each cell to about --faces triangles, and writes
  OUTDIR/bipolars.bin   positions as uint16 within the patch's bounding box, then
                        triangle indices as uint16, cell after cell
  OUTDIR/bipolars.json  the box, and per cell: segid, type, proofreader and where
                        its positions and indices sit in the .bin
"""
import argparse, json, math, os, sys
import numpy as np, trimesh

ap = argparse.ArgumentParser()
ap.add_argument("meshdir"); ap.add_argument("outdir")
ap.add_argument("--faces", type=int, default=2000)
a = ap.parse_args()
idx = json.load(open(os.path.join(a.meshdir, "index.json")))["cells"]
cells = []
for c in idx:
    p = os.path.join(a.meshdir, c["segid"] + ".glb")
    if not os.path.exists(p): continue
    tm = list(trimesh.load(p, force="scene").geometry.values())[0]
    cells.append((c, tm))
cx = np.mean([c["soma_um"][0] for c, _ in cells]); cy = np.mean([c["soma_um"][1] for c, _ in cells])
d = np.array([math.hypot(c["soma_um"][0] - cx, c["soma_um"][1] - cy) for c, _ in cells])
R = np.sort(d)[int(0.98 * (len(d) - 1))]
keep = []
for (c, tm), dist in zip(cells, d):
    lo, hi = tm.bounds
    reach = max(math.hypot(x - cx, y - cy) for x in (lo[0], hi[0]) for y in (lo[1], hi[1]))
    if dist > R * 1.15 or reach > R + 22: continue
    if len(tm.faces) > a.faces * 1.1:
        tm = tm.simplify_quadric_decimation(face_count=a.faces)
    tm.remove_unreferenced_vertices()
    keep.append((c, tm))
print(f"{len(keep)} of {len(cells)} cells kept", file=sys.stderr)
allv = np.vstack([tm.vertices for _, tm in keep])
lo, hi = allv.min(0), allv.max(0)
pos, ind, meta, vo, io = [], [], [], 0, 0
for c, tm in keep:
    v = np.round((tm.vertices - lo) / (hi - lo) * 65535).astype("<u2")
    f = tm.faces.astype("<u2"); assert len(tm.vertices) < 65536
    pos.append(v.ravel()); ind.append(f.ravel())
    meta.append({"segid": c["segid"], "type": c["type"] or "", "proofreader": c["proofreader"],
                 "v": [vo, len(tm.vertices)], "i": [io, len(tm.faces) * 3]})
    vo += len(tm.vertices); io += len(tm.faces) * 3
os.makedirs(a.outdir, exist_ok=True)
P = np.concatenate(pos); I = np.concatenate(ind)
with open(os.path.join(a.outdir, "bipolars.bin"), "wb") as f:
    f.write(P.tobytes()); f.write(I.tobytes())
json.dump({"box": [lo.round(3).tolist(), hi.round(3).tolist()], "positions": int(P.size), "indices": int(I.size),
           "soma_centre": [round(cx, 2), round(cy, 2)], "cells": meta},
          open(os.path.join(a.outdir, "bipolars.json"), "w"), separators=(",", ":"))
print(f"{P.nbytes/1e6:.1f} MB positions + {I.nbytes/1e6:.1f} MB indices", file=sys.stderr)
