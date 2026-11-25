"""Kids' stories: the child's drawings as paper-cutout puppets in a bright
storybook diorama (kids/<story>/). Built for "Attack of the Jelly Man".

    p = puppet("05", (0, 0, 0))          # cutouts/05.png standing at the origin
    hop_to(p, 1, 40, (3, 0, 0), hops=3)  # waddle-hop over there
    pop(p, 10); flip(p, 50); vanish(p, 80, 90)

A puppet is root (location / turning) -> pivot (squash, tilt, flips) -> card
(the textured plane, bottom edge at the feet, facing the camera at -Y).
Cutouts are made from the drawings by tools/cutout.py; sizes and names come
from the story's story.py (CUTOUTS).
"""
import importlib.util
import math
import os
import random

import bpy

from .common import (mat, box, cyl, ico, empty, link, text, FPS, reset_scene, add_sun)

STORY = os.environ.get("JAWS_EPISODE_DIR", "")


def story():
    spec = importlib.util.spec_from_file_location("story", os.path.join(STORY, "story.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


_CFG = None


def cfg(key):
    global _CFG
    if _CFG is None:
        _CFG = story().CUTOUTS
    return _CFG[key]


# ---------------------------------------------------------------- puppets
_CMATS = {}


def cutout_mat(key, glow=0.55):
    """The cutout PNG as a two-sided, alpha-clipped, mostly self-lit material,
    so the kid's colors stay bright from any light."""
    if key in _CMATS:
        return _CMATS[key]
    img = bpy.data.images.load(os.path.join(STORY, "cutouts", f"{key}.png"), check_existing=True)
    m = bpy.data.materials.new(f"cut_{key}")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.extension = "CLIP"
    d = nt.nodes.new("ShaderNodeBsdfDiffuse")
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Strength"].default_value = glow
    add = nt.nodes.new("ShaderNodeAddShader")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(tex.outputs["Color"], d.inputs["Color"])
    nt.links.new(tex.outputs["Color"], e.inputs["Color"])
    nt.links.new(d.outputs[0], add.inputs[0])
    nt.links.new(e.outputs[0], add.inputs[1])
    nt.links.new(tex.outputs["Alpha"], mix.inputs[0])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(add.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    m.blend_method = "CLIP"
    m.shadow_method = "CLIP"
    m.alpha_threshold = 0.5
    m.use_backface_culling = False
    _CMATS[key] = m
    return m


class Puppet:
    def __init__(self, root, pivot, card, key, w, h):
        self.root, self.pivot, self.card, self.key, self.w, self.h = root, pivot, card, key, w, h


def puppet(key, loc=(0, 0, 0), height=None, name=None, rot_z=0.0, coll=None):
    m = cutout_mat(key)
    img = m.node_tree.nodes["Image Texture"].image
    h = height or cfg(key).get("height", 2.5)
    w = h * img.size[0] / img.size[1]
    name = name or cfg(key)["name"].replace(" ", "")
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    pivot = empty(name + "_pivot", (0, 0, 0), parent=root, coll=coll)
    v = [(-w / 2, 0, 0), (w / 2, 0, 0), (w / 2, 0, h), (-w / 2, 0, h)]
    me = bpy.data.meshes.new(name + "_card")
    me.from_pydata(v, [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new()
    for li, uvc in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
        uv.data[li].uv = uvc
    me.materials.append(m)
    card = bpy.data.objects.new(name + "_card", me)
    link(card, pivot, coll)
    sol = card.modifiers.new("paper", "SOLIDIFY")       # a little cardboard thickness
    sol.thickness = 0.03
    return Puppet(root, pivot, card, key, w, h)


def _key(o, path, f, idx=-1):
    o.keyframe_insert(path, frame=f, index=idx)


def place(p, f, loc=None, rz=None):
    if loc is not None:
        p.root.location = loc
        _key(p.root, "location", f)
    if rz is not None:
        p.root.rotation_euler[2] = math.radians(rz)
        _key(p.root, "rotation_euler", f, 2)


def hop_to(p, f0, f1, dest, hops=3, height=0.5, rock=8.0, start=None):
    """Waddle-hop from where it is (or start) to dest between f0 and f1:
    little arcs, rocking side to side like a paper puppet on a stick."""
    a = start or tuple(p.root.location)
    n = max(1, f1 - f0)
    for f in range(f0, f1 + 1):
        t = (f - f0) / n
        ph = t * hops * math.pi
        p.root.location = [a[i] + (dest[i] - a[i]) * t for i in range(3)]
        p.root.location.z += abs(math.sin(ph)) * height
        _key(p.root, "location", f)
        p.pivot.rotation_euler[1] = math.radians(rock * math.sin(ph)) if hops else 0
        _key(p.pivot, "rotation_euler", f, 1)
    p.pivot.rotation_euler[1] = 0
    _key(p.pivot, "rotation_euler", f1 + 2, 1)


def fly(p, f0, f1, pts, tilt=12.0, ease=True):
    """Fly through a list of points (smooth, Catmull-ish via sine easing per leg)."""
    legs = len(pts) - 1
    for f in range(f0, f1 + 1):
        t = (f - f0) / max(1, f1 - f0)
        if ease:
            t = 0.5 - 0.5 * math.cos(math.pi * t)
        k = min(legs - 1, int(t * legs))
        u = t * legs - k
        a, b = pts[k], pts[k + 1]
        p.root.location = [a[i] + (b[i] - a[i]) * u for i in range(3)]
        _key(p.root, "location", f)
        dx = b[0] - a[0]
        p.pivot.rotation_euler[1] = math.radians(tilt * (1 if dx > 0 else -1 if dx < 0 else 0)) \
            * math.sin(math.pi * min(1, max(0, (f - f0) / max(1, f1 - f0))))
        _key(p.pivot, "rotation_euler", f, 1)


def bob(p, f0, f1, amp=0.04, period=20, sway=3.0, phase=0.0):
    """Idle: breathe (squash/stretch) and sway."""
    for f in range(f0, f1 + 1, 2):
        s = math.sin(2 * math.pi * (f / period) + phase)
        p.pivot.scale = (1 - amp * s * 0.6, 1, 1 + amp * s)
        _key(p.pivot, "scale", f)
        p.pivot.rotation_euler[1] = math.radians(sway * math.sin(math.pi * f / period + phase))
        _key(p.pivot, "rotation_euler", f, 1)


def jiggle(p, f0, f1, amp=0.12, period=8):
    """Wobbly jelly squash."""
    for f in range(f0, f1 + 1):
        s = math.sin(2 * math.pi * f / period)
        p.pivot.scale = (1 + amp * s, 1, 1 - amp * s)
        _key(p.pivot, "scale", f)


def squash(p, f, amt=0.35, length=8):
    """Quick squash-and-stretch (landing, chomping, gulping)."""
    for df, sx, sz in ((0, 1, 1), (2, 1 + amt, 1 - amt), (5, 1 - amt * 0.4, 1 + amt * 0.5), (length, 1, 1)):
        p.pivot.scale = (sx, 1, sz)
        _key(p.pivot, "scale", f + df)


def pop(p, f, length=8, s=1.0):
    obj = p.root
    for df, k in ((-1, 0.001), (0, 0.001), (int(length * 0.6), 1.25), (length, 1.0)):
        obj.scale = (k * s,) * 3
        _key(obj, "scale", max(0, f + df))


def vanish(p, f0, f1):
    p.root.scale = p.root.scale.copy()
    _key(p.root, "scale", f0)
    p.root.scale = (0.001,) * 3
    _key(p.root, "scale", f1)


def flip(p, f, length=6):
    """Turn around: the card swings half a turn about its vertical axis (mirrored)."""
    rz = p.root.rotation_euler[2]
    _key(p.root, "rotation_euler", f, 2)
    p.root.rotation_euler[2] = rz + math.pi
    _key(p.root, "rotation_euler", f + length, 2)


def spin(obj, f0, f1, turns=1.0, axis=1):
    obj.rotation_euler[axis] = 0
    _key(obj, "rotation_euler", f0, axis)
    obj.rotation_euler[axis] = 2 * math.pi * turns
    _key(obj, "rotation_euler", f1, axis)
    for fc in obj.animation_data.action.fcurves:
        if fc.data_path == "rotation_euler" and fc.array_index == axis:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"


def hide(obj, f, show_at=None):
    """Scale an object to nothing at f (and back at show_at)."""
    s = obj.scale.copy()
    obj.keyframe_insert("scale", frame=f - 1)
    obj.scale = (0.001,) * 3
    obj.keyframe_insert("scale", frame=f)
    if show_at:
        obj.keyframe_insert("scale", frame=show_at - 1)
        obj.scale = s
        obj.keyframe_insert("scale", frame=show_at)


# ---------------------------------------------------------------- the world
SKY = (0.16, 0.48, 1.0)


def start(F, sky=SKY, sun=(52, 0, 28)):
    reset_scene(F, world_color=sky)
    add_sun(sun, energy=1.7)


def make_land(seed=1, houses=6, trees=8, hills=True, clouds=5, depth=40, ground=(0.20, 0.58, 0.12), coll=None):
    """Storybook countryside: green ground, round hills, little houses, lollipop
    trees and puffy clouds, all behind the action (y > 3)."""
    rnd = random.Random(seed)
    g = mat("kid_grass", ground)
    box("Ground", (200, 200, 1), (0, 60, -0.5), g, coll=coll)
    if hills:
        for i, (x, y, r, c) in enumerate(((-14, 34, 12, (0.14, 0.46, 0.10)), (10, 40, 15, (0.18, 0.52, 0.12)),
                                          (30, 30, 10, (0.12, 0.42, 0.09)), (-34, 28, 11, (0.16, 0.50, 0.11)))):
            h = ico(f"Hill{i}", r, (x, y, -r * 0.55), mat(f"kid_hill{i}", c), coll=coll, subdiv=2)
            h.scale.z = 0.8
    walls = [(1.0, 0.85, 0.55), (0.95, 0.6, 0.6), (0.7, 0.85, 1.0), (1.0, 1.0, 0.85), (0.8, 0.7, 1.0)]
    roofs = [(0.85, 0.2, 0.15), (0.3, 0.35, 0.8), (0.55, 0.3, 0.2), (0.2, 0.55, 0.3)]
    for i in range(houses):
        x = rnd.uniform(-16, 16)
        y = rnd.uniform(9, 22)
        s = rnd.uniform(1.6, 2.4)
        root = empty(f"House{i}", (x, y, 0), coll=coll)
        box(f"HouseW{i}", (s * 1.2, s, s), (0, 0, s / 2), mat(f"kid_wall{i % 5}", walls[i % 5]), parent=root, coll=coll)
        r = cyl(f"HouseR{i}", s * 0.95, s * 0.7, (0, 0, s + s * 0.35), mat(f"kid_roof{i % 4}", roofs[i % 4]),
                n=4, r2=0, parent=root, coll=coll)
        r.rotation_euler[2] = math.pi / 4
        r.scale.x = 1.15
        box(f"HouseD{i}", (s * 0.3, 0.05, s * 0.5), (0, -s / 2 - 0.02, s * 0.25), mat("kid_door", (0.45, 0.25, 0.12)),
            parent=root, coll=coll)
        for wx in (-0.3, 0.3):
            box(f"HouseWin{i}{wx}", (s * 0.22, 0.05, s * 0.22), (wx * s, -s / 2 - 0.02, s * 0.68),
                mat("kid_window", (0.75, 0.92, 1.0), emit=0.6), parent=root, coll=coll)
    for i in range(trees):
        x = rnd.choice([-1, 1]) * rnd.uniform(5, 20)
        y = rnd.uniform(5, 18)
        h = rnd.uniform(1.5, 2.6)
        cyl(f"Trunk{i}", 0.18, h, (x, y, h / 2), mat("kid_trunk", (0.5, 0.3, 0.15)), n=6, coll=coll)
        ico(f"Leaves{i}", h * 0.55, (x, y, h + h * 0.3), mat(f"kid_leaf{i % 3}",
            [(0.2, 0.6, 0.2), (0.3, 0.7, 0.15), (0.15, 0.5, 0.25)][i % 3]), coll=coll)
    white = mat("kid_cloud", (1, 1, 1), emit=0.8)
    for i in range(clouds):
        root = empty(f"Cloud{i}", (rnd.uniform(-25, 25), rnd.uniform(35, 50), rnd.uniform(14, 26)), coll=coll)
        for k in range(4):
            ico(f"Puff{i}{k}", rnd.uniform(1.6, 2.6), ((k - 1.5) * 2.0, 0, rnd.uniform(-0.4, 0.6)), white,
                parent=root, coll=coll)
        root.keyframe_insert("location", frame=1)
        root.location.x += 3
        root.keyframe_insert("location", frame=600)
        for fc in root.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"


def make_sun_disc(loc=(-9, 45, 24), r=4.0):
    s = ico("SunDisc", r, loc, mat("kid_sun", (1.0, 0.85, 0.2), emit=2.0), subdiv=2)
    return s


def glass(name, color, alpha=0.3, emit=0.4):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = (*color, 1)
    e.inputs["Strength"].default_value = emit
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    mix.inputs[0].default_value = alpha
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(e.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    m.blend_method = "BLEND"
    m.shadow_method = "NONE"
    m.show_transparent_back = False
    return m


def bubble(name, loc, r=2.0, color=(0.5, 0.95, 1.0), coll=None):
    """Force-field bubble: see-through glowing sphere with a shine spot."""
    b = ico(name, r, loc, glass(name + "_m", color, 0.28, 0.9), coll=coll, subdiv=3)
    for poly in b.data.polygons:
        poly.use_smooth = True
    ico(name + "_shine", r * 0.16, (-r * 0.45, -r * 0.8, r * 0.45), mat("kid_shine", (1, 1, 1), emit=2.0),
        parent=b, coll=coll)
    return b


def beam(name, loc, h=14.0, r=1.8, color=(1.0, 1.0, 0.6), coll=None):
    """Tractor beam / spotlight cone, apex at the top."""
    c = cyl(name, r, h, (loc[0], loc[1], loc[2] + h / 2), glass(name + "_m", color, 0.35, 1.5), n=16, r2=r * 0.25,
            coll=coll)
    return c


def make_platform(name, loc, r=2.2, coll=None):
    root = empty(name, loc, coll=coll)
    cyl(name + "_base", r, 0.5, (0, 0, 0.25), mat("kid_metal", (0.6, 0.62, 0.7)), n=24, parent=root, coll=coll)
    cyl(name + "_ring", r * 0.85, 0.06, (0, 0, 0.52), mat("kid_glow", (0.3, 1.0, 0.9), emit=3.0), n=24,
        parent=root, coll=coll)
    cyl(name + "_top", r * 0.7, 0.08, (0, 0, 0.55), mat("kid_metal2", (0.75, 0.78, 0.85)), n=24, parent=root,
        coll=coll)
    return root


def make_cage(name, loc, w=3.0, h=4.0, coll=None):
    """Trap: a box of bars with a roof (dropped over a villain)."""
    root = empty(name, loc, coll=coll)
    bar = mat("kid_bars", (0.35, 0.35, 0.4), metal=0.6, rough=0.4)
    n = 6
    for side in range(4):
        for i in range(n):
            u = -w / 2 + w * i / (n - 1)
            x, y = [(u, -w / 2), (w / 2, u), (-u, w / 2), (-w / 2, -u)][side]
            cyl(f"{name}_bar{side}{i}", 0.06, h, (x, y, h / 2), bar, n=6, parent=root, coll=coll)
    box(name + "_roof", (w + 0.3, w + 0.3, 0.25), (0, 0, h), bar, parent=root, coll=coll)
    box(name + "_floor", (w + 0.3, w + 0.3, 0.15), (0, 0, 0.07), bar, parent=root, coll=coll)
    return root


def make_crystal(name, loc, size=1.0, color=(0.75, 0.3, 1.0), coll=None):
    """The mysterious glowing thing on a pedestal (the "cronchisk")."""
    root = empty(name, loc, coll=coll)
    cyl(name + "_ped", 0.6 * size, 1.4 * size, (0, 0, 0.7 * size), mat("kid_stone", (0.75, 0.72, 0.68)), n=8,
        parent=root, coll=coll)
    gem = empty(name + "_gem", (0, 0, 2.1 * size), parent=root, coll=coll)
    g = mat(name + "_glow", color, emit=1.1)
    cyl(name + "_top", 0.5 * size, 0.7 * size, (0, 0, 0.35 * size), g, n=6, r2=0, parent=gem, coll=coll)
    c2 = cyl(name + "_bot", 0.5 * size, 0.7 * size, (0, 0, -0.35 * size), g, n=6, r2=0, parent=gem, coll=coll)
    c2.rotation_euler[0] = math.pi
    l = bpy.data.lights.new(name + "_light", "POINT")
    l.energy = 300 * size
    l.color = color
    lo = bpy.data.objects.new(name + "_light", l)
    link(lo, gem, coll)
    return root, gem


def confetti(name, at, frame, count=40, spread=4.0, rise=5.0, life=30, seed=0, size=0.12, coll=None):
    """Celebration burst of colored bits that fly up, tumble and fall."""
    rnd = random.Random(seed)
    cols = [(1, 0.2, 0.2), (1, 0.85, 0.1), (0.2, 0.6, 1), (0.3, 0.9, 0.3), (1, 0.4, 0.9)]
    for i in range(count):
        m = mat(f"kid_conf{i % 5}", cols[i % 5], emit=1.2)
        o = box(f"{name}{i}", (size, size * 0.3, size * 1.6), at, m, coll=coll)
        vx, vy, vz = rnd.uniform(-spread, spread), rnd.uniform(-1, 1), rnd.uniform(rise * 0.6, rise * 1.3)
        o.scale = (0.001,) * 3
        o.keyframe_insert("scale", frame=frame - 1)
        o.scale = (1, 1, 1)
        o.keyframe_insert("scale", frame=frame)
        for k in range(0, life + 1, 2):
            t = k / FPS
            o.location = (at[0] + vx * t * 0.8, at[1] + vy * t, at[2] + vz * t - 6 * t * t)
            o.rotation_euler = (t * 9 + i, t * 7, t * 5 + i)
            o.keyframe_insert("location", frame=frame + k)
            o.keyframe_insert("rotation_euler", frame=frame + k)
        o.keyframe_insert("scale", frame=frame + life - 4)
        o.scale = (0.001,) * 3
        o.keyframe_insert("scale", frame=frame + life)


def sparkles(name, at, f0, f1, every=4, radius=2.0, seed=0, color=(1, 1, 0.6), coll=None):
    """Twinkly stars popping around a spot (heroes, the cronchisk)."""
    rnd = random.Random(seed)
    m = mat(name + "_m", color, emit=3.0)
    for i, f in enumerate(range(f0, f1, every)):
        loc = (at[0] + rnd.uniform(-radius, radius), at[1] - 0.3, at[2] + rnd.uniform(-radius, radius))
        o = star(f"{name}{i}", loc, rnd.uniform(0.15, 0.3), m, coll)
        o.scale = (0.001,) * 3
        o.keyframe_insert("scale", frame=f)
        o.scale = (1, 1, 1)
        o.keyframe_insert("scale", frame=f + 4)
        o.scale = (0.001,) * 3
        o.keyframe_insert("scale", frame=f + 10)


def star(name, loc, r, material, coll=None, points=5):
    v = [(0, 0, 0)]
    for i in range(points * 2):
        a = math.pi / 2 + i * math.pi / points
        rr = r if i % 2 == 0 else r * 0.45
        v.append((rr * math.cos(a), 0, rr * math.sin(a)))
    faces = [(0, 1 + i, 1 + (i + 1) % (points * 2)) for i in range(points * 2)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(v, [], faces)
    me.materials.append(material)
    o = bpy.data.objects.new(name, me)
    o.location = loc
    return link(o, None, coll)


def label(name, body, loc, size=1.0, color=(1, 1, 1), outline=(0.05, 0.05, 0.1), coll=None):
    """Big comic word (with a dark backing copy for an outline), faces -Y."""
    root = empty(name, loc, coll=coll)
    text(name + "_bk", body, (0.0, 0.06, -0.0), size, mat(name + "_bkm", outline, emit=0.2),
         extrude=0.12 * size, parent=root, coll=coll, bold=True).scale = (1.06, 1.06, 1.06)
    text(name + "_tx", body, (0, -0.02, 0), size, mat(name + "_txm", color, emit=1.0), extrude=0.05 * size,
         parent=root, coll=coll, bold=True)
    return root


def pop_obj(obj, f, length=8, s=1.0, out=None):
    for df, k in ((-1, 0.001), (0, 0.001), (int(length * 0.6), 1.2), (length, 1.0)):
        obj.scale = (k * s,) * 3
        obj.keyframe_insert("scale", frame=max(0, f + df))
    if out:
        obj.keyframe_insert("scale", frame=out)
        obj.scale = (0.001,) * 3
        obj.keyframe_insert("scale", frame=out + 5)
