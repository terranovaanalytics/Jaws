"""But a superhero banana guy stopped him in his trap."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K

F = int(shot_seconds("shot02", 6.5) * FPS)
K.start(F)
K.make_land(seed=4, houses=7, trees=6)
K.make_sun_disc()
jm = K.puppet("01", (1.0, 1.5, 0), height=3.6)
K.jiggle(jm, 1, int(F * 0.62), amp=0.06, period=10)
ban = K.puppet("02", (6, 0, 9), height=2.6)
land = int(F * 0.32)
K.fly(ban, 1, land, [(7, -1, 10), (3, -1, 6), (-1.7, 0, 0)], tilt=20)
K.squash(ban, land, 0.35)
K.sparkles("BanStar", (-1.7, -0.3, 1.5), land, int(F * 0.6), every=3, radius=1.4)
# the trap drops over the Jelly Man
cage = K.make_cage("Trap", (1.0, 1.5, 12), w=3.2, h=4.2)
drop = int(F * 0.55)
cage.keyframe_insert("location", frame=drop - 8)
cage.location.z = 0
cage.keyframe_insert("location", frame=drop)
K.squash(jm, drop, 0.3, length=10)
K.jiggle(jm, drop + 10, F, amp=0.12, period=6)
K.bob(ban, land + 9, F, amp=0.05, period=16)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (-0.3, -10, 2.0), (-0.3, 1, 2.6))
key_camera(cam, F, (-0.3, -8.6, 1.8), (-0.3, 1, 2.4))
add_shake(cam, drop, drop + 8, strength=0.12, rot_strength=0.01)
render(os.environ.get("JAWS_OUT", "renders/shot02_banana"))
