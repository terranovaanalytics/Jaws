"""Shot 12: "...kick the kids out of the bookstore and drain the water." Kids
come pouring out of the bookstore door and scatter, Brody waves them off;
then the pump kicks in and a geyser blasts out of the chimney, spraying
water and books everywhere."""
import math, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import (reset_scene, add_sun, add_camera, key_camera, add_shake, linear_keys, render, FPS,
                         shot_seconds, box, mat)
from jaws.town import make_bookstore
from jaws.props import make_pump, water_spray
from jaws.world import make_extra
from jaws.people import make_brody, make_jesse, point

F = int(shot_seconds("shot12", 4.5) * FPS)
reset_scene(F, world_color=(0.45, 0.75, 1.0))
add_sun((45, 0, -30), energy=2.4)
box("Street", (200, 200, 1), (0, 0, -0.5), mat("asphalt", (0.30, 0.30, 0.32)))
box("Sidewalk", (40, 5, 0.3), (0, -5.5, 0.15), mat("sidewalk", (0.72, 0.70, 0.66)))
st = make_bookstore(loc=(0, 0, 0.3))
for x in (-11, 11):
    box(f"Neighbor{x}", (11, 7, 8), (x, 0.5, 4.3), mat(f"nb{x}", (0.62, 0.6, 0.55) if x < 0 else (0.80, 0.78, 0.70)))
rnd = random.Random(12)
OUT = int(F * 0.45)
for i in range(9):                                   # kids stream out of the door
    kid = make_extra(f"Kid{i}", (0, -3.2, 0.3), seed=i, scale=0.7)
    go = 1 + i * 3
    kid.scale = (0.001,) * 3
    kid.keyframe_insert("scale", frame=max(1, go - 1))
    kid.scale = (0.7,) * 3
    kid.keyframe_insert("scale", frame=go)
    kid.keyframe_insert("location", frame=go)
    ang = math.radians(rnd.choice((-1, 1)) * rnd.uniform(20, 70) - 90)
    kid.location = (16 * math.cos(ang), -3.2 + 16 * math.sin(ang) * 0.4, 0.3)
    kid.rotation_euler[2] = ang + math.pi / 2
    kid.keyframe_insert("location", frame=go + 30)
    kid.keyframe_insert("rotation_euler", frame=go)
    linear_keys(kid)
b = make_brody("Brody", loc=(-3.2, -5.2, 0.3), rot_z=-20)
j = make_jesse("Jesse", loc=(3.4, -6.4, 0.3), rot_z=25)
point(b, 4, side="l", hold=OUT - 14)
pump, _ = make_pump(loc=(7.2, -5.6, 0.3))
import bpy
bpy.data.objects["Pump_hose"].hide_render = True
box("Hose", (5.6, 0.35, 0.35), (3.6, -4.2, 0.5), mat("pump_gray", (0.5, 0.52, 0.55)))
cx, cy, cz = st["chimney_top"]
water_spray("Geyser", (cx, cy, cz + 0.3), OUT, F, direction=(0.15, -0.35, 1.0), speed=14, rate=2, life=40)
book_cols = [(0.8, 0.15, 0.12), (0.15, 0.35, 0.7), (0.9, 0.75, 0.2), (0.2, 0.55, 0.3), (0.95, 0.95, 0.9)]
for i in range(16):                                  # books ride the geyser out
    bk = box(f"Book{i}", (0.6, 0.18, 0.8), (cx, cy, cz), mat(f"spine_{book_cols[i % 5]}", book_cols[i % 5]))
    f0 = OUT + 2 + i * 3
    vx, vy, vz = rnd.uniform(-4, 4), rnd.uniform(-5, -1), rnd.uniform(11, 15)
    bk.scale = (0.001,) * 3
    bk.keyframe_insert("scale", frame=f0 - 1)
    for k in range(0, 41, 3):
        t = k / 24
        bk.location = (cx + vx * t, cy + vy * t, cz + vz * t - 4.9 * t * t)
        bk.rotation_euler = (t * 9, t * 5, t * 3)
        bk.scale = (1, 1, 1)
        bk.keyframe_insert("location", frame=f0 + k)
        bk.keyframe_insert("rotation_euler", frame=f0 + k)
        bk.keyframe_insert("scale", frame=f0 + k)
for p in (b, j):                                     # look up at the geyser
    p.head.keyframe_insert("rotation_euler", frame=OUT)
    p.head.rotation_euler[0] = math.radians(-25)
    p.head.keyframe_insert("rotation_euler", frame=OUT + 6)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (1, -19, 3), (0, 0, 4))
key_camera(cam, F, (1, -25, 4), (0, 0, 8.5))
add_shake(cam, OUT, F, strength=0.05, rot_strength=0.005)
render(os.environ.get("JAWS_OUT", "renders/shot12_bookstore"))
