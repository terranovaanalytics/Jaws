#!/usr/bin/env bash
# Render every shot of an episode, skipping shots already rendered since
# episodes/<ep>/renders/.render_since was touched (so an interrupted run resumes).
#   tools/render_all.sh jaws6
# Start fresh with: touch episodes/<ep>/renders/.render_since
# Note: cloud sessions stop background jobs after 2 h. A full HD episode takes
# ~2.5 h, so expect to re-run this once; long shots can also be split with
# JAWS_RANGE (see tools/render.sh).
set -u
cd "$(dirname "$0")/.."
ep="episodes/${1:?usage: tools/render_all.sh <episode>}"
mkdir -p "$ep/renders"
mark="$ep/renders/.render_since"
[ -f "$mark" ] || touch "$mark"
for s in "$ep"/scenes/shot*.py; do
  n=$(basename "$s" .py)
  if [ "$ep/renders/$n.mp4" -nt "$mark" ]; then echo "skip $n"; continue; fi
  start=$(date +%s)
  tools/render.sh "$s" 2>&1 | grep -E "^->|Error:"
  echo "   $n took $(( $(date +%s) - start ))s"
done
echo ALL-DONE
