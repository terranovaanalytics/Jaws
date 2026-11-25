"""Shot 09: sunset. Agent Cherry parachutes in over the desert, lands in a roll, ready."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S

F = int(shot_seconds("shot09_cherry", 5.0) * FPS)
S.desert(F, sunset_sky=True)
O.make_lab_building("Lab", (6, 30, 0))
LAND = int(F * 3.0 / 5.0)
c = A.make_cherry("Cherry", (0, 3, 12), rot_z=0)
chute = O.make_parachute("Chute", (0, 0, 2.1))
chute.parent = c.root
O.move(c.root, 1, LAND, (1.5, 3.5, 12), (0, 1.5, 0), ease=False)
for f in range(1, LAND, 4):
    c.root.rotation_euler[1] = math.radians(6 * math.sin(f / 7))
    c.root.keyframe_insert("rotation_euler", index=1, frame=f)
c.root.rotation_euler[1] = 0
c.root.keyframe_insert("rotation_euler", index=1, frame=LAND)
A.arms_up(c, 2, frames=1, deg=-165)
# land: crouch, the chute falls away behind her
A.lean(c, LAND + 2, 30, frames=2)
A.lean(c, LAND + 12, 0, frames=8)
A.arm(c, "l", LAND + 4, -40, frames=4)
A.arm(c, "r", LAND + 4, -40, frames=4)
chute.keyframe_insert("location", frame=LAND)
chute.keyframe_insert("scale", frame=LAND)
chute.keyframe_insert("rotation_euler", frame=LAND)
chute.location = (0.5, 3.0, -1.5)
chute.scale = (1.2, 1.2, 0.15)
chute.rotation_euler = (math.radians(-30), 0, 0)
chute.keyframe_insert("location", frame=LAND + 20)
chute.keyframe_insert("scale", frame=LAND + 20)
chute.keyframe_insert("rotation_euler", frame=LAND + 20)
A.arm(c, "r", F - 14, -90, frames=6, roll=20)            # hand to earpiece: "I'm in."
A.look(c, F - 10, -10)
cam = add_camera((0, -6, 1.0), (0, 2, 6), lens=28)
key_camera(cam, 1, (0.5, -7, 0.8), (1.2, 3, 9.5))
key_camera(cam, LAND, (0.2, -6.5, 1.0), (0.1, 1.5, 1.8))
key_camera(cam, F, (0.1, -5.2, 1.2), (0, 1.5, 1.6))
add_shake(cam, LAND, LAND + 6, strength=0.12, rot_strength=0.01)
render(os.environ.get("JAWS_OUT", "renders/shot09_cherry"))
