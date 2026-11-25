"""Shot 15: Jelly brings Carrot (still inside him) to the big chair. It swivels round: SOMEONE, the real boss."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S

F = int(shot_seconds("shot15_someone", 5.5) * FPS)
S.lair(F, purple=False)
SPIN, SPOT = int(F * 2.4 / 5.5), int(F * 3.2 / 5.5)
ch = O.make_swivel_chair("Chair", (0.9, 2.6, 0), rot_z=180, color=(0.55, 0.04, 0.1))
so = A.make_someone("Someone", (0, 0.05, -0.08), rot_z=0)
so.root.parent = ch
for leg in (so.leg_l, so.leg_r):
    leg.rotation_euler[0] = math.radians(-90)
for a in (so.arm_l, so.arm_r):
    a.rotation_euler[0] = math.radians(-40)
ch.keyframe_insert("rotation_euler", index=2, frame=SPIN)
ch.rotation_euler[2] = math.radians(-20)
ch.keyframe_insert("rotation_euler", index=2, frame=SPIN + 12)
A.arm(so, "r", SPOT + 10, -110, frames=8, roll=-20)       # adjusts the monocle
A.look(so, SPOT + 10, 10, tilt=-8)
dim = O.point_light("Dim", (0.9, 1.0, 4), 120, (0.6, 0.5, 0.9), radius=1)
spot = O.spot_light("Spot", (0.9, 1.6, 6.5), (0.9, 2.6, 0.8), 0, (1.0, 0.9, 0.7), angle=34, blend=0.25)
spot.data.keyframe_insert("energy", frame=SPOT - 1)
spot.data.energy = 4500
spot.data.keyframe_insert("energy", frame=SPOT)
j = A.make_jelly("Jelly", (-4.0, 1.3, 0), rot_z=-100)
O.move(j.root, 1, SPIN - 10, (-4.0, 1.3, 0), (-1.5, 1.2, 0), ease=False)
A.walk(j, 1, SPIN - 10, period=16, swing=18)
A.wobble(j, 1, F, amp=0.05, period=14)
A.turn(j, SPIN - 2, -140, frames=10)
A.lean(j, SPOT + 6, 25, frames=8)                         # Jelly bows to the boss
inside = A.make_carrot("Inside", (0, -0.05, 0.12))
inside.root.parent = j.body
inside.root.scale = (0.42,) * 3
A.arms_up(inside, SPOT + 2, frames=3)
A.look(inside, SPOT, -40)
cam = add_camera((-0.4, -6, 2.2), (0, 2, 1.6), lens=28)
key_camera(cam, 1, (-1.2, -6.0, 2.2), (-1.0, 2, 1.5))
key_camera(cam, SPIN, (-0.4, -5.6, 2.0), (0.0, 2, 1.5))
key_camera(cam, F, (0.5, -3.6, 1.9), (0.7, 2.4, 1.9))
render(os.environ.get("JAWS_OUT", "renders/shot15_someone"))
