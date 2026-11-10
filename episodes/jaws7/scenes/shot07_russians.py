"""Shot 7: "And guess who it is? It's the frickin' Russians!" Slow push along
the sub's black sail to the big red star... a sailor in a fur hat pops up in
the lit window and gives a little wave. Dramatic jolt on "Russians"."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import add_camera, key_camera, add_shake, render, FPS, shot_seconds
from jaws.spy import make_russian
from _sets import wave, glow_light
from _deepsub import build_deepsub, SUB, SCALE

F = int(shot_seconds("shot07", 2.9) * FPS)
HIT = int(F * 0.42)                         # "It's the frickin' Russians!"
s, sub = build_deepsub(F, lights_on=1, flood=15000)
sx, sz = SUB[0] + 5 * SCALE, SUB[2] + 3 * SCALE      # sail base
star = (SUB[0] + 6.6 * SCALE, SUB[1] - 0.95 * SCALE, SUB[2] + 5.4 * SCALE)
top = SUB[2] + 7.75 * SCALE                     # pops up over the top of the sail
r = make_russian("Ivan", loc=(sx - 2.0, SUB[1], top - 5.0), rot_z=0, seed=0, stache=True)
r.root.scale = (1.4,) * 3
r.root.keyframe_insert("location", frame=1)
r.root.keyframe_insert("location", frame=HIT - 3)
r.root.location.z = top
r.root.keyframe_insert("location", frame=HIT + 1)
wave(r, HIT + 2, F, period=6)
glow_light("StarLight", (star[0], star[1] - 6, star[2] + 1), (1.0, 0.9, 0.8), 1500, radius=2)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=30)
key_camera(cam, 1, (star[0] + 10, star[1] - 22, star[2] - 2), (star[0], star[1], star[2] + 0.5))
key_camera(cam, HIT, (star[0] + 3, star[1] - 15, star[2] - 1), (star[0] - 1.5, star[1], star[2] + 2.4))
key_camera(cam, F, (star[0] + 1, star[1] - 12, star[2] - 0.5), (star[0] - 2.5, star[1], star[2] + 3.0))
add_shake(cam, HIT, HIT + 8, strength=0.3, rot_strength=0.02)
render(os.environ.get("JAWS_OUT", "renders/shot07_russians"))
