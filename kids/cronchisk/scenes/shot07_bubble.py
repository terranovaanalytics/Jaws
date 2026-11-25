"""Shot 07: Dr. Blip, trapped in his own force-field bubble, is floated out between the Twins. Alarms."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S
from jaws.soviet import alarm_light

F = int(shot_seconds("shot07_bubble", 4.5) * FPS)
S.lab_int(F)
bench = box("Bench", (4, 1.2, 1.0), (-4, 5, 0.5), mat("bench", (0.4, 0.42, 0.46)))
for k in range(3):
    from jaws.props import make_beaker
    make_beaker(f"Beaker{k}", (-5 + k * 0.8, 5, 1.0), color=[(0.4, 1, 0.3), (1, 0.4, 0.8), (0.3, 0.7, 1)][k])
alarm_light("Alarm1", (-3, 6.6, 5.5), 1, F, period=12, energy=700)
alarm_light("Alarm2", (4, 6.6, 5.5), 1, F, period=12, energy=700)
bub = ico("Bubble", 1.35, (0, 0, 0), A.glass("field_m", (0.5, 0.95, 1.0), 0.3, 1.0), subdiv=3)
for poly in bub.data.polygons:
    poly.use_smooth = True
ico("Shine", 0.2, (-0.6, -1.05, 0.6), mat("shine", (1, 1, 1), emit=2.5), parent=bub)
bl = A.make_blip("Blip", (0, 0, -0.95), rot_z=0)
bl.root.parent = bub
bl.root.scale = (0.8, 0.8, 0.8)
y = 2.2
O.move(bub, 1, F, (-3.2, y, 1.75), (2.4, y, 1.95), ease=False)
twins = []
for k, dx in enumerate((-1.55, 1.55)):
    t = A.make_twin(f"Twin{k}", (-3.2 + dx, y, 0), rot_z=-90)
    O.move(t.root, 1, F, (-3.2 + dx, y, 0), (2.4 + dx, y, 0), ease=False)
    A.walk(t, 1, F, period=16, swing=22)
    A.arm(t, "l" if k == 0 else "r", 4, -90, frames=3, roll=0)
    twins.append(t)
for k in range(5):                                       # Blip pounds on the bubble
    f = 8 + k * 18
    A.arms_up(bl, f, frames=4, deg=-150)
    A.arms_up(bl, f + 9, frames=4, deg=-100)
A.look(bl, 10, -20)
from jaws.soviet import sweat
sweat("Sweat", bl.head, 4, F, every=12)
cam = add_camera((0, -5, 2.2), (0, 2, 1.8), lens=26)
key_camera(cam, 1, (-2.0, -4.6, 2.1), (-1.6, 2, 1.8))
key_camera(cam, F, (1.6, -4.2, 2.1), (1.6, 2, 1.8))
render(os.environ.get("JAWS_OUT", "renders/shot07_bubble"))
