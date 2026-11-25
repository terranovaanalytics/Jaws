"""And then two space alien guys stepped onto the platform."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K

F = int(shot_seconds("shot03", 5.1) * FPS)
K.start(F)
K.make_land(seed=5, houses=5, trees=7)
K.make_sun_disc()
K.make_platform("Pad", (1.2, 1, 0), r=2.4)
bm = K.beam("Beam", (1.2, 1, 0.5), h=16, r=2.2, color=(0.6, 1.0, 0.8))
ban = K.puppet("02", (-1.7, -1.6, 0), height=2.3)
K.bob(ban, 1, F, amp=0.04, period=18)
for i, (x, f0) in enumerate(((0.3, 0.08), (2.1, 0.25))):
    al = K.puppet("03", (x, 1, 7), height=2.6, name=f"Alien{i}")
    a = int(F * f0)
    K.place(al, 1, (x, 1, 7))
    K.place(al, a, (x, 1, 7))
    K.place(al, a + 18, (x, 1, 0.6))
    K.squash(al, a + 18, 0.3)
    K.hop_to(al, a + 24, a + 40, (x - 0.1, 0.8, 0.6), hops=2, height=0.4)
    K.bob(al, a + 44, F, amp=0.05, period=14, phase=i * 2)
K.hide(bm, int(F * 0.8))
cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (0, -11, 2.4), (0, 1, 3.0))
key_camera(cam, F, (0, -9.5, 2.0), (0, 1, 2.6))
render(os.environ.get("JAWS_OUT", "renders/shot03_aliens"))
