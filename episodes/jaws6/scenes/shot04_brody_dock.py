"""Shot 4: "Police Chief Brody... is watching from the dock". Over his shoulder
at the fireworks, then the camera arcs round to his face, lit by the bursts.
Mini flag in one hand, hot dog in the other."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import add_camera, key_camera, render, FPS, shot_seconds, box, cyl, mat
from jaws.people import make_brody
from jaws.town import make_flag
from _harbor import build_harbor, show, BARGE

F = int(shot_seconds("shot04", 3.6) * FPS)
h = build_harbor(F, pier_bunting=True)
show(h["barge"], 1, F, every=6, seed=4)
dx, dy, dz = h["dock_end"]
b = make_brody("Brody", loc=(dx - 2, dy + 0.5, dz), rot_z=0)
b.head.rotation_euler = (math.radians(-18), 0, math.radians(8))     # looking up at the show
# little flag in the left hand, hot dog in the right
b.arm_l.rotation_euler = (math.radians(-40), 0, math.radians(-10))
f = make_flag("HandFlag", (0, -0.05, -0.62), size=0.22, pole=0.55)
f.parent = b.arm_l
b.arm_r.rotation_euler = (math.radians(-55), 0, 0)
bun = box("Bun", (0.12, 0.34, 0.1), (0, -0.08, -0.62), mat("bun", (0.85, 0.62, 0.3)))
bun.parent = b.arm_r
dog = cyl("Dog", 0.04, 0.42, (0, -0.08, -0.56), mat("frank", (0.65, 0.22, 0.12)), n=6, rot=(90, 0, 0))
dog.parent = b.arm_r
b.arm_r.keyframe_insert("rotation_euler", frame=int(F * 0.55))
b.arm_r.rotation_euler = (math.radians(-95), 0, math.radians(15))  # absent-minded bite
b.arm_r.keyframe_insert("rotation_euler", frame=int(F * 0.75))

hx, hy, hz = dx - 2, dy + 0.5, dz + 1.9
cam = add_camera((0, 0, 0), (0, 0, 0), lens=32)
key_camera(cam, 1, (hx + 1.1, hy + 2.8, hz + 0.25), (hx - 1.2, hy - 8, hz + 2.2))
key_camera(cam, int(F * 0.4), (hx + 2.6, hy + 1.0, hz + 0.1), (hx - 1.5, hy - 8, hz + 2.0))
key_camera(cam, F, (hx + 1.8, hy - 2.6, hz - 0.3), (hx, hy, hz + 0.15))
render(os.environ.get("JAWS_OUT", "renders/shot04_brody_dock"))
