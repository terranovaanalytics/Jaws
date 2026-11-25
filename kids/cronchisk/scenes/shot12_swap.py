"""Shot 12: the Meanie barracks. Every Meanie bought extra arms from Jelly. Carrot, in a Meanie helmet,
sneaks down the line and disarms them all: pop, pop, pop, the extra arms drop off."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S

F = int(shot_seconds("shot12_swap", 5.5) * FPS)
S.lair(F)
times = [int(F * t / 5.5) for t in (1.0, 1.7, 2.4, 3.1, 3.8)]
xs = [-1.8, -0.9, 0.0, 0.9, 1.8]
ms = []
for i, x in enumerate(xs):
    m = A.make_meanie(f"Meanie{i}", (x, 2.0, 0), rot_z=0)
    col = [(0.9, 0.2, 0.2), (0.2, 0.5, 0.9), (0.3, 0.75, 0.3), (1.0, 0.75, 0.1), (0.95, 0.45, 0.8)][i]
    x = A.add_arms(m, color=col)
    A.arm(m, "l", 2, -90, frames=1, roll=-20)            # all four fists up, menacing
    A.arm(m, "r", 2, -90, frames=1, roll=20)
    A.arm(x, "l", 2, -60, frames=1, roll=-40)
    A.arm(x, "r", 2, -60, frames=1, roll=40)
    t = times[i]
    for k, side in enumerate(("arm_l", "arm_r")):        # the extra arms pop off and fall
        piv = getattr(x, side)
        drop = box(f"Dropped{i}{k}", (0.17, 0.19, 0.6), (0, 0, 0), mat(f"xarm_{col}", col))
        hand = box(f"DroppedH{i}{k}", (0.15, 0.15, 0.14), (0, 0, -0.35), m.mats["skin"], parent=drop)
        O.hide_at(piv, t + k * 2)
        O.show_at(drop, t + k * 2)
        sx = (k * 2 - 1) * 0.55
        O.move(drop, t + k * 2, t + k * 2 + 10, (xs[i] + sx, 2.0, 1.3), (xs[i] + sx * 1.6, 1.6, 0.1), ease=False)
        drop.keyframe_insert("rotation_euler", frame=t + k * 2)
        drop.rotation_euler = (math.radians(90), 0, math.radians(30 * (k * 2 - 1)))
        drop.keyframe_insert("rotation_euler", frame=t + k * 2 + 10)
    A.arm(m, "l", t + 4, -10, frames=4)                   # and the fight goes out of them
    A.arm(m, "r", t + 4, -10, frames=4)
    A.bounce(m, 1, F, amp=0.01, period=30 + i * 3)
    ms.append(m)
cr = A.make_carrot("Carrot", (-3.0, 1.1, 0), rot_z=-60, disguise=True)
pts = [(-3.0, 1.1, 0)] + [(x - 0.3, 1.1, 0) for x in xs] + [(3.0, 1.1, 0)]
key = [1] + [t - 4 for t in times] + [F - 4]
for (a, fa), (b_, fb) in zip(zip(pts, key), zip(pts[1:], key[1:])):
    O.move(cr.root, fa, fb, a, b_, ease=False)
A.walk(cr, 1, F, period=10, swing=30)
for t in times:
    A.arm(cr, "l", t - 2, -100, frames=3)
    A.arm(cr, "l", t + 3, -10, frames=3)
for i, (m, t) in enumerate(zip(ms, times)):
    A.look(m, int(F * 0.82) + i * 2, (i - 2) * 6, frames=6, tilt=28)   # everyone looks down at their carrot
cam = add_camera((0, -6, 2.8), (0, 2.0, 1.3), lens=24)
key_camera(cam, 1, (-0.4, -6.2, 2.8), (-0.3, 2.0, 1.2))
key_camera(cam, F, (0.4, -5.6, 2.6), (0.3, 2.0, 1.3))
render(os.environ.get("JAWS_OUT", "renders/shot12_swap"))
