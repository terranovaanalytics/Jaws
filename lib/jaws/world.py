"""Ocean, Amity Island, the car ferry, small boats, extras, gulls, splashes."""
import math
import random
import bmesh
import bpy
from .common import (mat, mesh_obj, empty, box, cyl, ico, link, box_data,
                     fix_normals)

# ---------------------------------------------------------------- ocean
def make_ocean(size=600, segs=80, color=(0.08, 0.38, 0.68), wave=0.35, coll=None):
    """Big flat-shaded grid with a Wave modifier = wobbly PS1 water."""
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=segs, y_segments=segs, size=size / 2)
    me = bpy.data.meshes.new("Ocean")
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat("ocean", color))
    o = link(bpy.data.objects.new("Ocean", me), coll=coll)
    # flat far plane out to the horizon so the wavy grid has no visible edge
    far = bpy.data.meshes.new("OceanFar")
    far.from_pydata([(-4000, -4000, -0.4), (4000, -4000, -0.4), (4000, 4000, -0.4), (-4000, 4000, -0.4)],
                    [], [(0, 1, 2, 3)])
    far.materials.append(mat("ocean", color))
    link(bpy.data.objects.new("OceanFar", far), coll=coll)
    if wave:
        w = o.modifiers.new("Wave", "WAVE")
        w.height, w.width, w.speed, w.narrowness = wave, 9.0, 0.12, 1.2
        w.start_position_x = w.start_position_y = 0
        w.falloff_radius = 0
    return o


# ---------------------------------------------------------------- island
ISLAND_R = (60.0, 45.0)   # half-extent in x, y
ISLAND_H = 10.0
ISLAND_Z = -4.0           # blob center; top sits ~6 m above the water


def island_z(x, y):
    """Approximate ground height on Amity at (x, y) (island at origin)."""
    rx, ry = ISLAND_R
    t = 1 - (x / rx) ** 2 - (y / ry) ** 2
    return ISLAND_Z + ISLAND_H * math.sqrt(max(0.0, t))


def _blob(name, sx, sy, sz, z, m, seed, coll):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
    rnd = random.Random(seed)
    for v in bm.verts:
        k = 1 + rnd.uniform(-0.07, 0.07)
        v.co.x, v.co.y, v.co.z = v.co.x * sx * k, v.co.y * sy * k, v.co.z * sz * k
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(m)
    o = link(bpy.data.objects.new(name, me), coll=coll)
    o.location.z = z
    return o


def _house(name, loc, rot, wall, roof, coll):
    w, d, h = 4.0, 3.0, 2.6
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot)
    box(f"{name}_walls", (w, d, h), (0, 0, h / 2), wall, parent=root, coll=coll)
    rh = 1.6
    v = [(-w / 2 - .2, -d / 2 - .2, h), (w / 2 + .2, -d / 2 - .2, h), (w / 2 + .2, d / 2 + .2, h),
         (-w / 2 - .2, d / 2 + .2, h), (-w / 2 - .2, 0, h + rh), (w / 2 + .2, 0, h + rh)]
    f = [(0, 1, 2, 3), (0, 1, 5, 4), (3, 2, 5, 4), (0, 4, 3), (1, 2, 5)]
    mesh_obj(f"{name}_roof", v, f, [roof], parent=root, coll=coll)
    win = mat("window", (0.15, 0.22, 0.35))
    door = mat("door", (0.25, 0.32, 0.55))
    box(f"{name}_win1", (0.7, 0.05, 0.7), (-1.0, -d / 2 - 0.02, 1.5), win, parent=root, coll=coll)
    box(f"{name}_win2", (0.7, 0.05, 0.7), (1.0, -d / 2 - 0.02, 1.5), win, parent=root, coll=coll)
    box(f"{name}_door", (0.7, 0.05, 1.3), (0, -d / 2 - 0.02, 0.65), door, parent=root, coll=coll)
    return root


def make_lighthouse(name="Lighthouse", loc=(0, 0, 0), coll=None):
    root = empty(name, loc, coll=coll)
    white = mat("lh_white", (0.96, 0.96, 0.94))
    red = mat("lh_red", (0.85, 0.10, 0.10))
    black = mat("lh_black", (0.08, 0.08, 0.09))
    lamp = mat("lh_lamp", (1.0, 0.92, 0.45), emit=5.0)
    cyl(f"{name}_tower", 1.7, 12, (0, 0, 6), white, n=8, r2=1.15, parent=root, coll=coll)
    for k, z in enumerate((3.0, 7.0, 11.0)):
        r = 1.7 - (1.7 - 1.15) * z / 12 + 0.06
        cyl(f"{name}_band{k}", r, 1.4, (0, 0, z), red, n=8, parent=root, coll=coll)
    cyl(f"{name}_deck", 1.7, 0.3, (0, 0, 12.15), black, n=8, parent=root, coll=coll)
    cyl(f"{name}_lamp", 0.85, 1.6, (0, 0, 13.1), lamp, n=8, parent=root, coll=coll)
    cyl(f"{name}_cap", 1.15, 1.3, (0, 0, 14.5), red, n=8, r2=0, parent=root, coll=coll)
    return root


def make_island(seed=5, coll=None, houses=26):
    """Amity Island at the origin. Harbor faces -Y (toward most cameras).
    Returns dict: root, dock_end (where boats tie up), lighthouse,
    carousel_spot (flat ground reserved for the carousel)."""
    rnd = random.Random(seed)
    root = empty("Amity", coll=coll)
    grass = mat("grass", (0.30, 0.72, 0.25))
    sand = mat("beach", (0.95, 0.86, 0.58))
    _blob("Amity_land", ISLAND_R[0], ISLAND_R[1], ISLAND_H, ISLAND_Z, grass, seed, coll).parent = root
    _blob("Amity_beach", ISLAND_R[0] * 1.07, ISLAND_R[1] * 1.08, ISLAND_H * 0.55,
          ISLAND_Z + 0.5, sand, seed + 1, coll).parent = root
    # little trees
    leaf = mat("tree", (0.12, 0.48, 0.15))
    trunk = mat("trunk", (0.40, 0.26, 0.14))
    walls = [mat("house_white", (0.97, 0.97, 0.95)), mat("house_cream", (0.98, 0.93, 0.80))]
    roof = mat("roof_gray", (0.45, 0.47, 0.50))
    lh_xy = (44.0, 18.0)
    carousel_xy = (-6.0, -14.0)
    placed = [lh_xy, carousel_xy, (8, -30)]
    tries = 0
    n = 0
    while n < houses and tries < 2000:
        tries += 1
        x, y = rnd.uniform(-48, 48), rnd.uniform(-36, 36)
        if (x / 50) ** 2 + (y / 37) ** 2 > 0.85:
            continue
        if any((x - px) ** 2 + (y - py) ** 2 < 60 for px, py in placed):
            continue
        placed.append((x, y))
        _house(f"House{n:02d}", (x, y, island_z(x, y) - 0.4), rnd.choice((0, 90, 15, -10)),
               rnd.choice(walls), roof, coll).parent = root
        n += 1
    for k in range(18):
        x, y = rnd.uniform(-45, 45), rnd.uniform(-30, 34)
        if (x / 50) ** 2 + (y / 37) ** 2 > 0.8 or any((x - px) ** 2 + (y - py) ** 2 < 20 for px, py in placed):
            continue
        z = island_z(x, y)
        cyl(f"Trunk{k}", 0.3, 2, (x, y, z + 0.6), trunk, n=5, parent=root, coll=coll)
        cyl(f"Tree{k}", 1.6, 4, (x, y, z + 3.2), leaf, n=6, r2=0, parent=root, coll=coll)
    lh = make_lighthouse("Lighthouse", (*lh_xy, island_z(*lh_xy) - 0.5), coll)
    lh.parent = root
    # harbor: breakwater arm of rocks + wooden pier, facing -Y
    rock = mat("rock", (0.50, 0.50, 0.52))
    for k in range(14):
        a = math.radians(200 + k * 8)
        x, y = -2 + 34 * math.cos(a) * 0.9, -30 + 22 * math.sin(a)
        if y > -40:
            continue
        box(f"Rock{k}", (4.5, 3.5, 3.0), (x, y, 0.4), rock, parent=root, coll=coll,
            rot=(rnd.uniform(-8, 8), rnd.uniform(-8, 8), rnd.uniform(0, 60)))
    wood = mat("dock_wood", (0.55, 0.40, 0.24))
    post = mat("dock_post", (0.30, 0.22, 0.14))
    px, y0, y1 = 10.0, -40.0, -60.0
    box("Pier", (4.0, abs(y1 - y0), 0.5), (px, (y0 + y1) / 2, 1.2), wood, parent=root, coll=coll)
    box("PierT", (14.0, 4.0, 0.5), (px, y1, 1.2), wood, parent=root, coll=coll)
    for k in range(6):
        y = y0 - k * 4
        for side in (-1, 1):
            cyl(f"Post{k}{side}", 0.25, 4, (px + side * 2.1, y, 0.0), post, n=5, parent=root, coll=coll)
    return dict(root=root, lighthouse=lh, dock_end=(px, y1 - 2.0, 1.45),
                carousel_spot=(*carousel_xy, island_z(*carousel_xy)))


# ---------------------------------------------------------------- ferry
def make_ferry(name="Ferry", loc=(0, 0, 0), rot_z=0.0, coll=None):
    """White-and-blue boxy car ferry, ~24 m long, bow toward +X.
    Origin = waterline center, so z<0 means sinking."""
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    blue = mat("ferry_blue", (0.08, 0.22, 0.62))
    white = mat("ferry_white", (0.97, 0.97, 0.97))
    glass = mat("ferry_glass", (0.10, 0.16, 0.30))
    red = mat("ferry_red", (0.80, 0.12, 0.10))
    black = mat("ferry_black", (0.06, 0.06, 0.07))
    L, W = 24.0, 7.0
    # hull: box with pointy-ish bow, blue below, white rail stripe on top
    v = [(-L / 2, -W / 2, -1.6), (L / 2 - 3, -W / 2, -1.6), (L / 2, -0.6, -1.0), (L / 2, 0.6, -1.0),
         (L / 2 - 3, W / 2, -1.6), (-L / 2, W / 2, -1.6),
         (-L / 2, -W / 2, 1.6), (L / 2 - 2.5, -W / 2, 1.6), (L / 2 + 1.2, -0.8, 1.9), (L / 2 + 1.2, 0.8, 1.9),
         (L / 2 - 2.5, W / 2, 1.6), (-L / 2, W / 2, 1.6)]
    f = [(0, 1, 2, 3, 4, 5), (6, 11, 10, 9, 8, 7)] + [(i, (i + 1) % 6, (i + 1) % 6 + 6, i + 6) for i in range(6)]
    mesh_obj(f"{name}_hull", v, f, [blue], parent=root, coll=coll)
    box(f"{name}_rail", (L - 0.2, W + 0.1, 0.5), (-0.1, 0, 1.75), white, parent=root, coll=coll)
    box(f"{name}_waterline", (L - 1, W + 0.12, 0.25), (-0.5, 0, 0.15), red, parent=root, coll=coll)
    # deck 1 (passenger cabin) with window strip, car deck open at the stern
    box(f"{name}_deck1", (15, W - 0.4, 2.4), (2.5, 0, 3.2), white, parent=root, coll=coll)
    for side in (-1, 1):
        box(f"{name}_win1{side}", (13.5, 0.06, 0.8), (2.5, side * (W / 2 - 0.2), 3.4), glass, parent=root, coll=coll)
        box(f"{name}_stripe{side}", (15, 0.06, 0.3), (2.5, side * (W / 2 - 0.19), 2.3), blue, parent=root, coll=coll)
    box(f"{name}_deck2", (9, W - 1.2, 1.8), (3.5, 0, 5.3), white, parent=root, coll=coll)
    for side in (-1, 1):
        box(f"{name}_win2{side}", (7.5, 0.06, 0.6), (3.5, side * (W / 2 - 0.6), 5.4), glass, parent=root, coll=coll)
    box(f"{name}_bridge", (3.2, W - 1.6, 1.4), (6.0, 0, 6.9), white, parent=root, coll=coll)
    box(f"{name}_bridgewin", (0.06, W - 1.8, 0.6), (7.62, 0, 7.0), glass, parent=root, coll=coll)
    cyl(f"{name}_stack", 0.9, 2.6, (1.5, 0, 7.3), blue, n=8, parent=root, coll=coll)
    cyl(f"{name}_stacktop", 0.95, 0.5, (1.5, 0, 8.7), black, n=8, parent=root, coll=coll)
    # tiny cars on the stern deck
    for k, c in enumerate([(0.9, 0.2, 0.2), (0.95, 0.85, 0.2), (0.2, 0.6, 0.3), (0.3, 0.4, 0.9)]):
        cm = mat(f"car{k}", c)
        x, y = -10 + (k // 2) * 3.4, -1.5 + (k % 2) * 3.0
        box(f"{name}_car{k}", (2.8, 1.5, 0.8), (x, y, 2.3), cm, parent=root, coll=coll)
        box(f"{name}_carTop{k}", (1.5, 1.4, 0.6), (x - 0.2, y, 3.0), cm, parent=root, coll=coll)
    return root


def bob(obj, start, end, period=48, roll=1.5, pitch=0.8, heave=0.15, phase=0):
    """Gentle sea motion keyed on top of an object's current transform."""
    base_r = tuple(obj.rotation_euler)
    base_z = obj.location.z
    for f in range(start, end + 1, 6):
        t = 2 * math.pi * (f + phase) / period
        obj.rotation_euler[0] = base_r[0] + math.radians(roll * math.sin(t))
        obj.rotation_euler[1] = base_r[1] + math.radians(pitch * math.sin(t * 0.7 + 1))
        obj.location.z = base_z + heave * math.sin(t * 1.3)
        obj.keyframe_insert("rotation_euler", frame=f)
        obj.keyframe_insert("location", index=2, frame=f)


# ---------------------------------------------------------------- small boats
_BOAT_COLORS = [(0.9, 0.2, 0.2), (0.95, 0.75, 0.15), (0.2, 0.6, 0.3), (0.95, 0.95, 0.95),
                (0.2, 0.45, 0.85), (0.95, 0.5, 0.15)]


def make_small_boat(name, loc=(0, 0, 0), rot_z=0.0, color=None, coll=None, seed=0):
    """Little ~5 m motorboat, bow toward +X, origin at waterline."""
    rnd = random.Random(seed)
    color = color or rnd.choice(_BOAT_COLORS)
    root = empty(name, loc, coll=coll)
    root.rotation_euler[2] = math.radians(rot_z)
    hull = mat(f"boat_{color}", color)
    white = mat("boat_white", (0.97, 0.97, 0.97))
    v = [(-2.4, -1.0, -0.5), (1.6, -0.8, -0.5), (2.6, 0, 0.0), (1.6, 0.8, -0.5), (-2.4, 1.0, -0.5),
         (-2.4, -1.1, 0.6), (1.6, -1.0, 0.6), (2.8, 0, 0.8), (1.6, 1.0, 0.6), (-2.4, 1.1, 0.6)]
    f = [(0, 1, 2, 3, 4), (5, 9, 8, 7, 6)] + [(i, (i + 1) % 5, (i + 1) % 5 + 5, i + 5) for i in range(5)]
    mesh_obj(f"{name}_hull", v, f, [hull], parent=root, coll=coll)
    box(f"{name}_cabin", (1.4, 1.4, 0.9), (-0.3, 0, 1.05), white, parent=root, coll=coll)
    box(f"{name}_wind", (0.05, 1.3, 0.4), (0.42, 0, 1.25), mat("ferry_glass", (0.10, 0.16, 0.30)), parent=root, coll=coll)
    return root


# ---------------------------------------------------------------- extras
_SHIRTS = [(0.9, 0.3, 0.3), (0.3, 0.5, 0.9), (0.95, 0.8, 0.2), (0.4, 0.8, 0.4),
           (0.9, 0.5, 0.8), (1, 1, 1), (0.95, 0.55, 0.15)]


def make_extra(name, loc=(0, 0, 0), seed=0, scale=1.0, coll=None):
    """Tiny background person (tourist / kid). Origin at feet."""
    rnd = random.Random(seed)
    root = empty(name, loc, coll=coll)
    root.scale = (scale,) * 3
    shirt = mat(f"shirt{seed % len(_SHIRTS)}", _SHIRTS[seed % len(_SHIRTS)])
    pants = mat("extra_pants", (0.22, 0.25, 0.4))
    skin = mat(f"skin{seed % 3}", [(0.95, 0.75, 0.6), (0.7, 0.5, 0.35), (0.45, 0.3, 0.2)][seed % 3])
    box(f"{name}_legs", (0.36, 0.22, 0.8), (0, 0, 0.4), pants, parent=root, coll=coll)
    box(f"{name}_body", (0.46, 0.26, 0.6), (0, 0, 1.1), shirt, parent=root, coll=coll)
    box(f"{name}_head", (0.3, 0.3, 0.3), (0, 0, 1.58), skin, parent=root, coll=coll)
    for side in (-1, 1):
        box(f"{name}_arm{side}", (0.12, 0.14, 0.55), (side * 0.3, 0, 1.12), shirt,
            parent=root, coll=coll, rot=(0, side * 25, 0))
    return root


# ---------------------------------------------------------------- effects
def make_gull(name, loc, coll=None):
    root = empty(name, loc, coll=coll)
    w = mat("gull", (1, 1, 1))
    wings = []
    for side in (-1, 1):
        piv = empty(f"{name}_wp{side}", (0, 0, 0), root, coll)
        box(f"{name}_wing{side}", (0.5, 1.2, 0.08), (0, side * 0.6, 0), w, parent=piv, coll=coll)
        wings.append((piv, side))
    box(f"{name}_body", (0.7, 0.25, 0.22), (0, 0, 0), w, parent=root, coll=coll)
    return root, wings


def flap(wings, start, end, period=8, angle=35, phase=0):
    f, s = start - phase, 1
    while f <= end:
        for piv, side in wings:
            piv.rotation_euler[0] = math.radians(angle * s * side)
            piv.keyframe_insert("rotation_euler", index=0, frame=f)
        s *= -1
        f += period // 2


def splash(name, at, frame, count=14, size=0.5, power=6.0, life=24, seed=0, coll=None,
           color=(1, 1, 1)):
    """Low-poly splash: white chunks fly up and fall back, shrinking."""
    rnd = random.Random(seed)
    m = mat(f"splash_{color}", color)
    g = 9.8
    for i in range(count):
        o = ico(f"{name}_{i}", size * rnd.uniform(0.6, 1.3), at, m, coll=coll, subdiv=0)
        a = rnd.uniform(0, 2 * math.pi)
        sp = power * rnd.uniform(0.3, 1.0)
        vx, vy, vz = math.cos(a) * sp * 0.5, math.sin(a) * sp * 0.5, power * rnd.uniform(0.7, 1.3)
        o.scale = (0.001,) * 3
        o.keyframe_insert("scale", frame=frame - 1)
        for k in range(0, life + 1, 2):
            t = k / 24
            o.location = (at[0] + vx * t, at[1] + vy * t, at[2] + vz * t - 0.5 * g * t * t)
            sc = max(0.001, 1 - k / life)
            o.scale = (sc,) * 3
            o.keyframe_insert("location", frame=frame + k)
            o.keyframe_insert("scale", frame=frame + k)


# ---------------------------------------------------------------- ragdolls
SCREAM = ["........",
          ".KK..KK.",
          ".KK..KK.",
          "........",
          "...RR...",
          "..RKKR..",
          "..RKKR..",
          "...RR..."]


def make_ragdoll_extra(name, loc=(0, 0, 0), seed=0, scale=1.0, coll=None, faces=True):
    """Tourist as ONE mesh (so it can be a single rigid body), with a
    pixel-art screaming face. Origin at the hips."""
    from .common import pixel_mat, decal
    shirt = mat(f"shirt{seed % len(_SHIRTS)}", _SHIRTS[seed % len(_SHIRTS)])
    pants = mat("extra_pants", (0.22, 0.25, 0.4))
    skin_c = [(0.95, 0.75, 0.6), (0.7, 0.5, 0.35), (0.45, 0.3, 0.2)][seed % 3]
    skin = mat(f"skin{seed % 3}", skin_c)
    # z offsets centered on the bounding box so the physics box fits the body
    parts = [((0.36, 0.22, 0.8), (0, 0, -0.5), 1), ((0.46, 0.26, 0.6), (0, 0, 0.2), 0),
             ((0.3, 0.3, 0.3), (0, 0, 0.68), 2),
             ((0.12, 0.14, 0.55), (-0.32, 0, 0.65), 0), ((0.12, 0.14, 0.55), (0.32, 0, 0.65), 0)]
    V, F, M = [], [], []
    for size, c, mi in parts:
        v, f = box_data(*[x * scale for x in size], *[x * scale for x in c])
        off = len(V)
        V += v
        F += [tuple(i + off for i in face) for face in f]
        M += [mi] * len(f)
    o = mesh_obj(name, V, F, [shirt, pants, skin], face_mat=M, loc=loc, coll=coll)
    if faces:
        fm = pixel_mat(f"scream{seed % 3}", SCREAM,
                       {".": skin_c, "K": (0.02, 0.02, 0.02), "R": (0.75, 0.05, 0.08)})
        decal(f"{name}_face", fm, (0.3 * scale, 0.3 * scale), (0, -0.152 * scale, 0.68 * scale),
              parent=o, coll=coll)
    return o


def rigid(obj, kind="ACTIVE", mass=1.0, bounce=0.3, friction=0.6, shape="BOX"):
    s = bpy.context.scene
    vl = bpy.context.view_layer
    for o in vl.objects:
        o.select_set(False)
    vl.objects.active = obj
    obj.select_set(True)
    bpy.ops.rigidbody.object_add(type=kind)
    s.rigidbody_world.point_cache.frame_end = s.frame_end
    rb = obj.rigid_body
    rb.mass, rb.restitution, rb.friction = mass, bounce, friction
    rb.collision_shape = shape
    return rb


def bake_physics():
    """No-op kept for scene compatibility: common.render() simulates the
    rigid-body cache after all scene edits (edits invalidate the cache)."""
