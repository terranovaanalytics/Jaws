#!/usr/bin/env bash
# Render every shot, skipping ones already rendered since tools/.render_since
# was touched (so an interrupted run resumes). Start fresh with: touch tools/.render_since
cd "$(dirname "$0")/.."
[ -f tools/.render_since ] || touch tools/.render_since
for s in scenes/shot*.py; do
  n=$(basename "$s" .py)
  if [ "renders/$n.mp4" -nt tools/.render_since ]; then echo "skip $n"; continue; fi
  start=$(date +%s)
  tools/render.sh "$s" 2>&1 | grep -E "^->|Error:"
  echo "   $n took $(( $(date +%s) - start ))s"
done
echo ALL-DONE
