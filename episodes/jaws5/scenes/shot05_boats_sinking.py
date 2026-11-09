"""Shot 5: the flotilla gets bumped. Sharks breach under boats, the boats
flip, splash and sink. Shaky cam on each hit."""
import math, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import (reset_scene, add_sun, add_camera, key_camera, add_shake, linear_keys,
                         render, FPS, shot_seconds)
from jaws.world import make_ocean, make_island, make_small_boat, bob, make_extra, splash
from jaws.shark import make_shark, open_jaw

F = int(shot_seconds("shot05", 7.0) * FPS)
reset_scene(F, world_color=(0.45, 0.75, 1.0))
add_sun((45, 0, 40), energy=2.4)
make_ocean()
make_island()["root"].location = (0, 170, 0)

rnd = random.Random(5)
boats = []
for i in range(9):
    x = -14 + (i % 3) * 13 + rnd.uniform(-2, 2)
    y = (i // 3) * 12 + rnd.uniform(-2, 2)
    b = make_small_boat(f"Boat{i}", loc=(x, y, 0), rot_z=-90 + rnd.uniform(-15, 15), seed=i)
    b.scale = (1.3,) * 3
    p = make_extra(f"Sailor{i}", (0, 0, 0), seed=i)
    p.parent = b
    p.location = (-0.8, 0, 0.6)
    boats.append(b)

hits = [(b, int(F * u)) for b, u in ((0, 0.18), (4, 0.37), (2, 0.54), (6, 0.67), (7, 0.75))]  # (boat, frame)
for n, (i, fh) in enumerate(hits):
    b = boats[i]
    bob(b, 1, fh, roll=4, pitch=3, phase=i * 9)
    x, y = b.location.x, b.location.y
    sh = make_shark(f"Bumper{n}", scale=3.2)
    sh.root.rotation_euler = (0, math.radians(-70), math.radians(rnd.uniform(0, 360)))
    for f, z in [(1, -16), (fh - 8, -10), (fh, 1.5), (fh + 6, 3), (fh + 18, -14)]:
        sh.root.location = (x + 0.5, y, z)
        sh.root.keyframe_insert("location", frame=f)
    open_jaw(sh, fh - 6, 1.0)
    open_jaw(sh, fh + 3, 0.2)
    # boat gets launched, flips, then sinks
    base = tuple(b.rotation_euler)
    for f, z, roll, pitch in [(fh, 0, 0, 0), (fh + 6, 4.5, 80, 20), (fh + 12, 5.5, 170, 30),
                              (fh + 20, -0.3, 200, 15), (min(F, fh + 70), -3.5, 210, 30)]:
        b.location.z = z
        b.rotation_euler = (base[0] + math.radians(roll), base[1] + math.radians(pitch), base[2])
        b.keyframe_insert("location", index=2, frame=f)
        b.keyframe_insert("rotation_euler", frame=f)
    splash(f"Hit{n}", (x, y, 0), fh, count=16, size=0.6, power=8, seed=n)
    splash(f"Land{n}", (x, y, 0), fh + 20, count=10, size=0.5, power=5, seed=n + 20)
for i in set(range(9)) - {h[0] for h in hits}:
    bob(boats[i], 1, F, roll=4, pitch=3, phase=i * 9)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (-3, -27, 9), (0, 9, 0))
key_camera(cam, F, (-1, -22, 7.5), (1, 10, 0.5))
linear_keys(cam)
for n, (i, fh) in enumerate(hits):
    add_shake(cam, fh, fh + 14, strength=0.3, rot_strength=0.025, seed=n)
render(os.environ.get("JAWS_OUT", "renders/shot05_boats_sinking"))
