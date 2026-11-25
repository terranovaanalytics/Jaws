"""But then Cherry Superhero came along. Yay, Cherry Superhero!"""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K

F = int(shot_seconds("shot07", 5.8) * FPS)
K.start(F)
K.make_land(seed=7, houses=6, trees=8)
K.make_sun_disc()
ch = K.puppet("05", (0, 0, 0), height=3.0)
land = int(F * 0.35)
K.fly(ch, 1, land, [(-7, 2, 12), (-3, 1, 7), (0, 0, 0)], tilt=18)
K.squash(ch, land, 0.35, 10)
K.bob(ch, land + 11, F, amp=0.05, period=14)
yay = int(F * 0.58)
K.confetti("Yay", (0, -0.5, 2.5), yay, count=50, spread=4, rise=7, life=34)
K.sparkles("Hero", (0, -0.2, 1.8), land, F, every=3, radius=1.9)
K.place(ch, yay - 1, (0, 0, 0))
K.place(ch, yay + 6, (0, 0, 0.9))
K.place(ch, yay + 12, (0, 0, 0))
cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (0, -8.5, 0.6), (0, 0, 2.8))
key_camera(cam, F, (0, -6.8, 0.6), (0, 0, 2.4))
add_shake(cam, land, land + 6, strength=0.1, rot_strength=0.01)
render(os.environ.get("JAWS_OUT", "renders/shot07_cherry"))
