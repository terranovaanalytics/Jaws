"""Shot 10: inside the cave. Brody's mech shark cruises in, opens its jaw and
spits out a giant ham. Every shark in the cave rushes in for a frenzy."""
import math, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import (reset_scene, add_sun, add_camera, key_camera, add_shake, linear_keys,
                         render, FPS, shot_seconds)
from jaws.props import make_cave_cutaway, make_bait
from jaws.world import splash
from jaws.shark import make_shark, swim_wag, open_jaw, chomp

F = int(shot_seconds("shot10", 6.0) * FPS)
reset_scene(F, world_color=(0.45, 0.75, 1.0))
add_sun((40, 0, 20), energy=2.4)
make_cave_cutaway()

DROP = int(F * 0.33)
RUSH = DROP + 18
mech = make_shark("Mech", scale=2.4, variant="mech")
for f, x, yaw in [(1, 20, 180), (DROP - 6, 2.5, 180), (DROP + 10, 2.0, 180), (DROP + 24, 3, 20), (F, 22, 0)]:
    mech.root.location = (x, 1.5, -9)
    mech.root.rotation_euler[2] = math.radians(yaw)
    mech.root.keyframe_insert("location", frame=f)
    mech.root.keyframe_insert("rotation_euler", index=2, frame=f)
swim_wag(mech, 1, F, period=14, angle=10)
open_jaw(mech, DROP - 4, 0)
open_jaw(mech, DROP, 1.0)
open_jaw(mech, DROP + 8, 1.0)
open_jaw(mech, DROP + 12, 0)

ham = make_bait("Ham", loc=(0.8, 1.2, -9.6))
ham.scale = (0.001,) * 3
ham.keyframe_insert("scale", frame=DROP - 1)
ham.scale = (1.0,) * 3
for f, x, z, spin in [(DROP, 0.8, -9.6, 0), (DROP + 6, 0.0, -10.5, 40), (DROP + 20, -0.5, -13.8, 120),
                      (F, -0.5, -14.2, 130)]:
    ham.location = (x, 1.2, z)
    ham.rotation_euler = (0, math.radians(spin), 0)
    ham.keyframe_insert("location", frame=f)
    ham.keyframe_insert("rotation_euler", frame=f)
    ham.keyframe_insert("scale", frame=f)

rnd = random.Random(10)
for i in range(12):
    sh = make_shark(f"Hungry{i}", scale=rnd.uniform(1.3, 1.7))
    a = 2 * math.pi * i / 12
    start = (math.cos(a) * 11, rnd.uniform(0, 4), -10 + math.sin(a) * 5)
    end = (-0.5 + math.cos(a) * 2.2, start[1] * 0.5, -13.0 + math.sin(a) * 1.2)
    yaw_in = math.atan2(end[1] - start[1], end[0] - start[0])
    sh.root.location = start
    sh.root.rotation_euler = (0, 0, math.atan2(0, end[0] - start[0]) + (0 if end[0] > start[0] else 0))
    sh.root.rotation_euler[2] = 0 if end[0] > start[0] else math.pi
    sh.root.keyframe_insert("location", frame=1)
    sh.root.keyframe_insert("location", frame=RUSH + rnd.randint(-6, 6))
    sh.root.location = end
    sh.root.keyframe_insert("location", frame=RUSH + 22 + rnd.randint(-4, 4))
    for f in range(RUSH + 26, F + 1, 4):      # frenzy wiggle around the ham
        sh.root.location = (end[0] + rnd.uniform(-0.6, 0.6), end[1], end[2] + rnd.uniform(-0.5, 0.5))
        sh.root.keyframe_insert("location", frame=f)
    swim_wag(sh, 1, F, period=6, angle=30, seed=i)
    chomp(sh, RUSH + 16, F, period=6)
splash("Frenzy", (-0.5, 1.0, -13), RUSH + 22, count=20, size=0.4, power=5, life=30, seed=3,
       color=(0.8, 0.9, 1.0))

cam = add_camera((0, 0, 0), (0, 0, 0), lens=24)
key_camera(cam, 1, (3, -19, -9), (3, 0, -10))
key_camera(cam, RUSH, (1, -17, -10), (0.5, 0, -11))
key_camera(cam, F, (0, -14, -11), (-0.3, 0, -12.5))
add_shake(cam, RUSH + 18, F, strength=0.12, rot_strength=0.01)
render(os.environ.get("JAWS_OUT", "renders/shot10_bait"))
