#!/usr/bin/env bash
# Render one scene script headlessly and upscale to 1080x1920 (nearest
# neighbor = chunky PS1 pixels).
#   tools/render.sh scenes/shot01_establishing.py
#   JAWS_JANK=2 tools/render.sh scenes/shot02_ferry_rammed.py   (jank level 0-3)
# Output: renders/<scene>.mp4 (animation) or renders/<scene>.png (still)
# Quick check: JAWS_FRAMES=1,72,144 tools/render.sh scenes/shot01_establishing.py
# JAWS_SUFFIX=_j2 appends to the output name (for side-by-side comparisons).
set -euo pipefail
cd "$(dirname "$0")/.."
scene="$1"; name="$(basename "$scene" .py)${JAWS_SUFFIX:-}"; out="renders/$name"
rm -rf "$out"; mkdir -p "$out"
JAWS_OUT="$out" xvfb-run -a -s "-screen 0 1280x1024x24" \
  blender -b --factory-startup --python-exit-code 1 -P "$scene" 2>&1 \
  | grep -E "Error|Traceback|^  File" || true
jank="$(cat "$out/jank" 2>/dev/null || echo 0)"

# low-res stage: dithered, reduced palette (jank >= 1)
pre="null"
[ "$jank" -ge 1 ] && pre="split[a][b];[a]palettegen=max_colors=48:stats_mode=full[p];[b][p]paletteuse=dither=bayer:bayer_scale=2"
up="scale=1080:1920:flags=neighbor"
# CRT/VHS stage at full res (jank >= 2): scanlines, color bleed, noise, vignette
post="null"
[ "$jank" -ge 2 ] && post="format=yuv420p,geq=lum='lum(X,Y)*(1-0.28*eq(mod(Y\,4)\,3))':cb='cb(X,Y)':cr='cr(X,Y)',chromashift=cbh=4:crh=-4,eq=saturation=1.25:contrast=1.05,noise=alls=7:allf=t,vignette=PI/5"

if [ -n "${JAWS_FRAMES:-}" ]; then
  for f in "$out"/preview_*.png; do
    ffmpeg -loglevel error -y -i "$f" -vf "$up" "${f%.png}_big.png"
  done
  echo "-> $out/preview_*_big.png"
elif [ -f "$out/still.png" ]; then
  ffmpeg -loglevel error -y -i "$out/still.png" -vf "$up" "renders/$name.png"
  echo "-> renders/$name.png"
else
  n=$(ls "$out"/f_*.png | wc -l)
  rate=24; [ "$jank" -ge 1 ] && rate=12      # frames were rendered on twos
  ffmpeg -loglevel error -y -framerate $rate -pattern_type glob -i "$out/f_*.png" \
    -vf "$pre,$up,$post,fps=24" -c:v libx264 -pix_fmt yuv420p -crf 18 "renders/$name.mp4"
  echo "-> renders/$name.mp4 ($n frames rendered, jank $jank)"
fi
