"""Shot 9: "Mr. President, played by Tom Brady, the Russians are making
radioactive mutant sharks and attacking my island. I need backup." The Oval
Office. Over Brody's shoulder at the President behind the big desk (cast
card on "played by Tom Brady"); the camera swings round to the side as
Brody points, throws his arms up, then begs."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import reset_scene, add_sun, add_camera, key_camera, render, FPS, shot_seconds, box, mat
from jaws.people import make_brody
from jaws.spy import make_oval_office, make_president
from jaws.town import make_flag
from _sets import face, glow_light

F = int(shot_seconds("shot09", 6.3) * FPS)
reset_scene(F, world_color=(0.85, 0.82, 0.70))
add_sun((40, 0, 160), energy=1.6)
o = make_oval_office()
glow_light("RoomFill", (0, -1, 5), (1.0, 0.92, 0.8), 1800, radius=4)
glow_light("WindowGlow", (0, 5.5, 3), (0.9, 0.95, 1.0), 900, radius=3)
make_flag("USFlag", (-2.4, 5.6, 0), size=0.9, pole=3.0, wave=False)
make_flag("USFlag2", (2.4, 5.6, 0), size=0.9, pole=3.0, rot_z=180, wave=False)
px, py, _ = o["behind"]
p = make_president("President", loc=(px, py - 0.2, 0), rot_z=0)
for arm in (p.arm_l, p.arm_r):                          # hands planted on the desk
    arm.rotation_euler = (math.radians(-38), 0, 0)
fx, fy, _ = o["front"]
b = make_brody("Brody", loc=(fx, fy + 0.4, 0), rot_z=180)
POINT = int(F * 0.16)            # "the Russians are making..."
ARMS = int(F * 0.66)             # "...attacking my island"
BEG = int(F * 0.86)              # "I need backup"
face(b.arm_r, POINT - 4, 0, axis=0)
face(b.arm_r, POINT, -85, axis=0)
f = POINT
while f < ARMS - 6:              # jabbing finger
    face(b.arm_r, f, -85, axis=0)
    face(b.arm_r, f + 3, -70, axis=0)
    f += 6
for arm, s in ((b.arm_l, 1), (b.arm_r, -1)):
    face(arm, ARMS - 2, -70 if arm is b.arm_r else 0, axis=0)
    face(arm, ARMS + 3, -165, axis=0)               # arms up!
    face(arm, BEG - 2, -165, axis=0)
    face(arm, BEG + 3, -60, axis=0)                 # pleading, palms out
    face(arm, BEG + 3, s * 25, axis=1)
face(b.torso, BEG - 2, 0, axis=0)
face(b.torso, BEG + 4, 12, axis=0)
face(p.head, 1, 0, axis=2)
face(p.head, ARMS + 2, 0, axis=2)
face(p.head, ARMS + 6, 10, axis=1)              # tilts his head
cam = add_camera((0, 0, 0), (0, 0, 0), lens=30)
hx, hy = fx, fy + 0.4
key_camera(cam, 1, (hx + 0.9, hy - 2.8, 2.6), (px, py, 2.0))
key_camera(cam, int(F * 0.45), (hx + 1.6, hy - 2.4, 2.4), (px, py - 0.6, 1.9))
key_camera(cam, F, (5.5, 2.6, 2.1), (0, 2.6, 1.6))
render(os.environ.get("JAWS_OUT", "renders/shot09_president"))
