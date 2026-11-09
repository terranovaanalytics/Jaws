"""Shot 16: "Brody looks back and says, 'Boys, we're going to Russia.'" Late
sun, red-orange sky. Brody stands waist-deep in the open hatch facing the bow,
spins round to us, then drops inside; the lid slams and the sub starts
pushing out of the cove toward the horizon."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import add_camera, key_camera, add_shake, render, FPS, shot_seconds
from jaws.people import make_brody
from jaws.spy import open_hatch
from jaws.world import splash
from _sets import cove, SUB_Z, move, face

F = int(shot_seconds("shot16", 2.8) * FPS)
c = cove(F, sign=False, sky=(0.95, 0.55, 0.35), sun=(1.0, 0.7, 0.45))
sub = c["sub"]
hx, _, hz = sub["hatch_xyz"]
open_hatch(sub, 1)
TURN = int(F * 0.22)
DUCK = int(F * 0.76)
b = make_brody("Brody", loc=(hx, 0, hz - 0.95), rot_z=90)
b.root.parent = sub["root"]
face(b.root, TURN, 90)
face(b.root, TURN + 5, -40)                   # looks back at us
face(b.head, TURN + 5, 0, axis=0)
face(b.head, TURN + 9, -8, axis=0)
face(b.arm_r, DUCK - 10, 0, axis=0)
face(b.arm_r, DUCK - 6, -60, axis=0)           # a little "let's go" wave of the hand
move(b.root, [(DUCK, (hx, 0, hz - 0.95)), (DUCK + 5, (hx, 0, hz - 3.2))])
open_hatch(sub, DUCK + 6)
open_hatch(sub, DUCK + 9, opened=False)
GO = int(F * 0.55)
move(sub["root"], [(GO, (0, 30, SUB_Z)), (F, (6, 30, SUB_Z - 0.4))])
splash("Wake", (24, 28, 0.2), GO + 4, count=12, size=0.4, power=4)
wx, wy, wz = hx, 30, SUB_Z + hz
cam = add_camera((0, 0, 0), (0, 0, 0), lens=30)
key_camera(cam, 1, (wx - 4.5, wy - 4.5, wz + 1.6), (wx, wy, wz + 0.9))
key_camera(cam, DUCK, (wx - 5.0, wy - 5.5, wz + 1.7), (wx + 0.5, wy, wz + 0.8))
key_camera(cam, F, (wx - 7, wy - 9, wz + 2.5), (wx + 8, wy + 4, wz + 1.0))
render(os.environ.get("JAWS_OUT", "renders/shot16_russia"))
