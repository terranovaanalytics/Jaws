"""Shot 9: "The sharks are back, and the radar shows them right under
Edgartown Harbor." The advanced radar again: blips swarm in and pile up in
a blinking cluster under the harbor. Brody and Jesse watch from behind."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, key_camera, render, FPS, shot_seconds, box, mat, text
from jaws.props import make_radar, radar_land, radar_sweep, dot_line, radar_blip, blink, GREEN
from jaws.people import make_brody, make_jesse
import random

F = int(shot_seconds("shot09", 4.0) * FPS)
reset_scene(F, world_color=(0.05, 0.07, 0.06))
add_sun((65, 0, 10), energy=1.2)
r = make_radar()
radar_land(r, "amity", (0, 0.9), 1.3, 0.8)
text("Radar_harbor_lbl", "EDGARTOWN HARBOR", (0, -0.42, -1.75), 0.36, mat("radar_text", GREEN, emit=3.0),
     parent=r["root"])
radar_sweep(r, 1, F)
H = (0.2, -0.45)                                    # the harbor, just below the island
for k, (a, n) in enumerate((((3.4, -1.8), 6), ((-3.2, -2.2), 6), ((0.6, -3.7), 5))):
    dot_line(r, f"in{k}", a, H, n, 1, int(F * 0.6), travel=0.75, period=8)
rnd = random.Random(9)
for i in range(14):                                 # the pile-up under the harbor
    d = radar_blip(r, f"pile{i}", (H[0] + rnd.uniform(-0.55, 0.55), H[1] + rnd.uniform(-0.35, 0.3)), size=0.2)
    blink(d, int(F * 0.45) + i, F, period=6, on=4, phase=i)
box("Desk", (14, 4, 1), (0, -2.5, -6.6), mat("desk", (0.35, 0.25, 0.16)))
b = make_brody("Brody", loc=(-2.6, -7.5, -8.4), rot_z=180)
j = make_jesse("Jesse", loc=(2.8, -7.0, -9.6), rot_z=180)
for p in (b, j):
    p.root.scale = (2.4,) * 3
    p.head.rotation_euler[0] = math.radians(10)
LEAN = int(F * 0.55)                                # both lean in toward the cluster
for p in (b, j):
    p.torso.keyframe_insert("rotation_euler", frame=LEAN - 8)
    p.torso.rotation_euler[0] = math.radians(10)
    p.torso.keyframe_insert("rotation_euler", frame=LEAN)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=32)
key_camera(cam, 1, (0, -19, -1.5), (0, 0, -0.5))
key_camera(cam, F, (0.2, -16.5, -1.3), (0.1, 0, -0.6))
render(os.environ.get("JAWS_OUT", "renders/shot09_radar"))
