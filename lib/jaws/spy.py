"""Jaws 7: Cold War kit. The Russian nuclear submarine, a little prop plane,
a black helicopter, the White House and the Oval Office, Maine pines, a radio
and jammer, and new blocky people (the President, a CIA agent, Russian sailors).

    sub = make_nuke_sub("Sub", loc, rot_z, scale)   # faces +X; sub["root"], ["hatch"] (lid pivot),
                                                    # ["hatch_xyz"] local hatch spot, ["window"]
    pl = make_plane("Plane"); spin(pl["prop"], 0, start, end)     # faces +X
    h = make_helicopter("Heli"); spin(h["rotor"], 2, start, end)  # faces +X
    make_white_house("WH", loc)  (front faces -Y; returns door spot)
    make_oval_office()           (returns desk spot; room centered at origin)
    make_pine, make_radio, make_jammer, static_burst
    make_president, make_agent, make_russian  (rigs like people.make_brody, face -Y)
"""
import math
import random
from .common import box, cyl, ico, empty, mat, text, mesh_obj
from .people import _build, BRODY


def spin(obj, axis, start, end, rpm=600.0, step=1):
    """Keyframe a fast spin (propellers, rotors). A few degrees short of a
    whole number of turns per key so it reads as a blur-ish stutter, PS1 style."""
    per_frame = rpm * 360 / 60 / 24
    for f in range(start, end + 1, step):
        obj.rotation_euler[axis] = math.radians((f - start) * per_frame % 360)
        obj.keyframe_insert("rotation_euler", index=axis, frame=f)


def star(name, loc, r, material, rot_z=0, parent=None, coll=None):
    """Flat five-point star in the XZ plane, facing -Y (rot_z=180: facing +Y)."""
    v = [(0, 0, 0)]
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.4
        v.append((rr * math.cos(a), 0, rr * math.sin(a)))
    f = [(0, 1 + (k + 1) % 10, 1 + k) for k in range(10)]
    o = mesh_obj(name, v, f, [material], loc=loc, parent=parent, coll=coll)
    o.rotation_euler[2] = math.radians(rot_z)
    return o


# ---------------------------------------------------------------- submarine
def make_nuke_sub(name="Sub", loc=(0, 0, 0), rot_z=0.0, scale=1.0, coll=None, crew_window=True):
    """Big black Soviet-style boat, 40 m long at scale 1, nose +X. Red star on
    the sail. The deck hatch sits behind the sail."""
    hull = mat("sub_hull", (0.10, 0.11, 0.12), rough=0.6, metal=0.3)
    belly = mat("sub_belly", (0.42, 0.10, 0.08))            # red anti-fouling below the waterline
    deck = mat("sub_deck", (0.16, 0.17, 0.18))
    red = mat("sub_star", (0.95, 0.08, 0.06), emit=1.2)
    white = mat("sub_num", (0.92, 0.90, 0.85), emit=0.6)
    glow = mat("sub_window", (1.0, 0.85, 0.45), emit=4.0)
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    root.scale = (scale,) * 3
    L, R = 30.0, 3.0
    cyl(f"{name}_hull", R, L, (0, 0, 0), hull, n=12, rot=(0, 90, 0), parent=root, coll=coll)
    cyl(f"{name}_belly", R * 1.01, L * 0.98, (0, 0, -0.9), belly, n=12, rot=(0, 90, 0), parent=root,
        coll=coll).scale = (0.75, 1, 1)
    cyl(f"{name}_nose", R, 6, (L / 2 + 3, 0, 0), hull, n=12, r2=0.6, rot=(0, 90, 0), parent=root, coll=coll)
    cyl(f"{name}_tailcone", R, 9, (-L / 2 - 4.5, 0, 0), hull, n=12, r2=0.5, rot=(0, -90, 0), parent=root,
        coll=coll)
    box(f"{name}_deck", (L * 0.9, 2.2, 0.4), (0, 0, R - 0.05), deck, parent=root, coll=coll)
    # sail (conning tower) with dive planes
    sx = 5.0
    box(f"{name}_sail", (7.0, 1.8, 4.4), (sx, 0, R + 2.2), hull, parent=root, coll=coll)
    box(f"{name}_sailtop", (6.0, 1.6, 0.4), (sx - 0.3, 0, R + 4.55), deck, parent=root, coll=coll)
    box(f"{name}_sailplane", (2.0, 7.0, 0.25), (sx + 1.2, 0, R + 3.95), hull, parent=root, coll=coll)
    for k, h in enumerate((1.2, 0.8, 0.6)):                  # periscope, mast, aerial
        cyl(f"{name}_mast{k}", 0.15, h * 2.5, (sx - 1.5 + k * 1.2, 0, R + 4.6 + h * 1.25), deck, n=5,
            parent=root, coll=coll)
    for side in (-1, 1):
        y = side * 0.92
        rot = (90, 0, 0) if side < 0 else (90, 0, 180)
        star(f"{name}_star{side}", (sx + 1.6, y * 1.03, R + 2.4), 1.2, red, rot_z=0 if side < 0 else 180,
             parent=root, coll=coll)
        text(f"{name}_num{side}", "K-7", (sx - 1.8, y * 1.01, R + 2.2), 1.1, white, rot=rot, parent=root,
             coll=coll, bold=True)
        if crew_window:
            box(f"{name}_win{side}", (1.0, 0.1, 0.55), (sx - 1.8, y * 1.02, R + 3.6), glow, parent=root,
                coll=coll)
    # stern planes + rudder + propeller
    box(f"{name}_sternplane", (2.2, 9.0, 0.25), (-L / 2 - 5.5, 0, 0), hull, parent=root, coll=coll)
    box(f"{name}_rudder", (2.2, 0.25, 6.5), (-L / 2 - 5.5, 0, 0), hull, parent=root, coll=coll)
    prop = empty(f"{name}_prop", (-L / 2 - 9.2, 0, 0), parent=root, coll=coll)
    bronze = mat("sub_prop", (0.6, 0.45, 0.2), rough=0.4, metal=0.8)
    for k in range(5):
        b = box(f"{name}_blade{k}", (0.2, 0.6, 2.2), (0, 0, 1.1), bronze, parent=prop, coll=coll)
        b.rotation_euler = (math.radians(15), 0, 0)
        b.location = (0, -1.1 * math.sin(k * 2 * math.pi / 5), 1.1 * math.cos(k * 2 * math.pi / 5))
        b.rotation_euler = (k * 2 * math.pi / 5, math.radians(20), 0)
    # deck hatch behind the sail: rim + lid on a hinge
    hx = -3.0
    cyl(f"{name}_hatchrim", 0.75, 0.35, (hx, 0, R + 0.3), deck, n=10, parent=root, coll=coll)
    cyl(f"{name}_hatchhole", 0.62, 0.05, (hx, 0, R + 0.48), mat("sub_hole", (0.01, 0.01, 0.01)), n=10,
        parent=root, coll=coll)
    hinge = empty(f"{name}_hatch", (hx - 0.7, 0, R + 0.5), parent=root, coll=coll)
    cyl(f"{name}_hatchlid", 0.72, 0.15, (0.7, 0, 0.05), hull, n=10, parent=hinge, coll=coll)
    box(f"{name}_wheel", (0.5, 0.08, 0.08), (0.7, 0, 0.17), bronze, parent=hinge, coll=coll)
    return dict(root=root, prop=prop, hatch=hinge, hatch_xyz=(hx, 0, R + 0.5), sail_xyz=(sx, 0, R + 4.75),
                deck_z=R + 0.15, length=L + 18)


def open_hatch(sub, frame, opened=True):
    sub["hatch"].rotation_euler[1] = math.radians(-115 if opened else 0)
    sub["hatch"].keyframe_insert("rotation_euler", index=1, frame=frame)


# ---------------------------------------------------------------- aircraft
def make_plane(name="Plane", loc=(0, 0, 0), rot_z=0.0, scale=1.0, coll=None):
    """Chunky little twin-tail commuter prop plane, nose +X, 6 m long."""
    body = mat("plane_body", (0.92, 0.90, 0.85))
    stripe = mat("plane_stripe", (0.15, 0.30, 0.65))
    glass = mat("plane_glass", (0.2, 0.3, 0.45), rough=0.3, metal=0.4)
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    root.scale = (scale,) * 3
    cyl(f"{name}_fuse", 0.6, 5.0, (0, 0, 0), body, n=8, rot=(0, 90, 0), parent=root, coll=coll)
    cyl(f"{name}_tailc", 0.6, 2.0, (-3.5, 0, 0.15), body, n=8, r2=0.2, rot=(0, -90, 0), parent=root, coll=coll)
    cyl(f"{name}_nosec", 0.6, 0.8, (2.9, 0, 0), body, n=8, r2=0.35, rot=(0, 90, 0), parent=root, coll=coll)
    box(f"{name}_stripe", (5.0, 1.25, 0.18), (0, 0, -0.05), stripe, parent=root, coll=coll)
    box(f"{name}_wing", (1.3, 9.0, 0.15), (0.4, 0, 0.35), body, parent=root, coll=coll)
    box(f"{name}_htail", (0.8, 3.0, 0.1), (-4.2, 0, 0.3), body, parent=root, coll=coll)
    box(f"{name}_vtail", (1.0, 0.1, 1.3), (-4.2, 0, 0.9), stripe, parent=root, coll=coll)
    box(f"{name}_wind", (0.5, 1.0, 0.4), (2.2, 0, 0.45), glass, parent=root, coll=coll)
    for k in range(4):
        for side in (-1, 1):
            box(f"{name}_win{k}{side}", (0.35, 0.05, 0.25), (1.3 - k * 0.8, side * 0.6, 0.18), glass,
                parent=root, coll=coll)
    prop = empty(f"{name}_prop", (3.35, 0, 0), parent=root, coll=coll)
    for k in range(2):
        box(f"{name}_pblade{k}", (0.06, 0.18, 2.0), (0, 0, 0), mat("plane_prop", (0.1, 0.1, 0.1)), parent=prop,
            coll=coll, rot=(k * 90, 0, 0))
    return dict(root=root, prop=prop)


def make_helicopter(name="Heli", loc=(0, 0, 0), rot_z=0.0, scale=1.0, coll=None):
    """Black government helicopter, nose +X, skids at z=0."""
    black = mat("heli_black", (0.05, 0.05, 0.06), rough=0.5, metal=0.4)
    glass = mat("heli_glass", (0.15, 0.2, 0.28), rough=0.2, metal=0.6)
    grey = mat("heli_grey", (0.3, 0.3, 0.32))
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    root.scale = (scale,) * 3
    box(f"{name}_cabin", (3.4, 2.0, 1.8), (0, 0, 1.6), black, parent=root, coll=coll)
    box(f"{name}_nose", (1.2, 1.7, 1.3), (2.2, 0, 1.4), glass, parent=root, coll=coll)
    box(f"{name}_boom", (4.5, 0.4, 0.45), (-3.8, 0, 2.1), black, parent=root, coll=coll)
    box(f"{name}_fin", (0.8, 0.12, 1.4), (-5.9, 0, 2.6), black, parent=root, coll=coll)
    box(f"{name}_door", (1.4, 0.04, 1.3), (-0.2, -1.02, 1.55), grey, parent=root, coll=coll)
    for side in (-1, 1):
        box(f"{name}_skid{side}", (4.0, 0.12, 0.12), (0, side * 1.0, 0.06), grey, parent=root, coll=coll)
        for x in (-0.9, 0.9):
            box(f"{name}_strut{side}{x}", (0.1, 0.1, 0.65), (x, side * 0.95, 0.4), grey, parent=root, coll=coll)
    cyl(f"{name}_mast", 0.15, 0.5, (0, 0, 2.75), grey, n=6, parent=root, coll=coll)
    rotor = empty(f"{name}_rotor", (0, 0, 3.0), parent=root, coll=coll)
    for k in range(2):
        box(f"{name}_blade{k}", (8.5, 0.35, 0.06), (0, 0, 0), black, parent=rotor, coll=coll, rot=(0, 0, k * 90))
    trot = empty(f"{name}_trotor", (-5.9, 0.15, 2.7), parent=root, coll=coll)
    box(f"{name}_tblade", (0.15, 0.04, 1.4), (0, 0, 0), black, parent=trot, coll=coll)
    return dict(root=root, rotor=rotor, trotor=trot, door=(-0.2, -1.3, 0))


# ---------------------------------------------------------------- Washington
def make_white_house(name="WhiteHouse", loc=(0, 0, 0), coll=None, fountain=True):
    """The President's house, blocky: white box, columned portico, balustrade,
    lawn, fountain, flag on the roof. Front faces -Y. Returns the door spot."""
    white = mat("wh_white", (0.96, 0.95, 0.92))
    trim = mat("wh_trim", (0.85, 0.84, 0.80))
    win = mat("wh_window", (0.25, 0.30, 0.38))
    roof = mat("wh_roof", (0.55, 0.57, 0.60))
    lawn = mat("wh_lawn", (0.30, 0.55, 0.22))
    path = mat("wh_path", (0.80, 0.76, 0.66))
    root = empty(name, loc, coll=coll)
    W, D, H = 34.0, 14.0, 10.0
    box(f"{name}_lawn", (160, 120, 0.4), (0, -30, -0.2), lawn, parent=root, coll=coll)
    box(f"{name}_path", (4.0, 40, 0.1), (0, -27, 0.02), path, parent=root, coll=coll)
    box(f"{name}_body", (W, D, H), (0, 0, H / 2), white, parent=root, coll=coll)
    box(f"{name}_cornice", (W + 0.6, D + 0.6, 0.6), (0, 0, H + 0.3), trim, parent=root, coll=coll)
    box(f"{name}_roof", (W - 1, D - 1, 1.5), (0, 0, H + 1.2), roof, parent=root, coll=coll)
    for k in range(int(W / 1.2)):                           # balustrade posts
        box(f"{name}_bal{k}", (0.25, 0.25, 0.9), (-W / 2 + 0.6 + k * 1.2, -D / 2 + 0.2, H + 1.05), trim,
            parent=root, coll=coll)
    for row, z in enumerate((2.6, 7.0)):
        for k in range(10):
            x = -W / 2 + 2 + k * (W - 4) / 9
            if abs(x) < 5:
                continue
            box(f"{name}_win{row}{k}", (1.4, 0.2, 2.2), (x, -D / 2 - 0.05, z), win, parent=root, coll=coll)
            box(f"{name}_pedi{row}{k}", (1.9, 0.3, 0.3), (x, -D / 2 - 0.1, z + 1.35), trim, parent=root, coll=coll)
    # portico: semicircle-ish of columns + roof slab
    box(f"{name}_portico", (11, 5, 0.8), (0, -D / 2 - 2.5, H - 0.4), trim, parent=root, coll=coll)
    box(f"{name}_steps", (9, 3, 0.6), (0, -D / 2 - 1.5, 0.3), trim, parent=root, coll=coll)
    for k in range(6):
        x = -4.5 + k * 1.8
        cyl(f"{name}_col{k}", 0.38, H - 0.8, (x, -D / 2 - 4.5 + abs(x) * 0.18, (H - 0.8) / 2), white, n=8,
            parent=root, coll=coll)
    box(f"{name}_door", (2.0, 0.2, 3.4), (0, -D / 2 - 0.1, 1.7), mat("wh_door", (0.30, 0.22, 0.15)), parent=root,
        coll=coll)
    if fountain:                                             # fountain on the lawn
        water = mat("wh_water", (0.35, 0.55, 0.65), emit=0.3)
        cyl(f"{name}_fount", 4.0, 0.6, (0, -40, 0.3), trim, n=12, parent=root, coll=coll)
        cyl(f"{name}_fwater", 3.7, 0.1, (0, -40, 0.62), water, n=12, parent=root, coll=coll)
        cyl(f"{name}_fjet", 0.25, 3.0, (0, -40, 2.0), water, n=6, r2=0.05, parent=root, coll=coll)
    for side in (-1, 1):                                     # hedges
        box(f"{name}_hedge{side}", (12, 1.2, 1.2), (side * 10, -D / 2 - 6, 0.6), mat("wh_hedge", (0.15, 0.38, 0.15)),
            parent=root, coll=coll)
    return dict(root=root, door=(loc[0], loc[1] - D / 2 - 0.4, loc[2]), roof_z=H + 2)


def make_oval_office(name="Office", coll=None):
    """Oval room around the origin: cream walls, tall windows behind the desk
    (+Y), gold drapes, navy rug with a seal-ish circle, two flags, the desk.
    Returns the spot behind the desk (president) and in front (visitor)."""
    wall = mat("oo_wall", (0.92, 0.86, 0.68))
    rug = mat("oo_rug", (0.12, 0.16, 0.32))
    gold = mat("oo_gold", (0.85, 0.65, 0.20), emit=0.2)
    wood = mat("oo_desk", (0.36, 0.20, 0.10))
    floor = mat("oo_floor", (0.45, 0.30, 0.18))
    sky = mat("oo_sky", (0.85, 0.92, 1.0), emit=2.0)
    root = empty(name, coll=coll)
    box(f"{name}_floor", (40, 40, 0.2), (0, 0, -0.1), floor, parent=root, coll=coll)
    rugo = cyl(f"{name}_rug", 6.0, 0.05, (0, -1.5, 0.03), rug, n=24, parent=root, coll=coll)
    rugo.scale = (1.25, 1, 1)
    cyl(f"{name}_seal", 1.6, 0.06, (0, -1.5, 0.05), gold, n=16, parent=root, coll=coll)
    cyl(f"{name}_sealin", 1.2, 0.07, (0, -1.5, 0.06), rug, n=16, parent=root, coll=coll)
    # oval wall from panels
    n, ax, ay, H = 22, 9.0, 7.0, 5.5
    for k in range(n):
        a = 2 * math.pi * (k + 0.5) / n
        x, y = ax * math.cos(a), ay * math.sin(a)
        w = 2 * math.pi * math.hypot(ax, ay) / math.sqrt(2) / n + 0.4
        p = box(f"{name}_wall{k}", (w, 0.3, H), (x, y, H / 2), wall, parent=root, coll=coll)
        p.rotation_euler[2] = math.atan2(ay * math.cos(a), -ax * math.sin(a))
        if 0.25 * math.pi < a < 0.75 * math.pi and k % 2 == 0:       # windows behind the desk
            wn = box(f"{name}_window{k}", (1.2, 0.1, 3.0), (x * 0.98, y * 0.98, 2.6), sky, parent=root, coll=coll)
            wn.rotation_euler[2] = p.rotation_euler[2]
            for s in (-1, 1):
                d = box(f"{name}_drape{k}{s}", (0.45, 0.25, 4.2), (0, 0, 0), gold, parent=root, coll=coll)
                d.rotation_euler[2] = p.rotation_euler[2]
                c, sn = math.cos(p.rotation_euler[2]), math.sin(p.rotation_euler[2])
                d.location = (x * 0.97 + s * 0.85 * c, y * 0.97 + s * 0.85 * sn, 2.3)
    box(f"{name}_ceiling", (24, 20, 0.2), (0, 0, H + 0.1), mat("oo_ceil", (0.95, 0.93, 0.85)), parent=root,
        coll=coll)
    # the desk
    dy = 3.2
    box(f"{name}_desk", (3.2, 1.5, 1.05), (0, dy, 0.53), wood, parent=root, coll=coll)
    box(f"{name}_desktop", (3.4, 1.7, 0.1), (0, dy, 1.1), mat("oo_desktop", (0.28, 0.15, 0.07)), parent=root,
        coll=coll)
    box(f"{name}_deskseal", (0.7, 0.05, 0.6), (0, dy - 0.77, 0.55), gold, parent=root, coll=coll)
    box(f"{name}_chair", (0.9, 0.8, 1.9), (0, dy + 1.4, 0.95), mat("oo_chair", (0.15, 0.10, 0.08)), parent=root,
        coll=coll)
    phone = box(f"{name}_phone", (0.4, 0.3, 0.15), (1.1, dy - 0.2, 1.23), mat("oo_redphone", (0.8, 0.05, 0.05)),
                parent=root, coll=coll)
    box(f"{name}_papers", (0.6, 0.45, 0.04), (-0.8, dy - 0.2, 1.17), mat("oo_paper", (0.95, 0.95, 0.92)),
        parent=root, coll=coll)
    return dict(root=root, behind=(0, dy + 0.8, 0), front=(0, dy - 2.4, 0), phone=phone, desk_top=1.15)


# ---------------------------------------------------------------- Maine / misc
def make_pine(name, loc, h=8.0, coll=None, seed=0):
    """Stacked-cone pine tree (Maine woods)."""
    rnd = random.Random(seed)
    root = empty(name, loc, coll=coll)
    cyl(f"{name}_trunk", 0.25 * h / 8, h * 0.3, (0, 0, h * 0.15), mat("pine_trunk", (0.30, 0.20, 0.12)), n=5,
        parent=root, coll=coll)
    green = mat("pine_green", (0.08, 0.28, 0.14))
    for k in range(3):
        r = (0.32 - k * 0.08) * h
        cyl(f"{name}_tier{k}", r, h * 0.42, (0, 0, h * (0.36 + k * 0.22)), green, n=6, r2=0, parent=root,
            coll=coll, rot=(0, 0, rnd.uniform(0, 60)))
    return root


def make_radio(name="Radio", loc=(0, 0, 0), coll=None):
    """Big old military radio set: grey box, dials, a speaker grille, a glowing
    frequency window (returned as 'window' so it can blink)."""
    grey = mat("radio_grey", (0.35, 0.38, 0.33))
    dark = mat("radio_dark", (0.08, 0.08, 0.08))
    root = empty(name, loc, coll=coll)
    box(f"{name}_case", (2.4, 1.0, 1.5), (0, 0, 0.75), grey, parent=root, coll=coll)
    w = box(f"{name}_window", (1.0, 0.05, 0.3), (-0.5, -0.52, 1.15), mat("radio_glow", (1.0, 0.7, 0.2), emit=3.0),
            parent=root, coll=coll)
    for k in range(3):
        cyl(f"{name}_dial{k}", 0.16, 0.12, (-0.8 + k * 0.4, -0.55, 0.55), dark, n=8, rot=(90, 0, 0), parent=root,
            coll=coll)
    for k in range(5):
        box(f"{name}_grille{k}", (0.8, 0.05, 0.06), (0.65, -0.52, 0.45 + k * 0.17), dark, parent=root, coll=coll)
    cyl(f"{name}_aerial", 0.03, 2.2, (1.0, 0.3, 2.6), dark, n=4, parent=root, coll=coll)
    return dict(root=root, window=w, speaker=(loc[0] + 0.65, loc[1] - 0.6, loc[2] + 0.8))


def make_jammer(name="Jammer", loc=(0, 0, 0), coll=None):
    """Homemade jammer: box, big dish antenna, blinking red light ('light')."""
    root = empty(name, loc, coll=coll)
    box(f"{name}_box", (0.8, 0.6, 0.5), (0, 0, 0.25), mat("jam_box", (0.15, 0.17, 0.12)), parent=root, coll=coll)
    cyl(f"{name}_pole", 0.04, 1.0, (0, 0, 1.0), mat("jam_pole", (0.6, 0.6, 0.6)), n=4, parent=root, coll=coll)
    cyl(f"{name}_dish", 0.55, 0.15, (0, -0.1, 1.5), mat("jam_dish", (0.75, 0.75, 0.72)), n=10, r2=0.2,
        rot=(70, 0, 0), parent=root, coll=coll)
    l = ico(f"{name}_light", 0.08, (0.25, -0.31, 0.4), mat("jam_light", (1.0, 0.05, 0.05), emit=6.0), parent=root,
            coll=coll)
    return dict(root=root, light=l)


def static_burst(name, at, start, end, every=3, life=6, seed=0, coll=None):
    """Zig-zag radio static lines flying out of a point (bad signal)."""
    rnd = random.Random(seed)
    m = mat("static_white", (1, 1, 1), emit=3.0)
    k = 0
    for f in range(start, end - life, every):
        o = empty(f"{name}{k}", at, coll=coll)
        for j in range(4):
            box(f"{name}{k}_z{j}", (0.35, 0.04, 0.06), (j * 0.3, 0, 0.12 * (1 if j % 2 else -1)), m, parent=o,
                coll=coll, rot=(0, 30 if j % 2 else -30, 0))
        ang = rnd.uniform(-0.8, 0.8)
        o.rotation_euler = (0, ang, 0)
        o.scale = (0.001,) * 3
        o.keyframe_insert("scale", frame=f - 1)
        o.keyframe_insert("location", frame=f)
        o.scale = (1, 1, 1)
        o.keyframe_insert("scale", frame=f + 1)
        o.location = (at[0] + 1.6 * math.cos(ang), at[1] - 0.4, at[2] - 1.6 * math.sin(ang))
        o.keyframe_insert("location", frame=f + life)
        o.keyframe_insert("scale", frame=f + life - 1)
        o.scale = (0.001,) * 3
        o.keyframe_insert("scale", frame=f + life)
        k += 1


# ---------------------------------------------------------------- people
PRESIDENT = dict(
    BRODY, leg_len=0.95, leg_w=0.22, torso=(0.64, 0.36, 0.74), arm_len=0.72, arm_w=0.17,
    head=(0.38, 0.38, 0.44),
    colors=dict(shirt=(0.10, 0.13, 0.25), pants=(0.10, 0.13, 0.25), shoes=(0.03, 0.03, 0.03),
                skin=(0.93, 0.72, 0.58), nose=(0.90, 0.62, 0.50), hair=(0.38, 0.26, 0.14),
                eyes=(0.15, 0.35, 0.55), belt=(0.10, 0.13, 0.25), collar=(0.96, 0.96, 0.96),
                tie=(0.05, 0.05, 0.08), dot=(0.9, 0.9, 0.9), pin=(0.85, 0.1, 0.1)),
)


def make_president(name="President", loc=(0, 0, 0), rot_z=0.0, coll=None):
    """Mr. President: navy suit, white collar, dark dotted tie, swept hair,
    lapel pin. Square jaw. Generic blocky guy (the photo card does the casting)."""
    P = _build(name, PRESIDENT, loc, rot_z, coll)
    b, t, h = P.b, P.torso, P.head
    HW, HD, HH, TW, TD, TH = P.HW, P.HD, P.HH, P.TW, P.TD, P.TH
    fy = -TD / 2
    b("collar", (0.26, 0.03, 0.24), (0, fy - 0.01, TH - 0.12), "collar", t)
    b("tie", (0.08, 0.04, 0.42), (0, fy - 0.03, TH - 0.3), "tie", t)
    b("pin", (0.05, 0.03, 0.05), (0.2, fy - 0.02, TH - 0.15), "pin", t)
    b("hair_top", (HW + 0.03, HD + 0.02, 0.12), (0, 0.02, HH + 0.04), "hair", h)
    b("hair_quiff", (HW * 0.8, 0.12, 0.08), (0.03, -HD / 2 + 0.06, HH + 0.12), "hair", h)
    b("hair_back", (HW + 0.03, 0.08, HH * 0.6), (0, HD / 2, HH * 0.66), "hair", h)
    b("jaw", (HW * 0.9, HD * 0.9, 0.1), (0, -0.01, 0.02), "skin", h)
    return P


AGENT = dict(
    BRODY, leg_len=1.02, leg_w=0.30, torso=(0.92, 0.48, 0.86), arm_len=0.78, arm_w=0.26,
    head=(0.42, 0.42, 0.46),
    colors=dict(shirt=(0.05, 0.05, 0.06), pants=(0.05, 0.05, 0.06), shoes=(0.02, 0.02, 0.02),
                skin=(0.92, 0.72, 0.58), nose=(0.88, 0.62, 0.50), hair=(0.40, 0.28, 0.15),
                eyes=(0.05, 0.05, 0.05), belt=(0.05, 0.05, 0.06), collar=(0.96, 0.96, 0.96),
                tie=(0.02, 0.02, 0.02), shades=(0.01, 0.01, 0.01), wire=(0.85, 0.85, 0.80)),
)


def make_agent(name="Agent", loc=(0, 0, 0), rot_z=0.0, coll=None):
    """Top CIA officer: huge (shoulders for days), black suit, black shades,
    earpiece wire, buzz cut. A big grin."""
    P = _build(name, AGENT, loc, rot_z, coll)
    b, t, h = P.b, P.torso, P.head
    HW, HD, HH, TW, TD, TH = P.HW, P.HD, P.HH, P.TW, P.TD, P.TH
    fy = -TD / 2
    b("collar", (0.28, 0.03, 0.26), (0, fy - 0.01, TH - 0.13), "collar", t)
    b("tie", (0.09, 0.04, 0.48), (0, fy - 0.03, TH - 0.33), "tie", t)
    b("hair_top", (HW + 0.02, HD + 0.02, 0.05), (0, 0.0, HH + 0.01), "hair", h)
    fz = -HD / 2
    b("shades", (HW + 0.03, 0.04, 0.1), (0, fz - 0.03, HH * 0.62), "shades", h)
    b("grin", (0.2, 0.03, 0.05), (0, fz - 0.01, HH * 0.22), "collar", h)
    b("wire", (0.03, 0.03, 0.3), (HW / 2 + 0.02, 0.05, HH * 0.15), "wire", h)
    return P


RUSSIAN = dict(
    BRODY, leg_len=0.9, leg_w=0.22, torso=(0.6, 0.36, 0.7), arm_len=0.68, arm_w=0.17,
    head=(0.38, 0.36, 0.42),
    colors=dict(shirt=(0.92, 0.92, 0.95), pants=(0.12, 0.14, 0.22), shoes=(0.03, 0.03, 0.03),
                skin=(0.95, 0.76, 0.64), nose=(0.95, 0.55, 0.50), hair=(0.25, 0.18, 0.10),
                eyes=(0.02, 0.02, 0.02), belt=(0.08, 0.06, 0.05), stripe=(0.12, 0.20, 0.55),
                fur=(0.40, 0.30, 0.20), hat=(0.12, 0.13, 0.18), star=(0.95, 0.1, 0.05),
                stache=(0.2, 0.13, 0.07)),
)


def make_russian(name="Russian", loc=(0, 0, 0), rot_z=0.0, coll=None, seed=0, stache=None):
    """Russian sailor: striped shirt, fur ushanka with a red star (ear flaps
    down), optional big mustache."""
    P = _build(name, RUSSIAN, loc, rot_z, coll)
    b, t, h = P.b, P.torso, P.head
    HW, HD, HH, TW, TD, TH = P.HW, P.HD, P.HH, P.TW, P.TD, P.TH
    for k in range(4):                                       # stripes
        b(f"stripe{k}", (TW + 0.02, TD + 0.02, 0.06), (0, 0, 0.18 + k * 0.15), "stripe", t)
    b("hat", (HW + 0.12, HD + 0.12, 0.22), (0, 0, HH + 0.08), "fur", h)
    b("hatcrown", (HW + 0.02, HD + 0.02, 0.1), (0, 0, HH + 0.22), "hat", h)
    b("hatstar", (0.08, 0.03, 0.08), (0, -HD / 2 - 0.07, HH + 0.1), "star", h)
    for side in (-1, 1):
        b(f"flap{side}", (0.06, 0.22, 0.28), (side * (HW / 2 + 0.05), 0, HH * 0.6), "fur", h)
    if stache if stache is not None else seed % 2 == 0:
        b("stache", (0.26, 0.06, 0.07), (0, -HD / 2 - 0.03, HH * 0.26), "stache", h)
    return P
