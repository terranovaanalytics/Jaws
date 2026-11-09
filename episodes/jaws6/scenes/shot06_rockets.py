"""Shot 6: the barge lies on its side and every rocket fires straight across
the harbor, flat over the water, into the sailboats. Sails catch fire, then
shells start bursting low over the boats. Side-on view."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import add_camera, key_camera, add_shake, render, FPS, shot_seconds
from jaws.fireworks import rocket_streak, fire, burst
from _harbor import build_harbor, BARGE, tip_barge, tube_world, target_sails

F = int(shot_seconds("shot06", 5.0) * FPS)
h = build_harbor(F)
tip_barge(h["barge"])
bx, by, bz = BARGE
rnd = random.Random(6)
sails = target_sails(h, 6)
FIRE0 = int(F * 0.22)
for k, (it, p) in enumerate(sails):                 # aimed shots: each sail gets hit
    f0 = 2 + int(k * (FIRE0 + 18) / len(sails))
    a = tube_world(h["barge"], rnd.randrange(24))
    rocket_streak(f"Hit{k}", a, p, f0, frames=9, seed=k, radius=2.5)
    fire(f"SailFire{k}", (p[0], p[1], p[2] - 1.5), f0 + 9, F, size=1.1, seed=k, light=k < 4)
f = 1
i = 0
while f < F - 10:                                    # the rest spray across the harbor
    a = tube_world(h["barge"], rnd.randrange(24))
    b = (a[0] + rnd.uniform(-30, 30), a[1] + rnd.uniform(25, 60), rnd.uniform(2, 9))
    rocket_streak(f"Spray{i}", a, b, f, frames=rnd.randint(8, 12), seed=100 + i, pop=f > F * 0.6)
    f += rnd.randint(2, 4)
    i += 1
BURST = int(F * 0.75)                               # "bombs bursting in the air"
for k in range(5):
    burst(f"Low{k}", (bx + rnd.uniform(-25, 25), by + rnd.uniform(10, 30), rnd.uniform(6, 14)), BURST + k * 4,
          seed=200 + k, radius=6)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=24)
key_camera(cam, 1, (bx + 30, by - 4, 4), (bx - 2, by + 14, 4))
key_camera(cam, F, (bx + 26, by - 8, 5), (bx - 2, by + 16, 6))
add_shake(cam, 1, F, strength=0.06, rot_strength=0.006)
render(os.environ.get("JAWS_OUT", "renders/shot06_rockets"))
