"""And then a carrot saved all of the people."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K

F = int(shot_seconds("shot10", 6.0) * FPS)
K.start(F)
K.make_land(seed=9, houses=8, trees=5)
K.make_sun_disc()
people = []
spots = [(-2.2, 0.9), (-1.3, 1.8), (-0.4, 1.2), (0.6, 1.9), (1.4, 1.0), (2.2, 1.7), (-1.9, 2.8), (1.3, 2.9)]
for i, (x, y) in enumerate(spots):
    p = K.puppet("08", (x, y, 0), height=1.5 + 0.15 * (i % 3), name=f"Person{i}")
    people.append(p)
    K.bob(p, 1, int(F * 0.45), amp=0.08, period=6 + i % 3, sway=8, phase=i)    # scared shiver
mns = [K.puppet("06", (x, 0.1, 0), height=1.9, name=f"Meanie{i}") for i, x in enumerate((-0.9, 1.0))]
car = K.puppet("09", (-5, -1.4, 0), height=2.6)
arrive = int(F * 0.35)
K.hop_to(car, 1, arrive, (0, -1.4, 0), hops=5, height=0.6)
K.squash(car, arrive, 0.3)
for i, m in enumerate(mns):
    K.flip(m, arrive + 2 + i * 3)
    K.hop_to(m, arrive + 8, arrive + 30, (8 * (1 if i else -1), 1.0, 0), hops=6, height=0.5, rock=16)
cheer = int(F * 0.5)
for i, p in enumerate(people):
    K.hop_to(p, cheer + i, F, (p.root.location.x, p.root.location.y, 0), hops=7, height=0.5, rock=6)
K.confetti("Cheer", (0, 1.5, 3), cheer, count=60, spread=5, rise=7, life=36)
K.bob(car, arrive + 9, F, amp=0.05, period=14)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (0, -7.2, 1.7), (0, 1.0, 1.7))
key_camera(cam, F, (0, -6.4, 1.6), (0, 1.0, 1.6))
render(os.environ.get("JAWS_OUT", "renders/shot10_carrot"))
