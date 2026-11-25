"""Shot 04: HQ briefing. Director C points at the wall screen: WANTED, the Twins. Banana listens, case in hand."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S

F = int(shot_seconds("shot04_briefing", 5.0) * FPS)
from jaws.common import reset_scene
sc = reset_scene(F, world_color=(0.1, 0.08, 0.06))
O.dark_room(sc, ambient=0.3)
G, K, W, D, R = (0.45, 0.9, 0.3), (0.02, 0.02, 0.02), (1, 1, 1), (0.12, 0.25, 0.35), (0.85, 0.1, 0.1)
rows = [
    "DDDDDDDDDDDDDDDDDDDDDDDD",
    "DDDDGDDDDGDDDDGDDDDGDDDD",
    "DDDDDGDDGDDDDDDGDDGDDDDD",
    "DDDGGGGGGGDDDDGGGGGGGDDD",
    "DDDGKKGKKGDDDDGKKGKKGDDD",
    "DDDGKKGKKGDDDDGKKGKKGDDD",
    "DDDGGGGGGGDDDDGGGGGGGDDD",
    "DDDGGWWWGGDDDDGGWWWGGDDD",
    "DDDDKKKKKDDDDDDKKKKKDDDD",
    "DDDKKKWKKKDDDDKKKWKKKDDD",
    "DDDKKKWKKKDDDDKKKWKKKDDD",
    "DDDDDDDDDDDDDDDDDDDDDDDD",
]
pic = O.screen_picture("twins_pic", rows, {"G": G, "K": K, "W": W, "D": D})
hq = O.make_office("HQ", (0, 0, 0), screen_mat=pic)
from jaws.common import decal
hq["screen"].hide_render = True
decal("ScreenPic", pic, (5.0, 2.6), (0, 3.68, 3.5))
text("Wanted", "WANTED", (0, 3.6, 4.75), 0.42, mat("wanted_red", R, emit=3.0), bold=True)
O.point_light("ScreenGlow", (0, 2.6, 3.4), 300, (0.5, 0.9, 0.6), radius=2, shadow=False)
O.point_light("Key", (-2.5, -3, 4), 700, (1.0, 0.85, 0.7), radius=1)
O.point_light("Lamp", (1.1, 0.4, 1.7), 60, (0.6, 1.0, 0.6), radius=0.2, shadow=False)
d = A.make_director("Director", (0, 1.7, 0), rot_z=0)
b = A.make_banana("Banana", (0.75, -0.9, 0), rot_z=160)
held = O.make_briefcase("Held")
A.hold(b, held["root"], "l", offset=(0.0, 0.0, -0.3), rot=(-90, 0, 90))
held["root"].scale = (0.8, 0.8, 0.8)
P = int(F * 0.3)
A.look(d, P - 4, 70, frames=8)
A.arm(d, "l", P, -130, frames=8, roll=-60)
A.look(d, int(F * 0.75), 0, frames=8)
A.arm(d, "l", int(F * 0.8), 0, frames=8)
A.look(b, P + 6, -15, frames=8, tilt=-10)
A.bounce(b, 1, F, amp=0.02, period=40)
cam = add_camera((-1.4, -6.5, 2.6), (0, 1.5, 2.5), lens=30)
key_camera(cam, 1, (-1.4, -6.8, 2.6), (0.1, 1.5, 2.7))
key_camera(cam, F, (-0.7, -4.6, 2.6), (0.1, 1.8, 2.8))
render(os.environ.get("JAWS_OUT", "renders/shot04_briefing"))
