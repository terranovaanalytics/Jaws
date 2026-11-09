"""Shot 2: a shark fin zooms in, the shark breaches and rams the ferry.
Impact shake, splash, passengers tumble off, ferry lists and starts sinking."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
from jaws.common import (reset_scene, add_sun, add_camera, key_camera, add_shake,
                         linear_keys, render, FPS)
from jaws.world import make_ocean, make_island, make_ferry, bob, make_extra, splash
from jaws.shark import make_shark, open_jaw, swim_wag

SECONDS = 7.0
F = int(SECONDS * FPS)
HIT = 62                      # frame of impact

reset_scene(F, world_color=(0.45, 0.75, 1.0))
add_sun((50, 0, -25), energy=2.4)
make_ocean()
isl = make_island()
isl["root"].location = (40, 160, 0)   # Amity in the background

ferry = make_ferry("Ferry", loc=(0, 0, 0), rot_z=0)
bob(ferry, 1, HIT)
# after impact: list toward camera, bow dips, sink
for f, roll, pitch, z in [(HIT, 0, 0, 0), (HIT + 4, 9, -2, -0.3), (HIT + 10, 6, -1, -0.5),
                          (HIT + 30, 16, 3, -1.4), (F, 26, 6, -3.6)]:
    ferry.rotation_euler = (math.radians(roll), math.radians(pitch), 0)
    ferry.location.z = z
    ferry.keyframe_insert("rotation_euler", frame=f)
    ferry.keyframe_insert("location", index=2, frame=f)

# shark: fin cuts toward the ferry, then breaches into the hull
S = 5.0
shark = make_shark("Shark", scale=S)
# fin crosses the foreground left->right (profile to camera), then breaches
path = [(1, (-12.5, -13, -2.3), 0, 22), (40, (-7, -11, -2.3), 0, 22),
        (52, (-4.5, -9.0, -0.8), -25, 28), (HIT, (-1.5, -6.6, 1.6), -30, 32),
        (HIT + 14, (0.5, -8.5, -3.0), 35, 32), (HIT + 40, (1.5, -10, -11), 60, 32)]
for f, loc, pitch, yaw in path:
    shark.root.location = loc
    shark.root.rotation_euler = (0, math.radians(pitch), math.radians(yaw))
    shark.root.keyframe_insert("location", frame=f)
    shark.root.keyframe_insert("rotation_euler", frame=f)
open_jaw(shark, 44, 0.0)
open_jaw(shark, 54, 1.0)
open_jaw(shark, HIT, 1.0)
open_jaw(shark, HIT + 3, 0.2)
swim_wag(shark, 1, F, period=8, angle=28)

splash("Wake", (-4.5, -9.0, 0), 50, count=10, size=0.5, power=5, seed=2)
splash("Hit", (0, -4.3, 1.0), HIT, count=22, size=0.8, power=9, life=30, seed=3)
splash("Fall", (0.5, -8.5, 0), HIT + 14, count=14, size=0.7, power=7, seed=4)

# passengers on the stern deck get flung overboard toward camera
for i in range(6):
    x = -9 + i * 1.6
    p = make_extra(f"Tourist{i}", (x, -1.5 + (i % 2), 1.85), seed=i, scale=1.5)
    p.parent = ferry
    start = HIT + 4 + i * 5
    p.keyframe_insert("location", frame=start)
    p.keyframe_insert("rotation_euler", frame=start)
    p.parent = None
    p.location = (x, -1.5 + (i % 2), 1.85)
    for k in range(0, 26, 3):
        t = k / 24
        p.location = (x + 0.5 * t, -1.5 - 7 * t, 2.2 + 5 * t - 9 * t * t)
        p.rotation_euler = (math.radians(-400 * t), math.radians(120 * t * (1 if i % 2 else -1)), 0)
        p.keyframe_insert("location", frame=start + k)
        p.keyframe_insert("rotation_euler", frame=start + k)
    splash(f"Plop{i}", (x + 0.5, -1.5 - 7 * 1.0, 0), start + 22, count=6, size=0.35,
           power=4, life=16, seed=10 + i)

cam = add_camera((-6, -34, 7), (-4, -8, 1), lens=30)
key_camera(cam, 1, (-7, -34, 7), (-5, -9, 0.5))
key_camera(cam, HIT, (-4, -29, 6), (-1, -5, 1.8))
key_camera(cam, F, (-3, -26, 5.5), (0, -3, 0.5))
linear_keys(cam)
add_shake(cam, HIT, HIT + 30, strength=0.35, rot_strength=0.03)
render(os.environ.get("JAWS_OUT", "renders/shot02_ferry_rammed"))
