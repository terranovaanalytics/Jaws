"""And then a little guy in a force field trapped him in a force field and took him away."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K

F = int(shot_seconds("shot05", 7.7) * FPS)
K.start(F)
K.make_land(seed=6, houses=6, trees=6)
K.make_sun_disc()
a0 = K.puppet("03", (-1.2, 0.2, 0), height=2.6, name="Alien0")
a1 = K.puppet("03", (0.4, 0.8, 0), height=2.6, name="Alien1")
ff = K.puppet("04", (6, -1.4, 0), height=2.4)
K.hop_to(ff, 1, int(F * 0.3), (1.3, -1.4, 0), hops=5, height=0.35)
K.bob(ff, int(F * 0.3) + 3, int(F * 0.55), amp=0.05, period=10)
K.bob(a0, 1, int(F * 0.45), amp=0.04, period=12)
K.bob(a1, 1, F, amp=0.04, period=12, phase=1.5)
trap = int(F * 0.47)
bub = K.bubble("Bubble", (-1.2, 0.2, 1.4), r=1.9)
K.pop_obj(bub, trap, 10)
K.squash(a0, trap + 4, 0.25)
away = int(F * 0.75)
# off they go: bubble (with the alien inside) floats after the force-field guy
for f in range(away, F + 1, 2):
    t = (f - away) / max(1, F - away)
    x = -1.2 - 7 * t
    z = 1.4 + 1.2 * t + 0.25 * math.sin(t * 12)
    bub.location = (x, 0.2, z)
    bub.keyframe_insert("location", frame=f)
    a0.root.location = (x, 0.2, z - 1.4)
    a0.root.keyframe_insert("location", frame=f)
K.flip(ff, int(F * 0.6))
K.hop_to(ff, int(F * 0.66), F, (-4.5, -1.4, 0), hops=8, height=0.35)
K.flip(a1, int(F * 0.8))
cam = add_camera((0, 0, 0), (0, 0, 0), lens=30)
key_camera(cam, 1, (0.3, -9.5, 2.0), (0.3, 0.5, 2.5))
key_camera(cam, F, (-1.2, -9.5, 2.0), (-1.2, 0.5, 2.5))
render(os.environ.get("JAWS_OUT", "renders/shot05_forcefield"))
