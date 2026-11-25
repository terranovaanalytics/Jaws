#!/usr/bin/env python3
"""Turn photos of kids' drawings into colored paper-cutout sprites.

    python3 tools/cutout.py kids/jellyman

Reads <story>/drawings/NN.jpg and the CUTOUTS table in <story>/story.py, writes
<story>/cutouts/NN.png: RGBA, the kid's pen lines kept (darkened), closed shapes
filled with the character's color, a white paper border round the silhouette,
transparent outside. Blender scenes stand these up as flat puppets.

How: the paper's brightness is estimated locally (big blur) so hand shadows and
the book's gutter don't count as ink; ink = clearly darker than its local
paper, or clearly colored. Small specks and far-off marks are dropped, closed
shapes are filled, then the whole figure gets a sticker border.
"""
import importlib.util
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as ndi


def load_story(path):
    spec = importlib.util.spec_from_file_location("story", os.path.join(path, "story.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def cutout(src, cfg, size=900):
    im = Image.open(src).convert("RGB")
    if cfg.get("rotate"):
        im = im.rotate(cfg["rotate"], expand=True)
    im.thumbnail((size, size), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    gray = 0.3 * r + 0.59 * g + 0.11 * b
    bg = ndi.median_filter(gray[::4, ::4], size=15)
    bg = ndi.zoom(bg, (gray.shape[0] / bg.shape[0], gray.shape[1] / bg.shape[1]), order=1)
    bg = bg[:gray.shape[0], :gray.shape[1]]
    dark = (bg - gray) / np.maximum(bg, 0.05)
    mx, mn = a.max(-1), a.min(-1)
    sat = (mx - mn) / np.maximum(mx, 1e-3)
    skin = (r > g + 0.06) & (r > b + 0.08)              # fingers holding the page
    ink = ((dark > cfg.get("thresh", 0.22)) | ((sat > 0.28) & (dark > 0.08))) & ~skin
    ink = ndi.binary_opening(ink, disk(1))
    # the book's gutter / page edges: long, nearly vertical straight lines
    H, W = ink.shape
    wide = ndi.binary_dilation(ink, np.ones((1, 9), bool))
    vert = ndi.binary_opening(wide, np.ones((int(H * cfg.get("gutter", 0.3)), 1), bool))
    ink &= ~ndi.binary_dilation(vert, np.ones((1, 15), bool))
    # keep the drawing: the biggest stroke group, plus the small marks (eyes,
    # mouths) that sit inside its box
    grp, n = ndi.label(ndi.binary_dilation(ink, disk(9)))
    if n:
        sizes = ndi.sum(ink, grp, range(1, n + 1))
        main = int(np.argmax(sizes)) + 1
        sl = ndi.find_objects(grp)
        my, mx_ = sl[main - 1]
        mh, mw = my.stop - my.start, mx_.stop - mx_.start
        keep = []
        for i, (sy, sx) in enumerate(sl):
            cy, cx = (sy.start + sy.stop) / 2, (sx.start + sx.stop) / 2
            near = (my.start - 0.1 * mh < cy < my.stop + 0.1 * mh and
                    mx_.start - 0.1 * mw < cx < mx_.stop + 0.1 * mw)
            if i + 1 == main or (near and sizes[i] > 0.004 * sizes.max()):
                keep.append(i + 1)
        ink &= np.isin(grp, keep)
    for box in cfg.get("erase", []):                     # (x0, y0, x1, y1) fractions
        h, w = ink.shape
        ink[int(box[1] * h):int(box[3] * h), int(box[0] * w):int(box[2] * w)] = False
    ys, xs = np.nonzero(ink)
    pad = 30
    y0, y1 = max(0, ys.min() - pad), min(ink.shape[0], ys.max() + pad)
    x0, x1 = max(0, xs.min() - pad), min(ink.shape[1], xs.max() + pad)
    ink = ink[y0:y1, x0:x1]
    a = a[y0:y1, x0:x1]
    # bolder, smoother line: thicken a touch
    line = ndi.binary_dilation(ink, disk(cfg.get("bold", 2)))
    closed = ndi.binary_closing(line, disk(cfg.get("close", 4)))
    filled = ndi.binary_fill_holes(closed)
    inside = filled & ~line
    sil = filled | line
    border = ndi.binary_dilation(sil, disk(cfg.get("border", 11)))
    border = ndi.binary_fill_holes(border)
    h, w = ink.shape
    out = np.zeros((h, w, 4), np.float32)
    out[border] = (1.0, 0.98, 0.94, 1.0)                 # paper edge
    fill = np.array(cfg["color"], np.float32)
    out[inside, :3] = fill
    out[inside, 3] = 1.0
    ink_col = np.array(cfg.get("ink", (0.06, 0.09, 0.12)), np.float32)
    out[line, :3] = ink_col
    out[line, 3] = 1.0
    top = np.zeros_like(sil)
    if cfg.get("top_color"):                             # e.g. carrot leaves
        top[:int(cfg["top_split"] * h)] = True
        tc = np.array(cfg["top_color"], np.float32)
        out[top & inside, :3] = tc
        out[top & line, :3] = tc * 0.45
    if cfg.get("solid"):                                 # colored-in drawing: strokes become fill
        out[line & ~top, :3] = fill
        if cfg.get("top_color"):
            out[line & top, :3] = tc
        edge = sil & ~ndi.binary_erosion(sil, disk(3))
        out[edge, :3] = ink_col
    if cfg.get("fill_alpha"):                            # see-through (force field)
        out[inside, 3] = cfg["fill_alpha"]
    out[..., 3] = ndi.gaussian_filter(out[..., 3], 0.8)  # soft edge
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), "RGBA")


def main():
    story = os.path.abspath(sys.argv[1])
    cfgs = load_story(story).CUTOUTS
    os.makedirs(os.path.join(story, "cutouts"), exist_ok=True)
    only = sys.argv[2:]
    for key, cfg in cfgs.items():
        if only and key not in only:
            continue
        img = cutout(os.path.join(story, "drawings", f"{key}.jpg"), cfg)
        dst = os.path.join(story, "cutouts", f"{key}.png")
        img.save(dst)
        print(f"{key} {cfg['name']:22s} {img.size[0]}x{img.size[1]} -> {dst}")


if __name__ == "__main__":
    main()
