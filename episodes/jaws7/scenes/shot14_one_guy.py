"""Shot 14: "They keep one Russian guy on board to make it look normal." The
sub surfaced in the cove, deck empty, and up on top of the sail, one lonely
Russian sailor waving at nobody with a big forced grin."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import add_camera, key_camera, render, FPS, shot_seconds, box, mat
from jaws.spy import make_russian
from _sets import cove, SUB_Z, wave

F = int(shot_seconds("shot14", 2.7) * FPS)
c = cove(F, sign=False)
sub = c["sub"]
sx, _, sz = sub["sail_xyz"]
top = (sx - 1.0, 30, SUB_Z + sz)
r = make_russian("Ivan", loc=top, rot_z=-15, seed=0, stache=True)
box("Grin", (0.24, 0.03, 0.05), (0, -0.2, 0.07), mat("grin", (1, 1, 1), emit=0.5), parent=r.head)
wave(r, 1, F, period=8)
r.arm_l.rotation_euler = (0, 0, math.radians(8))
cam = add_camera((0, 0, 0), (0, 0, 0), lens=30)
key_camera(cam, 1, (top[0] + 3, top[1] - 22, 2.0), (top[0], top[1], top[2] - 2.0))
key_camera(cam, F, (top[0] + 2, top[1] - 13, 3.5), (top[0], top[1], top[2] + 0.4))
render(os.environ.get("JAWS_OUT", "renders/shot14_one_guy"))
