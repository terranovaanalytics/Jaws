"""Shot 2: "Okay, buddy, but then we learned the sharks turned out to be
radioactive." Reuses the finished Jaws 6 mutant-swarm footage (already graded)
in Blender's sequencer, tagged PREVIOUSLY ON JAWS 6. Writes look "clip" so
tools/render.sh does not grade it twice."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import jaws.common as C
from jaws.common import reset_scene, render, FPS, shot_seconds, REPO

F = int(shot_seconds("shot02", 2.9) * FPS)
J6 = os.path.join(REPO, "episodes", "jaws6", "renders")
s = reset_scene(F)
se = s.sequence_editor_create()
a = se.sequences.new_movie("Mutants", os.path.join(J6, "shot15_mutants.mp4"), channel=1, frame_start=1)
a.frame_final_start, a.frame_final_end = 1, F + 1
t = se.sequences.new_effect("Tag", "TEXT", channel=3, frame_start=1, frame_end=F + 1)
t.text = "PREVIOUSLY ON JAWS 6"
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
render(os.environ.get("JAWS_OUT", "renders/shot02_recap"))
