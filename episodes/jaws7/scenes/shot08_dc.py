"""Shot 8: "Brody gets on a plane, flies to DC, walks right into the White
House and says..." A little prop plane buzzes across the sky over the White
House lawn; Brody marches up the path, past the fountain, to the front door.
Camera follows behind him."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import reset_scene, add_sun, add_camera, key_camera, render, FPS, shot_seconds, box, mat
from jaws.people import make_brody, walk
from jaws.spy import make_white_house, make_plane, spin
from jaws.town import make_flag
from _sets import move

F = int(shot_seconds("shot08", 4.2) * FPS)
reset_scene(F, world_color=(0.50, 0.72, 0.95))
add_sun((50, 0, 30), energy=2.4)
wh = make_white_house("WH", (0, 60, 0), fountain=False)
make_flag("RoofFlag", (0, 56, 13.3), size=1.6, pole=4)
for k in range(12):                                         # trees framing the lawn
    for side in (-1, 1):
        x, y = side * (24 + (k % 3) * 5), 10 + k * 6
        box(f"TreeT{k}{side}", (0.6, 0.6, 3), (x, y, 1.5), mat("trunk", (0.40, 0.26, 0.14)))
        box(f"TreeC{k}{side}", (4.5, 4.5, 4.5), (x, y, 5), mat("tree", (0.12, 0.48, 0.15)), rot=(0, 0, k * 17))
pl = make_plane("Plane", (-28, 48, 27), rot_z=-14)
move(pl["root"], [(1, (-28, 48, 27)), (int(F * 0.6), (26, 34, 21))], linear=True)
spin(pl["prop"], 0, 1, F, rpm=900)
door_y = wh["door"][1]
b = make_brody("Brody", loc=(0, 8, 0.05), rot_z=180)          # walking away from us, toward the house
move(b.root, [(1, (0, 8, 0.05)), (F, (0, door_y - 6, 0.05))], linear=True)
walk(b, 1, F, period=12)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (1.5, -6, 3.0), (0, 40, 12))
key_camera(cam, int(F * 0.5), (1.2, 6, 2.8), (0, 40, 8))
key_camera(cam, F, (0.8, door_y - 18, 2.6), (0, door_y, 4))
render(os.environ.get("JAWS_OUT", "renders/shot08_dc"))
