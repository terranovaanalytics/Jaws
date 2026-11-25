"""Shot 08: the bubble cracks. Dr. Blip runs down the red-alert corridor toward us, the Twins far behind."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S
from jaws.soviet import alarm_light, sweat

F = int(shot_seconds("shot08_escape", 4.0) * FPS)
from jaws.common import reset_scene
sc = reset_scene(F, world_color=(0.05, 0.0, 0.0))
O.dark_room(sc, ambient=0.25)
O.make_corridor("Cor", (0, -6, 0), length=40, w=4, h=3.5, lights=True)
for k in range(5):
    alarm_light(f"Alarm{k}", (1.7, 2 + k * 6, 3.0), 1, F, period=10, energy=900)
bl = A.make_blip("Blip", (0, 22, 0), rot_z=0)
O.move(bl.root, 4, F, (0, 22, 0), (0, 0.5, 0), ease=False)
A.run(bl, 4, F, period=8, swing=60)
A.arms_up(bl, 4, frames=2, deg=-160)
sweat("Sweat", bl.head, 4, F, every=8)
O.shards("Shards", (0, 22.5, 1.6), 3, count=26, power=4, life=30)
for k, dx in enumerate((-0.8, 0.8)):
    t = A.make_twin(f"Twin{k}", (dx, 32, 0), rot_z=0)
    O.move(t.root, 20, F, (dx, 32, 0), (dx, 20, 0), ease=False)
    A.run(t, 20, F, period=10, swing=40)
cam = add_camera((0, -5, 1.8), (0, 10, 1.6), lens=40)
key_camera(cam, 1, (0, -5, 1.8), (0, 15, 1.4))
key_camera(cam, F, (0, -5.5, 1.7), (0, 4, 1.5))
add_shake(cam, 1, F, strength=0.03, rot_strength=0.004)
render(os.environ.get("JAWS_OUT", "renders/shot08_escape"))
