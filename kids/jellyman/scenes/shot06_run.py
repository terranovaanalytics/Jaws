"""But then he was trapped... and run! (bubble drifts off, the other alien runs)"""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K

F = int(shot_seconds("shot06", 3.2) * FPS)
K.start(F)
K.make_land(seed=6, houses=6, trees=6)
K.make_sun_disc()
bub = K.bubble("Bubble", (-1.6, 3, 2.4), r=1.9)
a0 = K.puppet("03", (-1.6, 3, 1.0), height=2.6, name="Alien0")
for f in range(1, F + 1, 2):
    t = f / F
    x, z = -1.6 - 3 * t, 2.4 + 0.8 * t + 0.3 * math.sin(t * 9)
    bub.location = (x, 3, z)
    bub.keyframe_insert("location", frame=f)
    a0.root.location = (x, 3, z - 1.4)
    a0.root.keyframe_insert("location", frame=f)
    a0.pivot.rotation_euler[1] = math.radians(15 * math.sin(t * 14))
    a0.pivot.keyframe_insert("rotation_euler", index=1, frame=f)
a1 = K.puppet("03", (0.5, 0, 0), height=2.6, name="Alien1", rot_z=180)
K.squash(a1, 2, 0.3)
K.hop_to(a1, 6, F, (5.5, -0.5, 0), hops=8, height=0.6, rock=18)
dust = mat("kid_dust", (0.85, 0.8, 0.7))
for i in range(5):
    f = 10 + i * 8
    d = ico(f"Dust{i}", 0.35, (0.8 + i * 1.0, 0.2, 0.3), dust)
    d.scale = (0.001,) * 3
    d.keyframe_insert("scale", frame=f)
    d.scale = (1, 1, 1)
    d.keyframe_insert("scale", frame=f + 4)
    d.scale = (0.001,) * 3
    d.keyframe_insert("scale", frame=f + 16)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (0, -10, 2.2), (0, 1, 2.6))
key_camera(cam, F, (1.5, -10, 2.2), (1.5, 1, 2.6))
render(os.environ.get("JAWS_OUT", "renders/shot06_run"))
