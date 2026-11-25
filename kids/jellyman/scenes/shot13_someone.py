"""And then he saw someone."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K

F = int(shot_seconds("shot13", 5.7) * FPS)
K.start(F)
K.make_land(seed=11, houses=5, trees=6)
K.make_sun_disc()
cool = K.puppet("10", (-1.4, 0.2, 0), height=3.0, rot_z=180)
K.bob(cool, 1, F, amp=0.04, period=14)
bush = empty("Bush", (1.6, 0.6, 0))
for i, (x, z, r) in enumerate(((-0.6, 0.4, 0.7), (0.2, 0.6, 0.85), (0.9, 0.4, 0.65))):
    ico(f"BushPuff{i}", r, (x, 0, z), mat("kid_bush", (0.15, 0.5, 0.12)), parent=bush)
so = K.puppet("11", (1.6, 1.4, -2.6), height=2.3)
pop = int(F * 0.35)
K.place(so, 1, (1.6, 1.4, -2.6))
K.place(so, pop, (1.6, 1.4, -2.6))
K.place(so, pop + 8, (1.6, 1.4, 1.4))
K.place(so, pop + 12, (1.6, 1.4, 1.0))
K.hop_to(so, pop + 20, pop + 40, (1.2, -0.3, 0), hops=2, height=0.6, start=(1.6, 1.4, 1.0))
K.bob(so, pop + 42, F, amp=0.05, period=12)
see = int(F * 0.42)
K.flip(cool, see)
ex = K.label("Wow", "!", (-1.4, -0.4, 3.9), 1.4, color=(1, 0.9, 0.2))
K.pop_obj(ex, see + 2, 6)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (0, -8.5, 1.8), (0, 0.5, 2.2))
key_camera(cam, F, (0.0, -7.6, 1.7), (0.0, 0.5, 2.2))
render(os.environ.get("JAWS_OUT", "renders/shot13_someone"))
