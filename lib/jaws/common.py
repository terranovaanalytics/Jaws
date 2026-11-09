"""Scene, render, material and mesh helpers shared by every shot.

Look: 1998 PlayStation. Flat shading, flat colors, no anti-aliasing, hard
shadows, and a low internal resolution that gets nearest-neighbor upscaled
to 1080x1920 by tools/render.sh. Change PIXEL_SCALE to 1 for a crisp render.
"""
import math
import os
import bpy
import bmesh
from mathutils import Vector

FPS = 24
OUT_W, OUT_H = 1080, 1920
# LOOK: "sunny" = original bright palette | "70s" = hazy late-afternoon,
# muted olive/teal/amber palette, warm low sun (tools/render.sh adds the grade)
LOOK = os.environ.get("JAWS_LOOK", "70s")
AMBIENT = 0.25      # dim sky fill on objects
SELF_LIT = 0.40     # share of flat self-lit color in every material
# JANK: 0 clean full-HD low-poly (AA, AO, bloom) | 1 PS1 hardware (12fps, vertex wobble, low res,
# dithered palette) | 2 + fog/pop-in, ragdolls, CRT/VHS | 3 + deliberate bugs
JANK = int(os.environ.get("JAWS_JANK", "0"))   # project default: 0 = clean full HD
# A scene can opt into another level by putting
#   os.environ.setdefault("JAWS_JANK", "2")
# at its top, before importing jaws.*
PIXEL_SCALE = int(os.environ.get("JAWS_PIXEL_SCALE", "4" if JANK >= 1 else "1"))
# Individual knobs (default from JANK; override any one with an env var):
SNAP = int(os.environ.get("JAWS_SNAP", "1" if JANK >= 1 else "0"))      # PS1 vertex wobble
TWOS = int(os.environ.get("JAWS_TWOS", "1" if JANK >= 1 else "0"))      # animate on twos
AA = int(os.environ.get("JAWS_AA", "1" if JANK >= 1 else "8"))           # EEVEE samples (1 = jaggies)
HD = PIXEL_SCALE == 1 and JANK == 0      # polish: crisp shadows, AO, bloom
# (palette size is JAWS_COLORS in tools/render.sh: 48 at jank>=1, 0 = off)
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


# ---------------------------------------------------------------- scene
def look_color(c, sky=False):
    """Remap a color for the current LOOK. 70s: desaturate, warm it up,
    pull down the brights; skies go hazy and dusty."""
    if LOOK != "70s":
        return tuple(c)
    r, g, b = c[:3]
    L = 0.3 * r + 0.59 * g + 0.11 * b
    k = 0.55 if sky else 0.78                       # saturation kept
    r, g, b = (L + (x - L) * k for x in (r, g, b))
    r, g, b = r * 1.03, g * 0.98, b * 0.87          # warm / amber cast
    if sky:
        r, g, b = (x * 0.8 + h * 0.2 for x, h in zip((r, g, b), (0.72, 0.62, 0.48)))
    m = 0.92                                        # no pure white
    return tuple(min(1.0, x) * m for x in (r, g, b))


def reset_scene(frames=1, world_color=(0.45, 0.72, 0.95)):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    world_color = look_color(world_color, sky=True)
    s = bpy.context.scene
    s.render.engine = "BLENDER_EEVEE"
    s.render.fps = FPS
    s.frame_start, s.frame_end = 1, max(1, int(frames))
    s.render.resolution_x = OUT_W // PIXEL_SCALE
    s.render.resolution_y = OUT_H // PIXEL_SCALE
    s.render.resolution_percentage = 100
    s.render.image_settings.file_format = "PNG"
    s.render.film_transparent = False
    s.view_settings.view_transform = "Standard"   # flat, saturated colors
    s.view_settings.look = "None"
    ee = s.eevee
    ee.taa_render_samples = AA                     # 1 = jaggies on purpose
    ee.use_soft_shadows = False
    ee.shadow_cube_size = "512"
    ee.shadow_cascade_size = "1024"
    ee.use_gtao = False
    ee.use_bloom = False
    if HD:                                          # full-HD polish
        ee.shadow_cube_size = "2048"
        ee.shadow_cascade_size = "4096"
        ee.use_soft_shadows = True
        ee.use_gtao = True
        ee.gtao_distance = 1.5
        ee.gtao_factor = 0.8
        ee.use_bloom = True
        ee.bloom_threshold = 1.0
        ee.bloom_intensity = 0.04
        ee.bloom_radius = 5.0
    s["world_color"] = list(world_color)
    w = bpy.data.worlds.new("World")
    s.world = w
    w.use_nodes = True
    # Camera sees the full sky color; objects only get a dim ambient fill
    # from it, so flat colors stay saturated instead of washing out.
    nt = w.node_tree
    bg = nt.nodes["Background"]
    bg.inputs[0].default_value = (*world_color, 1)
    bg.inputs[1].default_value = 1.0
    amb = nt.nodes.new("ShaderNodeBackground")
    amb.inputs[0].default_value = (1, 1, 1, 1)
    amb.inputs[1].default_value = AMBIENT
    lp = nt.nodes.new("ShaderNodeLightPath")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs[0])
    nt.links.new(amb.outputs[0], mix.inputs[1])
    nt.links.new(bg.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], nt.nodes["World Output"].inputs[0])
    return s


def add_sun(rot_deg=(50, 10, 35), energy=2.2, color=(1, 0.97, 0.9)):
    if LOOK == "70s":     # low golden late-afternoon sun, long shadows
        rot_deg = (max(rot_deg[0], 64), rot_deg[1], rot_deg[2])
        color = (color[0], color[1] * 0.86, color[2] * 0.66)
        energy *= 1.15
    d = bpy.data.lights.new("Sun", "SUN")
    d.energy = energy
    d.color = color
    d.angle = math.radians(1.5) if HD else 0.0     # slightly soft shadow edges in HD
    o = bpy.data.objects.new("Sun", d)
    o.rotation_euler = [math.radians(a) for a in rot_deg]
    bpy.context.scene.collection.objects.link(o)
    return o


def add_camera(loc, target, lens=35):
    cam = bpy.data.cameras.new("Cam")
    cam.lens = lens
    cam.clip_end = 2000
    o = bpy.data.objects.new("Cam", cam)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    look_at(o, target)
    bpy.context.scene.camera = o
    return o


def look_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def key_camera(cam, frame, loc, target, lens=None):
    """Keyframe camera position + aim (and lens) at a frame."""
    cam.location = loc
    look_at(cam, target)
    cam.keyframe_insert("location", frame=frame)
    cam.keyframe_insert("rotation_euler", frame=frame)
    if lens:
        cam.data.lens = lens
        cam.data.keyframe_insert("lens", frame=frame)


def add_shake(obj, start, end, strength=0.08, rot_strength=0.01, seed=1):
    """Cheap handheld/impact shake via noise modifiers on location+rotation."""
    if obj.animation_data is None or obj.animation_data.action is None:
        obj.keyframe_insert("location", frame=start)
        obj.keyframe_insert("rotation_euler", frame=start)
    for fc in obj.animation_data.action.fcurves:
        amp = strength if fc.data_path == "location" else rot_strength
        m = fc.modifiers.new("NOISE")
        m.scale = 3.0
        m.strength = amp * 2
        m.phase = seed * 7 + fc.array_index * 13
        m.use_restricted_range = True
        m.frame_start, m.frame_end = start, end
        m.blend_in = m.blend_out = 2


def linear_keys(obj):
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"


def render(out_dir, still=False):
    """Render frames (or a single still) as PNGs into out_dir."""
    s = bpy.context.scene
    os.makedirs(out_dir, exist_ok=True)
    apply_jank(s)
    rng = os.environ.get("JAWS_RANGE")        # e.g. "1-110": render part of a shot
    if rng and not preview_env():
        a, b = (int(x) for x in rng.split("-"))
        s.frame_start, s.frame_end = max(1, a), min(s.frame_end, b)
    if s.rigidbody_world:       # simulate last, after every scene edit
        s.rigidbody_world.point_cache.frame_end = s.frame_end
        for f in range(s.frame_start, s.frame_end + 1):
            s.frame_set(f)
    with open(os.path.join(out_dir, "jank"), "w") as fh:
        fh.write(str(JANK))
    with open(os.path.join(out_dir, "look"), "w") as fh:
        fh.write(LOOK)
    with open(os.path.join(out_dir, "twos"), "w") as fh:
        fh.write(str(TWOS))
    with open(os.path.join(out_dir, "res"), "w") as fh:
        fh.write(f"{s.render.resolution_x}x{s.render.resolution_y}")
    preview = os.environ.get("JAWS_FRAMES")  # e.g. "1,72,144" for quick checks
    if preview:
        for f in [int(x) for x in preview.split(",")]:
            s.frame_set(f)
            s.render.filepath = os.path.join(out_dir, f"preview_{f:04d}.png")
            bpy.ops.render.render(write_still=True)
        return
    if still:
        s.render.filepath = os.path.join(out_dir, "still.png")
        bpy.ops.render.render(write_still=True)
    else:
        s.render.filepath = os.path.join(out_dir, "f_")
        bpy.ops.render.render(animation=True)


# ---------------------------------------------------------------- jank
def preview_env():
    return bool(os.environ.get("JAWS_FRAMES"))


def apply_jank(s):
    """Scene-wide PS1 degradation, applied right before rendering."""
    if TWOS:
        s.frame_step = 2                    # animate on twos: choppy 12fps
    if SNAP:
        ng = _ps1_snap_group(s.camera, s.render.resolution_y)
        for o in s.objects:
            # skip rigid bodies: snapping their mesh would resize their physics
            # shape every frame and make them hop on their own
            if o.type == "MESH" and not o.name.startswith("OceanFar") and o.rigid_body is None:
                m = o.modifiers.new("PS1Snap", "NODES")
                m.node_group = ng
    if JANK >= 2:
        _fog(s)


def _ps1_snap_group(cam, res_y):
    """Geometry Nodes: snap every vertex to a coarse SCREEN-space grid, like
    the PS1's integer vertex math. Moving things jitter and wobble."""
    import math as _m
    ng = bpy.data.node_groups.new("PS1Snap", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N, L = ng.nodes, ng.links
    gi, go = N.new("NodeGroupInput"), N.new("NodeGroupOutput")
    setp = N.new("GeometryNodeSetPosition")
    pos = N.new("GeometryNodeInputPosition")
    selfo = N.new("GeometryNodeSelfObject")
    me = N.new("GeometryNodeObjectInfo"); me.transform_space = "ORIGINAL"
    L.new(selfo.outputs[0], me.inputs["Object"])
    ci = N.new("GeometryNodeObjectInfo"); ci.transform_space = "ORIGINAL"
    ci.inputs["Object"].default_value = cam

    def vm(op, a, b=None):
        n = N.new("ShaderNodeVectorMath"); n.operation = op
        L.new(a, n.inputs[0])
        if b is not None:
            L.new(b, n.inputs[1])
        return n.outputs[0]

    def rot(v, r, inv=False):
        n = N.new("ShaderNodeVectorRotate"); n.rotation_type = "EULER_XYZ"; n.invert = inv
        L.new(v, n.inputs["Vector"]); L.new(r, n.inputs["Rotation"])
        return n.outputs[0]

    def m(op, a, b=None, bv=None):
        n = N.new("ShaderNodeMath"); n.operation = op
        L.new(a, n.inputs[0]) if not isinstance(a, float) else None
        if isinstance(a, float):
            n.inputs[0].default_value = a
        if b is not None:
            L.new(b, n.inputs[1])
        if bv is not None:
            n.inputs[1].default_value = bv
        return n.outputs[0]

    world = vm("ADD", rot(vm("MULTIPLY", pos.outputs[0], me.outputs["Scale"]), me.outputs["Rotation"]),
               me.outputs["Location"])
    c = rot(vm("SUBTRACT", world, ci.outputs["Location"]), ci.outputs["Rotation"], inv=True)
    sep = N.new("ShaderNodeSeparateXYZ"); L.new(c, sep.inputs[0])
    depth = m("MAXIMUM", m("MULTIPLY", sep.outputs[2], bv=-1.0), bv=0.2)
    fov_h = 2 * _m.tan(cam.data.angle / 2) if cam else 1.0
    step = fov_h / (res_y / 2.0)            # one cell = 2 output pixels
    comb = N.new("ShaderNodeCombineXYZ")
    for i, out in ((0, sep.outputs[0]), (1, sep.outputs[1])):
        q = m("SNAP", m("DIVIDE", out, depth), bv=step)
        L.new(m("MULTIPLY", q, depth), comb.inputs[i])
    L.new(sep.outputs[2], comb.inputs[2])
    w2 = vm("ADD", rot(comb.outputs[0], ci.outputs["Rotation"]), ci.outputs["Location"])
    local = vm("DIVIDE", rot(vm("SUBTRACT", w2, me.outputs["Location"]), me.outputs["Rotation"], inv=True),
               me.outputs["Scale"])
    L.new(gi.outputs[0], setp.inputs["Geometry"])
    L.new(local, setp.inputs["Position"])
    L.new(setp.outputs[0], go.inputs[0])
    return ng


def _fog(s, start=35.0, depth=120.0):
    """Thick distance fog in the sky color + short draw distance (pop-in)."""
    col = tuple(s.get("world_color", (0.5, 0.7, 0.9)))
    s.world.mist_settings.start = start
    s.world.mist_settings.depth = depth
    s.world.mist_settings.falloff = "LINEAR"
    s.view_layers[0].use_pass_mist = True
    if s.camera:
        s.camera.data.clip_end = start + depth * 0.9
    s.use_nodes = True
    nt = s.node_tree
    nt.nodes.clear()
    rl = nt.nodes.new("CompositorNodeRLayers")
    mix = nt.nodes.new("CompositorNodeMixRGB")
    mix.inputs[2].default_value = (*col, 1)
    comp = nt.nodes.new("CompositorNodeComposite")
    nt.links.new(rl.outputs["Mist"], mix.inputs[0])
    nt.links.new(rl.outputs["Image"], mix.inputs[1])
    nt.links.new(mix.outputs[0], comp.inputs[0])


# ---------------------------------------------------------------- materials
_MATS = {}


def mat(name, color, emit=0.0, rough=1.0, metal=0.0, flat=SELF_LIT):
    """PS1-style material (cached by name): diffuse shading plus a share of
    self-lit color so faces never go muddy. emit>0 makes it glow."""
    if name in _MATS and _MATS[name].name in bpy.data.materials:
        return _MATS[name]
    color = look_color(color)
    if LOOK == "70s" and not emit:
        flat = flat * 0.55          # more real shading, less flat self-light
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.diffuse_color = (*color, 1)
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    add = nt.nodes.new("ShaderNodeAddShader")
    if metal:
        d = nt.nodes.new("ShaderNodeBsdfPrincipled")
        d.inputs["Base Color"].default_value = (*color, 1)
        d.inputs["Metallic"].default_value = metal
        d.inputs["Roughness"].default_value = rough
    else:
        d = nt.nodes.new("ShaderNodeBsdfDiffuse")
        d.inputs["Color"].default_value = (*color, 1)
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = (*color, 1)
    e.inputs["Strength"].default_value = emit if emit else flat
    nt.links.new(d.outputs[0], add.inputs[0])
    nt.links.new(e.outputs[0], add.inputs[1])
    nt.links.new(add.outputs[0], out.inputs[0])
    _MATS[name] = m
    return m


# ---------------------------------------------------------------- meshes
def link(obj, parent=None, coll=None):
    (coll or bpy.context.scene.collection).objects.link(obj)
    if parent is not None:
        obj.parent = parent
    return obj


def empty(name, loc=(0, 0, 0), parent=None, coll=None):
    o = bpy.data.objects.new(name, None)
    o.empty_display_size = 0.2
    o.location = loc
    return link(o, parent, coll)


def mesh_obj(name, verts, faces, mats, face_mat=None, loc=(0, 0, 0),
             parent=None, coll=None, mesh=None):
    """Build an object from raw verts/faces. face_mat: list of material
    indices per face. Pass `mesh` to make a linked duplicate instead."""
    if mesh is None:
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(verts, [], faces)
        for m in mats:
            mesh.materials.append(m)
        if face_mat:
            for p, i in zip(mesh.polygons, face_mat):
                p.material_index = i
        fix_normals(mesh)
    o = bpy.data.objects.new(name, mesh)
    o.location = loc
    return link(o, parent, coll)


def fix_normals(mesh):
    """Make every face point outward so flat shading lights correctly."""
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()


def box_data(sx, sy, sz, cx=0, cy=0, cz=0):
    hx, hy, hz = sx / 2, sy / 2, sz / 2
    v = [(cx + x * hx, cy + y * hy, cz + z * hz)
         for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    f = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1),
         (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    return v, f


def box(name, size, loc=(0, 0, 0), material=None, parent=None, coll=None,
        rot=(0, 0, 0)):
    v, f = box_data(*size)
    o = mesh_obj(name, v, f, [material] if material else [], loc=loc,
                 parent=parent, coll=coll)
    o.rotation_euler = [math.radians(a) for a in rot]
    return o


def cyl_data(r, depth, n=8, r2=None):
    """Cylinder (or cone/frustum with r2) along Z, centered at origin."""
    r2 = r if r2 is None else r2
    v, f = [], []
    for i in range(n):
        a = 2 * math.pi * i / n
        v.append((r * math.cos(a), r * math.sin(a), -depth / 2))
    for i in range(n):
        a = 2 * math.pi * i / n
        v.append((r2 * math.cos(a), r2 * math.sin(a), depth / 2))
    for i in range(n):
        j = (i + 1) % n
        f.append((i, j, n + j, n + i))
    f.append(tuple(reversed(range(n))))
    f.append(tuple(range(n, 2 * n)))
    return v, f


def cyl(name, r, depth, loc=(0, 0, 0), material=None, n=8, r2=None,
        rot=(0, 0, 0), parent=None, coll=None):
    v, f = cyl_data(r, depth, n, r2)
    if r2 == 0:  # proper cone: collapse top ring to one vertex
        v = v[:n] + [(0, 0, depth / 2)]
        f = [(i, (i + 1) % n, n) for i in range(n)] + [tuple(reversed(range(n)))]
    o = mesh_obj(name, v, f, [material] if material else [], loc=loc,
                 parent=parent, coll=coll)
    o.rotation_euler = [math.radians(a) for a in rot]
    return o


def ico(name, r, loc=(0, 0, 0), material=None, parent=None, coll=None, subdiv=1):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=r)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if material:
        me.materials.append(material)
    o = bpy.data.objects.new(name, me)
    o.location = loc
    return link(o, parent, coll)


def collection(name):
    c = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c


# ---------------------------------------------------------------- pixel art
def pixel_mat(name, rows, palette, flat=None):
    """MS-Paint-style texture from ASCII art. rows: list of equal-length
    strings (top row first); palette: char -> (r,g,b) or None (transparent)."""
    if name in _MATS and _MATS[name].name in bpy.data.materials:
        return _MATS[name]
    h, w = len(rows), len(rows[0])
    img = bpy.data.images.new(name, w, h, alpha=True)
    px = []
    for row in reversed(rows):
        for ch in row:
            c = palette.get(ch)
            px += [*c, 1.0] if c else [0, 0, 0, 0]
    img.pixels = px
    img.pack()
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.blend_method = "CLIP"
    m.shadow_method = "NONE"
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"
    d = nt.nodes.new("ShaderNodeBsdfDiffuse")
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Strength"].default_value = SELF_LIT if flat is None else flat
    add = nt.nodes.new("ShaderNodeAddShader")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(tex.outputs["Color"], d.inputs["Color"])
    nt.links.new(tex.outputs["Color"], e.inputs["Color"])
    nt.links.new(d.outputs[0], add.inputs[0])
    nt.links.new(e.outputs[0], add.inputs[1])
    nt.links.new(tex.outputs["Alpha"], mix.inputs[0])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(add.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    _MATS[name] = m
    return m


def decal(name, material, size, loc, rot=(90, 0, 0), parent=None, coll=None):
    """Flat textured quad (faces -Y by default) for pixel-art faces/signs."""
    sx, sz = size
    v = [(-sx / 2, -sz / 2, 0), (sx / 2, -sz / 2, 0), (sx / 2, sz / 2, 0), (-sx / 2, sz / 2, 0)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(v, [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new()
    for li, (u, w) in zip(range(4), [(0, 0), (1, 0), (1, 1), (0, 1)]):
        uv.data[li].uv = (u, w)
    me.materials.append(material)
    o = bpy.data.objects.new(name, me)
    o.location = loc
    o.rotation_euler = [math.radians(a) for a in rot]
    return link(o, parent, coll)


# ---------------------------------------------------------------- text / timing
BOLD_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def text(name, body, loc=(0, 0, 0), size=1.0, material=None, rot=(90, 0, 0),
         align="CENTER", extrude=0.0, parent=None, coll=None, bold=False):
    """3D text (Blender's built-in font, or the system's DejaVu Sans Bold).
    Faces -Y by default."""
    cu = bpy.data.curves.new(name, "FONT")
    if bold and os.path.exists(BOLD_FONT):
        cu.font = bpy.data.fonts.load(BOLD_FONT, check_existing=True)
    cu.body = body
    cu.size = size
    cu.align_x = align
    cu.align_y = "CENTER"
    cu.extrude = extrude
    if material:
        cu.materials.append(material)
    o = bpy.data.objects.new(name, cu)
    o.location = loc
    o.rotation_euler = [math.radians(a) for a in rot]
    o.visible_shadow = False            # labels must not cast ghost copies...
    if material is not None:            # ...EEVEE (legacy) only honors this one
        material.shadow_method = "NONE"
    return link(o, parent, coll)


def shot_seconds(shot, default):
    """Shot length: from the episode's timing.json (written by tools/assemble.py from the
    narration timestamps) when present, else the scene's default."""
    import json
    p = os.path.join(os.environ.get("JAWS_EPISODE_DIR", REPO), "timing.json")
    if os.path.exists(p):
        with open(p) as fh:
            data = json.load(fh)
        t = data.get(shot) or next((v for k, v in data.items() if k.startswith(shot + "_")), None)
        if t:
            return float(t)
    return float(default)


def fog(s, start, depth, color):
    """Distance fog in `color` (used for underwater shots at any jank level)."""
    s["world_color"] = list(color)
    _fog(s, start, depth)
