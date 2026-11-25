"""And he stayed on the meanies, like the alien got in the spaceship with the
meanies in it."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K

F = int(shot_seconds("shot08", 8.5) * FPS)
K.start(F)
K.make_land(seed=8, houses=4, trees=6)
K.make_sun_disc()
ship = K.puppet("07", (1.4, 2.5, 3.2), height=3.6)
for f in range(1, F + 1, 3):
    ship.root.location.z = 3.2 + 0.25 * math.sin(f / 9)
    ship.root.keyframe_insert("location", index=2, frame=f)
bm = K.beam("ShipBeam", (1.4, 2.5, 0), h=4.0, r=1.4, color=(0.9, 1.0, 0.5))
al = K.puppet("03", (-0.5, 0.5, 0), height=2.4, name="Alien1")
mns = [K.puppet("06", (-2.0 + i * 0.9, -0.3 - 0.3 * i, 0), height=1.9, name=f"Meanie{i}") for i in range(3)]
ch = K.puppet("05", (-5, -0.8, 0), height=2.8)
board = int(F * 0.64)
for i, m in enumerate(mns):
    f0 = int(F * (0.15 + 0.12 * i))
    K.hop_to(m, f0, f0 + 24, (1.4, 2.5, 0), hops=4, height=0.5)
    K.place(m, f0 + 25, (1.4, 2.5, 0))
    K.place(m, f0 + 40, (1.4, 2.5, 3.0))
    K.vanish(m, f0 + 30, f0 + 42)
K.hop_to(al, int(F * 0.45), board - 14, (1.4, 2.5, 0), hops=4, height=0.5)
K.place(al, board - 13, (1.4, 2.5, 0))
K.place(al, board + 4, (1.4, 2.5, 3.0))
K.vanish(al, board - 4, board + 6)
K.hop_to(ch, int(F * 0.1), int(F * 0.7), (-1.3, -0.8, 0), hops=7, height=0.4)
K.squash(ship, board + 6, 0.2)
K.hide(bm, board + 12)
K.bob(ch, int(F * 0.7) + 3, F, amp=0.05, period=12)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (-0.3, -10.5, 2.4), (-0.3, 1, 3.0))
key_camera(cam, F, (0.0, -9.5, 2.4), (0.0, 1, 3.0))
render(os.environ.get("JAWS_OUT", "renders/shot08_spaceship"))
