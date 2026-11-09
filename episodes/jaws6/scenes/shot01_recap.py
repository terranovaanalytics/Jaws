"""Shot 1: "Previously on Jaws 5". Reuses the finished Jaws 5 footage (already
graded): the shark swarm (Shark 911), then the cutaway tilt down into the egg
cave. Built in Blender's video sequencer so it renders like any other shot;
it writes look "clip" so tools/render.sh does not grade it twice."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import bpy
import jaws.common as C
from jaws.common import reset_scene, render, FPS, shot_seconds, REPO

F = int(shot_seconds("shot01", 6.6) * FPS)
CUT = int(F * 0.55)            # "...Shark 911 | and then we learned... cave"
J5 = os.path.join(REPO, "episodes", "jaws5", "renders")

s = reset_scene(F)
se = s.sequence_editor_create()
a = se.sequences.new_movie("Swarm", os.path.join(J5, "shot03_swarm.mp4"), channel=1, frame_start=1 - 30)
a.frame_final_start, a.frame_final_end = 1, CUT                  # skip its first 30 frames
b_len = a.frame_duration
b = se.sequences.new_movie("Cave", os.path.join(J5, "shot09_cave.mp4"), channel=1, frame_start=CUT)
skip = max(0, b.frame_duration - (F - CUT + 1))                  # end of the tilt: the cave itself
b.frame_start = CUT - skip
b.frame_final_start, b.frame_final_end = CUT, F + 1
t = se.sequences.new_effect("Tag", "TEXT", channel=3, frame_start=1, frame_end=F + 1)
t.text = "PREVIOUSLY ON JAWS 5"
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
