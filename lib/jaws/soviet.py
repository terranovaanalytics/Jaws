"""Jaws 8 assets: the Cold War. Soviet sub (placeholder until the Jaws 7 sub
is swapped in), the Kremlin, Brezhnev (in a cut-off hoodie), Gronk, ushanka
disguises, the escape truck, border gate, plane, the war-room map, a
chalkboard playbook, speech bubbles and a Soviet flag.

Everyone faces -Y, root at the feet, like people.py."""
import math
import random
import bpy
from .common import box, cyl, ico, empty, mat, text, pixel_mat, decal, FPS
from .people import _build, Person


# ---------------------------------------------------------------- the sub
def make_sub(name="Sub", loc=(0, 0, 0), rot_z=0.0, scale=1.0, coll=None):
    """PLACEHOLDER Soviet nuclear sub (swap for the Jaws 7 model later).
    Long black cigar hull along +X (bow at +X), sail (conning tower) with a
    red star and hull number, periscope, red waterline. Origin at the
    waterline, center of the hull. ~30 m long at scale 1."""
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    root.scale = (scale,) * 3
    hull = mat("sub_hull", (0.10, 0.11, 0.12))
    red = mat("sub_red", (0.55, 0.08, 0.06))
    star = mat("sub_star", (0.95, 0.12, 0.08), emit=0.6)
    white = mat("sub_white", (0.92, 0.92, 0.88))
    L = 30.0
    cyl(f"{name}_hull", 2.2, L - 6, (0, 0, -0.6), hull, n=10, rot=(0, 90, 0), parent=root, coll=coll)
    cyl(f"{name}_bow", 2.2, 4, (L / 2 - 1, 0, -0.6), hull, n=10, r2=0.5, rot=(0, 90, 0), parent=root, coll=coll)
    cyl(f"{name}_stern", 2.2, 5, (-L / 2 + 0.5, 0, -0.6), hull, n=10, r2=0.4, rot=(0, -90, 0), parent=root,
        coll=coll)
    box(f"{name}_waterline", (L - 6, 4.5, 0.25), (0, 0, -0.95), red, parent=root, coll=coll)
    box(f"{name}_sail", (5.0, 1.6, 3.6), (3, 0, 2.6), hull, parent=root, coll=coll)
    box(f"{name}_sailtop", (4.6, 1.5, 0.3), (3.1, 0, 4.5), hull, parent=root, coll=coll)
    for side in (-1, 1):                                    # dive planes on the sail
        box(f"{name}_plane{side}", (1.4, 2.2, 0.15), (4.6, side * 1.8, 3.9), hull, parent=root, coll=coll)
        star_o = text(f"{name}_star{side}", "★", (3.4, side * 0.82, 1.9), 1.5, star,
                      rot=(90, 0, 0 if side < 0 else 180), parent=root, coll=coll, bold=True)
        text(f"{name}_num{side}", "K-19", (1.6 if side < 0 else 4.6, side * 0.82, 1.3), 0.5, white,
             rot=(90, 0, 0 if side < 0 else 180), parent=root, coll=coll, bold=True)
    box(f"{name}_rudder", (1.8, 0.2, 3.0), (-L / 2 - 1, 0, 0.2), hull, parent=root, coll=coll)
    peri = empty(f"{name}_periscope", (2.4, 0, 4.6), root, coll)
    cyl(f"{name}_peri", 0.12, 2.4, (0, 0, 1.2), hull, n=6, parent=peri, coll=coll)
    box(f"{name}_perihead", (0.5, 0.3, 0.3), (0.15, 0, 2.4), hull, parent=peri, coll=coll)
    return dict(root=root, periscope=peri, hatch=(3.1, 0, 4.7), length=L)


# ---------------------------------------------------------------- Kremlin
def make_onion(name, loc, r, color, parent=None, coll=None, stripes=None):
    """St. Basil's-style onion dome on a little drum, gold spike on top."""
    root = empty(name, loc, parent, coll)
    drum = mat("kremlin_drum", (0.88, 0.84, 0.74))
    cyl(f"{name}_drum", r * 0.75, r * 1.4, (0, 0, r * 0.7), drum, n=8, parent=root, coll=coll)
    m = mat(f"onion_{color}", color)
    d = ico(f"{name}_dome", r, (0, 0, r * 1.4 + r * 0.75), m, parent=root, coll=coll, subdiv=2)
    d.scale = (1, 1, 1.15)
    cyl(f"{name}_tip", r * 0.55, r * 1.1, (0, 0, r * 1.4 + r * 1.9), m, n=8, r2=0.0, parent=root, coll=coll)
    cyl(f"{name}_spike", 0.06 * r, r * 0.9, (0, 0, r * 1.4 + r * 2.8), mat("gold", (1.0, 0.78, 0.15), emit=0.3),
        n=4, parent=root, coll=coll)
    return root


def make_kremlin(name="Kremlin", loc=(0, 0, 0), coll=None, night=False):
    """Red crenellated wall along X facing -Y, the clock tower (Spasskaya-ish,
    glowing red star) in the middle and a cluster of colorful onion domes
    behind. ~70 m wide. Returns dict(root, window=(x,y,z) of a lit window in the
    tower, star)."""
    root = empty(name, loc, coll=coll)
    brick = mat("kremlin_brick", (0.62, 0.17, 0.12))
    dark = mat("kremlin_dark", (0.40, 0.10, 0.08))
    green = mat("kremlin_green", (0.20, 0.42, 0.32))
    W = 70
    box(f"{name}_wall", (W, 3, 9), (0, 0, 4.5), brick, parent=root, coll=coll)
    for k in range(int(W / 2.2)):                           # swallowtail merlons
        x = -W / 2 + 1.1 + k * 2.2
        box(f"{name}_merlon{k}", (1.2, 3.1, 1.4), (x, 0, 9.7), brick, parent=root, coll=coll)
    for side in (-1, 1):                                    # corner towers
        x = side * (W / 2 + 2)
        box(f"{name}_ct{side}", (6, 6, 14), (x, 0, 7), brick, parent=root, coll=coll)
        cyl(f"{name}_ctroof{side}", 4.2, 8, (x, 0, 18), green, n=4, r2=0, parent=root, coll=coll,
            rot=(0, 0, 45))
    # clock tower in the middle
    box(f"{name}_t1", (10, 8, 16), (0, -1, 8), brick, parent=root, coll=coll)
    box(f"{name}_t2", (8, 6.5, 8), (0, -1, 20), brick, parent=root, coll=coll)
    box(f"{name}_t3", (6, 5, 6), (0, -1, 27), brick, parent=root, coll=coll)
    cyl(f"{name}_spire", 3.6, 12, (0, -1, 36), green, n=8, r2=0.2, parent=root, coll=coll)
    face = mat("kremlin_clock", (0.10, 0.10, 0.12))
    cyl(f"{name}_clock", 2.3, 0.3, (0, -4.3, 20.5), face, n=12, rot=(90, 0, 0), parent=root, coll=coll)
    gold = mat("gold", (1.0, 0.78, 0.15), emit=0.3)
    cyl(f"{name}_ring", 2.5, 0.2, (0, -4.25, 20.5), gold, n=12, rot=(90, 0, 0), parent=root, coll=coll)
    for a, l in ((90, 1.6), (20, 1.2)):                     # hands
        h = box(f"{name}_hand{a}", (0.18, 0.1, l), (0, -4.5, 20.5), gold, parent=root, coll=coll)
        h.rotation_euler = (0, math.radians(a), 0)
        h.location.x += math.sin(math.radians(a)) * l / 2
        h.location.z += math.cos(math.radians(a)) * l / 2
    star = text(f"{name}_star", "★", (0, -1.5, 44.5), 7.0, mat("kremlin_star", (1.0, 0.1, 0.06), emit=5.0),
                rot=(90, 0, 0), extrude=0.3, parent=root, coll=coll, bold=True)
    box(f"{name}_gate", (4, 0.4, 6), (0, -5.05, 3), dark, parent=root, coll=coll)
    win = mat("window", (1.0, 0.75, 0.35), emit=1.6 if night else 0.2)
    for x in (-2.2, 2.2):
        box(f"{name}_win{x}", (1.2, 0.3, 2.0), (x, -5.0, 11), win, parent=root, coll=coll)
    # the cathedral cluster behind the wall
    rnd = random.Random(3)
    cols = [(0.85, 0.15, 0.12), (0.15, 0.45, 0.30), (0.95, 0.75, 0.15), (0.20, 0.35, 0.70),
            (0.95, 0.95, 0.90), (0.85, 0.40, 0.10)]
    body = mat("kremlin_cath", (0.92, 0.88, 0.78))
    for k, (x, y, r) in enumerate(((-22, 16, 3.2), (-16, 20, 4.2), (-10, 15, 2.8), (14, 18, 3.6),
                                   (20, 22, 4.6), (27, 16, 3.0), (-28, 22, 2.6))):
        h = rnd.uniform(10, 16)
        box(f"{name}_cath{k}", (r * 2.6, r * 2.6, h), (x, y, h / 2), body, parent=root, coll=coll)
        make_onion(f"{name}_onion{k}", (x, y, h), r, cols[k % len(cols)], parent=root, coll=coll)
    return dict(root=root, star=star, window=(0, -5.2, 11))


# ---------------------------------------------------------------- people
def _hat_ushanka(P, name, color=(0.62, 0.58, 0.52), star=True):
    """Fur ushanka with ear flaps (+ red star badge) on any people.py rig."""
    b, HW, HD, HH = P.b, P.HW, P.HD, P.HH
    P.mats["fur"] = mat(f"{name}_fur", color)
    P.mats["red"] = mat("soviet_red", (0.85, 0.10, 0.08), emit=0.3)
    b("ush_crown", (HW + 0.14, HD + 0.14, 0.30), (0, 0, HH + 0.12), "fur", P.head)
    b("ush_brim", (HW + 0.20, 0.14, 0.16), (0, -HD / 2 - 0.07, HH + 0.02), "fur", P.head)
    for side in (-1, 1):
        b(f"ush_flap{side}", (0.10, HD * 0.85, 0.40), (side * (HW / 2 + 0.08), 0, HH * 0.5), "fur", P.head)
    if star:
        b("ush_star", (0.10, 0.03, 0.10), (0, -HD / 2 - 0.15, HH + 0.03), "red", P.head)


def _fake_stache(P, color=(0.05, 0.03, 0.02)):
    """Big obviously-fake glued-on mustache."""
    P.mats["fake"] = mat("fake_stache", color)
    P.b("fake_stache", (P.HW * 0.95, 0.06, 0.09), (0, -P.HD / 2 - 0.04, P.HH * 0.27), "fake", P.head)


SOLDIER = dict(
    leg_len=0.92, leg_w=0.2, torso=(0.56, 0.32, 0.74), arm_len=0.72, arm_w=0.16,
    head=(0.34, 0.34, 0.40),
    colors=dict(shirt=(0.32, 0.34, 0.22), pants=(0.25, 0.27, 0.18), shoes=(0.05, 0.04, 0.04),
                skin=(0.93, 0.72, 0.56), nose=(0.90, 0.60, 0.46), hair=(0.25, 0.17, 0.10),
                eyes=(0.02, 0.02, 0.02), belt=(0.30, 0.20, 0.10)),
)


def make_soldier(name, loc=(0, 0, 0), rot_z=0.0, seed=0, disguise=True, coll=None, coat=None):
    """Soldier in a long Soviet greatcoat and ushanka. disguise=True: an
    American in costume (fake mustache, coat buttoned wrong, US sneakers)."""
    rnd = random.Random(seed)
    c = dict(SOLDIER, colors=dict(SOLDIER["colors"]))
    if coat:
        c["colors"]["shirt"] = coat
    if disguise:
        c["colors"]["shoes"] = (0.95, 0.95, 0.95)                       # white sneakers: a giveaway
        c["colors"]["skin"] = [(0.95, 0.75, 0.6), (0.7, 0.5, 0.35), (0.48, 0.32, 0.22)][seed % 3]
    P = _build(name, c, loc, rot_z, coll)
    P.b("coat", (P.TW + 0.06, P.TD + 0.06, 0.55), (0, 0, -0.18), "shirt", P.torso)
    _hat_ushanka(P, name, color=[(0.62, 0.58, 0.52), (0.50, 0.38, 0.26), (0.72, 0.70, 0.66)][rnd.randrange(3)])
    if disguise:
        _fake_stache(P)
    return P


BREZHNEV = dict(
    leg_len=0.85, leg_w=0.25, torso=(0.70, 0.42, 0.72), arm_len=0.66, arm_w=0.19,
    head=(0.44, 0.40, 0.46), sleeve="skin",
    colors=dict(shirt=(0.36, 0.38, 0.42), pants=(0.12, 0.12, 0.14), shoes=(0.04, 0.04, 0.04),
                skin=(0.92, 0.72, 0.60), nose=(0.88, 0.60, 0.50), hair=(0.30, 0.28, 0.26),
                eyes=(0.02, 0.02, 0.02), belt=(0.10, 0.10, 0.10), hood=(0.31, 0.33, 0.37),
                gold=(1.0, 0.80, 0.20), ribbon=(0.80, 0.10, 0.08), whistle=(0.85, 0.85, 0.80),
                brows=(0.12, 0.10, 0.09)),
)


def make_brezhnev(name="Brezhnev", loc=(0, 0, 0), rot_z=0.0, coll=None):
    """Soviet leader Brezhnev as played by a certain football coach: grey
    hoodie with the sleeves cut off, rows of Hero medals pinned to it, THE
    eyebrows, slicked grey hair, a whistle, and a headset."""
    P = _build(name, BREZHNEV, loc, rot_z, coll)
    b, t, h = P.b, P.torso, P.head
    HW, HD, HH, TW, TD, TH = P.HW, P.HD, P.HH, P.TW, P.TD, P.TH
    fy = -TD / 2
    b("hood", (TW * 0.8, 0.22, 0.22), (0, TD / 2 + 0.05, TH - 0.05), "hood", t)        # hood bunched behind
    b("pocket", (TW * 0.6, 0.03, 0.18), (0, fy - 0.015, 0.22), "hood", t)              # kangaroo pocket
    for side in (-1, 1):
        b(f"string{side}", (0.025, 0.02, 0.22), (side * 0.07, fy - 0.02, TH - 0.18), "whistle", t)
        b(f"cutoff{side}", (0.24, TD + 0.02, 0.06), (side * (TW / 2 + 0.0), 0, TH - 0.06), "hood", t)  # ragged hems
    for k in range(2):                                    # two gold Hero stars on red ribbons
        x = 0.12 + k * 0.13
        b(f"ribbon{k}", (0.09, 0.025, 0.07), (x, fy - 0.015, TH - 0.12), "ribbon", t)
        b(f"medal{k}", (0.08, 0.03, 0.08), (x, fy - 0.02, TH - 0.24), "gold", t)
    b("whistle", (0.05, 0.05, 0.09), (-0.07, fy - 0.03, TH - 0.33), "whistle", t)
    # hair: swept back grey slab
    b("hair_top", (HW + 0.03, HD + 0.06, 0.12), (0, 0.03, HH + 0.03), "hair", h)
    b("hair_back", (HW + 0.03, 0.08, HH * 0.7), (0, HD / 2, HH * 0.6), "hair", h)
    fz = -HD / 2
    for side in (-1, 1):                                  # THE eyebrows
        b(f"bigbrow{side}", (0.17, 0.07, 0.075), (side * HW * 0.24, fz - 0.03, HH * 0.79), "brows", h)
    b("jowls", (HW + 0.04, HD * 0.7, 0.12), (0, 0.02, HH * 0.12), "skin", h)
    b("frown", (0.16, 0.02, 0.025), (0, fz - 0.01, HH * 0.22), "brows", h)
    # headset: band over the head + mic boom
    b("hs_band", (HW + 0.08, 0.05, 0.05), (0, 0, HH + 0.10), "pants", h)
    for side in (-1, 1):
        b(f"hs_cup{side}", (0.06, 0.14, 0.14), (side * (HW / 2 + 0.04), 0, HH * 0.6), "pants", h)
    b("hs_boom", (0.03, 0.22, 0.03), (-(HW / 2 + 0.02), -0.12, HH * 0.32), "pants", h)
    return P


GRONK = dict(
    leg_len=1.10, leg_w=0.30, torso=(0.98, 0.52, 0.92), arm_len=0.92, arm_w=0.27,
    head=(0.46, 0.44, 0.50),
    colors=dict(shirt=(0.13, 0.14, 0.17), pants=(0.12, 0.13, 0.15), shoes=(0.04, 0.04, 0.04),
                skin=(0.92, 0.70, 0.55), nose=(0.88, 0.60, 0.46), hair=(0.40, 0.28, 0.16),
                eyes=(0.02, 0.02, 0.02), belt=(0.05, 0.05, 0.05), white=(0.95, 0.95, 0.93),
                tie=(0.05, 0.05, 0.06), shades=(0.02, 0.02, 0.03), earpiece=(0.85, 0.85, 0.80),
                teeth=(0.98, 0.98, 0.95)),
)


def make_gronk(name="Gronk", loc=(0, 0, 0), rot_z=0.0, coll=None):
    """CIA officer Gronk: a huge blocky guy in a black suit, white shirt,
    skinny black tie, mirror shades, earpiece, short buzzed hair and a big grin."""
    P = _build(name, GRONK, loc, rot_z, coll)
    b, t, h = P.b, P.torso, P.head
    HW, HD, HH, TW, TD, TH = P.HW, P.HD, P.HH, P.TW, P.TD, P.TH
    fy = -TD / 2
    b("shirtfront", (0.22, 0.02, TH * 0.55), (0, fy - 0.01, TH * 0.70), "white", t)
    b("tie", (0.08, 0.03, TH * 0.50), (0, fy - 0.025, TH * 0.68), "tie", t)
    b("hair_top", (HW + 0.01, HD + 0.01, 0.06), (0, 0.005, HH + 0.01), "hair", h)
    fz = -HD / 2
    b("shades", (HW + 0.03, 0.04, 0.10), (0, fz - 0.02, HH * 0.63), "shades", h)
    b("grin", (0.22, 0.02, 0.06), (0, fz - 0.01, HH * 0.24), "teeth", h)
    b("earpiece", (0.04, 0.05, 0.05), (HW / 2 + 0.02, 0, HH * 0.5), "earpiece", h)
    b("chin", (HW * 0.8, HD * 0.4, 0.08), (0, -0.05, 0.02), "skin", h)
    return P


# ---------------------------------------------------------------- vehicles
def make_truck(name="Truck", loc=(0, 0, 0), rot_z=0.0, coll=None, open_back=True):
    """Olive Soviet army truck, cab at +X, canvas-covered cargo bed (open at
    the back, -X). ~8 m long. Returns dict(root, wheels, bed=(local xyz of the
    bed floor center), back=(local xyz of the tailgate))."""
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    olive = mat("truck_olive", (0.30, 0.34, 0.20))
    canvas = mat("truck_canvas", (0.42, 0.42, 0.30))
    black = mat("tire", (0.05, 0.05, 0.05))
    glass = mat("truck_glass", (0.25, 0.32, 0.38), emit=0.1)
    box(f"{name}_chassis", (8, 2.4, 0.4), (0, 0, 1.0), olive, parent=root, coll=coll)
    box(f"{name}_cab", (2.2, 2.4, 2.0), (2.9, 0, 2.2), olive, parent=root, coll=coll)
    box(f"{name}_hood", (1.4, 2.0, 1.1), (4.6, 0, 1.75), olive, parent=root, coll=coll)
    box(f"{name}_wind", (0.05, 2.0, 0.8), (4.02, 0, 2.7), glass, parent=root, coll=coll)
    box(f"{name}_bed", (5.0, 2.5, 0.2), (-1.5, 0, 1.3), olive, parent=root, coll=coll)
    for side in (-1, 1):
        box(f"{name}_canvas{side}", (5.0, 0.08, 2.0), (-1.5, side * 1.24, 2.4), canvas, parent=root, coll=coll)
        box(f"{name}_door{side}", (1.2, 0.05, 1.0), (2.9, side * 1.22, 2.2), olive, parent=root, coll=coll)
        text(f"{name}_star{side}", "★", (2.9, side * 1.26, 2.2), 0.8,
             mat("soviet_red", (0.85, 0.10, 0.08), emit=0.3), rot=(90, 0, 0 if side < 0 else 180), parent=root,
             coll=coll, bold=True)
    box(f"{name}_roof", (5.0, 2.5, 0.1), (-1.5, 0, 3.45), canvas, parent=root, coll=coll)
    if not open_back:
        box(f"{name}_flap", (0.05, 2.5, 2.0), (-4.0, 0, 2.4), canvas, parent=root, coll=coll)
    wheels = []
    for x in (3.2, -0.6, -2.6):
        for side in (-1, 1):
            w = cyl(f"{name}_wheel{x}{side}", 0.55, 0.4, (x, side * 1.15, 0.55), black, n=8, rot=(90, 0, 0),
                    parent=root, coll=coll)
            wheels.append(w)
    for side in (-1, 1):
        box(f"{name}_lamp{side}", (0.1, 0.3, 0.25), (5.31, side * 0.7, 1.9),
            mat("headlamp", (1.0, 0.92, 0.7), emit=2.0), parent=root, coll=coll)
    return dict(root=root, wheels=wheels, bed=(-1.5, 0, 1.4), back=(-4.0, 0, 1.4))


def make_plane(name="Plane", loc=(0, 0, 0), rot_z=0.0, coll=None, scale=1.0):
    """Chunky 4-prop airliner, nose at +X. ~26 m long at scale 1.
    Returns dict(root, props)."""
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    root.scale = (scale,) * 3
    white = mat("plane_white", (0.92, 0.92, 0.90))
    blue = mat("plane_blue", (0.15, 0.30, 0.65))
    gray = mat("plane_gray", (0.55, 0.57, 0.60))
    win = mat("plane_win", (0.15, 0.18, 0.25))
    cyl(f"{name}_body", 1.6, 20, (0, 0, 0), white, n=10, rot=(0, 90, 0), parent=root, coll=coll)
    cyl(f"{name}_nose", 1.6, 3, (11.5, 0, 0), white, n=10, r2=0.3, rot=(0, 90, 0), parent=root, coll=coll)
    cyl(f"{name}_tailcone", 1.6, 5, (-12.5, 0, 0.4), white, n=10, r2=0.3, rot=(0, -90, 0), parent=root,
        coll=coll)
    box(f"{name}_stripe", (24, 3.3, 0.35), (0, 0, 0.2), blue, parent=root, coll=coll)
    box(f"{name}_wing", (4, 30, 0.3), (0.5, 0, -0.4), gray, parent=root, coll=coll)
    box(f"{name}_htail", (2.2, 10, 0.2), (-13.5, 0, 0.8), gray, parent=root, coll=coll)
    box(f"{name}_vtail", (3, 0.25, 4.5), (-13.2, 0, 3.0), blue, parent=root, coll=coll, rot=(0, -15, 0))
    for k in range(9):
        for side in (-1, 1):
            box(f"{name}_win{k}{side}", (0.5, 0.05, 0.4), (8 - k * 1.8, side * 1.58, 0.7), win, parent=root,
                coll=coll)
    props = []
    for y in (-10, -5, 5, 10):
        cyl(f"{name}_eng{y}", 0.6, 3, (2.6, y, -0.5), gray, n=8, rot=(0, 90, 0), parent=root, coll=coll)
        p = empty(f"{name}_prop{y}", (4.2, y, -0.5), root, coll)
        box(f"{name}_blade{y}", (0.1, 0.25, 3.2), (0, 0, 0), mat("prop_black", (0.08, 0.08, 0.08)), parent=p,
            coll=coll)
        props.append(p)
    return dict(root=root, props=props)


def spin(obj, start, end, axis=0, rps=4.0):
    """Keyframe a continuous spin (props, wheels)."""
    for f in (start, end):
        obj.rotation_euler[axis] = 2 * math.pi * rps * (f - start) / FPS
        obj.keyframe_insert("rotation_euler", index=axis, frame=f)
    for fc in obj.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"


# ---------------------------------------------------------------- props
def make_border_gate(name="Border", loc=(0, 0, 0), rot_z=0.0, coll=None, left="USSR", right="FINLAND"):
    """Red-and-white striped boom barrier across a road along X, a guard
    hut, and the sign. The boom pivots at the post (local -3, 0). Returns
    dict(root, boom pivot)."""
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    red = mat("boom_red", (0.85, 0.10, 0.08))
    white = mat("boom_white", (0.95, 0.95, 0.92))
    wood = mat("hut_wood", (0.45, 0.48, 0.32))
    box(f"{name}_post", (0.5, 0.5, 1.6), (0, -3.6, 0.8), red, parent=root, coll=coll)
    piv = empty(f"{name}_pivot", (0, -3.6, 1.4), root, coll)
    for k in range(7):
        box(f"{name}_boom{k}", (0.25, 1.0, 0.25), (0, 0.5 + k, 0), red if k % 2 else white, parent=piv,
            coll=coll)
    box(f"{name}_hut", (2.2, 2.2, 2.8), (0, -6.2, 1.4), wood, parent=root, coll=coll)
    box(f"{name}_hutroof", (2.6, 2.6, 0.25), (0, -6.2, 2.9), red, parent=root, coll=coll)
    box(f"{name}_hutwin", (2.22, 1.2, 0.8), (0, -6.2, 1.9), mat("hut_win", (1.0, 0.8, 0.5), emit=1.0), parent=root,
        coll=coll)
    # sign on two posts: USSR | FINLAND with an arrow
    sp = mat("sign_post", (0.3, 0.3, 0.3))
    for y in (-11.5, -8.5):
        cyl(f"{name}_sp{y}", 0.1, 3.2, (0, y, 1.6), sp, n=5, parent=root, coll=coll)
    box(f"{name}_sign", (0.12, 4.2, 1.4), (0, -10, 3.3), white, parent=root, coll=coll)
    blk = mat("sign_black", (0.05, 0.05, 0.05))
    text(f"{name}_lbl", f"{left} → {right}", (-0.08, -10, 3.3), 0.48, blk, rot=(90, 0, -90),
         parent=root, coll=coll, bold=True)
    return dict(root=root, boom=piv)


def make_map_table(name="Map", loc=(0, 0, 0), coll=None, size=(40, 26), soviet=True):
    """War-room map seen from above: parchment ocean, chunky continent blobs.
    Local layout (x right, y up the map): North America on the left (US east
    coast around x=-9, Amity at AMITY), Europe on the right, Leningrad at
    LENINGRAD. z=0 is the map surface. Returns dict(root, places)."""
    root = empty(name, loc, coll=coll)
    W, H = size
    sea = mat("map_sea", (0.16, 0.36, 0.46))
    land = mat("map_land", (0.86, 0.78, 0.56))
    ussr = mat("map_ussr", (0.72, 0.22, 0.16))
    usa = mat("map_usa", (0.40, 0.62, 0.32))
    edge = mat("map_frame", (0.30, 0.20, 0.12))
    box(f"{name}_sea", (W, H, 0.2), (0, 0, -0.1), sea, parent=root, coll=coll)
    box(f"{name}_frame", (W + 1.2, H + 1.2, 0.4), (0, 0, -0.35), edge, parent=root, coll=coll)

    def blob(nm, pts, m, z=0.06):
        from mathutils import Vector
        verts = [(x, y, 0) for x, y in pts] + [(x, y, z) for x, y in pts]
        n = len(pts)
        faces = [tuple(range(n))[::-1], tuple(range(n, 2 * n))]
        faces += [(i, (i + 1) % n, (i + 1) % n + n, i + n) for i in range(n)]
        me = bpy.data.meshes.new(f"{name}_{nm}")
        me.from_pydata(verts, [], faces)
        me.materials.append(m)
        o = bpy.data.objects.new(f"{name}_{nm}", me)
        from .common import link
        return link(o, root, coll)

    # North America (USA part greenish), Greenland, Europe, USSR (red), Scandinavia
    blob("canada", [(-20, 6), (-15, 13), (-8, 13), (-6, 9), (-8, 6.5), (-11, 5.2), (-13, 5), (-20, 4)], land)
    blob("usa", [(-20, 4), (-13, 5), (-11, 5.2), (-8.6, 4.4), (-9.4, 2.6), (-10.4, 0.8), (-11, -1.6),
                 (-11.6, -4), (-13.2, -4.6), (-20, -4)], usa)
    blob("mexico", [(-20, -4), (-13.2, -4.6), (-14, -7), (-16, -9), (-20, -9)], land)
    blob("greenland", [(-6, 13), (0, 13), (-1, 9.5), (-4, 8.5)], land)
    blob("iceland", [(1.2, 8.0), (3, 8.4), (3.2, 7.2), (1.6, 6.9)], land)
    blob("britain", [(5.2, 5.2), (6.4, 6.4), (6.6, 4.0), (5.6, 3.2)], land)
    blob("europe", [(7, 4.6), (8.5, 6.6), (11, 7), (11.6, 3.5), (11, 0), (9, -2), (6, -2.8), (5.6, -0.6),
                    (6.6, 1.6)], land)
    blob("africa", [(5, -4), (11, -3.6), (14, -6), (13, -13), (9, -13), (5.5, -7)], land)
    blob("scandinavia", [(9.2, 7.6), (11, 11.2), (13.2, 12), (13, 9.6), (11.6, 7.2)], land)
    blob("finland", [(13.2, 9.0), (13.4, 11.8), (15.0, 11.4), (14.7, 8.6)], land)
    blob("ussr", [(14.7, 8.6), (15.0, 11.4), (16, 13), (20, 13), (20, 0), (14, 0), (12, 2.5), (11.8, 5.2),
                  (13.2, 6.8)], ussr if soviet else land)
    lbl = mat("map_label", (0.10, 0.08, 0.06))
    for body, (x, y), sz in (("USA", (-15.5, 0.5), 1.6), ("ATLANTIC", (-1.5, -2), 1.1),
                             ("USSR", (17, 4.5), 1.4), ("EUROPE", (8.5, 2.0), 0.7)):
        text(f"{name}_lbl_{body}", body, (x, y, 0.08), sz, lbl if body != "ATLANTIC" else
             mat("map_label_sea", (0.75, 0.85, 0.85)), rot=(0, 0, 0), parent=root, coll=coll, bold=True)
    places = dict(amity=(-8.8, 3.6), leningrad=(14.3, 8.4), moscow=(16.5, 6.2), finland=(14.0, 10.2),
                  dc=(-10.6, 1.2))
    return dict(root=root, places=places, size=size)


def pin(name, at, color=(0.85, 0.10, 0.08), parent=None, coll=None, size=0.5):
    """Map pin: a stick with a ball. at = (x, y) on a map_table root."""
    root = empty(name, (at[0], at[1], 0), parent, coll)
    cyl(f"{name}_stick", 0.05 * size * 2, 1.2 * size * 2, (0, 0, 0.6 * size * 2), mat("pin_steel", (0.7, 0.7, 0.7)),
        n=4, parent=root, coll=coll)
    ico(f"{name}_ball", size * 0.6, (0, 0, 1.25 * size * 2), mat(f"pin_{color}", color, emit=0.4), parent=root,
        coll=coll)
    return root


def dotted_path(name, pts, start, end, parent=None, coll=None, z=0.12, step=0.9, color=(0.85, 0.10, 0.08),
                size=0.22):
    """Old-movie travel line: dashes appear one after another along the
    polyline pts (map coordinates) between start and end frames. Returns the
    list of dash objects and the head position per frame isn't tracked; use
    path_point for the moving icon."""
    m = mat(f"dash_{color}", color, emit=0.5)
    segs, total = [], 0.0
    for a, b in zip(pts, pts[1:]):
        d = math.dist(a, b)
        segs.append((a, b, d))
        total += d
    n = max(2, int(total / step))
    dashes = []
    for i in range(n):
        t = (i + 0.5) / n
        x, y, ang = path_point(pts, t)
        o = box(f"{name}_d{i}", (size * 1.8, size, 0.05), (x, y, z), m, parent=parent, coll=coll,
                rot=(0, 0, math.degrees(ang)))
        f = int(start + (end - start) * t)
        o.scale = (0.001,) * 3
        o.keyframe_insert("scale", frame=max(1, f - 1))
        o.scale = (1, 1, 1)
        o.keyframe_insert("scale", frame=f)
        dashes.append(o)
    return dashes


def path_point(pts, t):
    """Point and heading (radians) at fraction t along a polyline."""
    segs = [(a, b, math.dist(a, b)) for a, b in zip(pts, pts[1:])]
    total = sum(s[2] for s in segs)
    d = max(0.0, min(1.0, t)) * total
    for a, b, l in segs:
        if d <= l or (a, b, l) == segs[-1]:
            k = d / l if l else 0
            return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k,
                    math.atan2(b[1] - a[1], b[0] - a[0]))
        d -= l


def follow_path(obj, pts, start, end, z=0.3, every=2, turn=True, offset=0.0):
    """Keyframe obj moving along a map polyline (map coords) start->end."""
    for f in list(range(start, end + 1, every)) + [end]:
        t = (f - start) / max(1, end - start)
        x, y, ang = path_point(pts, t)
        obj.location = (x, y, z)
        obj.keyframe_insert("location", frame=f)
        if turn:
            obj.rotation_euler[2] = ang + offset
            obj.keyframe_insert("rotation_euler", index=2, frame=f)


def make_chalkboard(name="Board", loc=(0, 0, 0), rot_z=0.0, coll=None, w=6.0, h=3.6):
    """Green chalkboard on an easel, facing -Y. Returns dict(root, surface z
    center, chalk material). Local drawing plane: x across, z up, at y=-0.09."""
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    wood = mat("board_wood", (0.45, 0.30, 0.16))
    slate = mat("board_slate", (0.12, 0.22, 0.17), flat=0.3)
    cz = 1.2 + h / 2
    box(f"{name}_frame", (w + 0.3, 0.12, h + 0.3), (0, 0, cz), wood, parent=root, coll=coll)
    box(f"{name}_slate", (w, 0.05, h), (0, -0.07, cz), slate, parent=root, coll=coll)
    for side in (-1, 1):
        box(f"{name}_leg{side}", (0.14, 0.14, cz + h / 2), (side * (w / 2 - 0.3), 0.15, (cz + h / 2) / 2), wood,
            parent=root, coll=coll, rot=(-8, 0, 0))
    chalk = mat("chalk", (0.92, 0.92, 0.88), emit=0.6)
    return dict(root=root, cz=cz, chalk=chalk, w=w, h=h)


def chalk_mark(board, name, body, xz, size=0.5, frame=None, color=None):
    """Chalk text/symbol on a chalkboard (pops in at frame)."""
    m = board["chalk"] if color is None else mat(f"chalk_{color}", color, emit=0.25, flat=0.9)
    o = text(f"{board['root'].name}_{name}", body, (xz[0], -0.1, board["cz"] + xz[1]), size, m,
             parent=board["root"], bold=True)
    if frame is not None:
        o.scale = (0.001,) * 3
        o.keyframe_insert("scale", frame=max(1, frame - 1))
        o.scale = (1, 1, 1)
        o.keyframe_insert("scale", frame=frame + 2)
    return o


def chalk_arrow(board, name, a, b, frame=None, width=0.07):
    """Chalk arrow from a to b (board x,z), grows from a over 6 frames."""
    cz = board["cz"]
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    L = math.dist(a, b)
    piv = empty(f"{board['root'].name}_{name}", (a[0], -0.1, cz + a[1]), board["root"])
    piv.rotation_euler = (0, -ang, 0)
    box(f"{board['root'].name}_{name}_shaft", (L, 0.02, width), (L / 2, 0, 0), board["chalk"], parent=piv)
    for s in (-1, 1):
        box(f"{board['root'].name}_{name}_head{s}", (0.22, 0.02, width), (L - 0.08, 0, s * 0.06), board["chalk"],
            parent=piv, rot=(0, s * 40, 0))
    if frame is not None:
        piv.scale = (0.001, 1, 1)
        piv.keyframe_insert("scale", index=0, frame=max(1, frame - 1))
        piv.scale = (1, 1, 1)
        piv.keyframe_insert("scale", index=0, frame=frame + 6)
    return piv


def speech_bubble(name, loc, body, size=1.0, coll=None, rot=(90, 0, 0), color=(0.97, 0.97, 0.95),
                  text_color=(0.05, 0.05, 0.05)):
    """Comic speech bubble (white rounded box + tail) with text, faces -Y."""
    root = empty(name, loc, coll=coll)
    root.rotation_euler = [math.radians(a) - math.radians(r0) for a, r0 in zip(rot, (90, 0, 0))]
    white = mat(f"bubble_{color}", color, flat=0.9)
    n = max(len(l) for l in body.split("\n"))
    lines = body.count("\n") + 1
    w, h = (0.55 * n + 0.8) * size, (0.9 * lines + 0.5) * size
    box(f"{name}_box", (w, 0.08, h), (0, 0, 0), white, parent=root, coll=coll)
    for s in (-1, 1):
        cyl(f"{name}_cap{s}", h / 2, 0.08, (s * w / 2, 0, 0), white, n=10, rot=(90, 0, 0), parent=root, coll=coll)
    t = box(f"{name}_tail", (0.5 * size, 0.08, 0.9 * size), (-w * 0.25, 0, -h / 2 - 0.3 * size), white,
            parent=root, coll=coll, rot=(0, -30, 0))
    t.visible_shadow = False
    tm = mat(f"bubble_text_{text_color}", text_color, flat=0.9)
    text(f"{name}_txt", body, (0, -0.06, 0), 0.8 * size, tm, parent=root, coll=coll, bold=True)
    for o in root.children:
        o.visible_shadow = False
    return root


def make_soviet_flag(name="SovFlag", loc=(0, 0, 0), size=2.0, pole=6.0, rot_z=0.0, coll=None, wave=True):
    """Red flag with a yellow star / hammer-and-sickle in the corner, waving.
    Same rig as town.make_flag."""
    rows = ["RRRRRRRRRRRRRRRRRRRRRRRR",
            "RRRRYRRRRRRRRRRRRRRRRRRR",
            "RRRYYYRRRRRRRRRRRRRRRRRR",
            "RRRRYRRRRRRRRRRRRRRRRRRR",
            "RRRRRRRRRRRRRRRRRRRRRRRR",
            "RRRRRYYRRRRRRRRRRRRRRRRR",
            "RRYRRRYYRRRRRRRRRRRRRRRR",
            "RRYYRYRYRRRRRRRRRRRRRRRR",
            "RRRYYRRYRRRRRRRRRRRRRRRR",
            "RRYRYYYRRRRRRRRRRRRRRRRR",
            "RYRRRRRRRRRRRRRRRRRRRRRR",
            "RRRRRRRRRRRRRRRRRRRRRRRR",
            "RRRRRRRRRRRRRRRRRRRRRRRR",
            "RRRRRRRRRRRRRRRRRRRRRRRR",
            "RRRRRRRRRRRRRRRRRRRRRRRR",
            "RRRRRRRRRRRRRRRRRRRRRRRR"]
    m = pixel_mat("soviet_flag", rows, {"R": (0.80, 0.08, 0.06), "Y": (1.0, 0.85, 0.15)})
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    cyl(f"{name}_pole", 0.06 * size / 2, pole, (0, 0, pole / 2), mat("flag_pole", (0.7, 0.7, 0.72)), n=6,
        parent=root, coll=coll)
    W, H = size * 1.5, size
    import bmesh
    bm = bmesh.new()
    nx, nz = 12, 4
    vs = [[bm.verts.new((W * i / nx, 0, H * (k / nz - 0.5))) for k in range(nz + 1)] for i in range(nx + 1)]
    uvl = bm.loops.layers.uv.new()
    for i in range(nx):
        for k in range(nz):
            f = bm.faces.new((vs[i][k], vs[i + 1][k], vs[i + 1][k + 1], vs[i][k + 1]))
            for lp, (a, b) in zip(f.loops, ((i, k), (i + 1, k), (i + 1, k + 1), (i, k + 1))):
                lp[uvl].uv = (a / nx, b / nz)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(m)
    from .common import link
    o = link(bpy.data.objects.new(f"{name}_cloth", me), root, coll)
    o.location = (0, 0, pole - H / 2)
    if wave:
        w = o.modifiers.new("Wave", "WAVE")
        w.use_normal = False
        w.use_y = True
        w.use_x = False
        w.height, w.width, w.speed, w.narrowness = 0.25 * size / 2, 1.6 * size / 2, 0.25, 1.5
        w.start_position_x = 0
    return root


def make_recruit_booth(name="Booth", loc=(0, 0, 0), rot_z=0.0, sign="NAVY", coll=None,
                       color=(0.12, 0.20, 0.45)):
    """Little recruiting booth: counter, awning, big sign, a stack of
    pamphlets nobody takes, an empty folding chair."""
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    c = mat(f"booth_{sign}", color)
    white = mat("booth_white", (0.95, 0.95, 0.92))
    box(f"{name}_counter", (2.6, 1.0, 1.1), (0, 0, 0.55), c, parent=root, coll=coll)
    box(f"{name}_top", (2.8, 1.1, 0.08), (0, 0, 1.12), white, parent=root, coll=coll)
    for x in (-1.25, 1.25):
        cyl(f"{name}_pole{x}", 0.05, 2.6, (x, 0.4, 1.3), white, n=5, parent=root, coll=coll)
    for k in range(6):
        box(f"{name}_awn{k}", (2.8 / 6, 1.4, 0.08), (-1.4 + 2.8 / 12 + k * 2.8 / 6, 0.0, 2.65),
            c if k % 2 else white, parent=root, coll=coll, rot=(-12, 0, 0))
    box(f"{name}_signbg", (2.6, 0.06, 0.6), (0, -0.4, 3.15), white, parent=root, coll=coll)
    text(f"{name}_sign", sign, (0, -0.45, 3.15), min(0.42, 2.4 / (0.62 * len(sign))), mat(f"booth_lbl_{sign}", color), parent=root, coll=coll,
         bold=True)
    text(f"{name}_join", "JOIN NOW!", (0, -0.52, 0.65), 0.3, mat("booth_join", (0.95, 0.95, 0.92)), parent=root,
         coll=coll, bold=True)
    box(f"{name}_pamph", (0.4, 0.3, 0.25), (0.7, 0, 1.28), white, parent=root, coll=coll)
    chair = mat("chair_metal", (0.5, 0.5, 0.5))
    box(f"{name}_seat", (0.5, 0.5, 0.06), (0, 0.9, 0.5), chair, parent=root, coll=coll)
    box(f"{name}_back", (0.5, 0.06, 0.5), (0, 1.15, 0.8), chair, parent=root, coll=coll)
    return root


def make_tumbleweed(name, loc=(0, 0, 0), size=0.8, coll=None):
    root = empty(name, loc, coll=coll)
    m = mat("tumbleweed", (0.55, 0.42, 0.22))
    rnd = random.Random(len(name))
    for k in range(5):
        o = ico(f"{name}_b{k}", size * 0.55, (0, 0, 0), m, parent=root, coll=coll, subdiv=1)
        o.rotation_euler = (rnd.uniform(0, 3), rnd.uniform(0, 3), rnd.uniform(0, 3))
        o.scale = (1, 0.15, 1)
    return root


def roll(obj, a, b, start, end, radius=0.8, hops=3, hop_h=0.6):
    """Tumbleweed roll from a to b with little hops."""
    for f in range(start, end + 1, 2):
        t = (f - start) / max(1, end - start)
        x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        z = a[2] + abs(math.sin(t * math.pi * hops)) * hop_h
        obj.location = (x, y, z)
        obj.rotation_euler[1] = -math.dist(a[:2], (x, y)) / radius
        obj.keyframe_insert("location", frame=f)
        obj.keyframe_insert("rotation_euler", index=1, frame=f)


def alarm_light(name, at, start, end, period=12, color=(1.0, 0.1, 0.05), energy=800):
    """Flashing red alarm: a point light pulsing + an emissive dome."""
    d = bpy.data.lights.new(name, "POINT")
    d.color = color
    d.use_shadow = False
    o = bpy.data.objects.new(name, d)
    o.location = at
    bpy.context.scene.collection.objects.link(o)
    m = mat(f"{name}_dome", color, emit=4.0)
    ico(f"{name}_bulb", 0.25, at, m, subdiv=1)
    for f in range(start, end + 1, period // 2):
        on = ((f - start) // (period // 2)) % 2 == 0
        d.energy = energy if on else energy * 0.05
        d.keyframe_insert("energy", frame=f)
    for fc in d.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
    return o


def sweat(name, head, start, end, every=10, seed=0):
    """Cartoon sweat drops flying off a person's head (parented to it)."""
    rnd = random.Random(seed)
    m = mat("sweat", (0.6, 0.85, 1.0), emit=0.8)
    f, i = start, 0
    while f < end - 8:
        side = rnd.choice((-1, 1))
        o = ico(f"{name}_{i}", 0.05, (side * 0.22, -0.1, 0.4), m, parent=head, subdiv=1)
        o.scale = (0.001,) * 3
        o.keyframe_insert("scale", frame=max(1, f - 1))
        o.keyframe_insert("location", frame=f)
        o.scale = (1, 1, 1.5)
        o.keyframe_insert("scale", frame=f)
        o.location = (side * 0.55, -0.1, 0.2)
        o.keyframe_insert("location", frame=f + 8)
        o.scale = (0.001,) * 3
        o.keyframe_insert("scale", frame=f + 9)
        f += int(every * rnd.uniform(0.6, 1.3))
        i += 1
