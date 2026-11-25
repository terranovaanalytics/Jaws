"""Shot 01: inside Pier 9. Jelly is an arms dealer: the briefcase is full of spare arms. The Meanie buys a pair,
they pop on, and he waves all four. Jelly wobbles with glee."""
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
DEAL = int(F * 0.45)
A.arm(m, "l", OPEN - 2, -60)
A.arm(m, "r", OPEN - 2, -60)
A.arm(m, "l", OPEN + 14, -10)
A.arm(m, "r", OPEN + 14, -10)
A.look(m, OPEN + 8, -10, tilt=20)                        # peeks into the case
for k in (1, 2):
    O.hide_at(case["arms"][k], DEAL)
x = A.add_arms(m, color=(0.9, 0.2, 0.2))
for side in ("arm_l", "arm_r"):                         # the new arms pop on
    piv = getattr(x, side)
    for df, k in ((-1, 0.001), (0, 0.001), (4, 1.3), (7, 1.0)):
        piv.scale = (k,) * 3
        piv.keyframe_insert("scale", frame=DEAL + 2 + df)
pop = text("Pop", "POP!", (-0.7, 0.2, 2.9), 0.45, mat("pop_txt", (1.0, 0.85, 0.1), emit=2.0), bold=True, extrude=0.05)
O.show_at(pop, DEAL + 2, DEAL + 16)
A.look(m, DEAL + 10, 30, tilt=10)                        # admires them
for k in range(4):                                      # waves all four arms
    f = DEAL + 14 + k * 10
    A.arm(m, "l", f, -150, frames=5, roll=-20)
    A.arm(x, "r", f, -150, frames=5, roll=20)
    A.arm(m, "r", f, -40, frames=5)
    A.arm(x, "l", f, -40, frames=5)
    A.arm(m, "r", f + 5, -150, frames=5, roll=20)
    A.arm(x, "l", f + 5, -150, frames=5, roll=-20)
    A.arm(m, "l", f + 5, -40, frames=5)
    A.arm(x, "r", f + 5, -40, frames=5)
A.wobble(j, 1, DEAL, amp=0.03, period=20)
A.wobble(j, DEAL + 2, F, amp=0.12, period=6, seed=2)    # glee: business is good
A.arm(j, "r", DEAL - 8, -70, frames=6)                  # hands them over
spare = empty("Spare", (0, 0, 0))
box("SpareSleeve", (0.13, 0.13, 0.62), (0, 0, -0.1), mat("xarm_(0.9, 0.2, 0.2)", (0.9, 0.2, 0.2)), parent=spare)
box("SpareHand", (0.14, 0.14, 0.14), (0, 0, 0.27), mat("case_hand", (0.95, 0.76, 0.62)), parent=spare)
A.hold(j, spare, "r", offset=(0, -0.05, 0))
O.show_at(spare, OPEN + 14, DEAL + 1)
A.arm(j, "r", OPEN + 18, -150, frames=6, roll=10)      # holds a spare arm up: "Arms. Fresh."
A.arm(j, "r", DEAL + 4, -20, frames=6)
cam = add_camera((0, -7, 2.6), (0.4, 0.5, 1.6), lens=35)
key_camera(cam, 1, (0.7, -6.6, 3.5), (0.4, 0.4, 1.3))
key_camera(cam, int(F * 0.4), (0.3, -5.4, 3.3), (0.2, 0.5, 1.4))
key_camera(cam, F, (-0.3, -4.5, 2.7), (-0.3, 0.5, 1.7))
render(os.environ.get("JAWS_OUT", "renders/shot01_jelly"))
