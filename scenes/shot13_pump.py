"""Shot 13: the big pump. Water blasts out of the top of the carousel like a
fountain, Brody and Jesse admire their work... one shark comes out too."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
from jaws.common import (reset_scene, add_sun, add_camera, key_camera, add_shake, linear_keys,
                         render, FPS, shot_seconds, box, mat)
from jaws.props import make_carousel, make_pump, water_spray
from jaws.people import make_brody, make_jesse
from jaws.shark import make_shark, open_jaw, chomp

F = int(shot_seconds("shot13", 6.0) * FPS)
reset_scene(F, world_color=(0.45, 0.75, 1.0))
add_sun((45, 0, -30), energy=2.4)
box("Ground", (200, 200, 1), (0, 0, -0.5), mat("grass", (0.30, 0.72, 0.25)))
c = make_carousel()
pump, nozzle = make_pump(loc=(0, 0, 0.75))
import bpy
bpy.data.objects["Carousel_column"].hide_render = True   # the pump replaces the center column
ON = 12
water_spray("Spray", (0, 0, 10.6), ON, F, direction=(0.25, -0.45, 1.0), speed=13, rate=2, life=42)
water_spray("Spray2", (0, 0, 10.6), ON + 1, F, direction=(-0.3, -0.35, 1.0), speed=12, rate=3, life=42, seed=4)

# one very confused shark rides the geyser
sh = make_shark("Flyer", scale=1.6)
FL = int(F * 0.45)
for f, loc, rot in [(FL, (0, 0, 9), (0, -80, 0)), (FL + 12, (3, -5, 17), (0, -40, 30)),
                    (FL + 24, (6, -10, 15), (0, 30, 90)), (FL + 38, (8, -15, -2), (0, 85, 120))]:
    sh.root.location = loc
    sh.root.rotation_euler = [math.radians(a) for a in rot]
    sh.root.keyframe_insert("location", frame=f)
    sh.root.keyframe_insert("rotation_euler", frame=f)
sh.root.scale = (0.001,) * 3
sh.root.keyframe_insert("scale", frame=FL - 1)
sh.root.scale = (1.6,) * 3
sh.root.keyframe_insert("scale", frame=FL)
chomp(sh, FL, FL + 38, period=6)

b = make_brody("Brody", loc=(-3.0, -10, 0), rot_z=180)
j = make_jesse("Jesse", loc=(1.5, -10.5, 0), rot_z=180)
for p in (b, j):
    p.head.rotation_euler[0] = math.radians(-20)       # looking up at the geyser
# Brody: thumbs up / fist pump
b.arm_r.keyframe_insert("rotation_euler", index=0, frame=FL - 10)
b.arm_r.rotation_euler[0] = math.radians(-160)
b.arm_r.keyframe_insert("rotation_euler", index=0, frame=FL - 4)
# both heads track the flying shark
for p in (b, j):
    p.head.keyframe_insert("rotation_euler", frame=FL + 6)
    p.head.rotation_euler = (math.radians(-10), 0, math.radians(-35))
    p.head.keyframe_insert("rotation_euler", frame=FL + 30)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (-1, -20, 3), (0, 0, 7))
key_camera(cam, F, (-1, -30, 4), (1, 0, 9))
add_shake(cam, ON, F, strength=0.04, rot_strength=0.004)
render(os.environ.get("JAWS_OUT", "renders/shot13_pump"))
