"""Shot 17: 4... 3... 2... DARK CHERRY drops in and yanks the Cronchisk out. Deep cover all along."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S
from jaws.soviet import alarm_light, sweat

F = int(shot_seconds("shot17_dark_cherry", 5.0) * FPS)
S.lair(F, purple=False)
O.point_light("SidePurple", (-5, 1, 6), 700, (0.75, 0.35, 1.0), radius=2, shadow=False)
DROP, LAND, YANK = int(F * 0.9 / 5), int(F * 1.3 / 5), int(F * 1.6 / 5)
BADGE = int(F * 0.66)
dd = O.make_doomsday("DD", (0, 4.2, 0))
ring = cyl("DishRing", 1.6, 0.05, (0, 0, 0), mat("dish_glow", O.PINK, emit=5.0), n=16)
ring.parent = dd["dish"]
ring.location = (0, 0, 0.42)
O.hide_at(ring, YANK + 2)
nums = O.countdown("Count", (0, 2.6, 2.9), 1, 12, [4, 3, 2], size=0.6)
O.hide_at(nums[-1], YANK + 2)
off = text("CountOff", "- -", (0, 2.6, 2.9), 0.6, mat("count_off", (0.4, 0.4, 0.45), emit=1.0), bold=True)
O.show_at(off, YANK + 2)
sock = O.make_cronchisk("Socketed", (0, 2.9, 2.25), size=0.32, light=250)
O.hide_at(sock, YANK)
for k, x in enumerate((-4, 4)):
    al = alarm_light(f"Alarm{k}", (x, 7.4, 5.0), 1, YANK, period=12, energy=800)
so = A.make_someone("Someone", (-1.3, 1.5, 0), rot_z=20)
A.arms_up(so, 2, frames=1, deg=-150)
A.arm(so, "l", YANK + 4, -60, frames=4, roll=-40)        # shocked
A.arm(so, "r", YANK + 4, -60, frames=4, roll=40)
A.lean(so, YANK + 6, -15, frames=4)
A.look(so, YANK + 2, -50)
sweat("Sweat", so.head, YANK + 4, F, every=8)
dc = A.make_dark_cherry("DarkCherry", (0.9, 2.1, 7), rot_z=-160)
O.move(dc.root, DROP, LAND, (0.9, 2.1, 7), (0.9, 2.1, 0), ease=False)
dc.root.keyframe_insert("location", frame=1)
A.arms_up(dc, DROP, frames=1, deg=-175)
A.lean(dc, LAND + 1, 30, frames=1)
A.lean(dc, LAND + 8, 0, frames=6)
A.arm(dc, "l", LAND + 1, -30, frames=2)
A.arm(dc, "r", YANK, -95, frames=4, roll=15)
taken = O.make_cronchisk("Taken", size=0.32, light=300)
A.hold(dc, taken, "r", offset=(0, -0.1, -0.05))
O.show_at(taken, YANK)
A.arm(dc, "r", YANK + 10, -150, frames=8, roll=10)       # holds it up high
A.turn(dc, YANK + 14, -20, frames=10)
badge = box("Badge", (0.22, 0.04, 0.28), (0, 0, 0), mat("badge_gold", (1.0, 0.8, 0.2), metal=0.8, rough=0.3))
A.hold(dc, badge, "l", offset=(0, -0.08, 0.05))
O.show_at(badge, BADGE)
A.arm(dc, "l", BADGE + 6, -100, frames=8, roll=-25)
cam = add_camera((0, -6, 1.6), (0, 2.5, 2.2), lens=28)
key_camera(cam, 1, (0.3, -5.6, 1.5), (0.2, 2.5, 2.6))
key_camera(cam, YANK, (0.3, -5.2, 1.6), (0.3, 2.4, 2.1))
key_camera(cam, F, (0.7, -3.8, 1.7), (0.6, 2.2, 2.1))
add_shake(cam, LAND, LAND + 6, strength=0.12, rot_strength=0.012)
render(os.environ.get("JAWS_OUT", "renders/shot17_dark_cherry"))
