"""He needed the cronchisk. (A mysterious glowing gem on a pedestal.)"""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K

F = int(shot_seconds("shot14", 3.6) * FPS)
K.start(F)
K.make_land(seed=11, houses=5, trees=6)
K.make_sun_disc()
ped, gem = K.make_crystal("Cronchisk", (1.3, 0.5, 0), size=1.0)
K.spin(gem, 1, F, turns=0.8, axis=2)
for f in range(1, F + 1, 3):
    gem.location.z = 2.1 + 0.15 * math.sin(f / 5)
    gem.keyframe_insert("location", index=2, frame=f)
K.sparkles("Gleam", (1.3, 0.3, 2.2), 1, F, every=3, radius=1.0, color=(0.9, 0.7, 1.0))
so = K.puppet("11", (-2.0, -0.2, 0), height=2.4)
K.hop_to(so, 6, int(F * 0.8), (-0.4, -0.2, 0), hops=4, height=0.4)
q = K.label("Want", "?", (-0.4, -0.6, 3.3), 1.0, color=(1, 1, 1))
K.pop_obj(q, int(F * 0.3), 6)
q.parent = None
cam = add_camera((0, 0, 0), (0, 0, 0), lens=30)
key_camera(cam, 1, (0, -8, 1.6), (0, 0.4, 2.0))
key_camera(cam, F, (0.6, -6.2, 1.6), (0.6, 0.4, 2.0))
render(os.environ.get("JAWS_OUT", "renders/shot14_cronchisk"))
