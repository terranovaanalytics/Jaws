"""Shot 3: shark swarm. Dozens of fins circle the sinking ferry; a couple of
swimmers get gobbled. High camera slowly orbits in."""
import math, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, key_camera, render, FPS, shot_seconds
from jaws.world import make_ocean, make_island, make_ferry, bob, make_extra, splash
from jaws.shark import make_shark, swim_wag, open_jaw

F = int(shot_seconds("shot03", 7.0) * FPS)
reset_scene(F, world_color=(0.45, 0.75, 1.0))
add_sun((50, 0, -25), energy=2.4)
make_ocean()
make_island()["root"].location = (50, 190, 0)

ferry = make_ferry("Ferry", loc=(0, 0, -4.8))
ferry.rotation_euler = (math.radians(28), math.radians(10), math.radians(15))
bob(ferry, 1, F, roll=3, pitch=2, heave=0.3)
ferry.keyframe_insert("location", index=2, frame=F)

rnd = random.Random(11)
S = 3.6
sharks = []
for ring, (r, n, spd) in enumerate([(11, 7, 0.55), (16, 9, -0.42), (22, 10, 0.34)]):
    for i in range(n):
        sh = make_shark(f"Shark{ring}_{i}", scale=S * rnd.uniform(0.85, 1.15))
        a0 = 2 * math.pi * i / n + rnd.uniform(-0.2, 0.2)
        rr = r + rnd.uniform(-1.5, 1.5)
        z = -1.4 + rnd.uniform(-0.2, 0.2)
        for f in range(1, F + 1, 2):
            a = a0 + spd * f / FPS
            sh.root.location = (rr * math.cos(a), rr * math.sin(a), z)
            sh.root.rotation_euler = (0, 0, a + (math.pi / 2 if spd > 0 else -math.pi / 2))
            sh.root.keyframe_insert("location", frame=f)
            sh.root.keyframe_insert("rotation_euler", frame=f)
        swim_wag(sh, 1, F, period=10, seed=ring * 20 + i)
        sharks.append(sh)

# swimmers bobbing between rings; two get chomped from below
victims = [(8, -9, int(F * 0.30)), (-12, -6, int(F * 0.65))]
for i, (x, y) in enumerate([(8, -9), (-12, -6), (4, -14), (-6, -12), (13, -2)]):
    p = make_extra(f"Swimmer{i}", (x, y, -1.3), seed=i + 3, scale=1.5)
    for f in range(1, F + 1, 6):
        p.location.z = -1.3 + 0.25 * math.sin(f * 0.4 + i)
        p.rotation_euler[1] = math.radians(15 * math.sin(f * 0.3 + i))
        p.keyframe_insert("location", index=2, frame=f)
        p.keyframe_insert("rotation_euler", index=1, frame=f)
    for vx, vy, fv in victims:
        if (vx, vy) == (x, y):
            g = make_shark(f"Gobbler{i}", scale=3.5)
            g.root.rotation_euler = (0, math.radians(-75), math.radians(rnd.uniform(0, 360)))
            for f, z in [(1, -14), (fv - 8, -12), (fv, 0.5), (fv + 6, 1.5), (fv + 16, -12)]:
                g.root.location = (x, y, z)
                g.root.keyframe_insert("location", frame=f)
            open_jaw(g, fv - 4, 1.0)
            open_jaw(g, fv + 2, 1.0)
            open_jaw(g, fv + 5, 0.0)
            p.keyframe_insert("location", frame=fv + 2)
            p.location.z = -8
            p.keyframe_insert("location", frame=fv + 8)
            splash(f"Chomp{i}", (x, y, 0), fv, count=16, size=0.6, power=8, seed=i)

cam = add_camera((-30, -42, 30), (0, 0, -1), lens=28)
key_camera(cam, 1, (-22, -34, 20), (0, -3, -1))
key_camera(cam, F, (-9, -31, 14), (1, -4, -1))
render(os.environ.get("JAWS_OUT", "renders/shot03_swarm"))
