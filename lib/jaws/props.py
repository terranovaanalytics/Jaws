"""Carousel, radar screen, shark cave, drill rig, pump, bait, explosions."""
import math
import random
import bpy
from .common import (mat, mesh_obj, empty, box, cyl, ico, text, link, box_data,
                     cyl_data, add_shake, fog, add_sun)

# ---------------------------------------------------------------- carousel
def _horse(name, color, parent, coll):
    """Tiny blocky horse on a pole. Origin at pole center; faces +X."""
    root = empty(name, (0, 0, 0), parent, coll)
    m = mat(f"horse_{color}", color)
    mane = mat("horse_mane", (0.15, 0.08, 0.05))
    gold = mat("pole_gold", (1.0, 0.8, 0.2))
    box(f"{name}_body", (1.0, 0.35, 0.4), (0, 0, 0), m, parent=root, coll=coll)
    box(f"{name}_neck", (0.25, 0.25, 0.5), (0.45, 0, 0.3), m, parent=root, coll=coll, rot=(0, 25, 0))
    box(f"{name}_head", (0.45, 0.24, 0.22), (0.68, 0, 0.55), m, parent=root, coll=coll)
    box(f"{name}_mane", (0.12, 0.27, 0.4), (0.38, 0, 0.42), mane, parent=root, coll=coll, rot=(0, 25, 0))
    for dx in (-0.38, 0.38):
        for dy in (-0.12, 0.12):
            box(f"{name}_leg{dx}{dy}", (0.1, 0.1, 0.5), (dx, dy, -0.42), m, parent=root, coll=coll,
                rot=(0, 30 if dx > 0 else -30, 0))
    cyl(f"{name}_pole", 0.05, 3.0, (0, 0, 0.6), gold, n=5, parent=root, coll=coll)
    return root


def make_carousel(name="Carousel", loc=(0, 0, 0), coll=None, horses=10, sign=True):
    """Round carousel pavilion: 12-sided platform, striped cone roof, horses
    that bob up and down. Returns dict(root, rotor, floor_z, radius).
    animate_carousel() spins it."""
    R = 6.0
    root = empty(name, loc, coll=coll)
    wood = mat("car_wood", (0.62, 0.42, 0.25))
    white = mat("car_white", (0.98, 0.97, 0.94))
    red = mat("car_red", (0.88, 0.12, 0.15))
    gold = mat("pole_gold", (1.0, 0.8, 0.2))
    cyl(f"{name}_base", R + 0.6, 0.6, (0, 0, 0.3), mat("car_stone", (0.7, 0.68, 0.64)), n=12, parent=root, coll=coll)
    rotor = empty(f"{name}_rotor", (0, 0, 0.6), root, coll)
    cyl(f"{name}_floor", R, 0.3, (0, 0, 0.15), wood, n=12, parent=rotor, coll=coll)
    cyl(f"{name}_column", 0.9, 5.4, (0, 0, 2.9), mat("car_mirror", (0.85, 0.75, 0.95)), n=8, parent=rotor, coll=coll)
    colors = [(1, 1, 1), (0.25, 0.2, 0.15), (0.9, 0.8, 0.6), (0.55, 0.35, 0.2), (0.95, 0.95, 0.9)]
    hs = []
    for i in range(horses):
        a = 2 * math.pi * i / horses
        rr = R * 0.72
        h = _horse(f"{name}_horse{i}", colors[i % len(colors)], rotor, coll)
        h.location = (rr * math.cos(a), rr * math.sin(a), 1.4)
        h.rotation_euler[2] = a + math.pi / 2
        hs.append(h)
    # posts + striped roof (fixed to the building, not the rotor)
    for i in range(12):
        a = 2 * math.pi * (i + 0.5) / 12
        cyl(f"{name}_post{i}", 0.15, 5.0, ((R + 0.3) * math.cos(a), (R + 0.3) * math.sin(a), 3.1),
            white, n=6, parent=root, coll=coll)
    n = 16
    v = [(0, 0, 9.0)] + [((R + 1.2) * math.cos(2 * math.pi * i / n), (R + 1.2) * math.sin(2 * math.pi * i / n), 5.6)
                         for i in range(n)]
    f = [(0, 1 + i, 1 + (i + 1) % n) for i in range(n)] + [tuple(range(n, 0, -1))]
    mesh_obj(f"{name}_roof", v, f, [red, white], face_mat=[i % 2 for i in range(n)] + [1],
             parent=root, coll=coll)
    # scalloped valance
    for i in range(n):
        a = 2 * math.pi * (i + 0.5) / n
        box(f"{name}_val{i}", (2.4, 0.15, 0.5), ((R + 1.15) * math.cos(a), (R + 1.15) * math.sin(a), 5.4),
            red if i % 2 else white, parent=root, coll=coll, rot=(0, 0, math.degrees(a) + 90))
    cyl(f"{name}_flagpole", 0.06, 1.6, (0, 0, 9.7), gold, n=5, parent=root, coll=coll)
    box(f"{name}_flag", (0.8, 0.05, 0.45), (0.4, 0, 10.2), red, parent=root, coll=coll)
    if sign:
        text(f"{name}_sign", "FLYING HORSES", (0, -(R + 1.3), 6.3), 0.75,
             mat("sign_gold", (1.0, 0.85, 0.25), emit=0.8), extrude=0.05, parent=root, coll=coll)
    return dict(root=root, rotor=rotor, horses=hs, radius=R, floor_z=0.75)


def animate_carousel(c, start, end, rpm=4.0, bob=0.35, stop_at=None):
    """Spin the rotor and bob the horses (on twos-friendly keys)."""
    stop = end if stop_at is None else stop_at
    rot = 0.0
    for f in range(start, end + 1, 2):
        if f <= stop:
            rot = (f - start) / 24 * rpm / 60 * 2 * math.pi
        c["rotor"].rotation_euler[2] = rot
        c["rotor"].keyframe_insert("rotation_euler", index=2, frame=f)
        for i, h in enumerate(c["horses"]):
            t = (min(f, stop) - start) / 24
            h.location.z = 1.4 + bob * math.sin(t * 4 + i * 1.3)
            h.keyframe_insert("location", index=2, frame=f)


# ---------------------------------------------------------------- radar
GREEN = (0.25, 1.0, 0.35)


def make_radar(name="Radar", coll=None):
    """Vintage green radar CRT in a chunky bezel, screen facing -Y, centered
    at the origin, screen radius 4. Returns dict with root, R and helpers."""
    R = 4.0
    root = empty(name, (0, 0, 0), coll=coll)
    bez = mat("radar_bezel", (0.32, 0.36, 0.30))
    dark = mat("radar_dark", (0.02, 0.08, 0.03), emit=0.6)
    line = mat("radar_line", GREEN, emit=0.7)
    glow = mat("radar_glow", GREEN, emit=1.2)
    box(f"{name}_case", (11, 3, 13.5), (0, 1.6, 0.8), bez, parent=root, coll=coll)
    cyl(f"{name}_rim", R + 0.5, 0.4, (0, -0.05, 0), mat("radar_rim", (0.12, 0.13, 0.11)), n=24,
        rot=(90, 0, 0), parent=root, coll=coll)
    cyl(f"{name}_screen", R, 0.2, (0, -0.2, 0), dark, n=24, rot=(90, 0, 0), parent=root, coll=coll)
    for k, r in enumerate((1.33, 2.66, 3.95)):          # range rings: 24 dashes each
        for i in range(24):
            a = 2 * math.pi * i / 24
            box(f"{name}_ring{k}_{i}", (0.35 * r / 2, 0.02, 0.04), (r * math.cos(a), -0.32, r * math.sin(a)),
                line, parent=root, coll=coll, rot=(0, -math.degrees(a) + 90, 0))
    box(f"{name}_crossH", (2 * R, 0.02, 0.03), (0, -0.32, 0), line, parent=root, coll=coll)
    box(f"{name}_crossV", (0.03, 0.02, 2 * R), (0, -0.32, 0), line, parent=root, coll=coll)
    sweep = empty(f"{name}_sweep", (0, -0.34, 0), root, coll)
    box(f"{name}_beam", (R, 0.02, 0.07), (R / 2, 0, 0), glow, parent=sweep, coll=coll)
    for k in range(1, 6):                               # fading afterglow wedge
        m = mat(f"radar_trail{k}", GREEN, emit=0.9 / k)
        box(f"{name}_trail{k}", (R, 0.015, 0.05), (R / 2 * math.cos(math.radians(-6 * k)), 0.005 * k,
            R / 2 * math.sin(math.radians(-6 * k))), m, parent=sweep, coll=coll, rot=(0, 6 * k, 0))
    # knobs, label plate, little lamps
    knob = mat("radar_knob", (0.08, 0.08, 0.08))
    for i, x in enumerate((-3.6, -1.2, 1.2, 3.6)):
        cyl(f"{name}_knob{i}", 0.45, 0.4, (x, -0.2, -5.4), knob, n=8, rot=(90, 0, 0), parent=root, coll=coll)
    text(f"{name}_label", "ADVANCED RADAR DETECTION", (0, -0.15, 5.4), 0.55,
         mat("radar_label", (0.9, 0.85, 0.6)), parent=root, coll=coll)
    return dict(root=root, R=R, sweep=sweep, name=name)


def radar_sweep(r, start, end, rpm=20, stop_at=None):
    stop = end if stop_at is None else stop_at
    for f in range(start, end + 1, 2):
        t = (min(f, stop) - start) / 24
        r["sweep"].rotation_euler[1] = -t * rpm / 60 * 2 * math.pi
        r["sweep"].keyframe_insert("rotation_euler", index=1, frame=f)


def radar_blip(r, name, xz, size=0.28, color=GREEN, coll=None):
    m = mat(f"blip_{color}", color, emit=0.9)
    return cyl(f"{r['name']}_{name}", size, 0.05, (xz[0], -0.4, xz[1]), m, n=6, rot=(90, 0, 0),
               parent=r["root"], coll=coll)


def radar_land(r, name, xz, sx, sz, label=None, coll=None):
    """Glowing landmass blob on the screen, optional label."""
    m = mat("radar_land", (0.12, 0.45, 0.15), emit=1.0)
    o = cyl(f"{r['name']}_{name}", 1.0, 0.04, (xz[0], -0.36, xz[1]), m, n=9, rot=(90, 0, 0),
            parent=r["root"], coll=coll)
    o.scale = (sx, sz, 1)
    if label:
        text(f"{r['name']}_{name}_lbl", label, (xz[0], -0.42, xz[1] - sz - 0.35), 0.38,
             mat("radar_text", GREEN, emit=3.0), parent=r["root"], coll=coll)
    return o


def blink(obj, start, end, period=8, on=5, phase=0):
    """Hard on/off blink via hide_render keys."""
    obj.hide_render = True
    obj.keyframe_insert("hide_render", frame=1)
    f = start
    while f <= end:
        k = (f + phase) % period
        obj.hide_render = k >= on
        obj.keyframe_insert("hide_render", frame=f)
        f += 1


def dot_line(r, name, a, b, n, start, end, travel=0.6, period=8, coll=None):
    """n blinking dots in a line marching from a toward b."""
    dots = []
    for i in range(n):
        d = radar_blip(r, f"{name}{i}", a, coll=coll)
        u0 = i / n * (1 - travel)
        for f, u in ((start, u0), (end, u0 + travel)):
            d.location.x = a[0] + (b[0] - a[0]) * u
            d.location.z = a[1] + (b[1] - a[1]) * u
            d.keyframe_insert("location", frame=f)
        blink(d, start, end, period=period, phase=i)
        dots.append(d)
    return dots


# ---------------------------------------------------------------- underwater
def underwater(s, color=(0.04, 0.22, 0.40), start=6, depth=55, floor_z=-20, seed=3):
    """Dark-blue fog world with a sand floor, rocks and seaweed."""
    s.world.node_tree.nodes["Background"].inputs[0].default_value = (*color, 1)
    add_sun((25, 0, 10), energy=1.6, color=(0.7, 0.9, 1.0))
    fog(s, start, depth, color)
    rnd = random.Random(seed)
    box("Seafloor", (400, 400, 1), (0, 0, floor_z - 0.5), mat("seafloor", (0.75, 0.68, 0.45)))
    weed = mat("seaweed", (0.15, 0.55, 0.25))
    rock = mat("uw_rock", (0.35, 0.38, 0.40))
    for i in range(40):
        x, y = rnd.uniform(-60, 60), rnd.uniform(-10, 80)
        if rnd.random() < 0.5:
            h = rnd.uniform(2, 6)
            box(f"Weed{i}", (0.3, 0.3, h), (x, y, floor_z + h / 2), weed, rot=(rnd.uniform(-10, 10), 0, 0))
        else:
            sz = rnd.uniform(1, 4)
            box(f"URock{i}", (sz, sz, sz * 0.7), (x, y, floor_z), rock, rot=(0, 0, rnd.uniform(0, 90)))


# ---------------------------------------------------------------- cave cutaway
def make_cave_cutaway(name="Cave", coll=None, seed=7):
    """Cross-section diagram: island ground (green top layer) above a blocky
    cave full of water, tunnel opening to the ocean on the right.
    Cave interior spans x -12..12, z -16..-4. Ground surface at z = 0.
    Front cut face at y = -3; back wall at y = 6."""
    rnd = random.Random(seed)
    dirt = mat("dirt", (0.50, 0.33, 0.20))
    dirt2 = mat("dirt_dark", (0.38, 0.25, 0.15))
    grass = mat("grass", (0.30, 0.72, 0.25))
    rock = mat("cave_rock", (0.28, 0.27, 0.30))
    water = mat("cave_water", (0.05, 0.25, 0.45), flat=0.8)
    Y0, Y1 = -3.0, 6.0
    D = Y1 - Y0
    yc = (Y0 + Y1) / 2
    box(f"{name}_grass", (60, D + 4, 1.0), (-6, yc, -0.5), grass)
    box(f"{name}_roof", (60, D, 3.5), (-6, yc, -2.75), dirt)
    box(f"{name}_left", (24, D, 12), (-24, yc, -10), dirt)
    box(f"{name}_floor", (60, D, 10), (-6, yc, -21), dirt2)
    box(f"{name}_rightUpper", (6, D, 7), (15, yc, -7.5), dirt)       # tunnel below this
    box(f"{name}_back", (60, 1, 30), (-6, Y1 + 0.5, -15), mat("cave_back", (0.07, 0.22, 0.38), flat=0.7))
    # ocean cross-section to the right of the island
    box(f"{name}_sea", (40, 1, 16), (38, Y1 + 0.5, -8), mat("sea_section", (0.10, 0.40, 0.68), flat=0.7))
    box(f"{name}_seafloor", (40, D, 10), (38, yc, -21), dirt2)
    box(f"{name}_water", (27, D - 0.2, 12), (1.5, yc, -10), water)  # behind the cut, visual tint
    bpy.data.objects[f"{name}_water"].hide_render = True
    # jagged rock teeth around the cave edge
    for i in range(30):
        x = rnd.uniform(-12, 12)
        top = rnd.random() < 0.5
        sz = rnd.uniform(0.8, 2.2)
        z = -4 - sz * 0.3 if top else -16 + sz * 0.3
        box(f"{name}_tooth{i}", (sz, rnd.uniform(1, D), sz), (x, yc + rnd.uniform(-1, 1), z), rock,
            rot=(0, 45, rnd.uniform(-20, 20)))
    # strata stripes on the cut face
    for i, z in enumerate((-1.5, -3.2)):
        box(f"{name}_strata{i}", (60, 0.05, 0.3), (-6, Y0 - 0.03, z), dirt2)
    return dict(interior=((-12, 12), (-16, -4)), front_y=Y0, back_y=Y1, tunnel=(15, -12))


def make_bait(name="Bait", loc=(0, 0, 0), coll=None):
    """Giant cartoon ham hock: pink meat + white bone."""
    root = empty(name, loc, coll=coll)
    ico(f"{name}_meat", 0.9, (0, 0, 0), mat("ham", (0.95, 0.45, 0.50)), parent=root, coll=coll)
    cyl(f"{name}_bone", 0.18, 1.6, (0.9, 0, 0), mat("bone", (0.98, 0.96, 0.88)), n=6, rot=(0, 90, 0),
        parent=root, coll=coll)
    for dz in (-0.18, 0.18):
        ico(f"{name}_knob{dz}", 0.25, (1.7, 0, dz), mat("bone", (0.98, 0.96, 0.88)), parent=root, coll=coll, subdiv=0)
    return root


def explosion(name, at, frame, size=4.0, count=18, life=20, seed=0, coll=None):
    """Chunky fireball: orange/yellow/white balls burst out and fade (shrink),
    then gray smoke balls rise."""
    rnd = random.Random(seed)
    cols = [mat("fire_y", (1.0, 0.85, 0.2), emit=4), mat("fire_o", (1.0, 0.45, 0.05), emit=4),
            mat("fire_w", (1.0, 1.0, 0.9), emit=6)]
    smoke = mat("smoke", (0.35, 0.35, 0.38))
    for i in range(count):
        o = ico(f"{name}_fire{i}", 1.0, at, rnd.choice(cols), coll=coll, subdiv=1)
        d = [rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.6, 1)]
        o.scale = (0.001,) * 3
        o.keyframe_insert("scale", frame=frame - 1)
        for k in range(0, life + 1, 2):
            t = k / life
            o.location = [at[j] + d[j] * size * (t ** 0.5) for j in range(3)]
            s = size * 0.5 * math.sin(math.pi * min(1, t * 1.2)) + 0.001
            o.scale = (s,) * 3
            o.keyframe_insert("location", frame=frame + k)
            o.keyframe_insert("scale", frame=frame + k)
    for i in range(8):
        o = ico(f"{name}_smoke{i}", 1.0, at, smoke, coll=coll, subdiv=0)
        o.scale = (0.001,) * 3
        o.keyframe_insert("scale", frame=frame + 4)
        d = [rnd.uniform(-1, 1), rnd.uniform(-1, 1), 1]
        for k in range(6, life * 3, 3):
            t = k / (life * 3)
            o.location = [at[j] + d[j] * size * t * 1.5 for j in range(3)]
            o.scale = (size * 0.4 * (1 - t) + 0.001,) * 3
            o.keyframe_insert("location", frame=frame + k)
            o.keyframe_insert("scale", frame=frame + k)


# ---------------------------------------------------------------- machines
def make_drill(name="Drill", loc=(0, 0, 0), coll=None):
    """Yellow tripod drill rig with a spinning cone bit. Returns (root, bit)."""
    root = empty(name, loc, coll=coll)
    yel = mat("drill_yellow", (1.0, 0.8, 0.05))
    blk = mat("drill_black", (0.08, 0.08, 0.08))
    steel = mat("drill_steel", (0.65, 0.67, 0.70))
    for i in range(3):
        a = 2 * math.pi * i / 3
        box(f"{name}_leg{i}", (0.3, 0.3, 5.2), (1.2 * math.cos(a), 1.2 * math.sin(a), 2.4), yel,
            parent=root, coll=coll, rot=(math.degrees(-math.sin(a)) * 0.25, math.degrees(math.cos(a)) * 0.25, 0))
    box(f"{name}_motor", (1.4, 1.4, 1.4), (0, 0, 4.6), yel, parent=root, coll=coll)
    box(f"{name}_stripe", (1.45, 1.45, 0.3), (0, 0, 4.6), blk, parent=root, coll=coll)
    bit = empty(f"{name}_bitPivot", (0, 0, 3.9), root, coll)
    cyl(f"{name}_shaft", 0.2, 3.0, (0, 0, -1.5), steel, n=6, parent=bit, coll=coll)
    cyl(f"{name}_bit", 0.6, 1.2, (0, 0, -3.4), steel, n=6, r2=0, rot=(180, 0, 0), parent=bit, coll=coll)
    for k in range(3):
        box(f"{name}_flute{k}", (1.0, 0.08, 0.15), (0, 0, -1.0 - k * 0.8), blk, parent=bit, coll=coll, rot=(0, 0, k * 60))
    return root, bit


def make_pump(name="Pump", loc=(0, 0, 0), coll=None):
    """Big red industrial pump with gauges and a hose nozzle on top.
    Returns (root, nozzle_world_offset)."""
    root = empty(name, loc, coll=coll)
    red = mat("pump_red", (0.85, 0.12, 0.10))
    gray = mat("pump_gray", (0.5, 0.52, 0.55))
    white = mat("gauge", (0.95, 0.95, 0.9))
    box(f"{name}_body", (3, 2, 2.4), (0, 0, 1.2), red, parent=root, coll=coll)
    cyl(f"{name}_tank", 0.9, 2.6, (0, 0, 3.6), red, n=8, parent=root, coll=coll)
    for i, x in enumerate((-0.8, 0.8)):
        cyl(f"{name}_gauge{i}", 0.35, 0.1, (x, -1.05, 1.6), white, n=8, rot=(90, 0, 0), parent=root, coll=coll)
        box(f"{name}_needle{i}", (0.04, 0.05, 0.3), (x, -1.12, 1.68), mat("needle", (0.05, 0.05, 0.05)),
            parent=root, coll=coll, rot=(0, 30 - 60 * i, 0))
    cyl(f"{name}_hose", 0.35, 6.0, (0, 0, 7.9), gray, n=8, parent=root, coll=coll)
    text(f"{name}_label", "PUMP", (0, -1.03, 0.6), 0.6, mat("pump_label", (1, 1, 1)), parent=root, coll=coll)
    return root, (0, 0, 11.0)


def water_spray(name, at, frame_start, frame_end, direction=(0.4, -0.3, 1.0), speed=14,
                rate=2, life=36, seed=0, coll=None):
    """Fountain of chunky blue cubes shooting out of `at` (ballistic)."""
    rnd = random.Random(seed)
    m = [mat("spray_a", (0.35, 0.65, 1.0), emit=0.6), mat("spray_b", (0.8, 0.92, 1.0), emit=0.6)]
    g = 9.8
    n = 0
    for f0 in range(frame_start, frame_end, rate):
        for j in range(3):
            o = box(f"{name}_{n}", (0.6, 0.6, 0.6), at, rnd.choice(m), coll=coll)
            n += 1
            vx = direction[0] * speed + rnd.uniform(-2, 2)
            vy = direction[1] * speed + rnd.uniform(-2, 2)
            vz = direction[2] * speed + rnd.uniform(-2, 2)
            o.scale = (0.001,) * 3
            o.keyframe_insert("scale", frame=f0 - 1)
            for k in range(0, life + 1, 3):
                t = k / 24
                o.location = (at[0] + vx * t, at[1] + vy * t, at[2] + vz * t - 0.5 * g * t * t)
                o.scale = (1.0,) * 3 if k < life else (0.001,) * 3
                o.keyframe_insert("location", frame=f0 + k)
                o.keyframe_insert("scale", frame=f0 + k)
