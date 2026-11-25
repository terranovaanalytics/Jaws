"""And all the alien guys went their way home."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K

F = int(shot_seconds("shot16", 2.9) * FPS)
K.start(F)
K.make_land(seed=8, houses=4, trees=6)
K.make_sun_disc()
ship = K.puppet("07", (0, 2.5, 2.8), height=3.6)
K.squash(ship, 3, 0.2)
K.fly(ship, 6, F, [(0, 2.5, 2.8), (1.0, 4, 7), (6, 14, 18)], tilt=10, ease=True)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (0, -9, 1.6), (0, 2.5, 3.2))
key_camera(cam, F, (0, -9, 1.6), (0, 2.5, 6.0))
render(os.environ.get("JAWS_OUT", "renders/shot16_home"))
