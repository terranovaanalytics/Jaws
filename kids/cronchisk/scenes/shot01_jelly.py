"""Shot 01: inside Pier 9. A Meanie opens the briefcase: the Cronchisk blueprints glow pink; Jelly wobbles with glee."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S

F = int(shot_seconds("shot01_jelly", 5.0) * FPS)
S.warehouse_int(F)
OPEN = int(F * 0.25)
m = A.make_meanie("Meanie", (-1.25, 0.6, 0), rot_z=70)
j = A.make_jelly("Jelly", (1.45, 0.2, 0), rot_z=-55)
case = O.make_briefcase("Case", (0, 0.5, 1.1))
case["root"].rotation_euler[2] = math.radians(180)
O.open_case(case, OPEN, frames=10, deg=105)
glow = O.point_light("CaseGlow", (0, 0.5, 1.6), 0, O.PINK, radius=0.3, shadow=False)
glow.data.keyframe_insert("energy", frame=OPEN)
glow.data.energy = 220
glow.data.keyframe_insert("energy", frame=OPEN + 10)
A.arm(m, "l", OPEN - 2, -60)
A.arm(m, "r", OPEN - 2, -60)
A.arm(m, "l", OPEN + 14, -10)
A.arm(m, "r", OPEN + 14, -10)
A.lean(j, OPEN + 10, 18, frames=8)
A.wobble(j, 1, OPEN + 10, amp=0.03, period=20)
A.wobble(j, OPEN + 12, F, amp=0.12, period=6, seed=2)          # glee
for k in range(3):
    A.arm(j, "l", OPEN + 16 + k * 12, -70, frames=6, roll=-30)
    A.arm(j, "l", OPEN + 22 + k * 12, -40, frames=6, roll=10)
    A.arm(j, "r", OPEN + 16 + k * 12, -70, frames=6, roll=30)
    A.arm(j, "r", OPEN + 22 + k * 12, -40, frames=6, roll=-10)
A.look(m, OPEN + 20, -30)
cam = add_camera((0, -7, 2.6), (0.4, 0.5, 1.6), lens=35)
key_camera(cam, 1, (0.6, -7.5, 2.8), (0.4, 0.5, 1.6))
key_camera(cam, F, (0.2, -5.0, 2.3), (0.7, 0.4, 1.8))
render(os.environ.get("JAWS_OUT", "renders/shot01_jelly"))
