"""Shot 1: "If you've been following along, you know about the shark caves,
you know about the radioactive sharks, you know about the Russian nuclear
sub." Three quick clips of earlier episodes (already graded): the Jaws 5 egg
cave, the Jaws 6 glowing mutants, and the Jaws 7 sub. The sub is a
PLACEHOLDER (renders/_recap_sub.mp4, from _recap_sub.py) until the Jaws 7
footage exists: then point SUB_CLIP at it."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import bpy
import jaws.common as C
from jaws.common import reset_scene, render, FPS, shot_seconds, REPO

F = int(shot_seconds("shot01", 6.5) * FPS)
EP = os.path.join(REPO, "episodes")
SUB_CLIP = os.path.join(EP, "jaws8", "renders", "_recap_sub.mp4")   # TODO: Jaws 7 sub footage
# cut points, from the narration: "...the shark caves, | you know about the radioactive
# sharks, | you know about the Russian nuclear sub"
CUT1, CUT2 = int(F * 0.43), int(F * 0.69)
CLIPS = [(os.path.join(EP, "jaws5", "renders", "shot09_cave.mp4"), 1, CUT1, "JAWS 5", "end"),
         (os.path.join(EP, "jaws6", "renders", "shot15_mutants.mp4"), CUT1, CUT2, "JAWS 6", "start"),
         (SUB_CLIP, CUT2, F + 1, "JAWS 7", "start")]

s = reset_scene(F)
se = s.sequence_editor_create()
for k, (path, a, b, tag, part) in enumerate(CLIPS):
    m = se.sequences.new_movie(f"Clip{k}", path, channel=1, frame_start=a)
    n = b - a
    skip = max(0, m.frame_duration - n) if part == "end" else min(12, max(0, m.frame_duration - n))
    m.frame_start = a - skip
    m.frame_final_start, m.frame_final_end = a, b
    t = se.sequences.new_effect(f"Tag{k}", "TEXT", channel=3, frame_start=a, frame_end=b)
    t.text = f"PREVIOUSLY ON {tag}"
    t.font_size = 64
    t.use_bold = True
    t.location = (0.5, 0.93)
    t.align_x, t.align_y = "CENTER", "CENTER"
    t.color = (1, 0.92, 0.3, 1)
    t.use_shadow = True
    t.use_box = True
    t.box_color = (0, 0, 0, 0.55)
s.render.use_sequencer = True
s.view_settings.view_transform = "Standard"
s.sequencer_colorspace_settings.name = "sRGB"
C.LOOK = "clip"                 # tells render.sh: already graded
render(os.environ.get("JAWS_OUT", "renders/shot01_recap"))
