"""Shot 13: Carrot's helmet falls off. Jelly sees him... and swallows him whole. GULP."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S

F = int(shot_seconds("shot13_gulp", 5.0) * FPS)
S.lair(F)
POP, LUNGE = int(F * 0.28), int(F * 2.3 / 5)
cr = A.make_carrot("Carrot", (-0.6, 1.4, 0), rot_z=-20, disguise=True)
A.look(cr, 8, -30)
# helmet pops off
O.hide_at(cr.disguise, POP)
h2 = box("Helm2", (0.62, 0.56, 0.26), (-0.6, 1.4, 2.0), mat("Carrot_helm", (0.12, 0.12, 0.14)))
O.show_at(h2, POP)
O.move(h2, POP, POP + 14, (-0.6, 1.4, 2.0), (-1.6, 1.0, 0.13))
h2.keyframe_insert("rotation_euler", frame=POP)
h2.rotation_euler = (0.4, 1.2, 0.8)
h2.keyframe_insert("rotation_euler", frame=POP + 14)
for f, z in ((POP, 0), (POP + 4, 0.35), (POP + 8, 0)):         # startled hop
    cr.root.location.z = z
    cr.root.keyframe_insert("location", index=2, frame=f)
A.arms_up(cr, POP + 4, frames=3)
j = A.make_jelly("Jelly", (3.6, 2.4, 0), rot_z=-60)
O.move(j.root, 1, POP, (3.6, 2.4, 0), (1.5, 1.8, 0), ease=False)
A.walk(j, 1, POP, period=16, swing=18)
A.wobble(j, 1, LUNGE, amp=0.05, period=12)
A.look(j, POP + 6, 0, tilt=10)
A.look(cr, POP + 6, -60)
# the lunge: Jelly stretches over Carrot; the carrot vanishes into him
j.root.keyframe_insert("location", frame=LUNGE - 4)
j.root.location = (-0.4, 1.5, 0)
j.root.keyframe_insert("location", frame=LUNGE + 4)
A.lean(j, LUNGE, 40, frames=4)
A.lean(j, LUNGE + 10, 0, frames=6)
O.hide_at(cr.root, LUNGE + 2)
inside = A.make_carrot("Inside", (0, 0, 0.12))
inside.root.parent = j.body
inside.root.scale = (0.001,) * 3
inside.root.keyframe_insert("scale", frame=LUNGE + 1)
inside.root.scale = (0.42,) * 3
inside.root.keyframe_insert("scale", frame=LUNGE + 2)
A.arms_up(inside, LUNGE + 6, frames=4)
A.wobble(j, LUNGE + 4, F, amp=0.16, period=7, seed=3)
A.turn(j, LUNGE + 12, -20, frames=10)
g = text("Gulp", "GULP!", (-0.2, 0.6, 3.6), 0.8, mat("gulp_txt", (1.0, 0.85, 0.1), emit=2.0), bold=True, extrude=0.08)
O.show_at(g, LUNGE + 4, LUNGE + 26)
cam = add_camera((0, -6.0, 2.3), (0.4, 1.8, 1.4), lens=28)
key_camera(cam, 1, (0.5, -6.4, 2.2), (0.5, 1.8, 1.4))
key_camera(cam, F, (-0.3, -4.8, 2.0), (-0.3, 1.6, 1.3))
add_shake(cam, LUNGE, LUNGE + 6, strength=0.1, rot_strength=0.01)
render(os.environ.get("JAWS_OUT", "renders/shot13_gulp"))
