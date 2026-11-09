"""Shared set for the Fourth of July shots (3-8, 16): Edgartown Harbor at
dusk. Amity at the origin (pier at x=10, T-end at y=-62), the fireworks barge
out in the harbor, a ring of motorboats and sailboats full of spectators.
Not a shot itself (render_all only picks up shot*.py)."""
import math
import random
from jaws.common import box, cyl, mat, reset_scene, FPS
from jaws.world import make_ocean, make_island, make_small_boat, make_extra, bob
from jaws.fireworks import dusk, make_barge, firework, FW_COLORS
from jaws.town import make_sailboat, make_flag, bunting

BARGE = (-4.0, -104.0, 0.0)


def build_harbor(F, boats=True, extras=True, seed=6, pier_bunting=False):
    s = reset_scene(F)
    dusk(s)
    make_ocean(color=(0.04, 0.12, 0.22))
    isl = make_island()
    dx, dy, dz = isl["dock_end"]
    # pier dressing: bunting along the T, a flag at the end
    if pier_bunting:
        bunting("PierBunt", (dx - 7, dy + 2, dz + 2.6), (dx + 7, dy + 2, dz + 2.6), n=16, sag=0.6)
        for x in (dx - 7, dx + 7):
            cyl(f"BuntPost{x}", 0.12, 2.8, (x, dy + 2, dz + 1.2), mat("dock_post", (0.30, 0.22, 0.14)), n=5)
    make_flag("PierFlag", (dx + 6.5, dy - 0.5, dz), size=1.2, pole=5.0)
    barge = make_barge("Barge", BARGE, rot_z=0)
    fleet = []
    if boats:
        rnd = random.Random(seed)
        k = 0
        for ring, (r, n) in enumerate(((24, 9), (40, 13))):
            for i in range(n):
                a = math.radians(-20 + (i + 0.5 * ring) * 220 / n)
                x, y = BARGE[0] + r * math.cos(a) * 1.3, BARGE[1] + r * math.sin(a) * 0.8
                if y < BARGE[1] - 16 and abs(x - BARGE[0]) < 28:
                    continue                                              # keep the camera side open
                face = math.degrees(math.atan2(BARGE[1] - y, BARGE[0] - x))  # bow toward the show
                if rnd.random() < 0.45:
                    sb = make_sailboat(f"Sail{k}", (x, y, 0), rot_z=face + rnd.uniform(-30, 30), seed=k)
                    fleet.append(dict(kind="sail", root=sb["root"], sail=sb))
                    boat = sb["root"]
                else:
                    boat = make_small_boat(f"Boat{k}", (x, y, 0), rot_z=face + rnd.uniform(-25, 25), seed=k)
                    fleet.append(dict(kind="motor", root=boat))
                if extras:
                    for j in range(2):
                        e = make_extra(f"Fan{k}_{j}", (-1.2 - j * 0.9, (j - 0.5) * 0.7, 0.4), seed=k * 3 + j,
                                       scale=0.9)
                        e.parent = boat
                        e.rotation_euler[2] = math.radians(-90 + rnd.uniform(-30, 30))
                bob(boat, 1, F, phase=k * 11)
                k += 1
    return dict(scene=s, island=isl, dock_end=(dx, dy, dz), barge=barge, fleet=fleet)


def show(barge, start, end, every=10, seed=0, height=(26, 44), spread=16, finale=False, **kw):
    """Fireworks launched from the barge tubes between start and end."""
    rnd = random.Random(seed)
    bx, by, bz = BARGE
    f, i = start, 0
    while f < end:
        tx, ty, tz = barge["tubes"][rnd.randrange(len(barge["tubes"]))]
        launch = (bx + tx, by + ty, bz + tz)
        top = (bx + rnd.uniform(-spread, spread), by + rnd.uniform(-spread * 0.4, spread * 0.4),
               rnd.uniform(*height))
        firework(f"FW{seed}_{i}", launch, top, f, seed=seed * 100 + i, ring=rnd.random() < 0.25, **kw)
        i += 1
        f += max(2, int(every * rnd.uniform(0.5, 1.4)) // (3 if finale else 1))


TIP = -65          # degrees about X when the barge has tipped over (tubes aim at the fleet)


def tip_barge(barge, frame=None, angle=TIP, z=-0.6):
    """Tip the barge onto its side (keyed at frame, or set statically)."""
    r = barge["root"]
    r.rotation_euler[0] = math.radians(angle)
    r.location.z = z
    if frame is not None:
        r.keyframe_insert("rotation_euler", index=0, frame=frame)
        r.keyframe_insert("location", index=2, frame=frame)


def tube_world(barge, i):
    import bpy
    from mathutils import Vector
    bpy.context.view_layer.update()
    return tuple(barge["root"].matrix_world @ Vector(barge["tubes"][i]))


def target_sails(h, n=6):
    """The sailboats in the line of fire (north of the barge), nearest first,
    as (fleet item, world position of the sail)."""
    import bpy
    from mathutils import Vector
    bpy.context.view_layer.update()
    out = []
    for it in h["fleet"]:
        if it["kind"] != "sail":
            continue
        p = it["root"].matrix_world @ Vector(it["sail"]["sail_center"])
        if p.y > BARGE[1] + 4:
            out.append((it, tuple(p)))
    out.sort(key=lambda t: (t[1][0] - BARGE[0]) ** 2 + (t[1][1] - BARGE[1]) ** 2)
    return out[:n]


def harbor_ablaze(h, start, end, sails=6, seed=0, smoke=True):
    """Aftermath dressing: the line-of-fire sailboats burn, smoke hangs."""
    from jaws.fireworks import fire, smoke_pall
    for k, (it, p) in enumerate(target_sails(h, sails)):
        fire(f"SailFire{k}", (p[0], p[1], p[2] - 1.5), start, end, size=1.1, seed=k, light=k < 4)
    fire("BargeFire", (BARGE[0] + 5, BARGE[1] + 1, 1.0), start, end, size=1.6, seed=9)
    if smoke:
        smoke_pall("Pall", (BARGE[0], BARGE[1] + 6, 12), spread=(34, 8), height=8, count=9, seed=seed)


def chaos_bursts(start, end, every=6, seed=0):
    """Rockets skipping flat across the water and popping low over the boats."""
    from jaws.fireworks import rocket_streak
    rnd = random.Random(seed)
    f, i = start, 0
    while f < end:
        a = (BARGE[0] + rnd.uniform(-6, 6), BARGE[1] + rnd.uniform(-1, 2), rnd.uniform(2, 5))
        b = (BARGE[0] + rnd.uniform(-35, 35), BARGE[1] + rnd.uniform(12, 40), rnd.uniform(3, 14))
        rocket_streak(f"Chaos{seed}_{i}", a, b, f, frames=rnd.randint(8, 13), seed=seed * 50 + i)
        i += 1
        f += max(2, int(every * rnd.uniform(0.5, 1.5)))
