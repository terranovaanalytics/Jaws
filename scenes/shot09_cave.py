"""Shot 9: cutaway diagram. Tilt down from the Flying Horses carousel, through
the dirt, into a giant underwater cave packed with circling sharks."""
import math, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
from jaws.common import (reset_scene, add_sun, add_camera, key_camera, render, FPS, shot_seconds,
                         text, mat, box)
from jaws.props import make_carousel, animate_carousel, make_cave_cutaway
from jaws.shark import make_shark, swim_wag

F = int(shot_seconds("shot09", 6.0) * FPS)
reset_scene(F, world_color=(0.45, 0.75, 1.0))
add_sun((40, 0, 20), energy=2.4)
cave = make_cave_cutaway()
c = make_carousel(loc=(0, 1.5, 0))
animate_carousel(c, 1, F)

rnd = random.Random(9)
(x0, x1), (z0, z1) = cave["interior"]
for i in range(14):
    sh = make_shark(f"CaveShark{i}", scale=rnd.uniform(1.3, 1.8))
    cx, cz = rnd.uniform(-5, 5), rnd.uniform(-11, -9)
    rx, rz = rnd.uniform(4, 8), rnd.uniform(1.5, 3.5)
    y = rnd.uniform(0.0, 4.0)
    a0, spd = rnd.uniform(0, 6.28), rnd.choice((-1, 1)) * rnd.uniform(0.8, 1.3)
    for f in range(1, F + 1, 2):
        a = a0 + spd * f / FPS
        sh.root.location = (cx + rx * math.cos(a), y, cz + rz * math.sin(a))
        dx, dz = -rx * math.sin(a) * spd, rz * math.cos(a) * spd    # velocity direction
        sh.root.rotation_euler = (0, -math.atan2(dz, abs(dx)), 0 if dx > 0 else math.pi)
        sh.root.keyframe_insert("location", frame=f)
        sh.root.keyframe_insert("rotation_euler", frame=f)
    swim_wag(sh, 1, F, period=10, seed=i)

lbl = mat("label_white", (1, 1, 1), emit=1.0)
text("LblCave", "SHARK CAVE", (-7, -3.4, -14.6), 1.1, lbl, extrude=0.05)
box("Arrow", (0.25, 0.1, 3.5), (0, -3.4, -2.3), mat("label_yellow", (1, 0.9, 0.1), emit=1.0))
text("LblArrow", "V", (0, -3.4, -4.1), 1.4, mat("label_yellow", (1, 0.9, 0.1), emit=1.0), extrude=0.05)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
T = int(F * 0.35)
key_camera(cam, 1, (0, -24, 6), (0, 0, 4))
key_camera(cam, T, (0, -26, 3), (0, 0, 1))
key_camera(cam, F, (0, -30, -6), (0, 0, -7))
render(os.environ.get("JAWS_OUT", "renders/shot09_cave"))
