"""Shot 19: the yacht at sunset. Everyone toasts; Jelly sulks in a jar. THE END. Agent Banana will return."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S
from jaws.world import make_ocean
from jaws.fireworks import firework

F = int(shot_seconds("shot19_end", 6.5) * FPS)
from jaws.common import reset_scene
sc = reset_scene(F)
O.sunset(sc, energy=2.4, rot=(78, 0, 170))
make_ocean(color=(0.12, 0.25, 0.45), wave=0.25)
y = O.make_yacht("Yacht", (0, -1.5, 0), rot_z=-90)
DZ = 1.1
TOAST, END1, END2 = int(F * 1.2 / 6.5), int(F * 0.5), int(F * 0.66)
cast = [
    (A.make_blip, (-0.8, -4.0), 0), (A.make_director, (0.8, -4.0), 0),
    (A.make_banana, (-1.2, -5.2), 10), (A.make_cherry, (0.0, -5.3), 0), (A.make_dark_cherry, (1.2, -5.2), -10),
    (A.make_pocket, (-1.1, -6.5), 5), (A.make_carrot, (0.05, -6.5), -5),
]
people = []
for i, (mk, (x, yy), rz) in enumerate(cast):
    p = mk(mk.__name__[5:].title(), (x, yy, DZ), rot_z=rz)
    dr = O.make_glass_drink(f"Drink{i}", color=[(1, 0.6, 0.2), (0.9, 0.2, 0.3), (0.4, 0.8, 1.0)][i % 3])
    A.hold(p, dr, "r", offset=(0, -0.05, 0.1))
    A.arm(p, "r", 4, -40, frames=2)
    A.arm(p, "r", TOAST + i, -135, frames=6, roll=-15 if p.root.location.x > 0 else 15)
    A.arm(p, "r", TOAST + 22 + i, -50, frames=8)
    A.bounce(p, 1, F, amp=0.03, period=20 + i * 2)
    people.append(p)
# Jelly, captured, in a big jar
jar = cyl("Jar", 0.6, 1.5, (1.25, -6.6, DZ + 0.75), A.glass("jar_glass", (0.8, 0.95, 1.0), 0.22, 0.5), n=14)
cyl("JarLid", 0.64, 0.12, (1.25, -6.6, DZ + 1.55), mat("jar_lid", (0.75, 0.75, 0.8), metal=0.8), n=14)
j = A.make_jelly("Jelly", (1.25, -6.6, DZ + 0.05), rot_z=-30)
j.root.scale = (0.5,) * 3
A.wobble(j, 1, F, amp=0.05, period=22)
A.look(j, 30, -30, tilt=15)
A.arm(j, "l", 30, -10, frames=1)
from jaws.world import bob
bob(y["root"], 1, F, period=60, roll=1.0, pitch=0.5, heave=0.08)
gold = mat("end_gold", (1.0, 0.82, 0.3), emit=1.8)
pink = mat("end_pink", O.PINK, emit=2.0)
t1 = text("TheEnd", "THE END", (0, 14, 9.5), 2.0, gold, extrude=0.25, bold=True)
t2 = text("Return", "AGENT BANANA\nWILL RETURN", (0, 14, 6.9), 0.8, pink, extrude=0.1, bold=True)
O.show_at(t1, END1)
O.show_at(t2, END2)
for k, (x, f) in enumerate(((-6, END1 - 6), (5, END1 + 6), (-2, END2 + 4), (7, END2 + 14))):
    firework(f"FW{k}", (x, 30, 0), (x, 30, 14 + k), f, color=[(1, 0.4, 0.7), (1, 0.85, 0.3), (0.5, 0.8, 1)][k % 3],
             seed=k)
cam = add_camera((0, -14, 3.5), (0, -5, 2.2), lens=32)
key_camera(cam, 1, (0.3, -13.0, 5.2), (0.1, -5.0, 2.3))
key_camera(cam, END1 - 10, (0.2, -14.0, 5.0), (0.1, -4.5, 2.9))
key_camera(cam, F, (0, -16.0, 3.8), (0, 2, 6.0))
render(os.environ.get("JAWS_OUT", "renders/shot19_end"))
