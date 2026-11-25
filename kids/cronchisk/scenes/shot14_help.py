"""Shot 14: inside the jelly. Tiny Carrot, floating in purple, whispers into his wrist radio: HELP!"""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S
import random
from jaws.soviet import speech_bubble

F = int(shot_seconds("shot14_help", 4.0) * FPS)
S.lair(F)
j = A.make_jelly("Jelly", (0, 1.5, 0), rot_z=-10)
A.wobble(j, 1, F, amp=0.06, period=14)
inside = A.make_carrot("Inside", (0, -0.05, 0.12))
inside.root.parent = j.body
inside.root.scale = (0.42,) * 3
for f in range(1, F + 1, 4):                           # floating
    inside.root.location.z = 0.12 + 0.05 * math.sin(f / 6)
    inside.root.rotation_euler[1] = math.radians(8 * math.sin(f / 9))
    inside.root.keyframe_insert("location", index=2, frame=f)
    inside.root.keyframe_insert("rotation_euler", index=1, frame=f)
RADIO = int(F * 0.25)
A.arm(inside, "r", RADIO, -140, frames=6, roll=-35)
A.look(inside, RADIO, 10, tilt=-10)
A.arm(inside, "l", RADIO + 4, -60, frames=6)
watch = box("Watch", (0.14, 0.16, 0.08), (0, 0, 0), mat("watch_led", (0.3, 1.0, 0.4), emit=3.0))
A.hold(inside, watch, "r", offset=(0, 0, 0.18))
rnd = random.Random(2)
bm = A.glass("bub_m", (0.9, 0.8, 1.0), 0.45, 1.5)
for i in range(14):
    b = ico(f"Bub{i}", rnd.uniform(0.03, 0.07), (0, 0, 0), bm)
    b.parent = j.body
    x, f0 = rnd.uniform(-0.35, 0.35), rnd.randint(1, F - 30)
    O.move(b, f0, f0 + 30, (x, -0.25, 0.1), (x + 0.1, -0.25, 1.0), ease=False)
    O.show_at(b, f0, f0 + 30)
sb = speech_bubble("Help", (0.15, 0.7, 2.3), "HELP!", size=0.3)
O.show_at(sb, RADIO + 8)
cam = add_camera((0, -3, 1.4), (0, 1.5, 1.0), lens=35)
key_camera(cam, 1, (0.2, -3.0, 1.2), (0.0, 1.5, 0.9))
key_camera(cam, F, (0.1, -2.2, 1.3), (0.1, 1.5, 1.05))
render(os.environ.get("JAWS_OUT", "renders/shot14_help"))
