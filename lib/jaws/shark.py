"""Great white shark (and its mechanical twin), built from code.

    s = make_shark("Shark01", loc=(0,0,0), variant="real" | "mech", scale=1)
    s.root        -> empty to move/rotate the whole shark (faces +X)
    s.jaw         -> pivot, rotate Y to open:  open_jaw(s, frame, amount)
    s.tail        -> pivot, wags on Z:         swim_wag(s, start, end)

Meshes are built once per variant and shared by every copy, so swarms of
20-100 sharks are cheap (linked duplicates).
"""
import math
import random
from .common import fix_normals, mat, mesh_obj, empty, cyl_data, box_data

# (x, half-width, top, bottom) cross sections, nose toward +X
FRONT_RINGS = [(-0.40, 0.20, 0.27, -0.20), (0.00, 0.31, 0.36, -0.32),
               (0.45, 0.29, 0.32, -0.28), (0.50, 0.28, 0.31, -0.10),
               (0.75, 0.20, 0.24, -0.10), (0.95, 0.10, 0.14, -0.06)]
NOSE = (1.12, 0.0, 0.05)
TAIL_RINGS = [(-0.40, 0.20, 0.27, -0.20), (-0.70, 0.09, 0.15, -0.08),
              (-1.00, 0.03, 0.10, 0.00)]
N = 8  # octagonal cross sections: peak PlayStation fidelity


def _ring(x, w, top, bot):
    pts = []
    for i in range(N):
        a = 2 * math.pi * (i + 0.5) / N
        s, c = math.sin(a), math.cos(a)
        pts.append((x, w * c, s * (top if s > 0 else -bot)))
    return pts


def _palette(variant):
    if variant == "mech":
        return dict(
            back=mat("mech_back", (0.42, 0.45, 0.48), rough=0.5, metal=0.6),
            belly=mat("mech_belly", (0.28, 0.30, 0.33), rough=0.5, metal=0.6),
            mouth=mat("mech_mouth", (0.08, 0.08, 0.09)),
            teeth=mat("mech_teeth", (0.85, 0.85, 0.80), rough=0.4, metal=0.8),
            eye=mat("mech_eye", (1.0, 0.1, 0.05), emit=4.0),
            gill=mat("mech_gill", (0.15, 0.15, 0.17)),
            rivet=mat("mech_rivet", (0.62, 0.62, 0.60), rough=0.4, metal=0.8),
            glass=mat("porthole_glow", (1.0, 0.82, 0.3), emit=6.0),
            frame=mat("porthole_frame", (0.72, 0.55, 0.22), rough=0.4, metal=0.9),
        )
    return dict(
        back=mat("shark_back", (0.36, 0.44, 0.54)),
        belly=mat("shark_belly", (0.93, 0.93, 0.90)),
        mouth=mat("shark_mouth", (0.62, 0.08, 0.10)),
        teeth=mat("shark_teeth", (1.0, 1.0, 0.95)),
        eye=mat("shark_eye", (0.02, 0.02, 0.02)),
        gill=mat("shark_gill", (0.25, 0.28, 0.32)),
    )


def _tube(rings, cap_front=None, cap_back=True, mouth_x=None):
    """Loft octagon rings into a tube. Returns verts, faces, face_mat.
    Material slots: 0 back, 1 belly, 2 mouth."""
    verts, faces, fm = [], [], []
    for r in rings:
        verts += _ring(*r)
    for k in range(len(rings) - 1):
        a, b = k * N, (k + 1) * N
        for i in range(N):
            j = (i + 1) % N
            faces.append((a + i, b + i, b + j, a + j))
    if cap_front is not None:
        tip = len(verts)
        verts.append(cap_front)
        a = (len(rings) - 1) * N
        for i in range(N):
            faces.append((a + i, tip, a + (i + 1) % N))
    if cap_back:
        faces.append(tuple(range(N - 1, -1, -1)))
    for f in faces:  # color by facing direction: dark back, white belly
        pts = [verts[i] for i in f]
        cx = sum(p[0] for p in pts) / len(pts)
        cz = sum(p[2] for p in pts) / len(pts)
        down = cz < -0.04
        if mouth_x is not None and cx > mouth_x and cz < -0.05 and cz > -0.12:
            fm.append(2)               # palate, revealed when the jaw opens
        elif mouth_x is not None and mouth_x - 0.04 < cx < mouth_x + 0.04 and down:
            fm.append(2)               # back of throat
        else:
            fm.append(1 if down else 0)
    return verts, faces, fm


def _prism(tri, thick):
    """Extrude a triangle/polygon in the XZ plane to a slab along Y."""
    n = len(tri)
    v = [(x, -thick / 2, z) for x, z in tri] + [(x, thick / 2, z) for x, z in tri]
    f = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        f.append((i, j, n + j, n + i))
    return v, f


def _cone_y(r, h, n=4):
    """Little pyramid tooth pointing along -Z (flip with sign)."""
    v = [(r * math.cos(2 * math.pi * i / n), r * math.sin(2 * math.pi * i / n), 0)
         for i in range(n)] + [(0, 0, -h)]
    f = [tuple(range(n))] + [(i, (i + 1) % n, n)[::-1] for i in range(n)]
    return v, f


def _shift(v, dx=0, dy=0, dz=0, sx=1, sy=1, sz=1):
    return [(x * sx + dx, y * sy + dy, z * sz + dz) for x, y, z in v]


_CACHE = {}


def _build_meshes(variant):
    import bpy
    P = _palette(variant)
    slots = [P["back"], P["belly"], P["mouth"], P["teeth"], P["eye"], P["gill"]]
    if variant == "mech":
        slots += [P["rivet"], P["glass"], P["frame"]]

    def mk(name, V, F, M):
        me = bpy.data.meshes.new(f"{variant}_{name}")
        me.from_pydata(V, [], F)
        for s in slots:
            me.materials.append(s)
        for p, i in zip(me.polygons, M):
            p.material_index = i
        fix_normals(me)
        return me

    # ---- body (front half + head, upper teeth, eyes, gills, fins)
    bv, bf, bm = _tube(FRONT_RINGS, cap_front=NOSE, cap_back=False, mouth_x=0.48)
    V, F, M = list(bv), list(bf), list(bm)

    def add(v, f, m):
        off = len(V)
        V.extend(v)
        F.extend(tuple(i + off for i in face) for face in f)
        M.extend([m] * len(f))

    # dorsal fin (the triangle that ruins beach days)
    add(*_prism([(0.22, 0.28), (-0.30, 0.28), (-0.42, 0.95)], 0.06), 0)
    # pectoral fins
    for side in (-1, 1):
        wing = [(0.32, side * 0.24, -0.16), (0.04, side * 0.24, -0.18),
                (-0.12, side * 0.68, -0.42)]
        wv = wing + [(x, y, z + 0.04) for x, y, z in wing]
        wf = [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]
        add(wv, wf, 0)
    # eyes
    for side in (-1, 1):
        v, f = box_data(0.07, 0.03, 0.07, 0.78, side * 0.185, 0.07)
        add(v, f, 4)
    # gills: three dark slits each side
    for side in (-1, 1):
        for k in range(3):
            v, f = box_data(0.025, 0.02, 0.2, 0.30 - k * 0.07, side * 0.29, -0.02)
            add(v, f, 5)
    # upper teeth around the palate edge (point down)
    for k in range(7):
        x = 0.54 + k * 0.075
        w = 0.27 - (x - 0.5) * 0.85
        for side in (-1, 1):
            v, f = _cone_y(0.025, 0.07)
            add(_shift(v, x, side * max(0.04, w - 0.03), -0.10), f, 3)
    if variant == "mech":
        # rivets on every ring vertex, plus a glowing porthole on each side
        for r in FRONT_RINGS[:-1]:
            for p in _ring(*r):
                v, f = box_data(0.035, 0.035, 0.035, *p)
                add(v, f, 6)
        for side in (-1, 1):
            fv, ff = cyl_data(0.19, 0.06, 10)
            add([(x, side * (0.30 + z), y + 0.08) for x, y, z in fv], ff, 8)
            gv, gf = cyl_data(0.14, 0.08, 10)
            add([(x, side * (0.31 + z), y + 0.08) for x, y, z in gv], gf, 7)
    body = mk("body", V, F, M)

    # ---- tail section (wags) with crescent tail fin
    tv, tf, tm = _tube(TAIL_RINGS, cap_front=None, cap_back=True)
    tv = [(x + 0.40, y, z) for x, y, z in tv]  # pivot at x=-0.40
    V, F, M = list(tv), list(tf), list(tm)
    add(*_prism([(-0.55, 0.05), (-0.62, -0.04), (-1.00, 0.70), (-0.86, 0.66)], 0.05), 0)
    add(*_prism([(-0.55, 0.00), (-0.62, 0.06), (-0.88, -0.42), (-0.78, -0.38)], 0.05), 0)
    if variant == "mech":
        for r in TAIL_RINGS[:-1]:
            for p in _ring(*r):
                v, f = box_data(0.035, 0.035, 0.035, p[0] + 0.40, p[1], p[2])
                add(v, f, 6)
    tail = mk("tail", V, F, M)

    # ---- lower jaw (hinged at its back-top corner, x=0.47 z=-0.10)
    L = 0.60
    jv = [(0, -0.27, 0), (0, 0.27, 0), (L, -0.06, 0.03), (L, 0.06, 0.03),
          (0, -0.25, -0.20), (0, 0.25, -0.20), (L, -0.05, -0.04), (L, 0.05, -0.04)]
    jf = [(0, 2, 3, 1), (4, 5, 7, 6), (0, 4, 6, 2), (1, 3, 7, 5),
          (2, 6, 7, 3), (0, 1, 5, 4)]
    V, F, M = list(jv), list(jf), [2, 1, 0, 0, 1, 2]
    for k in range(6):
        x = 0.08 + k * 0.085
        w = 0.25 - x * 0.33
        for side in (-1, 1):
            v, f = _cone_y(0.025, 0.07)
            add(_shift(v, x, side * max(0.03, w - 0.03), 0.0, sz=-1), [t[::-1] for t in f], 3)
    if variant == "mech":
        for p in jv[4:]:
            v, f = box_data(0.035, 0.035, 0.035, *p)
            add(v, f, 6)
    jaw = mk("jaw", V, F, M)
    return dict(body=body, tail=tail, jaw=jaw)


class Shark:
    def __init__(self, root, jaw, tail, parts):
        self.root, self.jaw, self.tail, self.parts = root, jaw, tail, parts


def make_shark(name="Shark", loc=(0, 0, 0), rot_z=0.0, scale=1.0,
               variant="real", coll=None):
    if variant not in _CACHE:
        _CACHE[variant] = _build_meshes(variant)
    me = _CACHE[variant]
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    root.scale = (scale,) * 3
    body = mesh_obj(f"{name}_body", None, None, None, parent=root, coll=coll, mesh=me["body"])
    tail = empty(f"{name}_tailPivot", (-0.40, 0, 0), parent=root, coll=coll)
    tmesh = mesh_obj(f"{name}_tail", None, None, None, parent=tail, coll=coll, mesh=me["tail"])
    jaw = empty(f"{name}_jawPivot", (0.47, 0, -0.10), parent=root, coll=coll)
    jmesh = mesh_obj(f"{name}_jaw", None, None, None, parent=jaw, coll=coll, mesh=me["jaw"])
    return Shark(root, jaw, tail, [body, tmesh, jmesh])


def open_jaw(shark, frame, amount=1.0):
    """amount 0 = closed, 1 = wide open (~40 degrees). Keyframes at frame."""
    shark.jaw.rotation_euler[1] = math.radians(40 * amount)
    shark.jaw.keyframe_insert("rotation_euler", index=1, frame=frame)


def chomp(shark, start, end, period=8):
    """Snap the jaw open/closed repeatedly between start and end."""
    f, o = start, 0.0
    while f <= end:
        open_jaw(shark, f, o)
        o = 1.0 - o
        f += period // 2


def swim_wag(shark, start, end, period=12, angle=22, seed=None):
    """Side-to-side tail wag. seed staggers swarms so they don't sync up."""
    off = (random.Random(seed).randint(0, period) if seed is not None else 0)
    f, sign = start - off, 1
    while f <= end + period:
        shark.tail.rotation_euler[2] = math.radians(angle * sign)
        shark.tail.keyframe_insert("rotation_euler", index=2, frame=f)
        sign *= -1
        f += period // 2
