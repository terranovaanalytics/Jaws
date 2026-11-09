"""Shared sets and helpers for Jaws 7 shots. Not a shot itself.

    cove(F)        Maine cove: grey-blue sea, granite shore, pines, lighthouse,
                   WELCOME TO MAINE sign, the Russian sub surfaced (returns dict)
    deep(F, color) dark open-water underwater set
    move(obj, keys) keyframe a list of (frame, (x, y, z)) positions
    face(obj, frame, deg) keyframe a Z rotation
"""
import math, random
from jaws.common import reset_scene, add_sun, box, cyl, mat, text, empty
from jaws.world import make_ocean, make_lighthouse
from jaws.props import underwater
from jaws.spy import make_nuke_sub, make_pine, make_russian

SUB_Z = 0.6            # surfaced sub: root height (hull half out of the water)


def deck_z(sub):
    return SUB_Z + sub["deck_z"] + 0.2


def cove(F, sub_loc=(0, 30, SUB_Z), sign=True, seed=12, sky=(0.58, 0.68, 0.78), sun=(1, 0.97, 0.9)):
    s = reset_scene(F, world_color=sky)
    add_sun((55, 0, -40), energy=2.3, color=sun)
    make_ocean(color=(0.06, 0.22, 0.32))
    rnd = random.Random(seed)
    granite = mat("granite", (0.52, 0.50, 0.48))
    granite2 = mat("granite2", (0.40, 0.39, 0.38))
    box("Shore", (400, 60, 6), (0, 105, 1.0), mat("shore_moss", (0.22, 0.32, 0.18)))
    for k in range(40):                                   # granite boulders along the waterline
        x = -120 + k * 6 + rnd.uniform(-2, 2)
        sz = rnd.uniform(3, 7)
        box(f"Boulder{k}", (sz, sz * 0.8, sz * 0.7), (x, 74 + rnd.uniform(-2, 3), rnd.uniform(0, 1.5)),
            granite if k % 3 else granite2, rot=(rnd.uniform(-15, 15), rnd.uniform(-15, 15), rnd.uniform(0, 90)))
    for k in range(70):                                   # the Maine woods
        x, y = rnd.uniform(-130, 130), rnd.uniform(80, 130)
        make_pine(f"Pine{k}", (x, y, 4.0), h=rnd.uniform(9, 16), seed=k)
    make_lighthouse("Lighthouse", (-46, 78, 3.5))
    if sign:
        wood = mat("sign_wood", (0.30, 0.20, 0.12))
        for x in (-4.2, 4.2):
            cyl(f"SignPost{x}", 0.2, 5, (x - 28, 76, 4.5), wood, n=5)
        box("SignBoard", (10, 0.4, 3.4), (-28, 75.8, 6.5), mat("sign_green", (0.12, 0.35, 0.22)))
        white = mat("sign_white", (0.95, 0.95, 0.9), emit=0.5)
        text("SignTxt1", "WELCOME TO", (-28, 75.5, 7.3), 1.0, white, bold=True)
        text("SignTxt2", "MAINE", (-28, 75.5, 5.9), 1.8, white, bold=True)
    sub = make_nuke_sub("Sub", sub_loc, rot_z=0)
    return dict(scene=s, sub=sub)


def trail(name, pts, start=None, end=None, width=2.4):
    """Glowing green radioactive streak on the water through (x, y) points.
    With start/end, the segments pop on one after another."""
    from jaws.town import pop_in
    g = mat("trail_glow", (0.45, 1.0, 0.3), emit=3.0)
    g2 = mat("trail_haze", (0.25, 0.7, 0.2), emit=1.0)
    segs = list(zip(pts, pts[1:]))
    for k, (a, b) in enumerate(segs):
        L = math.dist(a, b)
        ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
        c = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        o = box(f"{name}{k}", (L + 0.3, width * 0.45, 0.06), (*c, 0.25), g, rot=(0, 0, ang))
        h = box(f"{name}H{k}", (L + 0.3, width, 0.04), (*c, 0.2), g2, rot=(0, 0, ang))
        if start is not None:
            f = start + int((end - start) * k / max(1, len(segs) - 1))
            for x in (o, h):
                x.scale = (0.001,) * 3
                x.keyframe_insert("scale", frame=1)
                pop_in(x, f, overshoot=1.0)


def deep(F, color=(0.02, 0.10, 0.12), start=8, depth=60, floor_z=-30):
    s = reset_scene(F)
    underwater(s, color=color, start=start, depth=depth, floor_z=floor_z)
    return s


def move(obj, keys, linear=False):
    for f, p in keys:
        obj.location = p
        obj.keyframe_insert("location", frame=f)
    if linear:
        for fc in obj.animation_data.action.fcurves:
            if fc.data_path == "location":
                for kp in fc.keyframe_points:
                    kp.interpolation = "LINEAR"


def face(obj, frame, deg, axis=2):
    obj.rotation_euler[axis] = math.radians(deg)
    obj.keyframe_insert("rotation_euler", index=axis, frame=frame)


def hands_up(p, frame, ramp=4):
    for arm in (p.arm_l, p.arm_r):
        face(arm, frame - ramp, 0, axis=0)
        face(arm, frame, -175, axis=0)


def wave(p, start, end, period=8, side="r"):
    """Stiff friendly wave: arm up, forearm-less wag side to side."""
    arm = p.arm_r if side == "r" else p.arm_l
    face(arm, start, -160, axis=0)
    f, k = start, 1
    while f <= end:
        arm.rotation_euler[1] = math.radians(25 * k)
        arm.keyframe_insert("rotation_euler", index=1, frame=f)
        k *= -1
        f += period // 2


def glow_light(name, loc, color, energy, radius=1.0):
    import bpy
    d = bpy.data.lights.new(name, "POINT")
    d.color, d.energy, d.shadow_soft_size = color, energy, radius
    o = bpy.data.objects.new(name, d)
    o.location = loc
    bpy.context.scene.collection.objects.link(o)
    return o
