"""...because he was in somewhere. (X-ray: the carrot is inside the cool man.)"""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K

F = int(shot_seconds("shot12", 4.6) * FPS)
K.start(F)
K.make_land(seed=10, houses=5, trees=7)
K.make_sun_disc()
cool = K.puppet("10", (0, 0.2, 0), height=3.4)
K.hop_to(cool, 1, F, (0.6, 0.2, 0), hops=5, height=0.15, rock=4)
# a round x-ray window on his tummy with the little carrot wiggling inside
win = cyl("XRay", 0.62, 0.02, (0.04, -0.06, 1.7), mat("kid_xray", (0.1, 0.12, 0.25), emit=0.5), n=24,
          rot=(90, 0, 0), parent=cool.root)
mini = K.puppet("09", (0.05, -0.1, 1.15), height=1.05, name="MiniCarrot")
mini.root.parent = cool.root
for f in range(1, F + 1, 2):
    mini.pivot.rotation_euler[1] = math.radians(18 * math.sin(f / 2.5))
    mini.pivot.keyframe_insert("rotation_euler", index=1, frame=f)
help_ = K.label("Help", "HELP!", (0.6, -0.5, 3.4), 0.5, color=(1, 1, 1))
help_.parent = cool.root
K.pop_obj(help_, int(F * 0.3), 6)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=30)
key_camera(cam, 1, (0, -8, 1.6), (0, 0.2, 2.0))
key_camera(cam, F, (0.5, -5.8, 1.6), (0.5, 0.2, 2.0))
render(os.environ.get("JAWS_OUT", "renders/shot12_inside"))
