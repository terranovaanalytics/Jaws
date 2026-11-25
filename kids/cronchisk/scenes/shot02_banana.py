"""Shot 02: Agent Banana crashes through the skylight, grabs the case; Jelly oozes down the drain."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S

F = int(shot_seconds("shot02_banana", 5.5) * FPS)
S.warehouse_int(F)
CRASH, LAND = int(F * 0.08), int(F * 0.17)
GRAB, OOZE, GONE = int(F * 0.3), int(F * 0.48), int(F * 0.72)
m = A.make_meanie("Meanie", (-1.25, 0.5, 0), rot_z=90)
j = A.make_jelly("Jelly", (1.45, 0.35, 0), rot_z=-90)
case = O.make_briefcase("Case", (0, 0.5, 1.1), open_lid=False)
case["root"].rotation_euler[2] = math.radians(180)
b = A.make_banana("Banana", (-0.3, -0.3, 7.5), rot_z=0)
O.shards("Shards", (0, 0.5, 7.0), CRASH, count=30, power=6, life=40)
import bpy
O.hide_at(bpy.data.objects["Skylight"], CRASH)
O.move(b.root, CRASH, LAND, (-0.3, -0.3, 7.5), (-0.3, -0.6, 0), ease=False)
b.root.keyframe_insert("location", frame=LAND + 3)
A.arms_up(b, CRASH + 2, frames=2)
A.arm(b, "l", LAND + 4, -20, frames=3)
A.arm(b, "r", LAND + 2, -40, frames=3)
A.lean(b, LAND + 2, 35, frames=2)            # superhero landing crouch
A.lean(b, LAND + 12, 0, frames=8)
# grab the case
A.arm(b, "r", GRAB, -80, frames=6)
A.arm(b, "r", GRAB + 10, -15, frames=8)
O.hide_at(case["root"], GRAB + 4)                     # the case leaves the crate...
held = O.make_briefcase("Held")                          # ...and appears in Banana's hand
A.hold(b, held["root"], "r", offset=(0.0, 0.0, -0.3), rot=(-90, 0, 90))
held["root"].scale = (0.8, 0.8, 0.8)
O.show_at(held["root"], GRAB + 4)
A.turn(b, F - 10, 15, frames=10)
# Meanie: hands up
A.arms_up(m, LAND + 6, frames=4)
A.arms_up(A.add_arms(m, color=(0.9, 0.2, 0.2)), LAND + 6, frames=4, deg=-150)
A.wobble(j, 1, OOZE, amp=0.06, period=8)
# Jelly squeezes down the drain
drain = O.make_drain("Drain", (2.5, -0.9, 0.0))
O.move(j.root, LAND + 8, OOZE, (1.45, 0.35, 0), (2.5, -0.9, 0))
A.turn(j, LAND + 14, -40, frames=8)
for f, sx, sz, z in ((OOZE, 1, 1, 0), (OOZE + 8, 1.35, 0.45, 0), (GONE - 6, 1.1, 0.12, -0.2), (GONE, 0.3, 0.05, -0.6)):
    j.root.scale = (sx, sx, sz)
    j.root.keyframe_insert("scale", frame=f)
    j.root.location = (2.5, -0.9, z)
    j.root.keyframe_insert("location", frame=f)
cam = add_camera((0, -9, 2.6), (0, 0.5, 2.2), lens=32)
key_camera(cam, 1, (0, -10, 2.0), (0, 0.4, 3.6))
key_camera(cam, LAND, (0, -10, 2.0), (0, 0.2, 2.0))
key_camera(cam, F, (0.6, -7.5, 2.2), (0.6, 0, 1.4))
add_shake(cam, LAND, LAND + 8, strength=0.25, rot_strength=0.02)
render(os.environ.get("JAWS_OUT", "renders/shot02_banana"))
