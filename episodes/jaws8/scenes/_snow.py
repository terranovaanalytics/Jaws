"""Snow helpers for the escape shots (9, 10). Not a shot."""
import random
from jaws.common import ico, mat, linear_keys


def snowfall(center, size, start, end, n=120, seed=0, fall=1.4):
    """Chunky snowflakes drifting down through a box around center."""
    rnd = random.Random(seed)
    m = mat("snowflake", (0.95, 0.96, 1.0), emit=0.6)
    cx, cy, cz = center
    sx, sy, sz = size
    for i in range(n):
        x, y = cx + rnd.uniform(-sx, sx), cy + rnd.uniform(-sy, sy)
        z0 = cz + rnd.uniform(0, sz)
        o = ico(f"Flake{seed}_{i}", rnd.uniform(0.03, 0.06), (x, y, z0), m, subdiv=1)
        o.visible_shadow = False
        d = fall * (end - start) / 24.0
        o.keyframe_insert("location", frame=start)
        o.location = (x + rnd.uniform(-0.6, 0.6), y, z0 - d)
        o.keyframe_insert("location", frame=end)
        linear_keys(o)


def pines(xs_ys, seed=0, scale=1.0):
    rnd = random.Random(seed)
    from jaws.common import cyl
    leaf = mat("pine", (0.12, 0.30, 0.20))
    snow = mat("snow_cap", (0.92, 0.94, 0.97))
    trunk = mat("trunk", (0.40, 0.26, 0.14))
    for k, (x, y) in enumerate(xs_ys):
        h = rnd.uniform(5, 8) * scale
        cyl(f"PineT{seed}_{k}", 0.25 * scale, 1.5 * scale, (x, y, 0.75 * scale), trunk, n=5)
        cyl(f"Pine{seed}_{k}", h * 0.32, h, (x, y, 1.2 * scale + h / 2), leaf, n=6, r2=0)
        cyl(f"PineS{seed}_{k}", h * 0.12, h * 0.35, (x, y, 1.2 * scale + h * 0.84), snow, n=6, r2=0)
