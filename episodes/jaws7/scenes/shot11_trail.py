"""Shot 11: "And they go looking for the sub. But it's gone. And all that's
left is a radioactive trail." Brody, Jesse and the agent in a little boat on
empty open water, heads swiveling. Nothing. Then a glowing green streak
lights up across the water, zig-zagging off to the horizon; camera cranes up."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import reset_scene, add_sun, add_camera, key_camera, render, FPS, shot_seconds
from jaws.world import make_ocean, bob
from _sets import trail, face
from _crew import boat_crew

F = int(shot_seconds("shot11", 4.9) * FPS)
reset_scene(F, world_color=(0.55, 0.68, 0.80))
add_sun((55, 0, -30), energy=2.2)
make_ocean(color=(0.06, 0.26, 0.40))
boat, c = boat_crew((0, 0, 0), rot_z=90)
bob(boat, 1, F, period=40, roll=3, pitch=1.5, heave=0.2)
GONE = int(F * 0.30)
REVEAL = int(F * 0.56)
for k, p in enumerate(c.values()):          # looking around... nothing
    for i, (fr, deg) in enumerate(((1, 0), (GONE - 6, 45), (GONE + 6, -45), (REVEAL - 4, -10), (REVEAL + 4, 0))):
        face(p.head, fr + k * 2, deg * (1 if k % 2 else -1))
c["agent"].arm_r.rotation_euler[0] = 0
face(c["agent"].arm_r, REVEAL + 4, 0, axis=0)
face(c["agent"].arm_r, REVEAL + 10, -88, axis=0)     # points down the trail
pts = [(0, 7)] + [(7 * math.sin(k * 0.9), 7 + k * 14) for k in range(1, 22)]
trail("Trail", pts, REVEAL, int(F * 0.85))
cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (-6, -9, 3.0), (0, 0, 1.6))
key_camera(cam, REVEAL, (-5, -10, 4.5), (0, 3, 1.4))
key_camera(cam, F, (-3, -22, 11), (0, 35, -3))
render(os.environ.get("JAWS_OUT", "renders/shot11_trail"))
