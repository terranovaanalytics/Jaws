"""Shot 00: midnight, Pier 9. Rain, neon; Jelly waddles along the dock to the warehouse."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S

F = int(shot_seconds("shot00_harbor", 6.0) * FPS)
S.harbor_ext(F)
j = A.make_jelly("Jelly", (-3.2, -2.0, 0.6), rot_z=200)
for f in range(1, F + 1, 2):
    t = f / F
    j.root.location = (-3.2 + 1.6 * t, -2.0 + 9.0 * t, 0.6)
    j.root.keyframe_insert("location", frame=f)
A.walk(j, 1, F, period=16, swing=20)
A.wobble(j, 1, F, amp=0.05, period=16)
cam = add_camera((0, -16, 9), (0, 6, 2), lens=30)
key_camera(cam, 1, (1.5, -15, 9.5), (-1, 5, 1.5))
key_camera(cam, F, (0.5, -8.5, 2.6), (-1.5, 6, 2.2))
render(os.environ.get("JAWS_OUT", "renders/shot00_harbor"))
