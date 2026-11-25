"""Once upon a time there was a Jelly Man, here to take over the world."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K

F = int(shot_seconds("shot01", 6.8) * FPS)
K.start(F)
K.make_land(seed=4, houses=7, trees=6)
K.make_sun_disc()
jm = K.puppet("01", (0, 4, 0), height=5.0)
K.pop(jm, 4, 10)
K.jiggle(jm, 1, int(F * 0.45), amp=0.07, period=10)
# stomps toward the town (and the camera)
K.hop_to(jm, int(F * 0.45), int(F * 0.85), (0, 1.5, 0), hops=3, height=0.8, rock=6)
for k in range(3):
    f = int(F * 0.45) + int((k + 1) * (F * 0.40) / 3)
    K.squash(jm, f, 0.2)
K.jiggle(jm, int(F * 0.85) + 8, F, amp=0.06, period=10)
# the world he wants: a little spinning globe
globe = ico("Globe", 0.7, (2.1, 2.5, 3.6), mat("kid_sea", (0.1, 0.35, 0.95)), subdiv=2)
land = mat("kid_land", (0.2, 0.75, 0.2))
globe.data.materials.append(land)
for i, poly in enumerate(globe.data.polygons):
    if (i * 7) % 5 < 2:
        poly.material_index = 1
K.spin(globe, 1, F, turns=1.2, axis=2)
globe.parent = jm.root
globe.location = (2.0, -0.3, 3.4)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (0, -9, 1.0), (0, 3, 3.6))
key_camera(cam, F, (0, -7.5, 0.9), (0, 3, 3.6))
add_shake(cam, int(F * 0.5), int(F * 0.9), strength=0.06, rot_strength=0.006)
render(os.environ.get("JAWS_OUT", "renders/shot01_jelly"))
