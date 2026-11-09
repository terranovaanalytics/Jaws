"""Shot 14: the radar goes quiet. Silence... then beep beep beep: a NEW line
of dots heading straight for Edgartown Harbor. Crash zoom."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, key_camera, render, FPS, shot_seconds, box, mat
from jaws.props import make_radar, radar_land, radar_sweep, dot_line
from jaws.people import make_brody, make_jesse

F = int(shot_seconds("shot14", 8.0) * FPS)
reset_scene(F, world_color=(0.05, 0.07, 0.06))
add_sun((65, 0, 10), energy=1.2)
r = make_radar()
radar_land(r, "amity", (0.6, 0.3), 0.9, 0.6, label="AMITY")
radar_land(r, "edgartown", (-1.9, -1.3), 0.7, 0.5, label="EDGARTOWN HARBOR")
radar_sweep(r, 1, F)
BEEP = int(F * 0.40)   # lands on "beep, beep, beep" in the narration
dot_line(r, "new", (2.4, -3.1), (-1.6, -1.2), 8, BEEP, F, travel=0.55, period=6)
box("Desk", (14, 4, 1), (0, -2.5, -6.6), mat("desk", (0.35, 0.25, 0.16)))

b = make_brody("Brody", loc=(-2.6, -7.5, -8.4), rot_z=180)
j = make_jesse("Jesse", loc=(2.8, -7.0, -9.6), rot_z=180)
for p in (b, j):
    p.root.scale = (2.4,) * 3
    p.head.rotation_euler[0] = math.radians(10)
# when the beeping starts they slowly turn to look at each other
b.head.keyframe_insert("rotation_euler", frame=BEEP + 20)
j.head.keyframe_insert("rotation_euler", frame=BEEP + 20)
b.head.rotation_euler = (math.radians(5), 0, math.radians(-50))
j.head.rotation_euler = (math.radians(5), 0, math.radians(50))
b.head.keyframe_insert("rotation_euler", frame=BEEP + 34)
j.head.keyframe_insert("rotation_euler", frame=BEEP + 34)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=32)
key_camera(cam, 1, (0, -19, -1.5), (0, 0, -0.5))
key_camera(cam, BEEP + 36, (0, -16, -1.2), (0, 0, -0.3))
key_camera(cam, BEEP + 44, (-0.8, -8, -0.8), (-0.6, 0, -1.2))   # crash zoom on the dots
key_camera(cam, F, (-0.8, -7.5, -0.8), (-0.6, 0, -1.2))
render(os.environ.get("JAWS_OUT", "renders/shot14_radar_again"))
