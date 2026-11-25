"""Shot 05: the desert landing pad. The Orbiter has landed; THE TWINS stride out in matching suits."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S

F = int(shot_seconds("shot05_twins", 4.5) * FPS)
S.desert(F)
O.make_pad("Pad", (0, 9, 0), r=7)
orb = O.make_orbiter("Orbiter", (0, 10, 1.65), rot_z=0)
O.blink(orb["nav"][0], 1, F, period=16, on=5)
O.blink(orb["nav"][1], 1, F, period=16, on=5, phase=8)
lab = O.make_lab_building("Lab", (-13, 22, 0))
twins = [A.make_twin(f"Twin{s}", (s * 0.65, 8.5, 0.2), rot_z=0) for s in (-1, 1)]
STOP = int(F * 0.7)
for t in twins:
    x = t.root.location.x
    O.move(t.root, 1, STOP, (x, 8.5, 0.2), (x, 1.2, 0.0), ease=False)
    A.walk(t, 1, STOP, period=14, swing=26)
A.arm(twins[0], "r", STOP + 6, -70, frames=6)      # straighten the tie, in sync
A.arm(twins[1], "l", STOP + 6, -70, frames=6)
for t in twins:
    A.look(t, STOP + 14, 0, tilt=-8)
cam = add_camera((0, -6, 0.5), (0, 4, 2.2), lens=28)
key_camera(cam, 1, (0.4, -6.5, 0.45), (0, 5, 2.6))
key_camera(cam, F, (0.1, -4.6, 0.7), (0, 2, 1.9))
render(os.environ.get("JAWS_OUT", "renders/shot05_twins"))
