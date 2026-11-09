"""Shot 10: Brody's mechanical shark sub tails a line of sharks across the
open sea, through the tunnel and into a cave... the camera follows and tilts
up: the cave ends right underneath the bookstore."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import add_camera, key_camera, render, FPS, shot_seconds, mat, box
from jaws.shark import make_shark, swim_wag
from _cave import build_cave, follow, label, TUNNEL

F = int(shot_seconds("shot10", 7.1) * FPS)
s, cave, store = build_cave(F)
tx, tz = TUNNEL
N = 6
for i in range(N + 1):
    mech = i == N
    sh = make_shark(f"S{i}", scale=2.4 if mech else 1.7, variant="mech" if mech else "real")
    lag = i * 0.075
    y = 1.0 + (i % 3) * 0.9
    loop_x = -8 + (i % 4) * 3.5
    pts = [(52, y, -9 - (i % 2)), (tx + 3, y, tz), (tx - 6, y, tz + 1), (loop_x + 2, y, -11 + (i % 3)),
           (loop_x - 2, y, -12.5 + (i % 3) * 0.5)]
    if mech:
        pts = [(58, 1.6, -9.5), (tx + 3, 1.6, tz), (tx - 6, 1.6, tz + 1.5), (5.5, 1.6, -9.5)]
    f0 = 1
    f1 = int(F * (0.62 + lag * 0.5)) if not mech else int(F * 0.8)
    start_off = int(F * lag)
    sh.root.location = pts[0]
    sh.root.rotation_euler[2] = math.pi
    follow(sh.root, [pts[0]] + pts, f0 + start_off, f1)
    swim_wag(sh, 1, F, period=14 if mech else 10, angle=10 if mech else 24, seed=i)

lab = label("LblStore", "BOOKSTORE", (0, -2.5, 12.6), 1.7, color=(1, 0.9, 0.1))
label("LblCave", "SHARK CAVE", (-3.8, -3.4, -5.6), 1.0)
yl = mat("label_yellow", (1, 0.9, 0.1), emit=1.0)
box("Arrow", (0.25, 0.1, 3.5), (0, -3.4, -2.3), yl)
label("LblArrowHead", "V", (0, -3.4, -4.1), 1.4)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (44, -22, -8), (40, 0, -9.5))
key_camera(cam, int(F * 0.35), (22, -24, -9), (16, 0, -11))
key_camera(cam, int(F * 0.62), (6, -27, -9), (3, 0, -10))
key_camera(cam, int(F * 0.78), (2, -30, -6), (1, 0, -6))
key_camera(cam, F, (1, -34, -1), (0.5, 0, 0))
render(os.environ.get("JAWS_OUT", "renders/shot10_mech_cave"))
