"""Title: ATTACK OF THE JELLY MAN. Plays under the false starts
("Okay, once upon a time... I mean, once upon a time...")."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K

F = int(shot_seconds("shot00", 10.7) * FPS)
K.start(F)
K.make_land(seed=3, houses=5)
K.make_sun_disc((10, 45, 22))
top = K.label("TitleTop", "ATTACK OF THE", (0, 2, 10.9), 1.2, color=(1.0, 0.9, 0.2))
big = K.label("TitleBig", "JELLY MAN", (0, 2, 8.6), 2.05, color=(0.85, 0.5, 1.0))
K.pop_obj(top, int(F * 0.06), 10)
K.pop_obj(big, int(F * 0.14), 12)
jm = K.puppet("01", (0, 1, -4.6), height=4.6)
rise = int(F * 0.25)
K.place(jm, 1, (0, 1, -4.6))
K.place(jm, rise, (0, 1, -4.6))
K.place(jm, rise + 14, (0, 1, 0.4))
K.place(jm, rise + 18, (0, 1, 0))
K.jiggle(jm, rise, F, amp=0.08, period=12)
add_shake(jm.root, rise + 14, rise + 22, strength=0.05, rot_strength=0.0)
# the heroes peek in at the sides
for i, (k, x, f) in enumerate((("05", -2.9, 0.45), ("02", 2.9, 0.55), ("09", -1.7, 0.65), ("12", 1.7, 0.75))):
    p = K.puppet(k, (x, -3.5 + abs(x) * 0.3, 0), height=2.0)
    K.pop(p, int(F * f), 8)
    K.bob(p, int(F * f) + 9, F, amp=0.05, period=18, phase=i)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=30)
key_camera(cam, 1, (0, -15.5, 3.4), (0, 2, 5.2))
key_camera(cam, F, (0, -13.5, 3.2), (0, 2, 5.0))
render(os.environ.get("JAWS_OUT", "renders/shot00_title"))
