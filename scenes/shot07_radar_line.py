"""Shot 7: the advanced radar detection shows a line of blinking dots
marching toward Amity. Brody and Jesse watch from the foreground."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, key_camera, render, FPS, shot_seconds, box, mat
from jaws.props import make_radar, radar_land, radar_sweep, dot_line
from jaws.people import make_brody, make_jesse

F = int(shot_seconds("shot07", 6.0) * FPS)
reset_scene(F, world_color=(0.05, 0.07, 0.06))
add_sun((65, 0, 10), energy=1.2)
r = make_radar()
radar_land(r, "amity", (0, 0), 0.9, 0.6, label="AMITY")
radar_sweep(r, 1, F)
dot_line(r, "sharks", (3.3, 2.4), (0.5, 0.3), 9, 1, F, travel=0.45)
box("Desk", (14, 4, 1), (0, -2.5, -6.6), mat("desk", (0.35, 0.25, 0.16)))

# the heroes, from behind, bottom of frame
b = make_brody("Brody", loc=(-2.6, -7.5, -8.4), rot_z=180)
j = make_jesse("Jesse", loc=(2.8, -7.0, -9.6), rot_z=180)
b.head.rotation_euler[0] = math.radians(10)
j.head.rotation_euler = (math.radians(12), math.radians(-10), 0)
for p in (b, j):
    p.root.scale = (2.4,) * 3

cam = add_camera((0, 0, 0), (0, 0, 0), lens=32)
key_camera(cam, 1, (0, -19, -1.5), (0, 0, -0.5))
key_camera(cam, F, (0.3, -15.5, -1.0), (0.2, 0, 0))
render(os.environ.get("JAWS_OUT", "renders/shot07_radar_line"))
