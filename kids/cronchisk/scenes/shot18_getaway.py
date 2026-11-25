"""Shot 18: sunset. The mesa lair blows up; the Twins walk away with their pay and never look back."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S
from jaws.props import explosion
from jaws.fireworks import fire, flash_light

F = int(shot_seconds("shot18_getaway", 5.0) * FPS)
S.desert(F, sunset_sky=True)
B1, B2 = int(F * 1.0 / 5), int(F * 1.6 / 5)
rock = mat("lair_rock", (0.66, 0.34, 0.2))
box("LairMesa", (26, 14, 13), (0, 30, 6.5), rock)
box("LairMesa2", (30, 16, 3), (0, 30, 1.5), mat("lair_rock2", (0.58, 0.3, 0.18)))
door = box("Hangar", (8, 0.2, 5), (0, 22.9, 2.5), mat("hangar_glow", (0.75, 0.35, 1.0), emit=3.0))
explosion("Boom1", (-4, 22, 5), B1, size=7, count=24, life=26, seed=1)
explosion("Boom2", (5, 23, 9), B2, size=9, count=28, life=30, seed=2)
explosion("Boom3", (0, 24, 13), B2 + 10, size=8, count=22, life=28, seed=3)
flash_light("Flash1", (-4, 18, 6), B1, (1.0, 0.6, 0.3), energy=12000, decay=20)
flash_light("Flash2", (5, 18, 9), B2, (1.0, 0.6, 0.3), energy=16000, decay=24)
fire("Fire1", (-4, 22.5, 1), B1 + 6, F, size=2.5, seed=1)
fire("Fire2", (4, 22.5, 1), B2 + 6, F, size=3.0, seed=2)
twins = []
for k, x in enumerate((-0.7, 0.7)):
    t = A.make_twin(f"Twin{k}", (x, 9, 0), rot_z=0)
    O.move(t.root, 1, F, (x, 9, 0), (x, 1.8, 0), ease=False)
    A.walk(t, 1, F, period=18, swing=22)
    sack = empty(f"Sack{k}", (0, 0, 0))
    ico(f"SackBag{k}", 0.32, (0, 0, -0.25), mat("sack", (0.75, 0.65, 0.45)), parent=sack)
    text(f"SackSign{k}", "$", (0, -0.31, -0.25), 0.36, mat("dollar", (0.1, 0.5, 0.15), emit=0.6), parent=sack,
         bold=True)
    A.hold(t, sack, "r" if k == 0 else "l")
    twins.append(t)
for t in twins:
    A.look(t, 2, 0, tilt=-6)
shades = mat("pilot_shades", (0.02, 0.02, 0.03))
for t in twins:                                           # and they put on shades
    sh = box(f"{t.name}_shades", (0.48, 0.05, 0.1), (0, -0.23, 0.25), shades)
    sh.parent = t.head
    O.show_at(sh, B2 + 20)
cam = add_camera((0, -5, 0.8), (0, 8, 3), lens=26)
key_camera(cam, 1, (0, -5.5, 0.6), (0, 10, 3.8))
key_camera(cam, F, (0, -4.0, 0.9), (0, 8, 3.0))
add_shake(cam, B1, B1 + 8, strength=0.12, rot_strength=0.01)
add_shake(cam, B2, B2 + 10, strength=0.18, rot_strength=0.014, seed=2)
render(os.environ.get("JAWS_OUT", "renders/shot18_getaway"))
