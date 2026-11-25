"""Shot 10: the Orbiter lifts off at sunset with Agent Cherry hanging from its landing gear; a Twin spots her."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S

F = int(shot_seconds("shot10_orbiter", 5.0) * FPS)
S.desert(F, sunset_sky=True)
O.make_pad("Pad", (0, 9, 0), r=7)
O.make_lab_building("Lab", (-14, 24, 0))
orb = O.make_orbiter("Orbiter", (0, 9, 4.6), rot_z=0)
r = orb["root"]
for f in range(1, F + 1, 3):
    t = f / F
    r.location = (0, 9 + 10 * t ** 2, 4.6 + 9 * t ** 1.6)
    r.rotation_euler = (math.radians(-6 * t + 1.5 * math.sin(f / 5)), math.radians(2 * math.sin(f / 7)), 0)
    r.keyframe_insert("location", frame=f)
    r.keyframe_insert("rotation_euler", frame=f)
for k in range(2):
    O.blink(orb["nav"][k], 1, F, period=14, on=5, phase=k * 7)
c = A.make_cherry("Cherry", (0, -3.5, -4.0))
c.root.parent = r
A.arms_up(c, 1, frames=1, deg=-178)
for f in range(1, F + 1, 4):                               # legs dangle and kick
    c.root.rotation_euler[0] = math.radians(5 * math.sin(f / 6))
    c.root.keyframe_insert("rotation_euler", index=0, frame=f)
A.walk(c, 1, F, period=20, swing=18)
tw = A.make_twin("Pilot", (0, -0.6, -0.15))
tw.root.parent = r
tw.root.scale = (0.75, 0.75, 0.75)
A.look(tw, int(F * 0.45), 0, tilt=35)                       # looks down: spotted her
q = text("Alert", "!", (0, -0.6, 2.4), 1.2, mat("alert_red", (1, 0.15, 0.1), emit=3.0), bold=True, extrude=0.1)
q.parent = r
O.show_at(q, int(F * 0.5), int(F * 0.8))
O.point_light("Under", (0, 0, -1), 0, (0.7, 0.3, 1.0), radius=2, shadow=False).parent = r
cam = add_camera((0, -6, 1.0), (0, 8, 4), lens=26)
key_camera(cam, 1, (1.5, -4.5, 0.8), (0, 6, 3.4))
key_camera(cam, F, (0.5, -3.5, 1.0), (0, 14, 9.5))
add_shake(cam, 1, F, strength=0.04, rot_strength=0.004)
render(os.environ.get("JAWS_OUT", "renders/shot10_orbiter"))
