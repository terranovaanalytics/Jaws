#!/usr/bin/env bash
# Render one scene script headlessly and upscale to 1080x1920 (nearest
# neighbor = chunky PS1 pixels).
#   tools/render.sh scenes/shot01_establishing.py
#   JAWS_JANK=2 tools/render.sh scenes/shot02_ferry_rammed.py   (jank level 0-3)
# Output: renders/<scene>.mp4 (animation) or renders/<scene>.png (still)
# Knobs: JAWS_PIXEL_SCALE=1..4 (1 = native 1080x1920), JAWS_SNAP=0/1 (vertex wobble),
#        JAWS_AA=1..16 (anti-aliasing samples), JAWS_COLORS=0|N (dithered palette),
#        JAWS_TWOS=0/1 (12 fps animation), JAWS_LOOK=sunny|70s
# Quick check: JAWS_FRAMES=1,72,144 tools/render.sh scenes/shot01_establishing.py
# JAWS_SUFFIX=_j2 appends to the output name (for side-by-side comparisons).
set -euo pipefail
cd "$(dirname "$0")/.."
scene="$1"; name="$(basename "$scene" .py)${JAWS_SUFFIX:-}"; out="renders/$name"
rm -rf "$out"; mkdir -p "$out"
JAWS_OUT="$out" xvfb-run -a -s "-screen 0 1280x1024x24" \
  blender -b --factory-startup --python-exit-code 1 -P "$scene" 2>&1 \
  | grep -E "Error|Traceback|^  File" | grep -vE "distutils|Error processing line" || true
jank="$(cat "$out/jank" 2>/dev/null || echo 0)"
look="$(cat "$out/look" 2>/dev/null || echo sunny)"

# film grade (look=70s): gentle S-curve, teal shadows / amber highlights,
# no pure white; then at full res a warm halation glow, grain and vignette
grade="null"; film="null"
if [ "$look" = "70s" ]; then
  grade="curves=r='0/0.03 0.25/0.23 0.5/0.52 0.75/0.79 1/0.97':g='0/0.03 0.25/0.22 0.5/0.49 0.75/0.75 1/0.93':b='0/0.07 0.25/0.24 0.5/0.44 0.75/0.65 1/0.80',colorbalance=rs=-0.04:bs=0.05:rh=0.05:bh=-0.05,eq=saturation=0.95"
  film="split[fa][fb];[fb]curves=all='0/0 0.72/0 1/1',gblur=sigma=16,colorchannelmixer=rr=1:gg=0.55:bb=0.3[fg];[fa][fg]blend=all_mode=screen:all_opacity=0.35,vignette=PI/5.5"   # grain is added once, in tools/assemble.py
fi

# low-res stage: dithered, reduced palette (jank >= 1)
pre="null"
colors="${JAWS_COLORS:-$([ "$jank" -ge 1 ] && echo 48 || echo 0)}"   # 0 = full color
[ "$colors" -gt 0 ] && pre="split[a][b];[a]palettegen=max_colors=$colors:stats_mode=full[p];[b][p]paletteuse=dither=bayer:bayer_scale=2"
up="scale=1080:1920:flags=neighbor"
# CRT/VHS stage at full res (jank >= 2): scanlines, color bleed, noise, vignette
post="null"
[ "$jank" -ge 2 ] && post="format=yuv420p,geq=lum='lum(X,Y)*(1-0.28*eq(mod(Y\,4)\,3))':cb='cb(X,Y)':cr='cr(X,Y)',chromashift=cbh=4:crh=-4,eq=saturation=1.25:contrast=1.05,noise=alls=7:allf=t,vignette=PI/5"

if [ -n "${JAWS_FRAMES:-}" ]; then
  for f in "$out"/preview_*.png; do
    ffmpeg -loglevel error -y -i "$f" -vf "$grade,$pre,$up,$film" "${f%.png}_big.png"
  done
  echo "-> $out/preview_*_big.png"
elif [ -f "$out/still.png" ]; then
  ffmpeg -loglevel error -y -i "$out/still.png" -vf "$grade,$up,$film" "renders/$name.png"
  echo "-> renders/$name.png"
else
  n=$(ls "$out"/f_*.png | wc -l)
  rate=24; [ "$(cat "$out/twos" 2>/dev/null || echo 0)" = "1" ] && rate=12   # rendered on twos
  ffmpeg -loglevel error -y -framerate $rate -pattern_type glob -i "$out/f_*.png" \
    -vf "$grade,$pre,$up,$film,$post,fps=24" -c:v libx264 -pix_fmt yuv420p -crf 18 "renders/$name.mp4"
  echo "-> renders/$name.mp4 ($n frames rendered, jank $jank)"
fi
