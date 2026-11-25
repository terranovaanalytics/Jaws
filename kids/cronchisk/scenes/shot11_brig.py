"""Shot 11: the brig in Jelly's lair. Cherry zaps the lock with her laser watch and frees Pocket, Dr. Blip's kid."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S

F = int(shot_seconds("shot11_brig", 5.0) * FPS)
S.lair(F)
ZAP, OPEN = int(F * 1.4 / 5), int(F * 2.2 / 5)
cell = O.make_cell("Cell", (0.5, 3.0, 0), w=3.0, h=3.2)
wall = mat("cell_wall", (0.16, 0.16, 0.2))
for s in (-1, 1):
    box(f"CellSide{s}", (0.2, 2.6, 3.4), (0.5 + s * 1.6, 4.3, 1.7), wall)
box("CellBack", (3.4, 0.2, 3.4), (0.5, 5.6, 1.7), wall)
box("CellBunk", (1.2, 2.0, 0.5), (1.4, 4.4, 0.25), mat("bunk", (0.35, 0.3, 0.3)))
O.point_light("CellLight", (0.5, 4.2, 3.0), 120, (0.9, 0.9, 1.0), radius=0.5)
k = A.make_pocket("Pocket", (0.4, 4.0, 0), rot_z=0)
A.look(k, 10, -10, tilt=10)
c = A.make_cherry("Cherry", (-2.6, 0.4, 0), rot_z=150)
O.move(c.root, 1, ZAP - 10, (-2.6, 0.4, 0), (-1.2, 1.9, 0), ease=False)
A.walk(c, 1, ZAP - 10, period=12, swing=26)
A.arm(c, "r", ZAP - 2, -88, frames=6, roll=-10)
watch = box("Watch", (0.14, 0.16, 0.08), (0, 0, 0), mat("watch", (0.8, 0.8, 0.85), metal=0.8))
A.hold(c, watch, "r", offset=(0, 0, 0.18))
O.beam_shot("Zap", (-0.9, 2.4, 1.15), (0.95, 2.95, 1.2), ZAP, life=12, color=(1.0, 0.1, 0.1), width=0.03)
from jaws.fireworks import burst
burst("Sparks", (0.95, 2.95, 1.2), ZAP + 10, color=(1.0, 0.7, 0.2), count=16, radius=0.8, life=12, light=False)
d = cell["door"]
d.keyframe_insert("rotation_euler", index=2, frame=OPEN)
d.rotation_euler[2] = math.radians(-100)
d.keyframe_insert("rotation_euler", index=2, frame=OPEN + 8)
A.arm(c, "r", OPEN + 4, -10, frames=6)
# Pocket jumps for joy and runs to her
for i in range(2):
    f = OPEN + 4 + i * 8
    k.root.location.z = 0
    k.root.keyframe_insert("location", index=2, frame=f)
    k.root.location.z = 0.45
    k.root.keyframe_insert("location", index=2, frame=f + 4)
k.root.location.z = 0
k.root.keyframe_insert("location", index=2, frame=OPEN + 20)
A.arms_up(k, OPEN + 6, frames=4)
O.move(k.root, OPEN + 22, F - 6, (0.4, 4.0, 0), (-0.4, 1.6, 0), ease=False)
A.run(k, OPEN + 22, F - 6, period=8, swing=45)
A.arm(k, "l", F - 6, -20)
A.arm(k, "r", F - 6, -20)
A.look(c, OPEN + 24, 20, frames=8, tilt=15)
A.arm(c, "l", F - 4, -120, frames=8, roll=-20)              # thumbs up
cam = add_camera((-0.5, -5.5, 2.2), (0, 2.8, 1.4), lens=30)
key_camera(cam, 1, (-0.8, -5.5, 2.3), (-0.6, 2.6, 1.5))
key_camera(cam, F, (-0.2, -4.6, 2.0), (-0.3, 2.4, 1.2))
render(os.environ.get("JAWS_OUT", "renders/shot11_brig"))
