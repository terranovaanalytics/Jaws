"""Shot 5: the grand finale is going off when a fin streaks in and a shark
rams the fireworks barge. It rocks... and tips onto its side."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import add_camera, key_camera, add_shake, render, FPS, shot_seconds
from jaws.world import splash
from jaws.shark import make_shark, open_jaw, swim_wag
from _harbor import build_harbor, show, BARGE, tip_barge, TIP

F = int(shot_seconds("shot05", 4.4) * FPS)
HIT = int(F * 0.35)
TIPF = int(F * 0.74)
h = build_harbor(F)
show(h["barge"], 1, TIPF - 2, every=6, seed=5, finale=True)
bx, by, bz = BARGE
br = h["barge"]["root"]
for f, roll, z in [(1, 0, 0), (HIT, 0, 0), (HIT + 4, 9, 0.3), (HIT + 10, -6, -0.1), (HIT + 18, 4, 0),
                   (TIPF - 4, -8, 0), (TIPF + 2, TIP * 0.7, -0.4), (TIPF + 6, TIP * 1.08, -0.7), (TIPF + 10, TIP, -0.6)]:
    br.rotation_euler[0] = math.radians(roll)
    br.location.z = z
    br.keyframe_insert("rotation_euler", index=0, frame=f)
    br.keyframe_insert("location", index=2, frame=f)

S = 5.0
sh = make_shark("Shark", scale=S)
path = [(1, (bx - 26, by - 9, -2.3), 0, 8), (HIT - 14, (bx - 9, by - 7.5, -2.3), 0, 12),
        (HIT - 5, (bx - 4.5, by - 6.5, -0.4), -25, 30), (HIT, (bx - 2, by - 4.6, 1.2), -28, 40),
        (HIT + 12, (bx + 1, by - 7.5, -3.0), 35, 50), (F, (bx + 3, by - 10, -12), 60, 50)]
for f, loc, pitch, yaw in path:
    sh.root.location = loc
    sh.root.rotation_euler = (0, math.radians(pitch), math.radians(yaw))
    sh.root.keyframe_insert("location", frame=f)
    sh.root.keyframe_insert("rotation_euler", frame=f)
open_jaw(sh, HIT - 12, 0)
open_jaw(sh, HIT - 4, 1)
open_jaw(sh, HIT + 2, 0.2)
swim_wag(sh, 1, F, period=8, angle=28)
splash("Wake", (bx - 6, by - 7, 0), HIT - 10, count=10, size=0.5, power=5, seed=2)
splash("Hit", (bx - 1, by - 3.6, 1), HIT, count=24, size=0.8, power=10, life=30, seed=3)
splash("Tip", (bx, by + 3, 0), TIPF + 6, count=26, size=0.9, power=9, life=30, seed=4)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (bx - 8, by - 38, 5), (bx - 3, by, 9))
key_camera(cam, HIT, (bx - 5, by - 33, 4.5), (bx - 1, by, 6))
key_camera(cam, F, (bx - 3, by - 30, 4.5), (bx, by, 4))
add_shake(cam, HIT, HIT + 20, strength=0.35, rot_strength=0.03)
add_shake(cam, TIPF, TIPF + 14, strength=0.3, rot_strength=0.025, seed=2)
render(os.environ.get("JAWS_OUT", "renders/shot05_barge_rammed"))
