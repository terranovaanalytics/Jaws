"""Blocky characters. Everyone faces -Y; root sits at the feet.

    p = make_brody("Brody", loc=(0,0,0), rot_z=0)
    p = make_jesse("Jesse", ...)
    p.root, p.head, p.torso, p.arm_l, p.arm_r, p.leg_l, p.leg_r  (pivots)
    walk(p, start, end); point(p, frame, side="r")
"""
import math
from .common import box, empty, mat


class Person:
    pass


def _build(name, c, loc, rot_z, coll):
    P = Person()
    m = {k: mat(f"{name}_{k}", v) for k, v in c["colors"].items()}
    P.mats = m
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    P.root = root
    LL, LW = c["leg_len"], c["leg_w"]
    TW, TD, TH = c["torso"]
    AL, AW = c["arm_len"], c["arm_w"]
    HW, HD, HH = c["head"]
    hip = LL + 0.08

    def b(nm, size, loc_, mk, parent):
        return box(f"{name}_{nm}", size, loc_, m[mk], parent=parent, coll=coll)

    for side, attr in ((1, "leg_l"), (-1, "leg_r")):
        piv = empty(f"{name}_{attr}", (side * (TW / 2 - LW / 2 - 0.02), 0, hip), root, coll)
        b(f"{attr}_m", (LW, LW * 1.08, LL), (0, 0, -LL / 2), "pants", piv)
        b(f"{attr}_shoe", (LW * 1.1, LW * 1.5, 0.1), (0, -0.05, -LL - 0.03), "shoes", piv)
        setattr(P, attr, piv)
    torso = empty(f"{name}_torso", (0, 0, hip), root, coll)
    P.torso = torso
    b("chest", (TW, TD, TH), (0, 0, TH / 2), "shirt", torso)
    b("belt", (TW + 0.02, TD + 0.02, 0.08), (0, 0, 0.06), "belt", torso)
    sh_z = TH - 0.06
    for side, attr in ((1, "arm_l"), (-1, "arm_r")):
        piv = empty(f"{name}_{attr}", (side * (TW / 2 + AW / 2), 0, sh_z), torso, coll)
        b(f"{attr}_m", (AW, AW * 1.1, AL), (0, 0, -AL / 2 + AW / 2), c.get("sleeve", "shirt"), piv)
        b(f"{attr}_hand", (AW * 0.9, AW * 0.9, 0.14), (0, 0, -AL + AW / 2 - 0.05), "skin", piv)
        setattr(P, attr, piv)
    b("neck", (0.15, 0.15, 0.1), (0, 0, TH + 0.03), "skin", torso)
    head = empty(f"{name}_head", (0, 0, TH + 0.06), torso, coll)
    P.head = head
    b("headbox", (HW, HD, HH), (0, 0, HH / 2), "skin", head)
    fy = -HD / 2  # face plane
    for side in (-1, 1):
        b(f"eye{side}", (0.06, 0.02, 0.055), (side * HW * 0.23, fy - 0.005, HH * 0.62), "eyes", head)
        b(f"brow{side}", (0.11, 0.025, 0.03), (side * HW * 0.23, fy - 0.01, HH * 0.75), "hair", head)
    b("nose", (0.07, 0.07, 0.09), (0, fy - 0.03, HH * 0.42), "nose", head)
    P.name, P.c, P.HW, P.HD, P.HH, P.TW, P.TD, P.TH = name, c, HW, HD, HH, TW, TD, TH
    P.b = b
    return P


BRODY = dict(
    leg_len=0.85, leg_w=0.24, torso=(0.66, 0.38, 0.68), arm_len=0.66, arm_w=0.18,
    head=(0.40, 0.38, 0.44),
    colors=dict(shirt=(0.78, 0.66, 0.43), pants=(0.48, 0.38, 0.24),
                shoes=(0.05, 0.04, 0.04), skin=(0.95, 0.74, 0.58),
                nose=(0.92, 0.62, 0.48), hair=(0.12, 0.08, 0.05),
                eyes=(0.02, 0.02, 0.02), belt=(0.08, 0.06, 0.05),
                gold=(1.0, 0.78, 0.15), dark=(0.58, 0.47, 0.28),
                stache=(0.01, 0.01, 0.01), tie=(0.25, 0.18, 0.10)),
)


def make_brody(name="Brody", loc=(0, 0, 0), rot_z=0.0, coll=None):
    P = _build(name, BRODY, loc, rot_z, coll)
    b, t, h = P.b, P.torso, P.head
    HW, HD, HH, TW, TD, TH = P.HW, P.HD, P.HH, P.TW, P.TD, P.TH
    fy = -TD / 2
    b("gut", (TW * 0.82, 0.12, 0.34), (0, fy - 0.05, 0.30), "shirt", t)   # donut era
    b("buckle", (0.12, 0.03, 0.07), (0, fy - 0.03, 0.06), "gold", t)
    b("tie", (0.07, 0.03, 0.34), (0, fy - 0.11, 0.42), "tie", t)
    for side in (-1, 1):
        b(f"pocket{side}", (0.15, 0.02, 0.13), (side * 0.18, fy - 0.01, 0.52), "dark", t)
        b(f"epaulet{side}", (0.20, TD + 0.02, 0.04), (side * (TW / 2 - 0.05), 0, TH + 0.01), "dark", t)
    b("badge", (0.08, 0.03, 0.10), (0.18, fy - 0.025, 0.63), "gold", t)  # star-ish
    # hair: flat-top slab + back, then THE MUSTACHE
    b("hair_top", (HW + 0.03, HD + 0.03, 0.10), (0, 0.01, HH + 0.02), "hair", h)
    b("hair_back", (HW + 0.03, 0.08, HH * 0.75), (0, HD / 2, HH * 0.6), "hair", h)
    for side in (-1, 1):
        b(f"sideburn{side}", (0.03, 0.12, 0.16), (side * (HW / 2 + 0.01), 0.04, HH * 0.6), "hair", h)
    fz = -HD / 2
    b("stache", (0.32, 0.08, 0.085), (0, fz - 0.04, HH * 0.25), "stache", h)
    for side in (-1, 1):
        b(f"stache_end{side}", (0.07, 0.07, 0.12), (side * 0.15, fz - 0.04, HH * 0.17), "stache", h)
    return P


JESSE = dict(
    leg_len=1.08, leg_w=0.16, torso=(0.42, 0.26, 0.80), arm_len=0.82, arm_w=0.12,
    head=(0.30, 0.30, 0.38), sleeve="shirt",
    colors=dict(shirt=(0.18, 0.20, 0.22), pants=(0.20, 0.30, 0.55),
                shoes=(0.92, 0.92, 0.90), skin=(0.88, 0.68, 0.52),
                nose=(0.84, 0.58, 0.44), hair=(0.30, 0.20, 0.10),
                eyes=(0.02, 0.02, 0.02), belt=(0.10, 0.08, 0.06),
                beanie=(0.95, 0.08, 0.08), beanie_band=(0.80, 0.04, 0.05),
                shades=(0.02, 0.02, 0.03), lens=(0.10, 0.12, 0.25)),
)


def make_jesse(name="Jesse", loc=(0, 0, 0), rot_z=0.0, coll=None):
    P = _build(name, JESSE, loc, rot_z, coll)
    b, h = P.b, P.head
    HW, HD, HH = P.HW, P.HD, P.HH
    b("beanie", (HW + 0.03, HD + 0.03, 0.17), (0, 0, HH + 0.02), "beanie", h)
    b("beanie_band", (HW + 0.05, HD + 0.05, 0.07), (0, 0, HH - 0.05), "beanie_band", h)
    fz = -HD / 2
    b("shades_bar", (HW + 0.02, 0.03, 0.035), (0, fz - 0.02, HH * 0.66), "shades", h)
    for side in (-1, 1):
        b(f"lens{side}", (0.11, 0.03, 0.08), (side * 0.075, fz - 0.025, HH * 0.6), "lens", h)
    return P


def _rot_key(obj, axis, deg, frame):
    obj.rotation_euler[axis] = math.radians(deg)
    obj.keyframe_insert("rotation_euler", index=axis, frame=frame)


def walk(p, start, end, period=12, swing=28):
    """Stiff PS1 walk: legs and arms swing on X, a tiny bob on the torso."""
    f, s = start, 1
    while f <= end:
        _rot_key(p.leg_l, 0, swing * s, f)
        _rot_key(p.leg_r, 0, -swing * s, f)
        _rot_key(p.arm_l, 0, -swing * s * 0.8, f)
        _rot_key(p.arm_r, 0, swing * s * 0.8, f)
        s *= -1
        f += period // 2


def point(p, frame, side="r", hold=24):
    """Raise an arm straight forward to point, hold, lower."""
    arm = p.arm_r if side == "r" else p.arm_l
    _rot_key(arm, 0, 0, frame)
    _rot_key(arm, 0, -85, frame + 6)
    _rot_key(arm, 0, -85, frame + 6 + hold)
    _rot_key(arm, 0, 0, frame + 12 + hold)
