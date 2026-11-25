"""And then they ate the superhero. Oh no!"""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K

F = int(shot_seconds("shot04", 4.9) * FPS)
K.start(F)
K.make_land(seed=5, houses=5, trees=7)
K.make_sun_disc()
K.make_platform("Pad", (1.2, 1, 0), r=2.4)
ban = K.puppet("02", (-1.7, -1.6, 0), height=2.3)
K.bob(ban, 1, int(F * 0.3), amp=0.04, period=10)
als = [K.puppet("03", (x, 0.8, 0.6), height=2.6, name=f"Alien{i}") for i, x in enumerate((0.2, 2.0))]
go = int(F * 0.12)
K.hop_to(als[0], go, go + 20, (-0.9, -0.9, 0), hops=3, height=0.5)
K.hop_to(als[1], go + 4, go + 26, (0.5, -0.3, 0), hops=3, height=0.5)
chomp = int(F * 0.45)
for f in (chomp, chomp + 9, chomp + 18):
    K.squash(als[0], f, 0.3, 7)
    K.squash(als[1], f + 3, 0.3, 7)
K.place(ban, chomp - 1, (-1.7, -1.6, 0))
K.place(ban, chomp + 14, (-0.9, -0.6, 0.9))
K.vanish(ban, chomp + 2, chomp + 16)
for i, a in enumerate(als):
    K.bob(a, chomp + 30, F, amp=0.05, period=10, phase=i)
oh = K.label("OhNo", "OH NO!", (-0.4, -1.0, 4.4), 1.0, color=(1.0, 0.3, 0.25))
K.pop_obj(oh, int(F * 0.77), 6)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=30)
key_camera(cam, 1, (-0.4, -9.5, 1.8), (-0.4, 0.5, 2.4))
key_camera(cam, F, (-0.6, -7.5, 1.6), (-0.6, 0.5, 2.4))
add_shake(cam, chomp, chomp + 26, strength=0.08, rot_strength=0.008)
render(os.environ.get("JAWS_OUT", "renders/shot04_eat"))
