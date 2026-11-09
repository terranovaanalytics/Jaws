"""Shot 3: "Running it back for Jaws 6. Fourth of July. Edgartown Harbor. The
whole town is out on boats for the fireworks." Dusk; the harbor full of boats,
the barge starts the show. Camera: slow rising push-in over the water."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import add_camera, key_camera, render, FPS, shot_seconds, text, mat
from _harbor import build_harbor, show, BARGE

F = int(shot_seconds("shot03", 6.6) * FPS)
h = build_harbor(F, pier_bunting=True)
show(h["barge"], 4, F, every=7, seed=3)
# spectators close to camera, looking up at the show
from jaws.world import make_small_boat, make_extra, bob
import math
bx, by, _ = BARGE
for i, (x, y, rz) in enumerate([(bx - 6.5, by - 47, 60), (bx + 6, by - 44, 120)]):
    b = make_small_boat(f"Near{i}", (x, y, 0), rot_z=rz, seed=20 + i)
    for j in range(3):
        e = make_extra(f"NearFan{i}{j}", (-1.4 + j * 0.9, 0, 0.4), seed=40 + i * 3 + j, scale=0.9)
        e.parent = b
        e.rotation_euler[2] = math.radians(-90)
    bob(b, 1, F, phase=i * 17)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=24)
key_camera(cam, 1, (bx - 5, by - 62, 4), (bx, by + 10, 16))
key_camera(cam, F, (bx - 2, by - 46, 6), (bx, by + 10, 21))
render(os.environ.get("JAWS_OUT", "renders/shot03_fourth"))
