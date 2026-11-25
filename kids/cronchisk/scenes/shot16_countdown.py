"""Shot 16: Someone drops the Cronchisk into the doomsday uplink. The dish powers up; the countdown starts."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S
from jaws.soviet import alarm_light

F = int(shot_seconds("shot16_countdown", 5.0) * FPS)
S.lair(F, purple=False)
O.point_light("SidePurple", (-5, 1, 6), 700, (0.75, 0.35, 1.0), radius=2, shadow=False)
PLACE, POWER, COUNT = int(F * 1.4 / 5), int(F * 1.6 / 5), int(F * 2.0 / 5)
dd = O.make_doomsday("DD", (0, 4.2, 0))
so = A.make_someone("Someone", (-1.0, 1.6, 0), rot_z=150)
held = O.make_cronchisk("Held", size=0.32, light=150)
A.hold(so, held, "r", offset=(0, -0.1, -0.05))
A.arm(so, "r", PLACE - 10, -95, frames=10, roll=-20)
O.hide_at(held, PLACE)
sock = O.make_cronchisk("Socketed", (0, 2.9, 2.25), size=0.32, light=0)
O.show_at(sock, PLACE)
glow = O.point_light("SockGlow", (0, 2.6, 2.6), 0, O.PINK, radius=0.5, shadow=False)
glow.data.keyframe_insert("energy", frame=POWER - 1)
glow.data.energy = 350
glow.data.keyframe_insert("energy", frame=POWER + 6)
A.arm(so, "r", PLACE + 10, -20, frames=8)
A.turn(so, PLACE + 18, 200, frames=10)                   # turns to us, triumphant
A.arms_up(so, PLACE + 26, frames=6, deg=-150)
A.bounce(so, PLACE + 30, F, amp=0.06, period=10)          # evil laugh
ring = cyl("DishRing", 1.6, 0.05, (0, 0, 0), mat("dish_glow", O.PINK, emit=5.0), n=16)
ring.parent = dd["dish"]
ring.location = (0, 0, 0.42)
O.show_at(ring, POWER)
O.countdown("Count", (0, 2.6, 2.9), COUNT, 14, [10, 9, 8, 7, 6, 5], size=0.6)
for k, x in enumerate((-4, 4)):
    alarm_light(f"Alarm{k}", (x, 7.4, 5.0), COUNT, F, period=12, energy=800)
cam = add_camera((0, -6, 1.2), (0, 3, 3), lens=26)
key_camera(cam, 1, (-1.5, -5.6, 1.3), (-0.4, 3, 2.6))
key_camera(cam, F, (0.6, -4.4, 1.0), (0, 3, 3.2))
render(os.environ.get("JAWS_OUT", "renders/shot16_countdown"))
