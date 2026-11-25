"""Operation Cronchisk: spy-thriller props and sets (blocky, primitives only).

    night(s) / sunset(s)          sky moods (gradient world + matching sun)
    rain(name, center, ...)       falling rain streaks (shared mesh, cheap)
    make_dock, make_crate, make_lamp_post, make_neon_sign, make_briefcase
    make_office (HQ briefing room with wall screen), make_desert, make_pad
    make_vault_door + bite(), make_corridor, make_orbiter, make_parachute
    make_cell, make_blaster, make_carrot_stick, make_doomsday (+ countdown)
    make_cronchisk (the glowing pink crystal), make_yacht, make_jelly_mold
    make_swivel_chair, laser_grid, show/hide_at
"""
import math
import random

import bpy

from .common import box, cyl, ico, empty, mat, text, link, FPS, HD
from .agents import glass

PINK = (1.0, 0.35, 0.75)


# ---------------------------------------------------------------- visibility
def show_at(obj, f, hide_at=None):
    """Scale-pop an object in at frame f (and out at hide_at)."""
    s = tuple(obj.scale)
    obj.scale = (0.001,) * 3
    obj.keyframe_insert("scale", frame=max(0, f - 1))
    obj.scale = s
    obj.keyframe_insert("scale", frame=f)
    if hide_at:
        obj.keyframe_insert("scale", frame=hide_at - 1)
        obj.scale = (0.001,) * 3
        obj.keyframe_insert("scale", frame=hide_at)
    _const(obj)


def hide_at(obj, f):
    obj.keyframe_insert("scale", frame=max(0, f - 1))
    obj.scale = (0.001,) * 3
    obj.keyframe_insert("scale", frame=f)
    _const(obj)


def _const(obj, path="scale"):
    for fc in obj.animation_data.action.fcurves:
        if fc.data_path == path:
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"


def move(obj, f0, f1, a, b, ease=True, path="location"):
    """Keyframe obj.<path> from a at f0 to b at f1 (eased)."""
    setattr(obj, path, a)
    obj.keyframe_insert(path, frame=f0)
    setattr(obj, path, b)
    obj.keyframe_insert(path, frame=f1)
    if not ease:
        for fc in obj.animation_data.action.fcurves:
            if fc.data_path == path:
                for kp in fc.keyframe_points:
                    kp.interpolation = "LINEAR"


# ---------------------------------------------------------------- skies
def _gradient(s, horizon, mid, zenith, ambient, ambient_color):
    nt = s.world.node_tree
    bg = nt.nodes["Background"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.elements[0].position, cr.elements[0].color = 0.0, (*horizon, 1)
    cr.elements[1].position, cr.elements[1].color = 0.6, (*zenith, 1)
    e = cr.elements.new(0.16)
    e.color = (*mid, 1)
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    s["world_color"] = list(mid)
    for n in nt.nodes:
        if n.type == "BACKGROUND" and n is not bg:
            n.inputs[0].default_value = (*ambient_color, 1)
            n.inputs[1].default_value = ambient


def _sun(name, energy, color, rot):
    d = bpy.data.lights.new(name, "SUN")
    d.energy = energy
    d.color = color
    d.angle = math.radians(2.0) if HD else 0.0
    o = bpy.data.objects.new(name, d)
    o.rotation_euler = [math.radians(a) for a in rot]
    bpy.context.scene.collection.objects.link(o)
    return o


def night(s, moon=0.5, ambient=0.18):
    """Rainy neon night: deep blue-black sky, cold blue moonlight."""
    _gradient(s, (0.10, 0.12, 0.22), (0.04, 0.05, 0.12), (0.01, 0.01, 0.03), ambient, (0.45, 0.55, 1.0))
    return _sun("Moon", moon, (0.6, 0.7, 1.0), (55, 0, -30))


def sunset(s, energy=2.2, rot=(76, 0, 160)):
    """Golden-hour sky: orange horizon, pink, deep blue top; warm low sun."""
    _gradient(s, (1.0, 0.55, 0.2), (0.85, 0.35, 0.45), (0.12, 0.15, 0.4), 0.35, (0.8, 0.6, 0.9))
    return _sun("SunsetSun", energy, (1.0, 0.65, 0.4), rot)


def dark_room(s, ambient=0.06):
    """Interior with no sky: near-black world, only placed lights."""
    _gradient(s, (0.02, 0.02, 0.03), (0.01, 0.01, 0.02), (0.0, 0.0, 0.0), ambient, (0.6, 0.6, 0.8))


def point_light(name, loc, energy=500, color=(1, 1, 1), radius=0.3, shadow=True):
    d = bpy.data.lights.new(name, "POINT")
    d.energy = energy
    d.color = color
    d.shadow_soft_size = radius
    d.use_shadow = shadow
    o = bpy.data.objects.new(name, d)
    o.location = loc
    bpy.context.scene.collection.objects.link(o)
    return o


def spot_light(name, loc, target, energy=2000, color=(1, 1, 1), angle=30, blend=0.3):
    d = bpy.data.lights.new(name, "SPOT")
    d.energy = energy
    d.color = color
    d.spot_size = math.radians(angle)
    d.spot_blend = blend
    o = bpy.data.objects.new(name, d)
    o.location = loc
    from mathutils import Vector
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.collection.objects.link(o)
    return o


# ---------------------------------------------------------------- weather
_RAIN = {}


def rain(name, center, f0, f1, size=(16, 10), height=12, count=160, speed=26, seed=0, coll=None):
    """Rain: thin light streaks that fall and loop (one shared mesh)."""
    rnd = random.Random(seed)
    if "mesh" not in _RAIN or _RAIN["mesh"].name not in bpy.data.meshes:
        tmp = box("_rainproto", (0.025, 0.025, 0.6), material=glass("rain_m", (0.75, 0.85, 1.0), 0.45, 1.2))
        _RAIN["mesh"] = tmp.data
        bpy.data.objects.remove(tmp, do_unlink=True)
    me = _RAIN["mesh"]
    period = max(4, int(height / speed * FPS))
    for i in range(count):
        o = bpy.data.objects.new(f"{name}{i}", me)
        link(o, None, coll)
        x = center[0] + rnd.uniform(-size[0] / 2, size[0] / 2)
        y = center[1] + rnd.uniform(-size[1] / 2, size[1] / 2)
        off = rnd.randint(0, period)
        o.rotation_euler[1] = math.radians(8)
        for f in range(f0 - period, f1 + period, period):
            for k, z in ((0, height), (period - 1, 0.0)):
                o.location = (x, y, center[2] + z)
                o.keyframe_insert("location", index=2, frame=f + off + k)
            o.location.z = center[2] + height
        for fc in o.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"


# ---------------------------------------------------------------- harbor
def make_dock(name="Dock", loc=(0, 0, 0), size=(14, 8), coll=None):
    root = empty(name, loc, coll=coll)
    wood = mat("dock_wood", (0.32, 0.24, 0.17))
    wet = mat("dock_wet", (0.22, 0.17, 0.13), rough=0.25, metal=0.2)
    n = int(size[0] / 0.5)
    for i in range(n):
        box(f"{name}_plank{i}", (0.46, size[1], 0.2), (-size[0] / 2 + 0.25 + i * 0.5, 0, -0.1),
            wet if i % 3 == 0 else wood, parent=root, coll=coll)
    for x in range(int(-size[0] / 2), int(size[0] / 2) + 1, 3):
        for y in (-size[1] / 2, size[1] / 2):
            cyl(f"{name}_post{x}{y}", 0.2, 3, (x, y, -1.2), wood, n=6, parent=root, coll=coll)
    return root


def make_crate(name, loc, s=1.0, rot_z=0, coll=None, color=(0.5, 0.36, 0.2)):
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    m = mat(f"crate_{color}", color)
    d = mat(f"crate_d_{color}", tuple(c * 0.6 for c in color))
    box(f"{name}_b", (s, s, s), (0, 0, s / 2), m, parent=root, coll=coll)
    for k in (-1, 1):
        box(f"{name}_slat{k}", (s * 1.02, s * 1.02, s * 0.1), (0, 0, s / 2 + k * s * 0.33), d, parent=root, coll=coll)
    return root


def make_lamp_post(name, loc, h=4.5, color=(1.0, 0.8, 0.5), energy=400, coll=None):
    root = empty(name, loc, coll=coll)
    iron = mat("lamp_iron", (0.08, 0.08, 0.09))
    cyl(f"{name}_pole", 0.08, h, (0, 0, h / 2), iron, n=6, parent=root, coll=coll)
    box(f"{name}_arm", (0.7, 0.1, 0.1), (0.3, 0, h), iron, parent=root, coll=coll)
    cyl(f"{name}_shade", 0.3, 0.25, (0.6, 0, h - 0.1), iron, n=8, r2=0.1, parent=root, coll=coll)
    ico(f"{name}_bulb", 0.14, (0.6, 0, h - 0.27), mat(f"lamp_bulb_{color}", color, emit=6.0), parent=root, coll=coll)
    l = bpy.data.lights.new(f"{name}_light", "POINT")
    l.energy, l.color, l.shadow_soft_size = energy, color, 0.2
    lo = bpy.data.objects.new(f"{name}_light", l)
    lo.location = (0.6, 0, h - 0.5)
    link(lo, root, coll)
    return root


def make_neon_sign(name, body, loc, size=1.0, color=(1.0, 0.2, 0.6), rot=(90, 0, 0), energy=300, coll=None,
                   flicker=None):
    """Glowing neon word on a dark backing board, with a colored light."""
    root = empty(name, loc, coll=coll)
    root.rotation_euler = [math.radians(a) - math.radians(r0) for a, r0 in zip(rot, (90, 0, 0))]
    w = len(body) * 0.62 * size + 0.6
    box(f"{name}_board", (w, 0.15, 1.3 * size), (0, 0.12, 0), mat("neon_board", (0.05, 0.05, 0.07)), parent=root,
        coll=coll)
    t = text(f"{name}_txt", body, (0, -0.02, 0), size, mat(f"neon_{color}", color, emit=7.0), parent=root, coll=coll,
             bold=True, extrude=0.03)
    l = bpy.data.lights.new(f"{name}_light", "POINT")
    l.energy, l.color, l.use_shadow = energy, color, False
    lo = bpy.data.objects.new(f"{name}_light", l)
    lo.location = (0, -1.0, 0)
    link(lo, root, coll)
    if flicker:
        f0, f1 = flicker
        rnd = random.Random(len(body))
        f = f0
        while f < f1:
            on = rnd.random() > 0.25
            l.energy = energy if on else energy * 0.1
            l.keyframe_insert("energy", frame=f)
            f += rnd.randint(2, 9)
        for fc in l.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"
    return root, t


def make_briefcase(name="Case", loc=(0, 0, 0), coll=None, color=(0.08, 0.08, 0.09), open_lid=False):
    """Black briefcase (root at the hinge-side bottom). r['lid'] rotates open on X.
    Inside: rolled blueprints + a pink glow."""
    root = empty(name, loc, coll=coll)
    m = mat(f"case_{color}", color, rough=0.3, metal=0.3)
    chrome = mat("case_chrome", (0.8, 0.8, 0.85), metal=0.9, rough=0.2)
    box(f"{name}_base", (0.8, 0.55, 0.12), (0, 0, 0.06), m, parent=root, coll=coll)
    lid = empty(f"{name}_lidp", (0, 0.275, 0.12), parent=root, coll=coll)
    box(f"{name}_lid", (0.8, 0.55, 0.1), (0, -0.275, 0.05), m, parent=lid, coll=coll)
    box(f"{name}_handle", (0.24, 0.05, 0.06), (0, -0.3, 0.12), chrome, parent=root, coll=coll)
    for s in (-1, 1):
        box(f"{name}_latch{s}", (0.06, 0.03, 0.05), (s * 0.25, -0.28, 0.11), chrome, parent=root, coll=coll)
    bp = mat("blueprint", (0.15, 0.35, 0.85), emit=0.6)
    for k in range(3):
        cyl(f"{name}_roll{k}", 0.05, 0.6, (0, -0.15 + k * 0.12, 0.15), bp, n=6, rot=(0, 90, 0), parent=root,
            coll=coll)
    ico(f"{name}_glow", 0.07, (0.25, 0.1, 0.15), mat("crystal_glow", PINK, emit=4.0), parent=root, coll=coll)
    if open_lid:
        lid.rotation_euler[0] = math.radians(-100)
    return dict(root=root, lid=lid)


def open_case(case, f, frames=8, deg=-105):
    lid = case["lid"]
    lid.rotation_euler[0] = 0
    lid.keyframe_insert("rotation_euler", index=0, frame=f)
    lid.rotation_euler[0] = math.radians(deg)
    lid.keyframe_insert("rotation_euler", index=0, frame=f + frames)


def make_drain(name, loc, coll=None):
    root = empty(name, loc, coll=coll)
    iron = mat("drain_iron", (0.12, 0.12, 0.13), metal=0.6, rough=0.4)
    box(f"{name}_hole", (1.2, 1.2, 0.02), (0, 0, 0.012), mat("drain_dark", (0.0, 0.0, 0.0)), parent=root, coll=coll)
    for i in range(5):
        box(f"{name}_bar{i}", (1.2, 0.08, 0.05), (0, -0.48 + i * 0.24, 0.03), iron, parent=root, coll=coll)
    box(f"{name}_frame", (1.3, 1.3, 0.03), (0, 0, 0.0), iron, parent=root, coll=coll)
    return root


def make_skylight(name, loc, w=3.0, coll=None):
    """A glass ceiling panel and the shards that burst from it."""
    root = empty(name, loc, coll=coll)
    box(f"{name}_glass", (w, w, 0.05), (0, 0, 0), glass("skylight_m", (0.7, 0.85, 1.0), 0.3, 0.6), parent=root,
        coll=coll)
    return root


def shards(name, at, frame, count=26, power=5.0, life=30, seed=0, coll=None):
    """Glass shards that burst outward and fall."""
    rnd = random.Random(seed)
    m = glass("shard_m", (0.8, 0.92, 1.0), 0.55, 1.5)
    for i in range(count):
        o = box(f"{name}{i}", (rnd.uniform(0.1, 0.3), 0.02, rnd.uniform(0.1, 0.35)), at, m, coll=coll)
        v = (rnd.uniform(-1, 1) * power * 0.5, rnd.uniform(-1, 1) * power * 0.5, rnd.uniform(-0.5, 0.6) * power)
        o.scale = (0.001,) * 3
        o.keyframe_insert("scale", frame=frame - 1)
        o.scale = (1, 1, 1)
        o.keyframe_insert("scale", frame=frame)
        for k in range(0, life + 1, 2):
            t = k / FPS
            z = at[2] + v[2] * t - 9.8 * t * t
            o.location = (at[0] + v[0] * t, at[1] + v[1] * t, max(0.02, z))
            o.rotation_euler = (t * 8 + i, t * 5, t * 6)
            o.keyframe_insert("location", frame=frame + k)
            o.keyframe_insert("rotation_euler", frame=frame + k)


def make_warehouse(name="Warehouse", loc=(0, 0, 0), w=16, d=10, h=6, coll=None):
    """Harbor warehouse interior: back wall, side walls, roof beams, a hanging lamp."""
    root = empty(name, loc, coll=coll)
    wall = mat("wh_wall", (0.25, 0.27, 0.3))
    brick = mat("wh_brick", (0.35, 0.18, 0.14))
    beam = mat("wh_beam", (0.15, 0.12, 0.1))
    box(f"{name}_floor", (w, d + 20, 0.2), (0, -10, -0.1), mat("wh_floor", (0.2, 0.2, 0.22), rough=0.3, metal=0.1),
        parent=root, coll=coll)
    box(f"{name}_ceil", (w, d + 20, 0.3), (0, -10, h + 0.3), mat("wh_ceil", (0.1, 0.09, 0.09)), parent=root,
        coll=coll)
    box(f"{name}_back", (w, 0.3, h), (0, d / 2, h / 2), brick, parent=root, coll=coll)
    for s in (-1, 1):
        box(f"{name}_side{s}", (0.3, d, h), (s * w / 2, 0, h / 2), wall, parent=root, coll=coll)
    for i in range(5):
        box(f"{name}_beam{i}", (w, 0.25, 0.35), (0, -d / 2 + i * d / 4, h), beam, parent=root, coll=coll)
    for i in range(6):           # brick rows
        box(f"{name}_mortar{i}", (w, 0.32, 0.04), (0, d / 2 - 0.01, 0.6 + i * 0.9), mat("wh_mortar", (0.4, 0.38, 0.36)),
            parent=root, coll=coll)
    return root


# ---------------------------------------------------------------- HQ
def make_office(name="HQ", loc=(0, 0, 0), coll=None, screen_mat=None):
    """Agency briefing room: dark wood panels, long desk, a big wall screen
    (r['screen'] is the screen object; pass screen_mat for its picture)."""
    root = empty(name, loc, coll=coll)
    panel = mat("hq_panel", (0.28, 0.17, 0.1))
    dark = mat("hq_dark", (0.12, 0.08, 0.05))
    box(f"{name}_floor", (14, 12, 0.2), (0, 0, -0.1), mat("hq_carpet", (0.35, 0.08, 0.1)), parent=root, coll=coll)
    box(f"{name}_wall", (14, 0.3, 7), (0, 4, 3.5), panel, parent=root, coll=coll)
    for i in range(-3, 4):
        box(f"{name}_strip{i}", (0.08, 0.32, 7), (i * 2, 3.98, 3.5), dark, parent=root, coll=coll)
    for s in (-1, 1):
        box(f"{name}_side{s}", (0.3, 12, 7), (s * 7, -2, 3.5), panel, parent=root, coll=coll)
    box(f"{name}_frame", (5.4, 0.2, 3.3), (0, 3.85, 3.6), mat("hq_frame", (0.05, 0.05, 0.06)), parent=root, coll=coll)
    scr = box(f"{name}_screen", (5.0, 0.1, 2.9), (0, 3.74, 3.6),
              screen_mat or mat("hq_screen", (0.1, 0.25, 0.35), emit=1.2), parent=root, coll=coll)
    desk = mat("hq_desk", (0.2, 0.12, 0.07), rough=0.4)
    box(f"{name}_desk", (3.2, 1.3, 0.12), (0, 0.6, 1.0), desk, parent=root, coll=coll)
    for x in (-1.4, 1.4):
        box(f"{name}_dleg{x}", (0.3, 1.1, 1.0), (x, 0.6, 0.5), desk, parent=root, coll=coll)
    box(f"{name}_lamp", (0.15, 0.15, 0.45), (1.1, 0.5, 1.28), mat("hq_brass", (0.85, 0.65, 0.2), metal=0.7),
        parent=root, coll=coll)
    box(f"{name}_lampshade", (0.5, 0.25, 0.18), (1.1, 0.45, 1.52), mat("hq_green", (0.1, 0.5, 0.2), emit=0.8),
        parent=root, coll=coll)
    box(f"{name}_folder", (0.5, 0.35, 0.04), (-0.6, 0.4, 1.08), mat("hq_folder", (0.85, 0.7, 0.4)), parent=root,
        coll=coll)
    box(f"{name}_stamp", (0.3, 0.02, 0.08), (-0.6, 0.22, 1.105), mat("hq_red", (0.8, 0.05, 0.05), emit=0.5),
        parent=root, coll=coll, rot=(90, 0, 15))
    return dict(root=root, screen=scr)


def screen_picture(name, rows, palette):
    """Wall-screen material from ASCII art (glows)."""
    from .common import pixel_mat
    return pixel_mat(name, rows, palette, flat=1.4)


# ---------------------------------------------------------------- desert base
def make_desert(seed=3, coll=None, color=(0.86, 0.62, 0.36)):
    rnd = random.Random(seed)
    box("Sand", (400, 400, 1), (0, 100, -0.5), mat("sand", color), coll=coll)
    rock = [mat("mesa1", (0.72, 0.38, 0.22)), mat("mesa2", (0.62, 0.32, 0.2)), mat("mesa3", (0.8, 0.48, 0.28))]
    for i in range(9):
        x = rnd.uniform(-90, 90)
        y = rnd.uniform(60, 140)
        w, h = rnd.uniform(10, 30), rnd.uniform(8, 22)
        root = empty(f"Mesa{i}", (x, y, 0), coll=coll)
        box(f"Mesa{i}_a", (w, w * 0.6, h), (0, 0, h / 2), rock[i % 3], parent=root, coll=coll)
        box(f"Mesa{i}_b", (w * 1.15, w * 0.7, h * 0.25), (0, 0, h * 0.12), rock[(i + 1) % 3], parent=root, coll=coll)
    cac = mat("cactus", (0.2, 0.5, 0.25))
    for i in range(10):
        x, y = rnd.uniform(-30, 30), rnd.uniform(8, 50)
        if abs(x) < 7 and y < 20:
            continue
        h = rnd.uniform(1.5, 3)
        cyl(f"Cactus{i}", 0.25, h, (x, y, h / 2), cac, n=6, coll=coll)
        cyl(f"CactusArm{i}", 0.15, h * 0.4, (x + 0.4, y, h * 0.6), cac, n=6, coll=coll)


def make_pad(name="Pad", loc=(0, 0, 0), r=6.0, coll=None):
    """Landing pad: concrete disc, yellow ring and a big H, edge lights."""
    root = empty(name, loc, coll=coll)
    cyl(f"{name}_base", r, 0.2, (0, 0, 0.1), mat("pad_concrete", (0.55, 0.55, 0.56)), n=24, parent=root, coll=coll)
    cyl(f"{name}_ring", r * 0.88, 0.02, (0, 0, 0.21), mat("pad_yellow", (1.0, 0.8, 0.1)), n=24, parent=root, coll=coll)
    cyl(f"{name}_inner", r * 0.8, 0.03, (0, 0, 0.215), mat("pad_concrete", (0.55, 0.55, 0.56)), n=24, parent=root,
        coll=coll)
    y = mat("pad_yellow", (1.0, 0.8, 0.1))
    for s in (-1, 1):
        box(f"{name}_H{s}", (0.5, r * 0.9, 0.03), (s * r * 0.3, 0, 0.23), y, parent=root, coll=coll)
    box(f"{name}_Hx", (r * 0.6, 0.5, 0.03), (0, 0, 0.23), y, parent=root, coll=coll)
    for k in range(12):
        a = k / 12 * 2 * math.pi
        ico(f"{name}_light{k}", 0.12, (r * 0.95 * math.cos(a), r * 0.95 * math.sin(a), 0.25),
            mat("pad_light", (0.3, 1.0, 0.4), emit=5.0), parent=root, coll=coll)
    return root


def make_lab_building(name="Lab", loc=(0, 0, 0), coll=None):
    """Low concrete bunker with a satellite dish and a red-striped door."""
    root = empty(name, loc, coll=coll)
    c = mat("lab_concrete", (0.7, 0.7, 0.68))
    box(f"{name}_body", (14, 8, 4), (0, 0, 2), c, parent=root, coll=coll)
    box(f"{name}_roof", (14.6, 8.6, 0.4), (0, 0, 4.2), mat("lab_roof", (0.45, 0.45, 0.47)), parent=root, coll=coll)
    box(f"{name}_door", (2.4, 0.1, 3), (0, -4.02, 1.5), mat("lab_door", (0.3, 0.32, 0.35), metal=0.5), parent=root,
        coll=coll)
    for k in range(4):
        box(f"{name}_stripe{k}", (2.4, 0.12, 0.15), (0, -4.04, 0.4 + k * 0.7),
            mat("lab_stripe", (0.9, 0.1, 0.05), emit=0.5), parent=root, coll=coll)
    dish = cyl(f"{name}_dish", 1.6, 0.4, (4, 1, 5.6), mat("lab_dish", (0.9, 0.9, 0.92)), n=12, r2=0.3,
               parent=root, coll=coll, rot=(-40, 0, 0))
    cyl(f"{name}_dishpole", 0.12, 1.4, (4, 1, 4.8), c, n=6, parent=root, coll=coll)
    return dict(root=root, dish=dish)


def make_vault_door(name="Vault", loc=(0, 0, 0), r=2.2, coll=None, rot_z=0):
    """Round steel vault door in a wall. Returns dict(root, chunks): chunks are
    the door segments that bite() removes one by one."""
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    steel = mat("vault_steel", (0.62, 0.64, 0.68), metal=0.7, rough=0.35)
    dark = mat("vault_dark", (0.35, 0.36, 0.4), metal=0.6, rough=0.4)
    box(f"{name}_wall", (12, 0.8, 7), (0, 0.6, 3.5), mat("vault_wall", (0.55, 0.55, 0.53)), parent=root, coll=coll)
    box(f"{name}_hole", (r * 2.1, 0.82, r * 2.1), (0, 0.6, r + 0.3), mat("vault_black", (0.02, 0.02, 0.02)),
        parent=root, coll=coll)
    for k in range(16):                     # the rim: a ring of steel blocks round the hole
        a = 2 * math.pi * k / 16
        box(f"{name}_rim{k}", (0.9, 0.3, 0.5), (r * 1.12 * math.cos(a), 0.05, r + 0.3 + r * 1.12 * math.sin(a)),
            dark, parent=root, coll=coll, rot=(0, -math.degrees(a), 0))
    chunks = []
    n = 8
    for i in range(n):                      # pie wedges, so bites take visible chunks
        a0 = 2 * math.pi * i / n
        verts = [(0, 0, 0)]
        for k in range(4):
            a = a0 + (2 * math.pi / n) * k / 3
            verts.append((r * math.cos(a), 0, r * math.sin(a)))
        verts += [(x, -0.4, z) for x, _, z in verts]
        m = len(verts) // 2
        faces = [tuple(range(m)), tuple(reversed(range(m, 2 * m)))]
        for k in range(m):
            j = (k + 1) % m
            faces.append((k, m + k, m + j, j))
        me = bpy.data.meshes.new(f"{name}_w{i}")
        me.from_pydata(verts, [], faces)
        me.materials.append(steel)
        o = bpy.data.objects.new(f"{name}_w{i}", me)
        o.location = (0, -0.1, r + 0.3)
        link(o, root, coll)
        chunks.append(o)
    hub = cyl(f"{name}_hub", 0.45, 0.6, (0, -0.4, r + 0.3), dark, n=12, rot=(90, 0, 0), parent=root, coll=coll)
    for k in range(3):
        box(f"{name}_spoke{k}", (1.6, 0.12, 0.14), (0, -0.7, r + 0.3), steel, parent=root, coll=coll,
            rot=(0, k * 60, 0))
    return dict(root=root, chunks=chunks, hub=hub)


# ---------------------------------------------------------------- corridors & ships
def make_corridor(name="Corridor", loc=(0, 0, 0), length=30, w=4, h=3.5, coll=None, color=(0.75, 0.77, 0.8),
                  lights=True):
    """Long sci-fi corridor along +Y: panels, floor stripes, ceiling light bars."""
    root = empty(name, loc, coll=coll)
    wall = mat(f"cor_wall_{color}", color)
    dark = mat(f"cor_dark_{color}", tuple(c * 0.55 for c in color))
    box(f"{name}_floor", (w, length, 0.2), (0, length / 2, -0.1), mat("cor_floor", (0.3, 0.32, 0.35), rough=0.3,
        metal=0.3), parent=root, coll=coll)
    box(f"{name}_ceil", (w, length, 0.2), (0, length / 2, h), dark, parent=root, coll=coll)
    for s in (-1, 1):
        box(f"{name}_wall{s}", (0.2, length, h), (s * w / 2, length / 2, h / 2), wall, parent=root, coll=coll)
        box(f"{name}_stripe{s}", (0.05, length, 0.12), (s * (w / 2 - 0.12), length / 2, 0.8),
            mat("cor_stripe", (1.0, 0.75, 0.1), emit=0.6), parent=root, coll=coll)
    for i in range(int(length / 3)):
        y = i * 3 + 1.5
        for s in (-1, 1):
            box(f"{name}_rib{i}{s}", (0.3, 0.3, h), (s * (w / 2 - 0.1), y, h / 2), dark, parent=root, coll=coll)
        if lights:
            box(f"{name}_lbar{i}", (w * 0.5, 0.25, 0.06), (0, y, h - 0.12), mat("cor_light", (0.9, 0.95, 1.0), emit=4.0),
                parent=root, coll=coll)
    box(f"{name}_end", (w, 0.2, h), (0, length, h / 2), dark, parent=root, coll=coll)
    return root


def make_orbiter(name="Orbiter", loc=(0, 0, 0), rot_z=0.0, scale=1.0, coll=None):
    """THE ORBITER: Jelly's stealth saucer-jet. Flat grey flying wing with a
    domed cockpit, purple underglow, blinking lights. Nose -Y. Returns
    dict(root, glow, gear, windows)."""
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    root.scale = (scale,) * 3
    hull = mat("orb_hull", (0.5, 0.52, 0.58), metal=0.5, rough=0.45)
    dark = mat("orb_dark", (0.2, 0.21, 0.25), metal=0.4, rough=0.5)
    verts = [(0, -6, 0), (7, 2.5, 0), (2.5, 4, 0), (0, 3, 0), (-2.5, 4, 0), (-7, 2.5, 0)]
    top = [(x * 0.92, y * 0.92, 0.6) for x, y, _ in verts]
    v = verts + top
    faces = [tuple(reversed(range(6))), tuple(range(6, 12))]
    for k in range(6):
        j = (k + 1) % 6
        faces.append((k, j, 6 + j, 6 + k))
    me = bpy.data.meshes.new(f"{name}_wing")
    me.from_pydata(v, [], faces)
    me.materials.append(hull)
    w = bpy.data.objects.new(f"{name}_wing", me)
    link(w, root, coll)
    dome = ico(f"{name}_dome", 1.6, (0, -0.5, 0.6), glass("orb_glass", (0.4, 0.9, 1.0), 0.5, 0.8), parent=root,
               coll=coll, subdiv=2)
    dome.scale = (1, 1.4, 0.55)
    box(f"{name}_spine", (1.2, 6, 0.5), (0, 0.5, 0.65), dark, parent=root, coll=coll)
    for s in (-1, 1):
        box(f"{name}_fin{s}", (0.15, 1.6, 1.4), (s * 2.2, 3, 1.2), dark, parent=root, coll=coll,
            rot=(0, s * 15, 0))
        cyl(f"{name}_eng{s}", 0.5, 0.4, (s * 1.6, 3.6, 0.3), mat("orb_engine", (0.7, 0.3, 1.0), emit=5.0), n=10,
            rot=(90, 0, 0), parent=root, coll=coll)
    glow = cyl(f"{name}_under", 2.5, 0.05, (0, 0.5, -0.03), mat("orb_glow", (0.7, 0.3, 1.0), emit=4.0), n=16,
               parent=root, coll=coll)
    lights = []
    for k, (x, y, c) in enumerate(((6.8, 2.4, (1, 0.1, 0.1)), (-6.8, 2.4, (0.1, 1, 0.2)), (0, -5.8, (1, 1, 1)))):
        lights.append(ico(f"{name}_nav{k}", 0.15, (x, y, 0.3), mat(f"orb_nav{k}", c, emit=6.0), parent=root,
                          coll=coll))
    gear = empty(f"{name}_gear", (0, 0, 0), parent=root, coll=coll)
    for k, (x, y) in enumerate(((0, -3.5), (-2.5, 2), (2.5, 2))):
        cyl(f"{name}_strut{k}", 0.1, 1.4, (x, y, -0.7), dark, n=6, parent=gear, coll=coll)
        box(f"{name}_foot{k}", (0.6, 0.6, 0.1), (x, y, -1.4), dark, parent=gear, coll=coll)
    return dict(root=root, glow=glow, gear=gear, nav=lights, dome=dome)


def blink(obj, f0, f1, period=12, on=4, phase=0):
    s = tuple(obj.scale)
    for f in range(f0, f1 + 1):
        lit = ((f + phase) % period) < on
        obj.scale = s if lit else (0.001,) * 3
        obj.keyframe_insert("scale", frame=f)
    _const(obj)


def make_parachute(name="Chute", loc=(0, 0, 0), coll=None, colors=((0.95, 0.2, 0.15), (1, 1, 1))):
    """Striped round canopy (dome of wedges) + lines; root at the harness point."""
    root = empty(name, loc, coll=coll)
    n = 10
    R, H = 2.4, 3.2
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        v = [(0, 0, H + 0.9)]
        for a in (a0, (a0 + a1) / 2, a1):
            v.append((R * 0.7 * math.cos(a), R * 0.7 * math.sin(a), H + 0.6))
        for a in (a0, (a0 + a1) / 2, a1):
            v.append((R * math.cos(a), R * math.sin(a), H))
        faces = [(0, 1, 2), (0, 2, 3), (1, 4, 5, 2), (2, 5, 6, 3)]
        me = bpy.data.meshes.new(f"{name}_g{i}")
        me.from_pydata(v, [], faces)
        me.materials.append(mat(f"chute_{colors[i % 2]}", colors[i % 2]))
        o = bpy.data.objects.new(f"{name}_g{i}", me)
        link(o, root, coll)
    line = mat("chute_line", (0.9, 0.9, 0.9))
    for i in range(0, n, 2):
        a = 2 * math.pi * i / n
        x, y = R * math.cos(a), R * math.sin(a)
        L = math.sqrt(x * x + y * y + H * H)
        o = cyl(f"{name}_line{i}", 0.015, L, (x / 2, y / 2, H / 2), line, n=4, parent=root, coll=coll)
        from mathutils import Vector
        o.rotation_euler = Vector((x, y, H)).to_track_quat("Z", "Y").to_euler()
    return root


def make_cell(name="Cell", loc=(0, 0, 0), w=3.0, h=3.2, coll=None):
    """Brig cell front: bars with a door (r['door'] swings open on Z)."""
    root = empty(name, loc, coll=coll)
    bar = mat("cell_bar", (0.3, 0.3, 0.35), metal=0.7, rough=0.3)
    for i in range(7):
        x = -w / 2 + i * w / 6
        if 2 <= i <= 4:
            continue
        cyl(f"{name}_bar{i}", 0.05, h, (x, 0, h / 2), bar, n=6, parent=root, coll=coll)
    box(f"{name}_top", (w + 0.2, 0.2, 0.2), (0, 0, h), bar, parent=root, coll=coll)
    door = empty(f"{name}_door", (-w / 6, 0, 0), parent=root, coll=coll)
    for i in range(3):
        cyl(f"{name}_dbar{i}", 0.05, h - 0.2, (i * w / 6 + w / 12, 0, h / 2), bar, n=6, parent=door, coll=coll)
    box(f"{name}_dbox", (0.25, 0.12, 0.3), (w / 3 - 0.05, -0.05, 1.2), mat("cell_lock", (0.8, 0.1, 0.1), emit=1.5),
        parent=door, coll=coll)
    return dict(root=root, door=door)


def make_blaster(name="Blaster", coll=None, color=(0.25, 0.25, 0.3)):
    """Toy-like ray gun (grip down, barrel along -Y) to hold in a hand."""
    root = empty(name, (0, 0, 0), coll=coll)
    m = mat(f"blaster_{color}", color, metal=0.4, rough=0.4)
    box(f"{name}_grip", (0.08, 0.1, 0.22), (0, 0, 0.0), m, parent=root, coll=coll)
    cyl(f"{name}_barrel", 0.06, 0.4, (0, -0.2, 0.12), m, n=8, rot=(90, 0, 0), parent=root, coll=coll)
    cyl(f"{name}_tip", 0.08, 0.06, (0, -0.42, 0.12), mat("blaster_tip", (1.0, 0.2, 0.1), emit=3.0), n=8,
        rot=(90, 0, 0), parent=root, coll=coll)
    return root


def make_carrot_stick(name="Stick", coll=None):
    root = empty(name, (0, 0, 0), coll=coll)
    cyl(f"{name}_c", 0.05, 0.45, (0, -0.18, 0.1), mat("stick_orange", (1.0, 0.5, 0.08)), n=6, r2=0.02,
        rot=(90, 0, 0), parent=root, coll=coll)
    box(f"{name}_leaf", (0.04, 0.12, 0.12), (0, 0.06, 0.12), mat("stick_leaf", (0.25, 0.7, 0.2)), parent=root,
        coll=coll)
    return root


def make_rack(name="Rack", loc=(0, 0, 0), n=6, coll=None):
    """Weapons rack along X: a board with pegs."""
    root = empty(name, loc, coll=coll)
    box(f"{name}_board", (n * 0.6 + 0.4, 0.15, 1.6), (0, 0.1, 1.4), mat("rack_board", (0.25, 0.27, 0.3)),
        parent=root, coll=coll)
    return root


def make_cronchisk(name="Cronchisk", loc=(0, 0, 0), size=1.0, coll=None, light=400):
    """THE CRONCHISK: a glowing pink double-pointed crystal with a point light.
    root is the gem's center (spin it on Z)."""
    root = empty(name, loc, coll=coll)
    g = mat("cronchisk_m", PINK, emit=3.0)
    cyl(f"{name}_top", 0.35 * size, 0.6 * size, (0, 0, 0.3 * size), g, n=6, r2=0, parent=root, coll=coll)
    b = cyl(f"{name}_bot", 0.35 * size, 0.6 * size, (0, 0, -0.3 * size), g, n=6, r2=0, parent=root, coll=coll)
    b.rotation_euler[0] = math.pi
    for k in range(3):
        o = cyl(f"{name}_spur{k}", 0.12 * size, 0.4 * size, (0, 0, 0), g, n=6, r2=0, parent=root, coll=coll)
        a = k * 2 * math.pi / 3
        o.location = (0.3 * size * math.cos(a), 0.3 * size * math.sin(a), -0.05 * size)
        o.rotation_euler = (0.9 * math.sin(a), -0.9 * math.cos(a), 0)
    if light:
        l = bpy.data.lights.new(f"{name}_light", "POINT")
        l.energy, l.color, l.use_shadow = light * size, PINK, False
        lo = bpy.data.objects.new(f"{name}_light", l)
        link(lo, root, coll)
    return root


def make_doomsday(name="Doomsday", loc=(0, 0, 0), coll=None):
    """The doomsday satellite uplink: a big dish on a base, a crystal socket
    and a red countdown display. Returns dict(root, socket, display, dish)."""
    root = empty(name, loc, coll=coll)
    steel = mat("dd_steel", (0.45, 0.47, 0.52), metal=0.6, rough=0.4)
    dark = mat("dd_dark", (0.12, 0.12, 0.14))
    box(f"{name}_base", (4, 3, 1.6), (0, 0, 0.8), steel, parent=root, coll=coll)
    box(f"{name}_console", (3, 0.6, 0.8), (0, -1.6, 1.0), dark, parent=root, coll=coll, rot=(-25, 0, 0))
    cyl(f"{name}_mast", 0.35, 4, (0, 0.4, 3.6), steel, n=8, parent=root, coll=coll)
    dish = cyl(f"{name}_dish", 3.2, 0.8, (0, 0.4, 6.0), mat("dd_dish", (0.42, 0.44, 0.5), metal=0.5, rough=0.4), n=16, r2=0.6,
               parent=root, coll=coll, rot=(-60, 0, 0))
    cyl(f"{name}_feed", 0.08, 2.4, (0, -0.6, 6.6), steel, n=6, parent=root, coll=coll, rot=(-60, 0, 0))
    socket = empty(f"{name}_socket", (0, -1.3, 1.95), parent=root, coll=coll)
    cyl(f"{name}_sock", 0.45, 0.25, (0, 0, -0.1), mat("dd_sock", (0.2, 0.2, 0.25), metal=0.6), n=10, parent=socket,
        coll=coll)
    box(f"{name}_disp", (2.0, 0.1, 0.9), (0, -1.55, 2.9), dark, parent=root, coll=coll)
    for s in (-1, 1):
        ico(f"{name}_warn{s}", 0.18, (s * 1.7, -1.5, 1.8), mat("dd_warn", (1, 0.1, 0.05), emit=4.0), parent=root,
            coll=coll)
    return dict(root=root, socket=socket, dish=dish, display_at=(loc[0], loc[1] - 1.62, loc[2] + 2.9))


def countdown(name, at, f0, step, values, size=0.6, color=(1.0, 0.1, 0.05), coll=None, rot=(90, 0, 0)):
    """Digits that change every `step` frames starting at f0 (e.g. 10..1)."""
    m = mat(f"{name}_m", color, emit=6.0)
    objs = []
    for i, v in enumerate(values):
        o = text(f"{name}{i}", str(v), at, size, m, coll=coll, bold=True, rot=rot)
        last = i == len(values) - 1
        show_at(o, max(1, f0 + i * step) if i else 1, None if last else f0 + (i + 1) * step)
        objs.append(o)
    return objs


def laser_grid(name, origin, n=5, w=4.0, h=2.4, coll=None, color=(1.0, 0.05, 0.05)):
    """Security lasers across a corridor (thin glowing bars along X)."""
    m = mat(f"{name}_m", color, emit=8.0)
    root = empty(name, origin, coll=coll)
    for i in range(n):
        z = 0.4 + i * (h - 0.4) / max(1, n - 1)
        o = box(f"{name}{i}", (w, 0.025, 0.025), (0, 0, z), m, parent=root, coll=coll, rot=(0, (i % 2 * 2 - 1) * 8, 0))
        o.visible_shadow = False
    return root


def make_swivel_chair(name="Chair", loc=(0, 0, 0), rot_z=0, coll=None, color=(0.65, 0.05, 0.1)):
    """Villain's high-backed swivel chair (root spins on Z). Seat height 0.8."""
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    m = mat(f"chair_{color}", color, rough=0.5)
    steel = mat("chair_steel", (0.2, 0.2, 0.22), metal=0.7)
    cyl(f"{name}_stem", 0.08, 0.6, (0, 0, 0.3), steel, n=6, parent=root, coll=coll)
    for k in range(5):
        box(f"{name}_leg{k}", (0.6, 0.08, 0.06), (0, 0, 0.04), steel, parent=root, coll=coll, rot=(0, 0, k * 72))
    box(f"{name}_seat", (1.0, 0.9, 0.25), (0, 0, 0.72), m, parent=root, coll=coll)
    box(f"{name}_back", (1.1, 0.25, 1.8), (0, 0.45, 1.6), m, parent=root, coll=coll)
    for s in (-1, 1):
        box(f"{name}_arm{s}", (0.15, 0.8, 0.12), (s * 0.55, 0, 1.05), m, parent=root, coll=coll)
    return root


def make_yacht(name="Yacht", loc=(0, 0, 0), rot_z=0.0, coll=None):
    """White motor yacht, bow +X; deck at z~1.4. Returns dict(root, deck_z)."""
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    white = mat("yacht_white", (0.96, 0.96, 0.94))
    blue = mat("yacht_blue", (0.1, 0.2, 0.45))
    wood = mat("yacht_teak", (0.6, 0.38, 0.2))
    glassm = mat("yacht_glass", (0.1, 0.15, 0.25), metal=0.5, rough=0.2)
    box(f"{name}_hull", (12, 4, 1.4), (0, 0, 0.3), white, parent=root, coll=coll)
    cyl(f"{name}_bow", 2.0, 1.4, (6.0, 0, 0.3), white, n=3, parent=root, coll=coll).scale = (2.0, 1.0, 1.0)
    box(f"{name}_stripe", (12.05, 4.05, 0.2), (0, 0, -0.1), blue, parent=root, coll=coll)
    box(f"{name}_deck", (12, 3.8, 0.1), (0, 0, 1.05), wood, parent=root, coll=coll)
    box(f"{name}_cabin", (5, 3, 1.4), (-0.5, 0, 1.8), white, parent=root, coll=coll)
    box(f"{name}_window", (5.05, 3.05, 0.5), (-0.5, 0, 2.0), glassm, parent=root, coll=coll)
    box(f"{name}_bridge", (3, 2.4, 0.9), (-1, 0, 2.95), white, parent=root, coll=coll)
    box(f"{name}_mast", (0.12, 0.12, 1.6), (-1, 0, 4.2), white, parent=root, coll=coll)
    for s in (-1, 1):
        box(f"{name}_rail{s}", (6, 0.06, 0.06), (-3.3 + 0, s * 1.85, 1.75), mat("yacht_chrome", (0.85, 0.85, 0.9),
            metal=0.9, rough=0.2), parent=root, coll=coll)
    return dict(root=root, deck_z=1.1)


def make_jelly_mold(name="Mold", loc=(0, 0, 0), coll=None, size=1.0):
    """A wobbly purple jelly mold on a plate (the carrot hides inside)."""
    root = empty(name, loc, coll=coll)
    cyl(f"{name}_plate", 0.6 * size, 0.04, (0, 0, 0.02), mat("plate", (1, 1, 1)), n=16, parent=root, coll=coll)
    j = glass("mold_jelly", (0.62, 0.25, 0.85), 0.6, 0.9)
    body = empty(f"{name}_body", (0, 0, 0.04), parent=root, coll=coll)
    for k in range(3):
        cyl(f"{name}_tier{k}", (0.45 - k * 0.1) * size, 0.22 * size, (0, 0, (0.11 + k * 0.22) * size), j, n=10,
            parent=body, coll=coll)
    return dict(root=root, body=body)


def make_glass_drink(name, coll=None, color=(1.0, 0.6, 0.2)):
    """Cocktail glass with an olive, to hold for the toast."""
    root = empty(name, (0, 0, 0), coll=coll)
    g = glass("drink_glass", (0.85, 0.95, 1.0), 0.35, 0.6)
    cyl(f"{name}_stem", 0.02, 0.18, (0, 0, 0.09), g, n=6, parent=root, coll=coll)
    cyl(f"{name}_bowl", 0.16, 0.16, (0, 0, 0.26), g, n=8, r2=0.02, parent=root, coll=coll).rotation_euler[0] = math.pi
    cyl(f"{name}_drink", 0.13, 0.04, (0, 0, 0.3), mat(f"drink_{color}", color, emit=0.8), n=8, parent=root, coll=coll)
    ico(f"{name}_olive", 0.04, (0.03, 0, 0.32), mat("olive", (0.4, 0.6, 0.1)), parent=root, coll=coll)
    return root


def beam_shot(name, a, b, f, life=4, color=(1.0, 0.15, 0.1), width=0.06, coll=None):
    """A blaster bolt: a glowing bar from a to b, visible for `life` frames."""
    from mathutils import Vector
    va, vb = Vector(a), Vector(b)
    d = vb - va
    o = cyl(name, width, d.length, tuple((va + vb) / 2), mat(f"bolt_{color}", color, emit=8.0), n=6, coll=coll)
    o.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    o.visible_shadow = False
    show_at(o, f, f + life)
    return o
