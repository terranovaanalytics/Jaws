"""And then a carrot got eaten up by a cool man."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K

F = int(shot_seconds("shot11", 5.6) * FPS)
K.start(F)
K.make_land(seed=10, houses=5, trees=7)
K.make_sun_disc()
car = K.puppet("09", (1.2, -0.3, 0), height=2.4)
K.bob(car, 1, int(F * 0.3), amp=0.05, period=14)
cool = K.puppet("10", (-6.5, 0.2, 0), height=3.0)
K.hop_to(cool, 1, int(F * 0.4), (-1.0, 0.2, 0), hops=4, height=0.3, rock=6)
K.bob(car, int(F * 0.3), int(F * 0.5), amp=0.1, period=4, sway=10)       # uh oh shiver
gulp = int(F * 0.55)
K.place(car, gulp - 6, (1.2, -0.3, 0))
K.place(car, gulp + 6, (-0.8, -0.1, 1.8))
K.vanish(car, gulp, gulp + 8)
K.squash(cool, gulp + 6, 0.3, 8)
K.squash(cool, gulp + 16, 0.25, 8)
K.bob(cool, gulp + 26, F, amp=0.05, period=12)
g = K.label("Gulp", "GULP!", (-1.0, -0.8, 4.1), 0.9, color=(1.0, 0.9, 0.3))
K.pop_obj(g, gulp + 8, 6)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=30)
key_camera(cam, 1, (0, -8, 1.8), (0, 0.3, 2.3))
key_camera(cam, F, (-0.3, -6.8, 1.7), (-0.3, 0.3, 2.3))
add_shake(cam, gulp + 4, gulp + 12, strength=0.05, rot_strength=0.005)
render(os.environ.get("JAWS_OUT", "renders/shot11_eaten"))
