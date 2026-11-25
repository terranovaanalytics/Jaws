"""But another mean cherry guy stopped him. And he said, "Buh-bye!" """
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty
from jaws import kids as K
from jaws.soviet import speech_bubble

F = int(shot_seconds("shot15", 7.9) * FPS)
K.start(F)
K.make_land(seed=11, houses=5, trees=6)
K.make_sun_disc()
ped, gem = K.make_crystal("Cronchisk", (2.6, 1.5, 0), size=1.0)
K.spin(gem, 1, F, turns=1.5, axis=2)
so = K.puppet("11", (-2.6, -0.2, 0), height=2.4)
K.hop_to(so, 1, int(F * 0.12), (-1.8, -0.2, 0), hops=2, height=0.4)
mc = K.puppet("12", (0.6, -0.2, 12), height=3.0)
drop = int(F * 0.12) + 6
K.place(mc, 1, (0.6, -0.2, 12))
K.place(mc, drop - 10, (0.6, -0.2, 12))
K.place(mc, drop, (0.6, -0.2, 0))
K.squash(mc, drop, 0.35, 10)
K.squash(so, drop + 2, 0.3)
K.hop_to(so, drop + 6, drop + 18, (-2.4, -0.2, 0), hops=1, height=0.5)
K.bob(so, drop + 20, int(F * 0.78), amp=0.08, period=5, sway=8)
K.bob(mc, drop + 11, F, amp=0.04, period=12)
say = int(F * 0.75)
sb = speech_bubble("Bye", (-0.3, -1.5, 4.0), "BUH-BYE!", size=0.85)
K.pop_obj(sb, say, 6)
boot = int(F * 0.8)
K.squash(mc, boot - 4, 0.3, 6)
K.fly(so, boot, F, [(-2.4, -0.2, 0), (-5, 2, 5), (-9, 8, 12)], tilt=0, ease=False)
K.spin(so.card, boot, F, turns=2.5, axis=1)
K.vanish(so, F - 8, F)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (0, -9.5, 1.8), (0, 0.5, 2.4))
key_camera(cam, F, (-0.5, -9.3, 1.8), (-0.5, 0.5, 2.6))
add_shake(cam, drop, drop + 8, strength=0.12, rot_strength=0.01)
render(os.environ.get("JAWS_OUT", "renders/shot15_mean_cherry"))
