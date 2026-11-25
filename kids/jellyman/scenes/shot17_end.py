"""The end! Oh, yay!"""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K

F = int(shot_seconds("shot17", 2.7) * FPS)
K.start(F)
K.make_land(seed=3, houses=5)
K.make_sun_disc((10, 45, 22))
end = K.label("TheEnd", "THE END", (0, 1.5, 5.2), 1.35, color=(1.0, 0.85, 0.2))
K.pop_obj(end, 3, 8)
cast = ["01", "02", "03", "04", "05", "06", "08", "09", "10", "11", "12"]
for i, k in enumerate(cast):
    back = i % 2
    x = -2.3 + 4.6 * (i // 2) / 5 + (0.46 if back else 0)
    y = 0.8 if back else -1.0
    p = K.puppet(k, (x, y, 0), height=1.7 if k != "01" else 2.1)
    K.pop(p, 4 + i * 2, 6)
    K.hop_to(p, 18 + i, F, (x, y, 0), hops=6, height=0.45, rock=8)
K.confetti("End", (0, 0.5, 4), 20, count=70, spread=6, rise=8, life=40)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (0, -8.6, 2.0), (0, 1, 2.7))
key_camera(cam, F, (0, -8.0, 2.0), (0, 1, 2.7))
render(os.environ.get("JAWS_OUT", "renders/shot17_end"))
