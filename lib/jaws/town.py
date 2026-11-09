"""Town dressing: the bookstore, a cinema marquee, sailboats, a PA speaker
pole with floating music notes, a waving flag, bunting, comic symbols
(question mark, light bulb), the review-score tomato."""
import math
import random
import bpy
from .common import mat, mesh_obj, empty, box, cyl, ico, text, link, pixel_mat


# ---------------------------------------------------------------- bookstore
def make_bookstore(name="Bookstore", loc=(0, 0, 0), rot_z=0.0, coll=None, sign="BOOKS"):
    """Two-story gray-shingled shop, white trim, front faces -Y. Big display
    windows full of colored book spines, a hanging sign, a chimney.
    Origin at ground center. Returns dict(root, door, chimney_top, roof_top,
    size)."""
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    W, D, H = 10.0, 7.0, 6.4
    shingle = mat("shingle", (0.55, 0.55, 0.52))
    trim = mat("trim_white", (0.95, 0.95, 0.92))
    roof = mat("roof_dark", (0.25, 0.26, 0.28))
    glass = mat("shop_glass", (0.14, 0.20, 0.28))
    door = mat("shop_door", (0.12, 0.30, 0.22))
    brick = mat("brick", (0.55, 0.25, 0.18))
    box(f"{name}_walls", (W, D, H), (0, 0, H / 2), shingle, parent=root, coll=coll)
    for x in (-W / 2, W / 2):                                      # corner boards
        box(f"{name}_corner{x}", (0.25, D + 0.1, H), (x, 0, H / 2), trim, parent=root, coll=coll)
    box(f"{name}_band", (W + 0.1, D + 0.1, 0.3), (0, 0, 3.3), trim, parent=root, coll=coll)
    rh = 2.8
    v = [(-W / 2 - .3, -D / 2 - .3, H), (W / 2 + .3, -D / 2 - .3, H), (W / 2 + .3, D / 2 + .3, H),
         (-W / 2 - .3, D / 2 + .3, H), (-W / 2 - .3, 0, H + rh), (W / 2 + .3, 0, H + rh)]
    f = [(0, 1, 2, 3), (0, 1, 5, 4), (3, 2, 5, 4), (0, 4, 3), (1, 2, 5)]
    mesh_obj(f"{name}_roof", v, f, [roof], parent=root, coll=coll)
    box(f"{name}_chimney", (1.0, 1.0, 3.0), (W / 2 - 2, 0.8, H + 2.0), brick, parent=root, coll=coll)
    fy = -D / 2
    # ground floor: door in the middle, two display windows with books
    box(f"{name}_door", (1.4, 0.1, 2.4), (0, fy - 0.03, 1.2), door, parent=root, coll=coll)
    box(f"{name}_doortrim", (1.8, 0.08, 0.2), (0, fy - 0.05, 2.5), trim, parent=root, coll=coll)
    rnd = random.Random(4)
    spine_cols = [(0.8, 0.15, 0.12), (0.15, 0.35, 0.7), (0.9, 0.75, 0.2), (0.2, 0.55, 0.3),
                  (0.6, 0.3, 0.6), (0.95, 0.95, 0.9), (0.9, 0.45, 0.15)]
    for side in (-1, 1):
        cx = side * 3.0
        box(f"{name}_win{side}", (3.4, 0.08, 2.0), (cx, fy - 0.03, 1.6), glass, parent=root, coll=coll)
        box(f"{name}_sill{side}", (3.8, 0.3, 0.2), (cx, fy - 0.15, 0.5), trim, parent=root, coll=coll)
        for row, z in enumerate((0.95, 1.85)):          # two shelves of spines
            x = cx - 1.5
            while x < cx + 1.4:
                w = rnd.uniform(0.12, 0.22)
                h = rnd.uniform(0.5, 0.75)
                c = rnd.choice(spine_cols)
                box(f"{name}_book{side}{row}_{x:.2f}", (w, 0.06, h), (x + w / 2, fy - 0.1, z + h / 2 - 0.25),
                    mat(f"spine_{c}", c), parent=root, coll=coll)
                x += w + 0.02
    # upstairs windows
    for k, x in enumerate((-3.0, 0, 3.0)):
        box(f"{name}_up{k}", (1.2, 0.08, 1.5), (x, fy - 0.03, 4.8), glass, parent=root, coll=coll)
        box(f"{name}_uptrim{k}", (1.5, 0.1, 0.15), (x, fy - 0.05, 5.6), trim, parent=root, coll=coll)
    # sign board over the door
    sb = mat("sign_board_green", (0.10, 0.28, 0.20))
    box(f"{name}_signboard", (6.0, 0.2, 0.9), (0, fy - 0.15, 3.0 + 0.0), sb, parent=root, coll=coll)
    text(f"{name}_sign", sign, (0, fy - 0.27, 3.0), 0.7, mat("sign_gold", (1.0, 0.85, 0.25), emit=0.8),
         parent=root, coll=coll, bold=True)
    return dict(root=root, door=(0, fy - 0.5, 0), chimney_top=(W / 2 - 2, 0.8, H + 3.5),
                roof_top=(0, 0, H + rh), size=(W, D, H))


# ---------------------------------------------------------------- cinema
def make_marquee(name="Cinema", loc=(0, 0, 0), title="JAWS 5", coll=None):
    """Old cinema front (faces -Y): marquee with a title and chasing bulbs,
    a vertical THEATER sign. Returns dict(root, bulbs)."""
    root = empty(name, loc, coll=coll)
    wall = mat("cinema_wall", (0.60, 0.22, 0.18))
    cream = mat("cinema_cream", (0.95, 0.90, 0.75))
    dark = mat("cinema_dark", (0.10, 0.08, 0.08))
    bulb_m = mat("bulb", (1.0, 0.85, 0.45), emit=4.0)
    box(f"{name}_front", (14, 4, 14), (0, 2, 7), wall, parent=root, coll=coll)
    box(f"{name}_doors", (6, 0.2, 3), (0, -0.05, 1.5), dark, parent=root, coll=coll)
    box(f"{name}_marquee", (12, 3.0, 2.6), (0, -1.5, 5.0), cream, parent=root, coll=coll)
    box(f"{name}_mqtop", (12.4, 3.4, 0.4), (0, -1.5, 6.5), wall, parent=root, coll=coll)
    text(f"{name}_title", title, (0, -3.05, 5.15), 1.6, mat("marquee_red", (0.85, 0.08, 0.08)),
         parent=root, coll=coll, bold=True)
    text(f"{name}_now", "NOW SHOWING", (0, -3.05, 4.05), 0.5, mat("marquee_ink", (0.1, 0.1, 0.1)),
         parent=root, coll=coll, bold=True)
    bulbs = []
    n = 0
    for k in range(25):
        for z in (3.75, 6.25):
            o = ico(f"{name}_bulb{n}", 0.14, (-6 + k * 0.5, -3.05, z), bulb_m, parent=root, coll=coll, subdiv=0)
            bulbs.append(o)
            n += 1
    # vertical sign
    box(f"{name}_vert", (1.4, 1.0, 6.5), (0, -0.6, 10.8), cream, parent=root, coll=coll)
    for i, ch in enumerate("THEATER"):
        text(f"{name}_v{i}", ch, (0, -1.12, 13.5 - i * 0.82), 0.7, mat("marquee_red", (0.85, 0.08, 0.08)),
             parent=root, coll=coll, bold=True)
    return dict(root=root, bulbs=bulbs)


def chase_bulbs(bulbs, start, end, period=6):
    """Theater-light chase: every third bulb on, stepping along."""
    for i, b in enumerate(bulbs):
        for f in range(start, end + 1, 2):
            b.hide_render = ((f // 2 + i // 2) % 3) == 0
            b.keyframe_insert("hide_render", frame=f)


def make_tomato(name="Tomato", loc=(0, 0, 0), size=1.0, coll=None):
    """Chunky cartoon tomato with a green leafy top."""
    root = empty(name, loc, coll=coll)
    t = ico(f"{name}_body", size, (0, 0, 0), mat("tomato", (0.9, 0.12, 0.08), flat=0.6), parent=root,
            coll=coll, subdiv=1)
    t.scale = (1.0, 1.0, 0.82)
    leaf = mat("tomato_leaf", (0.2, 0.6, 0.15), flat=0.6)
    for k in range(5):
        a = k * 72
        box(f"{name}_leaf{k}", (size * 0.8, size * 0.18, size * 0.08),
            (size * 0.3 * math.cos(math.radians(a)), size * 0.3 * math.sin(math.radians(a)), size * 0.8),
            leaf, parent=root, coll=coll, rot=(0, -12, a))
    cyl(f"{name}_stem", size * 0.08, size * 0.35, (0, 0, size * 0.95), leaf, n=5, parent=root, coll=coll)
    return root


# ---------------------------------------------------------------- boats
def make_sailboat(name, loc=(0, 0, 0), rot_z=0.0, color=None, coll=None, seed=0, sail_color=None):
    """~6 m sailboat, bow toward +X, origin at waterline. Returns dict(root,
    sail_center (local), mast_top (local))."""
    rnd = random.Random(seed)
    color = color or rnd.choice([(0.95, 0.95, 0.95), (0.2, 0.3, 0.6), (0.7, 0.15, 0.12), (0.15, 0.4, 0.3)])
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    hull = mat(f"boat_{color}", color)
    v = [(-2.8, -1.0, -0.4), (1.8, -0.9, -0.4), (3.2, 0, 0.0), (1.8, 0.9, -0.4), (-2.8, 1.0, -0.4),
         (-2.8, -1.1, 0.5), (1.8, -1.05, 0.5), (3.4, 0, 0.7), (1.8, 1.05, 0.5), (-2.8, 1.1, 0.5)]
    f = [(0, 1, 2, 3, 4), (5, 9, 8, 7, 6)] + [(i, (i + 1) % 5, (i + 1) % 5 + 5, i + 5) for i in range(5)]
    mesh_obj(f"{name}_hull", v, f, [hull], parent=root, coll=coll)
    mast = mat("mast", (0.75, 0.72, 0.65))
    cyl(f"{name}_mast", 0.08, 7.5, (0.4, 0, 4.2), mast, n=5, parent=root, coll=coll)
    box(f"{name}_boom", (3.2, 0.1, 0.1), (-1.2, 0, 1.2), mast, parent=root, coll=coll)
    sc = sail_color or rnd.choice([(0.97, 0.95, 0.88), (0.97, 0.95, 0.88), (0.9, 0.8, 0.6)])
    sail = mat(f"sail_{sc}", sc)
    sv = [(0.3, 0, 1.3), (-2.7, 0, 1.3), (0.3, 0, 7.6)]
    sf = [(0, 1, 2)]
    mesh_obj(f"{name}_main", sv + [(x, 0.04, z) for x, _, z in sv], sf + [(5, 4, 3)], [sail],
             parent=root, coll=coll)
    jv = [(0.5, 0, 1.0), (3.2, 0, 0.8), (0.5, 0, 6.8)]
    mesh_obj(f"{name}_jib", jv + [(x, 0.04, z) for x, _, z in jv], [(0, 1, 2), (5, 4, 3)], [sail],
             parent=root, coll=coll)
    return dict(root=root, sail_center=(-0.6, 0, 3.6), mast_top=(0.4, 0, 7.9))


# ---------------------------------------------------------------- flag, bunting
def _flag_mat():
    W, H = 19, 13
    rows = []
    for r in range(H):
        row = ""
        for c in range(W):
            if r < 7 and c < 8:
                row += "*" if (r in (1, 3, 5) and c in (1, 3, 5)) or (r in (2, 4) and c in (2, 4, 6)) else "B"
            else:
                row += "R" if r % 2 == 0 else "W"
        rows.append(row)
    return pixel_mat("us_flag", rows, {"R": (0.75, 0.1, 0.12), "W": (0.95, 0.93, 0.88),
                                       "B": (0.12, 0.16, 0.42), "*": (0.95, 0.93, 0.88)}, flat=0.5)


def make_flag(name="Flag", loc=(0, 0, 0), size=2.0, pole=6.0, rot_z=0.0, coll=None, wave=True):
    """Stars-and-stripes on a pole, waving (Wave modifier on a subdivided
    quad). Flag faces -Y, flies toward +X."""
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    cyl(f"{name}_pole", 0.07, pole, (0, 0, pole / 2), mat("pole_white", (0.9, 0.9, 0.88)), n=6,
        parent=root, coll=coll)
    ico(f"{name}_ball", 0.14, (0, 0, pole + 0.1), mat("pole_gold", (1.0, 0.8, 0.2)), parent=root, coll=coll,
        subdiv=0)
    W, H = size * 1.5, size
    nx, nz = 16, 8
    v, f, uvs = [], [], []
    for j in range(nz + 1):
        for i in range(nx + 1):
            v.append((0.08 + W * i / nx, 0, pole - H + H * j / nz))
    for j in range(nz):
        for i in range(nx):
            a = j * (nx + 1) + i
            f.append((a, a + 1, a + nx + 2, a + nx + 1))
    me = bpy.data.meshes.new(f"{name}_cloth")
    me.from_pydata(v, [], f)
    uv = me.uv_layers.new()
    for p in me.polygons:
        for li in p.loop_indices:
            x, _, z = v[me.loops[li].vertex_index]
            uv.data[li].uv = ((x - 0.08) / W, (z - (pole - H)) / H)
    me.materials.append(_flag_mat())
    o = link(bpy.data.objects.new(f"{name}_cloth", me), root, coll)
    if wave:
        m = o.modifiers.new("Wave", "WAVE")
        m.use_x, m.use_y = True, False        # ripples travel along the flag
        m.height, m.width, m.narrowness, m.speed = 0.18 * size, 1.1 * size, 1.5, 0.35
        m.start_position_x = -2
        m.use_normal = True                    # the cloth's normals point along Y: ripple sideways
        m.use_normal_x = m.use_normal_z = False
        m.use_normal_y = True
    return root


def bunting(name, a, b, n=14, sag=0.8, coll=None):
    """String of red/white/blue pennant triangles between points a and b."""
    cols = [mat("bunt_r", (0.8, 0.12, 0.12)), mat("bunt_w", (0.95, 0.93, 0.88)), mat("bunt_b", (0.15, 0.2, 0.55))]
    for i in range(n):
        t = (i + 0.5) / n
        p = [a[k] + (b[k] - a[k]) * t for k in range(3)]
        p[2] -= sag * 4 * t * (1 - t)
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) / n * 0.4
        ux, uy = dx / math.hypot(dx, dy), dy / math.hypot(dx, dy)
        v = [(p[0] - ux * L, p[1] - uy * L, p[2]), (p[0] + ux * L, p[1] + uy * L, p[2]), (p[0], p[1], p[2] - L * 1.6)]
        mesh_obj(f"{name}_{i}", v, [(0, 1, 2)], [cols[i % 3]], coll=coll)


# ---------------------------------------------------------------- PA speaker
def make_pa_pole(name="PA", loc=(0, 0, 0), rot_z=0.0, coll=None):
    """Wooden pole with two gray horn speakers and a cable running down to a
    plug box at the base. Speakers face -Y. Returns dict(root, horns(local),
    plug(local))."""
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    wood = mat("pole_wood", (0.40, 0.28, 0.17))
    gray = mat("horn_gray", (0.62, 0.64, 0.62))
    blk = mat("cable", (0.05, 0.05, 0.05))
    cyl(f"{name}_pole", 0.18, 7.0, (0, 0, 3.5), wood, n=6, parent=root, coll=coll)
    box(f"{name}_xarm", (2.4, 0.2, 0.2), (0, 0, 6.4), wood, parent=root, coll=coll)
    horns = []
    for side in (-1, 1):
        cyl(f"{name}_horn{side}", 0.15, 1.2, (side * 0.9, -0.5, 6.1), gray, n=8, r2=0.6, rot=(90, 0, 0),
            parent=root, coll=coll)
        cyl(f"{name}_driver{side}", 0.25, 0.5, (side * 0.9, 0.2, 6.1), gray, n=8, rot=(90, 0, 0),
            parent=root, coll=coll)
        horns.append((side * 0.9, -1.2, 6.1))
    box(f"{name}_cable", (0.06, 0.06, 5.8), (0.22, 0, 3.2), blk, parent=root, coll=coll)
    box(f"{name}_box", (0.5, 0.3, 0.6), (0.22, -0.15, 0.6), mat("plugbox", (0.55, 0.55, 0.5)), parent=root,
        coll=coll)
    return dict(root=root, horns=horns, plug=(0.22, -0.3, 0.45))


def music_notes(name, at, start, end, every=6, rise=3.5, life=30, size=0.7, seed=0, coll=None):
    """Musical notes pop out of `at` and float up, wobbling, then vanish."""
    rnd = random.Random(seed)
    m = mat("note_white", (1.0, 1.0, 0.95), emit=1.5)
    n = 0
    for f0 in range(start, end, every):
        o = text(f"{name}_{n}", rnd.choice(["♪", "♫"]), at, size, m, bold=True, coll=coll)
        n += 1
        o.scale = (0.001,) * 3
        o.keyframe_insert("scale", frame=max(1, f0 - 1))
        dx = rnd.uniform(-1.5, 1.5)
        for k in range(0, life + 1, 3):
            t = k / life
            o.location = (at[0] + dx * t + 0.3 * math.sin(t * 9 + n), at[1] - t * 0.5, at[2] + rise * t)
            sc = 1.0 if t < 0.8 else max(0.001, (1 - t) / 0.2)
            o.scale = (sc,) * 3
            o.keyframe_insert("location", frame=f0 + k)
            o.keyframe_insert("scale", frame=f0 + k)


# ---------------------------------------------------------------- comic symbols
def question_mark(name, loc, size=1.0, coll=None):
    return text(name, "?", loc, size, mat("comic_white", (1, 1, 1), emit=1.2), extrude=0.08 * size,
                bold=True, coll=coll)


def light_bulb(name, loc, size=1.0, coll=None):
    """Idea bulb: glowing yellow globe on a gray screw base, little rays."""
    root = empty(name, loc, coll=coll)
    ico(f"{name}_glass", 0.45 * size, (0, 0, 0.25 * size), mat("idea_glow", (1.0, 0.9, 0.3), emit=4.0),
        parent=root, coll=coll, subdiv=1)
    cyl(f"{name}_base", 0.2 * size, 0.35 * size, (0, 0, -0.3 * size), mat("idea_base", (0.6, 0.6, 0.6)), n=8,
        parent=root, coll=coll)
    ray = mat("idea_ray", (1.0, 0.95, 0.5), emit=3.0)
    for k in range(7):
        a = math.radians(-90 + k * 30)
        box(f"{name}_ray{k}", (0.08 * size, 0.04, 0.35 * size),
            (0.85 * size * math.cos(a + math.pi / 2) * -1, -0.05, 0.25 * size + 0.85 * size * math.sin(a + math.pi / 2)),
            ray, parent=root, coll=coll, rot=(0, math.degrees(a), 0))
    return root


def pop_in(obj, frame, scale=1.0, overshoot=1.25, out_frame=None):
    """Cartoon pop: scale 0 -> overshoot -> 1 (and optionally pop out)."""
    obj.scale = (0.001,) * 3
    obj.keyframe_insert("scale", frame=max(1, frame - 1))
    obj.scale = (scale * overshoot,) * 3
    obj.keyframe_insert("scale", frame=frame + 3)
    obj.scale = (scale,) * 3
    obj.keyframe_insert("scale", frame=frame + 6)
    if out_frame:
        obj.keyframe_insert("scale", frame=out_frame - 1)
        obj.scale = (0.001,) * 3
        obj.keyframe_insert("scale", frame=out_frame)
