"""Night / Fourth of July kit: dusk sky, fireworks, the fireworks barge,
burning things (flames + smoke) and flickering fire light.

    s = reset_scene(F); dusk(s)            # orange horizon, deep blue sky, warm rim sun
    firework("FW1", launch, burst, frame, color)
    rocket_streak("R1", start, end, frame)  # flat, fast rocket (no arc) + burst at the end
    b = make_barge("Barge", loc, rot_z)     # b["tubes"]: local mortar positions
    fire("Fire1", at, start, end, size)     # flickering flame cones + rising smoke
"""
import math
import random
import bpy
from mathutils import Vector
from .common import mat, mesh_obj, empty, box, cyl, ico, text, link, LOOK, HD

FW_COLORS = [(1.0, 0.12, 0.08), (1.0, 0.95, 0.85), (0.2, 0.4, 1.0), (1.0, 0.7, 0.1),
             (0.25, 1.0, 0.3), (1.0, 0.25, 0.85), (1.0, 0.12, 0.08), (0.2, 0.4, 1.0)]


# ---------------------------------------------------------------- sky
def dusk(s, horizon=(1.0, 0.48, 0.22), mid=(0.50, 0.24, 0.38), zenith=(0.07, 0.07, 0.20),
         sun=True, ambient=0.12, ambient_color=(0.55, 0.6, 1.0)):
    """Fourth-of-July dusk: gradient sky (orange horizon -> purple -> deep
    blue), a low warm rim sun and a dim bluish ambient fill."""
    nt = s.world.node_tree
    bg = nt.nodes["Background"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.elements[0].position, cr.elements[0].color = 0.0, (*horizon, 1)
    cr.elements[1].position, cr.elements[1].color = 0.55, (*zenith, 1)
    e = cr.elements.new(0.14)
    e.color = (*mid, 1)
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    s["world_color"] = list(mid)
    for n in nt.nodes:                       # the object ambient fill from reset_scene
        if n.type == "BACKGROUND" and n is not bg:
            n.inputs[0].default_value = (*ambient_color, 1)
            n.inputs[1].default_value = ambient
    if sun:
        d = bpy.data.lights.new("DuskSun", "SUN")
        d.energy = 1.4
        d.color = (1.0, 0.55, 0.3)
        d.angle = math.radians(2.0) if HD else 0.0
        o = bpy.data.objects.new("DuskSun", d)
        o.rotation_euler = (math.radians(80), 0, math.radians(160))   # low, from behind the harbor
        s.collection.objects.link(o)
    # lights at night: house windows and the lighthouse lamp glow (cached by name,
    # so this must run before make_island)
    mat("window", (1.0, 0.75, 0.35), emit=1.6)
    return s


def flash_light(name, at, frame, color, energy=40000, decay=14, radius=1.0):
    """Point light that pops on at `frame` and fades out (fireworks, explosions)."""
    d = bpy.data.lights.new(name, "POINT")
    d.color = color[:3]
    d.shadow_soft_size = radius
    d.use_shadow = False
    o = bpy.data.objects.new(name, d)
    o.location = at
    bpy.context.scene.collection.objects.link(o)
    for f, e in ((frame - 1, 0), (frame, energy), (frame + decay // 3, energy * 0.45), (frame + decay, 0)):
        d.energy = e
        d.keyframe_insert("energy", frame=max(1, f))
    return o


# ---------------------------------------------------------------- fireworks
_SPARK_MESH = {}


def _spark(name, color, size):
    key = (tuple(round(c, 3) for c in color), size)
    if key not in _SPARK_MESH:
        o = ico(f"spark_src_{len(_SPARK_MESH)}", size, (0, 0, -9999), mat(f"fw_{key[0]}", color, emit=1.5),
                subdiv=0)
        o.hide_render = True
        _SPARK_MESH[key] = o.data
    return mesh_obj(name, None, None, None, mesh=_SPARK_MESH[key])


def _streak(name, color, length=1.6, width=0.12):
    o = cyl(name, width, length, (0, 0, 0), mat(f"fw_trail_{tuple(round(c, 3) for c in color)}", color, emit=6.0),
            n=4, r2=width * 0.3)
    return o


def _aim(o, d):
    o.rotation_euler = Vector(d).to_track_quat("Z", "Y").to_euler()


def burst(name, at, frame, color=None, count=40, radius=8.0, life=30, seed=0, light=True,
          size=0.34, gravity=3.0, ring=False):
    """Peony burst: sparks fly out radially, slow down, droop and fade."""
    rnd = random.Random(seed)
    color = color or rnd.choice(FW_COLORS)
    for i in range(count):
        o = _spark(f"{name}_s{i}", color, size)
        if ring:          # flat ring burst (looks great side-on)
            a = 2 * math.pi * i / count
            d = Vector((math.cos(a), rnd.uniform(-0.15, 0.15), math.sin(a)))
        else:
            d = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 1))).normalized()
        r = radius * rnd.uniform(0.8, 1.05)
        o.scale = (0.001,) * 3
        o.location = at
        o.keyframe_insert("scale", frame=frame - 1)
        o.keyframe_insert("location", frame=frame - 1)
        for k in range(0, life + 1, 2):
            t = k / life
            p = Vector(at) + d * r * (1 - (1 - t) ** 3)
            p.z -= gravity * t * t
            o.location = p
            sc = 1.6 if k == 0 else (1.0 if t < 0.55 else max(0.001, (1 - t) / 0.45))
            o.scale = (sc,) * 3
            o.keyframe_insert("location", frame=frame + k)
            o.keyframe_insert("scale", frame=frame + k)
    core = _spark(f"{name}_core", (1, 1, 0.9), size * 3.5)
    core.location = at
    for f, sc in ((frame - 1, 0.001), (frame, 1.0), (frame + 3, 0.6), (frame + 6, 0.001)):
        core.scale = (sc,) * 3
        core.keyframe_insert("scale", frame=f)
    if light:
        flash_light(f"{name}_light", at, frame, color)
    return color


def firework(name, launch, burst_at, frame, color=None, rise=None, seed=0, **kw):
    """Mortar shell: a glowing streak rises from `launch` to `burst_at` (arriving
    `rise` frames after `frame`) and bursts. Returns the burst frame."""
    launch, burst_at = Vector(launch), Vector(burst_at)
    rise = rise or max(8, int((burst_at - launch).length / 1.6))
    rnd = random.Random(seed)
    color = color or rnd.choice(FW_COLORS)
    s = _streak(f"{name}_shell", (1.0, 0.85, 0.6))
    _aim(s, burst_at - launch)
    s.scale = (0.001,) * 3
    s.keyframe_insert("scale", frame=frame - 1)
    for k in range(0, rise + 1, 2):
        t = k / rise
        s.location = launch + (burst_at - launch) * (1 - (1 - t) ** 1.6)
        s.scale = (1, 1, 1)
        s.keyframe_insert("location", frame=frame + k)
        s.keyframe_insert("scale", frame=frame + k)
    s.scale = (0.001,) * 3
    s.keyframe_insert("scale", frame=frame + rise + 1)
    burst(name, tuple(burst_at), frame + rise, color, seed=seed, **kw)
    return frame + rise


def rocket_streak(name, start, end, frame, frames=10, color=None, seed=0, pop=True, **kw):
    """A rocket that fires FLAT and fast from start to end (the tipped barge),
    leaving a short spark trail, then pops in a small burst."""
    start, end = Vector(start), Vector(end)
    rnd = random.Random(seed)
    color = color or rnd.choice(FW_COLORS)
    s = _streak(f"{name}_rkt", (1.0, 0.8, 0.45), length=2.6, width=0.18)
    _aim(s, end - start)
    s.scale = (0.001,) * 3
    s.keyframe_insert("scale", frame=frame - 1)
    for k in range(0, frames + 1):
        t = k / frames
        s.location = start + (end - start) * t + Vector((0, 0, 0.6 * math.sin(math.pi * t)))
        s.scale = (1, 1, 1)
        s.keyframe_insert("location", frame=frame + k)
        s.keyframe_insert("scale", frame=frame + k)
    s.scale = (0.001,) * 3
    s.keyframe_insert("scale", frame=frame + frames + 1)
    for i in range(6):                         # trail embers that hang and fade
        e = _spark(f"{name}_ember{i}", (1.0, 0.7, 0.3), 0.14)
        t = (i + 1) / 7
        p = start + (end - start) * t + Vector((0, 0, 0.6 * math.sin(math.pi * t)))
        f0 = frame + int(frames * t)
        e.location = p
        e.scale = (0.001,) * 3
        e.keyframe_insert("scale", frame=f0 - 1)
        e.scale = (1, 1, 1)
        e.keyframe_insert("scale", frame=f0)
        e.keyframe_insert("location", frame=f0)
        e.location = p + Vector((0, 0, -1.2))
        e.scale = (0.001,) * 3
        e.keyframe_insert("location", frame=f0 + 14)
        e.keyframe_insert("scale", frame=f0 + 14)
    if pop:
        burst(name, tuple(end), frame + frames, color, seed=seed, **{"count": 16, "radius": 3.5, "life": 18, **kw})
    return frame + frames


# ---------------------------------------------------------------- barge
def make_barge(name="Barge", loc=(0, 0, 0), rot_z=0.0, coll=None):
    """Flat gray fireworks barge (~16 x 7 m), rows of black mortar tubes,
    crates and a little shed. Origin at the waterline. Returns dict(root,
    tubes=[local xyz of each tube mouth])."""
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    hull = mat("barge_hull", (0.30, 0.31, 0.33))
    deck = mat("barge_deck", (0.45, 0.43, 0.40))
    rust = mat("barge_rust", (0.50, 0.25, 0.12))
    tube = mat("mortar", (0.08, 0.08, 0.09))
    crate = mat("crate", (0.60, 0.45, 0.25))
    red = mat("hazard_red", (0.85, 0.12, 0.10))
    white = mat("hazard_white", (0.95, 0.95, 0.92))
    L, W = 16.0, 7.0
    box(f"{name}_hull", (L, W, 1.6), (0, 0, 0.1), hull, parent=root, coll=coll)
    box(f"{name}_deck", (L - 0.3, W - 0.3, 0.1), (0, 0, 0.95), deck, parent=root, coll=coll)
    box(f"{name}_rust", (L + 0.02, W + 0.02, 0.25), (0, 0, -0.45), rust, parent=root, coll=coll)
    for k in range(8):                                   # hazard stripes along the rail
        box(f"{name}_haz{k}", (L / 8, W + 0.06, 0.18), (-L / 2 + L / 16 + k * L / 8, 0, 0.82),
            red if k % 2 else white, parent=root, coll=coll)
    tubes = []
    for ix in range(6):
        for iy in range(4):
            x, y = -5.5 + ix * 1.6, -2.2 + iy * 1.45
            cyl(f"{name}_tube{ix}{iy}", 0.32, 1.4, (x, y, 1.65), tube, n=8, parent=root, coll=coll,
                rot=(0, 0, 0))
            tubes.append((x, y, 2.4))
    rack = mat("rack_wood", (0.42, 0.30, 0.18))
    box(f"{name}_rack", (10.2, 6.4, 0.5), (-1.5, 0, 1.25), rack, parent=root, coll=coll)
    box(f"{name}_shed", (3.0, 3.0, 2.4), (6.0, 0.8, 2.2), white, parent=root, coll=coll)
    box(f"{name}_shedroof", (3.3, 3.3, 0.2), (6.0, 0.8, 3.5), red, parent=root, coll=coll)
    for k, (x, y) in enumerate([(6.3, -2.4), (5.2, -2.6), (7.2, -1.9)]):
        box(f"{name}_crate{k}", (1.0, 1.0, 0.9), (x, y, 1.45), crate, parent=root, coll=coll,
            rot=(0, 0, k * 17))
    lbl = mat("barge_lbl", (0.95, 0.95, 0.92))
    text(f"{name}_label", "DANGER", (6.0, 0.8 - 1.52, 2.4), 0.55, mat("barge_lbl_red", (0.85, 0.1, 0.1)),
         parent=root, coll=coll, bold=True)
    text(f"{name}_side", "FIREWORKS", (0, -W / 2 - 0.02, 0.1), 0.9, lbl, parent=root, coll=coll, bold=True)
    return dict(root=root, tubes=tubes, size=(L, W))


def barge_point(b, local):
    """World position of a point given in barge-local coordinates (call after
    the barge's transform is set for the frame you care about)."""
    bpy.context.view_layer.update()
    return tuple(b["root"].matrix_world @ Vector(local))


# ---------------------------------------------------------------- fire
def fire(name, at, start, end, size=1.0, seed=0, smoke=True, light=True, light_energy=2500, coll=None):
    """Burning thing: flickering low-poly flame cones (scale jitter on twos),
    puffs of dark smoke rising, and an orange flickering point light."""
    rnd = random.Random(seed)
    cols = [mat("flame_o", (1.0, 0.42, 0.05), emit=5.0), mat("flame_y", (1.0, 0.82, 0.25), emit=6.0),
            mat("flame_r", (0.95, 0.18, 0.04), emit=4.0)]
    root = empty(name, at, coll=coll)
    for i in range(5):
        h = size * rnd.uniform(1.4, 2.4)
        r = size * rnd.uniform(0.35, 0.6)
        piv = empty(f"{name}_fp{i}", (rnd.uniform(-0.5, 0.5) * size, rnd.uniform(-0.5, 0.5) * size, 0),
                    root, coll)
        cyl(f"{name}_flame{i}", r, h, (0, 0, h / 2), cols[i % 3], n=5, r2=0, parent=piv, coll=coll)
        piv.scale = (0.001,) * 3
        piv.keyframe_insert("scale", frame=max(1, start - 1))
        for f in range(start, end + 1, 2):
            g = min(1.0, (f - start + 2) / 8)            # grows in over 8 frames
            k = rnd.uniform(0.7, 1.25)
            piv.scale = (g * rnd.uniform(0.85, 1.1), g * rnd.uniform(0.85, 1.1), g * k)
            piv.rotation_euler = (rnd.uniform(-0.12, 0.12), rnd.uniform(-0.12, 0.12), rnd.uniform(0, 6.28))
            piv.keyframe_insert("scale", frame=f)
            piv.keyframe_insert("rotation_euler", frame=f)
        for fc in piv.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"
    if smoke:
        sm = mat("smoke_dark", (0.10, 0.09, 0.10), flat=0.05)
        period = 40
        for i in range(6):
            o = ico(f"{name}_smoke{i}", size * 0.6, at, sm, coll=coll, subdiv=1)
            o.scale = (0.001,) * 3
            o.keyframe_insert("scale", frame=max(1, start - 1))
            drift = Vector((rnd.uniform(0.5, 1.5), rnd.uniform(-0.5, 0.5), 0)) * size
            f0 = start + i * period // 6
            while f0 < end + period:
                for k, t in ((0, 0.0), (period // 2, 0.5), (period - 1, 1.0)):
                    o.location = Vector(at) + Vector((0, 0, size * (1.5 + 6 * t))) + drift * t * 3
                    sc = 0.001 if t == 1.0 else 0.6 + 1.6 * t
                    if t == 0.0:
                        sc = 0.3
                    o.scale = (sc,) * 3
                    o.keyframe_insert("location", frame=f0 + k)
                    o.keyframe_insert("scale", frame=f0 + k)
                o.scale = (0.001,) * 3
                o.keyframe_insert("scale", frame=f0 + period)
                f0 += period + 1
    if light:
        d = bpy.data.lights.new(f"{name}_light", "POINT")
        d.color = (1.0, 0.5, 0.15)
        d.use_shadow = False
        d.shadow_soft_size = size
        lo = bpy.data.objects.new(f"{name}_light", d)
        lo.location = (at[0], at[1], at[2] + size * 1.5)
        bpy.context.scene.collection.objects.link(lo)
        d.energy = 0
        d.keyframe_insert("energy", frame=max(1, start - 1))
        for f in range(start, end + 1, 3):
            d.energy = light_energy * size * size * min(1.0, (f - start + 3) / 9) * rnd.uniform(0.7, 1.2)
            d.keyframe_insert("energy", frame=f)
    return root


def smoke_pall(name, center, spread=(40, 20), height=8, count=14, seed=0, coll=None):
    """Static-ish low smoke clouds hanging over a battle (slow drift)."""
    rnd = random.Random(seed)
    sm = mat("smoke_haze", (0.10, 0.09, 0.10), flat=0.05)
    S = bpy.context.scene
    for i in range(count):
        p = (center[0] + rnd.uniform(-1, 1) * spread[0], center[1] + rnd.uniform(-1, 1) * spread[1],
             center[2] + rnd.uniform(0.3, 1) * height)
        o = ico(f"{name}_{i}", rnd.uniform(2.0, 3.5), p, sm, coll=coll, subdiv=2)
        o.scale = (rnd.uniform(1.6, 2.4), rnd.uniform(0.8, 1.2), rnd.uniform(0.35, 0.55))
        o.keyframe_insert("location", frame=1)
        o.location.x += rnd.uniform(2, 5)
        o.keyframe_insert("location", frame=S.frame_end)
