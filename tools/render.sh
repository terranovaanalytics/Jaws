#!/usr/bin/env bash
# Render one scene script headlessly and upscale to 1080x1920 (nearest
# neighbor = chunky PS1 pixels).
#   tools/render.sh scenes/shot01_establishing.py
# Output: renders/<scene>.mp4 (animation) or renders/<scene>.png (still)
set -euo pipefail
cd "$(dirname "$0")/.."
scene="$1"; name="$(basename "$scene" .py)"; out="renders/$name"
rm -rf "$out"; mkdir -p "$out"
JAWS_OUT="$out" xvfb-run -a -s "-screen 0 1280x1024x24" \
  blender -b --factory-startup --python-exit-code 1 -P "$scene" 2>&1 \
  | grep -E "Error|Traceback|Saved|^  File" | grep -v "^Saved: '.*f_0" || true
if [ -f "$out/still.png" ]; then
  ffmpeg -loglevel error -y -i "$out/still.png" -vf "scale=1080:1920:flags=neighbor" "renders/$name.png"
  echo "-> renders/$name.png"
else
  ls "$out"/f_*.png >/dev/null
  ffmpeg -loglevel error -y -framerate 24 -pattern_type glob -i "$out/f_*.png" \
    -vf "scale=1080:1920:flags=neighbor" -c:v libx264 -pix_fmt yuv420p -crf 18 "renders/$name.mp4"
  echo "-> renders/$name.mp4 ($(ls "$out"/f_*.png | wc -l) frames)"
fi
