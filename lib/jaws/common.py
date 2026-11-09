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
AMBIENT = 0.25      # dim sky fill on objects
SELF_LIT = 0.40     # share of flat self-lit color in every material
PIXEL_SCALE = int(os.environ.get("JAWS_PIXEL_SCALE", "3"))  # 3 -> renders at 360x640
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


# ---------------------------------------------------------------- scene
def reset_scene(frames=1, world_color=(0.45, 0.72, 0.95)):
    bpy.ops.wm.read_factory_settings(use_empty=True)
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
    ee.taa_render_samples = 1                      # jaggies on purpose
    ee.use_soft_shadows = False
    ee.shadow_cube_size = "512"
    ee.shadow_cascade_size = "1024"
    ee.use_gtao = False
    ee.use_bloom = False
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
    d = bpy.data.lights.new("Sun", "SUN")
    d.energy = energy
    d.color = color
    d.angle = 0.0
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


# ---------------------------------------------------------------- materials
_MATS = {}


def mat(name, color, emit=0.0, rough=1.0, metal=0.0, flat=SELF_LIT):
    """PS1-style material (cached by name): diffuse shading plus a share of
    self-lit color so faces never go muddy. emit>0 makes it glow."""
    if name in _MATS and _MATS[name].name in bpy.data.materials:
        return _MATS[name]
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
