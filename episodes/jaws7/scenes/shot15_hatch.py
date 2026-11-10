"""Shot 15: "And then Police Chief Brody, Jesse, and Gronk hop into the
submarine." On the sub's deck: the three line up at the open hatch and drop
in one at a time. The big agent gets a little stuck, wiggles, and pops
through. Ivan keeps waving on the sail."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import add_camera, key_camera, render, FPS, shot_seconds
from jaws.people import make_brody, make_jesse, walk
from jaws.spy import make_agent, make_russian, open_hatch
from _sets import cove, deck_z, SUB_Z, move, wave, face

F = int(shot_seconds("shot15", 3.6) * FPS)
c = cove(F, sign=False)
sub = c["sub"]
open_hatch(sub, 1)
hx, _, hz = sub["hatch_xyz"]
HX, HY, HZ = hx, 30, SUB_Z + hz
dz = deck_z(sub)
sx, _, sz = sub["sail_xyz"]
iv = make_russian("Ivan", loc=(sx - 1.0, 30, SUB_Z + sz), rot_z=-15, seed=0, stache=True)
wave(iv, 1, F, period=8)
people = [make_brody("Brody", (HX - 1.6, HY, dz), rot_z=90), make_jesse("Jesse", (HX - 3.0, HY, dz), rot_z=90),
          make_agent("Agent", (HX - 4.6, HY, dz), rot_z=90)]
starts = [int(F * 0.10), int(F * 0.36), int(F * 0.58)]
for k, (p, f0) in enumerate(zip(people, starts)):
    x0 = p.root.location.x
    if k:                                    # shuffle up behind the one in front
        move(p.root, [(1, (x0, HY, dz)), (starts[k - 1] + 4, (x0, HY, dz)), (starts[k - 1] + 12, (x0 + 1.4, HY, dz))])
        walk(p, starts[k - 1] + 4, starts[k - 1] + 12, period=8)
        x0 += 1.4
    move(p.root, [(f0, (x0, HY, dz)), (f0 + 5, (HX, HY, dz + 0.5))])   # hop onto the hatch
    if p.name == "Agent":                    # stuck at the shoulders... wiggle... pop
        move(p.root, [(f0 + 8, (HX, HY, dz - 0.9))])
        for i in range(4):
            face(p.root, f0 + 9 + i * 3, 90 + (12 if i % 2 else -12))
        face(p.root, f0 + 21, 90)
        move(p.root, [(f0 + 21, (HX, HY, dz - 0.9)), (f0 + 25, (HX, HY, dz - 3.2))])
    else:
        move(p.root, [(f0 + 10, (HX, HY, dz - 3.0))])
    for arm in (p.arm_l, p.arm_r):
        face(arm, f0 + 3, 0, axis=0)
        face(arm, f0 + 6, -170, axis=0)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (HX + 6, HY - 12, dz + 5), (HX - 2, HY, dz + 1))
key_camera(cam, F, (HX + 4.5, HY - 10, dz + 4), (HX - 1, HY, dz + 0.6))
render(os.environ.get("JAWS_OUT", "renders/shot15_hatch"))
