"""He especially saved the little kid. The little ... kid."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K

F = int(shot_seconds("shot09", 8.3) * FPS)
K.start(F)
K.make_land(seed=8, houses=4, trees=6)
K.make_sun_disc()
ship = K.puppet("07", (1.4, 2.5, 3.2), height=3.6)
for f in range(1, F + 1, 3):
    ship.root.location.z = 3.2 + 0.25 * math.sin(f / 9)
    ship.root.keyframe_insert("location", index=2, frame=f)
bm = K.beam("ShipBeam", (1.4, 2.5, 0), h=4.0, r=1.4, color=(0.9, 1.0, 0.5))
kid = K.puppet("08", (1.4, 2.3, 0), height=1.6)
ch = K.puppet("05", (-1.2, -0.8, 0), height=2.8)
grab = int(F * 0.3)
# the beam starts lifting the kid
for f in range(1, grab + 1, 2):
    kid.root.location = (1.4, 2.3, 1.6 * f / grab)
    kid.root.keyframe_insert("location", frame=f)
    kid.pivot.rotation_euler[1] = math.radians(12 * math.sin(f / 3))
    kid.pivot.keyframe_insert("rotation_euler", index=1, frame=f)
K.bob(ch, 1, int(F * 0.12), amp=0.05, period=10)
K.fly(ch, int(F * 0.12), grab, [(-1.2, -0.8, 0), (0.8, 1, 2.5), (1.4, 2.0, 1.2)], tilt=15)
save = int(F * 0.55)
K.fly(ch, grab, save, [(1.4, 2.0, 1.2), (0, 0.5, 3.5), (-1.9, -0.8, 0)], tilt=15)
K.fly(kid, grab, save, [(1.4, 2.3, 1.6), (0.3, 0.3, 3.9), (-0.6, -1.2, 0)], tilt=15)
K.hide(bm, grab + 6)
K.squash(ch, save, 0.3)
K.squash(kid, save, 0.4)
K.hop_to(kid, save + 8, F, (-0.6, -1.2, 0), hops=6, height=0.6, rock=10)
K.bob(ch, save + 9, F, amp=0.05, period=14)
K.sparkles("Hearts", (-0.6, -1.4, 1.6), save, F, every=4, radius=1.0, color=(1.0, 0.3, 0.5))
cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (0.0, -10.5, 2.4), (0.0, 1, 3.0), lens=26)
key_camera(cam, int(F * 0.6), (-0.3, -10, 2.0), (-0.3, 1, 2.6), lens=26)
key_camera(cam, F, (-1.0, -5.6, 1.2), (-1.0, 0, 1.5), lens=30)
render(os.environ.get("JAWS_OUT", "renders/shot09_kid"))
