"""Operation Cronchisk: blocky spy-thriller versions of the Jelly Man cast.

Every character is a people._build rig (p.root/torso/head/arm_l/arm_r/leg_l/
leg_r, faces -Y, root at the feet) plus the signature shape and color of the
kid's drawing: banana head, cherry head with a stem, carrot cone with
leaves, see-through purple jelly.

    j = make_jelly("Jelly", loc=(0, 0, 0))
    b = make_banana(...); c = make_cherry(...); make_meanie(..., seed=i)
    walk(p, f0, f1) / run(p, f0, f1) / arm(p, "r", f, deg) / look(p, f, deg)
    hold(p, obj, side="r")   # parent a prop to the hand
"""
import math
import random

import bpy

from .common import box, cyl, ico, empty, mat
from .people import _build, walk, point, _rot_key

__all__ = ["add_arms", "make_jelly", "make_banana", "make_twin", "make_blip", "make_cherry", "make_meanie",
           "make_pocket", "make_carrot", "make_director", "make_someone", "make_dark_cherry",
           "walk", "point", "run", "arm", "arms_up", "look", "lean", "hold", "wobble", "glass",
           "hand_pos", "bounce", "turn"]

SKIN = (0.95, 0.76, 0.62)


def _rig(name, colors, loc, rot_z, coll, **dims):
    c = dict(leg_len=0.85, leg_w=0.22, torso=(0.62, 0.36, 0.70), arm_len=0.66, arm_w=0.17,
             head=(0.38, 0.36, 0.42))
    c.update(dims)
    base = dict(shirt=(0.5, 0.5, 0.5), pants=(0.1, 0.1, 0.12), shoes=(0.03, 0.03, 0.03), skin=SKIN,
                nose=SKIN, hair=(0.1, 0.07, 0.05), eyes=(0.02, 0.02, 0.02), belt=(0.06, 0.05, 0.05))
    base.update(colors)
    c["colors"] = base
    if "sleeve" in dims:
        c["sleeve"] = dims["sleeve"]
    return _build(name, c, loc, rot_z, coll)


def _drop(P, *parts):
    """Remove default rig parts (e.g. the box head under a round cherry head)."""
    for p in parts:
        o = bpy.data.objects.get(f"{P.name}_{p}")
        if o:
            bpy.data.objects.remove(o, do_unlink=True)


def glass(name, color, alpha=0.55, emit=0.8):
    """See-through glowing material (jelly, force fields, visors)."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = (*color, 1)
    e.inputs["Strength"].default_value = emit
    d = nt.nodes.new("ShaderNodeBsdfDiffuse")
    d.inputs["Color"].default_value = (*color, 1)
    add = nt.nodes.new("ShaderNodeAddShader")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    mix.inputs[0].default_value = alpha
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(d.outputs[0], add.inputs[0])
    nt.links.new(e.outputs[0], add.inputs[1])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(add.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    m.blend_method = "BLEND"
    m.shadow_method = "HASHED"
    m.show_transparent_back = False
    return m


def _eyes(P, parent, y, z, spread, size=0.07, color="eyes"):
    for s in (-1, 1):
        P.b(f"eyeR{s}", (size, 0.03, size * 1.1), (s * spread, y, z), color, parent)


# ---------------------------------------------------------------- the cast
def make_jelly(name="Jelly", loc=(0, 0, 0), rot_z=0.0, coll=None):
    """JELLY, arms dealer: a wobbling see-through purple jelly with a dome
    head (like the drawing), tiny black sunglasses and a bow tie.
    p.body is the torso pivot to wobble; things parented inside show through."""
    purple = (0.62, 0.25, 0.85)
    P = _rig(name, dict(shirt=purple, pants=purple, skin=purple, shoes=(0.45, 0.15, 0.62), belt=purple,
                        nose=purple, hair=purple, bow=(0.03, 0.03, 0.03), shade=(0.02, 0.02, 0.03),
                        lens=(0.25, 0.05, 0.35), tooth=(1, 1, 1)),
             loc, rot_z, coll, leg_len=0.42, leg_w=0.26, torso=(1.15, 0.85, 1.05), arm_len=0.75, arm_w=0.24,
             head=(0.9, 0.8, 0.5))
    _drop(P, "belt", "neck", "nose", "brow-1", "brow1", "eye-1", "eye1")
    jel = glass(f"{name}_jelly", purple, alpha=0.5, emit=0.75)
    for o in list(P.root.children_recursive):
        if o.type == "MESH" and o.data.materials and o.data.materials[0].name.startswith(f"{name}_") \
                and o.data.materials[0].name.split("_")[-1] in ("shirt", "pants", "skin"):
            o.data.materials[0] = jel
    h, t = P.head, P.torso
    dome = ico(f"{name}_dome", 0.62, (0, 0, 0.38), jel, parent=h, coll=coll, subdiv=2)
    dome.scale = (1.0, 0.85, 0.75)
    for k in range(5):                                   # wavy skirt rim, as drawn
        a = k / 5 * 2 * math.pi
        ico(f"{name}_wave{k}", 0.24, (0.55 * math.cos(a), 0.4 * math.sin(a), 0.05), jel, parent=t, coll=coll)
    P.b("shades", (0.62, 0.05, 0.1), (0, -0.52, 0.42), "shade", h)
    for s in (-1, 1):
        P.b(f"lens{s}", (0.24, 0.06, 0.15), (s * 0.17, -0.53, 0.38), "lens", h)
    P.b("grin", (0.32, 0.04, 0.05), (0, -0.48, 0.14), "tooth", h)
    P.b("bow_c", (0.1, 0.06, 0.1), (0, -0.45, 0.98), "bow", t)
    for s in (-1, 1):
        P.b(f"bow{s}", (0.16, 0.05, 0.14), (s * 0.12, -0.45, 0.98), "bow", t)
    P.body = t
    return P


def make_banana(name="Banana", loc=(0, 0, 0), rot_z=0.0, coll=None):
    """AGENT BANANA: tall curved yellow banana head (stem poking out of the
    fedora), tan trench coat, belt, dark trousers."""
    P = _rig(name, dict(skin=(1.0, 0.86, 0.15), nose=(1.0, 0.86, 0.15), shirt=(0.72, 0.58, 0.36),
                        pants=(0.22, 0.2, 0.18), belt=(0.38, 0.27, 0.15), hair=(0.4, 0.3, 0.05),
                        hat=(0.22, 0.17, 0.12), band=(0.08, 0.06, 0.05), stem=(0.35, 0.25, 0.08),
                        coat=(0.66, 0.52, 0.31), tip=(0.35, 0.25, 0.08)),
             loc, rot_z, coll, head=(0.34, 0.32, 0.72), torso=(0.62, 0.38, 0.74))
    _drop(P, "nose")
    h, t = P.head, P.torso
    P.b("curve_lo", (0.30, 0.30, 0.22), (0, -0.07, -0.02), "skin", h)     # the banana bends forward
    P.b("tip", (0.12, 0.12, 0.08), (0, 0.02, -0.08), "tip", h)
    P.b("brim", (0.68, 0.62, 0.05), (0, 0, 0.66), "hat", h)
    P.b("crown", (0.42, 0.38, 0.22), (0, 0.01, 0.78), "hat", h)
    P.b("band", (0.43, 0.39, 0.06), (0, 0.01, 0.70), "band", h)
    P.b("stem", (0.1, 0.1, 0.22), (0, 0.04, 0.96), "stem", h)
    for s in (-1, 1):                                    # trench coat flaps + lapels
        P.b(f"flap{s}", (0.3, 0.05, 0.62), (s * 0.16, -0.2, -0.05), "coat", t)
        P.b(f"lapel{s}", (0.1, 0.04, 0.3), (s * 0.12, -0.22, 0.56), "band", t)
    return P


def make_twin(name="Twin", loc=(0, 0, 0), rot_z=0.0, coll=None, seed=0):
    """THE TWINS: green space aliens in matching black suits, antennae with
    glowing tips, big black eyes."""
    P = _rig(name, dict(skin=(0.45, 0.88, 0.32), nose=(0.45, 0.88, 0.32), shirt=(0.05, 0.05, 0.06),
                        pants=(0.05, 0.05, 0.06), collar=(0.95, 0.95, 0.95), tie=(0.02, 0.02, 0.02),
                        bulb=(0.7, 1.0, 0.4)), loc, rot_z, coll,
             head=(0.46, 0.4, 0.4), torso=(0.58, 0.34, 0.72), leg_len=0.9)
    _drop(P, "nose", "brow-1", "brow1", "eye-1", "eye1")
    h, t = P.head, P.torso
    for s in (-1, 1):
        P.b(f"bigeye{s}", (0.13, 0.03, 0.16), (s * 0.11, -0.21, 0.24), "eyes", h)
        P.b(f"ant{s}", (0.04, 0.04, 0.34), (s * 0.12, 0, 0.55), "skin", h).rotation_euler[1] = math.radians(s * 18)
        ico(f"{name}_bulb{s}", 0.07, (s * 0.18, 0, 0.73), mat(f"{name}_bulbm", (0.7, 1.0, 0.4), emit=3.0),
            parent=h, coll=coll)
    P.b("collar", (0.22, 0.03, 0.24), (0, -0.18, 0.58), "collar", t)
    P.b("tie", (0.07, 0.04, 0.4), (0, -0.2, 0.42), "tie", t)
    return P


def make_blip(name="Blip", loc=(0, 0, 0), rot_z=0.0, coll=None):
    """DR. BLIP, the scientist: pale blue skin (as drawn), long white lab
    coat, goggles pushed up, wild white hair."""
    P = _rig(name, dict(skin=(0.6, 0.88, 1.0), nose=(0.5, 0.8, 0.95), shirt=(0.95, 0.95, 0.95),
                        pants=(0.3, 0.32, 0.4), hair=(0.97, 0.97, 0.97), goggle=(0.25, 0.25, 0.3),
                        lensg=(0.6, 0.9, 1.0), pen=(0.1, 0.3, 0.9)), loc, rot_z, coll)
    h, t = P.head, P.torso
    P.b("coat_l", (0.64, 0.4, 0.38), (0, 0, -0.18), "shirt", t)
    for k, (x, z) in enumerate(((-0.14, 0.46), (0.0, 0.5), (0.14, 0.46), (-0.2, 0.36), (0.2, 0.36))):
        P.b(f"tuft{k}", (0.14, 0.3, 0.14), (x, 0.03, z), "hair", h)
    P.b("goggle", (0.42, 0.06, 0.08), (0, -0.18, 0.39), "goggle", h)
    for s in (-1, 1):
        P.b(f"glens{s}", (0.12, 0.06, 0.1), (s * 0.09, -0.21, 0.39), "lensg", h)
    P.b("pen", (0.03, 0.03, 0.14), (0.16, -0.2, 0.55), "pen", t)
    return P


def _cherry_head(P, color, coll, r=0.34):
    h = P.head
    _drop(P, "headbox", "nose", "brow-1", "brow1", "eye-1", "eye1")
    c = ico(f"{P.name}_cherry", r, (0, 0, r * 0.9), mat(f"{P.name}_cherrym", color, rough=0.4), parent=h,
            coll=coll, subdiv=2)
    for poly in c.data.polygons:
        poly.use_smooth = True
    ico(f"{P.name}_shine", r * 0.18, (-r * 0.45, -r * 0.75, r * 1.3), mat("cherry_shine", (1, 1, 1), emit=1.5),
        parent=h, coll=coll)
    stem = mat("cherry_stem", (0.25, 0.55, 0.15))
    s = cyl(f"{P.name}_stem", 0.03, 0.42, (0.06, 0, r * 1.95), stem, n=5, parent=h, coll=coll)
    s.rotation_euler[1] = math.radians(18)
    leaf = box(f"{P.name}_leaf", (0.2, 0.03, 0.09), (0.16, 0, r * 2.05), mat("cherry_leaf", (0.3, 0.7, 0.2)),
               parent=h, coll=coll)
    leaf.rotation_euler[1] = math.radians(-25)
    return c


def make_cherry(name="Cherry", loc=(0, 0, 0), rot_z=0.0, coll=None):
    """AGENT CHERRY: round shiny red cherry head with a stem and leaf, olive
    tactical vest, black cargo trousers, boots."""
    P = _rig(name, dict(skin=(0.95, 0.75, 0.6), shirt=(0.12, 0.12, 0.14), pants=(0.1, 0.1, 0.12),
                        vest=(0.38, 0.42, 0.22), pouch=(0.3, 0.33, 0.17), white=(1, 1, 1),
                        mouth=(0.35, 0.02, 0.05)), loc, rot_z, coll,
             torso=(0.56, 0.34, 0.68), leg_len=0.88)
    _cherry_head(P, (0.9, 0.06, 0.12), coll)
    h, t = P.head, P.torso
    for s in (-1, 1):
        P.b(f"ceye{s}", (0.07, 0.03, 0.09), (s * 0.11, -0.33, 0.36), "eyes", h)
        P.b(f"cbrow{s}", (0.11, 0.03, 0.03), (s * 0.11, -0.33, 0.46), "eyes", h).rotation_euler[1] = \
            math.radians(-s * 15)
    P.b("cmouth", (0.12, 0.03, 0.03), (0, -0.33, 0.2), "mouth", h)
    P.b("vest", (0.6, 0.4, 0.5), (0, 0, 0.38), "vest", t)
    for s in (-1, 1):
        P.b(f"pouch{s}", (0.14, 0.06, 0.14), (s * 0.15, -0.21, 0.3), "pouch", t)
    return P


def make_dark_cherry(name="DarkCherry", loc=(0, 0, 0), rot_z=0.0, coll=None):
    """DARK CHERRY: the rogue ex-agent. Dark red cherry head, black
    turtleneck, black shades, a scar-like stem."""
    P = _rig(name, dict(skin=(0.9, 0.72, 0.6), shirt=(0.04, 0.04, 0.05), pants=(0.05, 0.05, 0.06),
                        shade=(0.01, 0.01, 0.01), mouth=(0.2, 0.0, 0.03)), loc, rot_z, coll,
             torso=(0.6, 0.36, 0.72), leg_len=0.9)
    _cherry_head(P, (0.42, 0.02, 0.1), coll)
    h, t = P.head, P.torso
    P.b("dshades", (0.42, 0.05, 0.09), (0, -0.33, 0.36), "shade", h)
    P.b("dmouth", (0.12, 0.03, 0.03), (0.02, -0.33, 0.2), "mouth", h)
    P.b("neck_roll", (0.3, 0.3, 0.12), (0, 0, 0.72), "shirt", t)
    return P


def make_meanie(name="Meanie", loc=(0, 0, 0), rot_z=0.0, coll=None, seed=0):
    """MEANIES: identical purple henchmen, black jumpsuits, helmets with a
    glowing red visor."""
    P = _rig(name, dict(skin=(0.5, 0.3, 0.72), nose=(0.5, 0.3, 0.72), shirt=(0.08, 0.08, 0.1),
                        pants=(0.08, 0.08, 0.1), helm=(0.12, 0.12, 0.14), belt=(0.5, 0.3, 0.72),
                        badge=(0.95, 0.75, 0.1)), loc, rot_z, coll,
             head=(0.4, 0.38, 0.38), torso=(0.6, 0.36, 0.66))
    _drop(P, "eye-1", "eye1", "brow-1", "brow1")
    h, t = P.head, P.torso
    P.b("helm", (0.46, 0.44, 0.18), (0, 0.01, 0.38), "helm", h)
    P.b("visor", (0.42, 0.05, 0.1), (0, -0.2, 0.24), "helm", h)
    box(f"{name}_visorglow", (0.36, 0.03, 0.05), (0, -0.23, 0.24), mat("meanie_visor", (1.0, 0.08, 0.05), emit=4.0),
        parent=h, coll=coll)
    P.b("badge", (0.1, 0.03, 0.1), (0.16, -0.19, 0.52), "badge", t)
    return P


def make_pocket(name="Pocket", loc=(0, 0, 0), rot_z=0.0, coll=None):
    """POCKET, Dr. Blip's kid: small, big head, yellow t-shirt, backpack."""
    P = _rig(name, dict(shirt=(1.0, 0.82, 0.2), pants=(0.25, 0.4, 0.75), shoes=(0.9, 0.2, 0.2),
                        hair=(0.35, 0.2, 0.1), pack=(0.2, 0.65, 0.35), mouth=(0.6, 0.1, 0.1)), loc, rot_z, coll,
             leg_len=0.42, leg_w=0.16, torso=(0.42, 0.28, 0.42), arm_len=0.42, arm_w=0.13, head=(0.4, 0.38, 0.4))
    h, t = P.head, P.torso
    P.b("hair", (0.43, 0.41, 0.12), (0, 0.01, 0.42), "hair", h)
    P.b("pack", (0.34, 0.16, 0.36), (0, 0.22, 0.22), "pack", t)
    P.b("mouth", (0.1, 0.03, 0.04), (0, -0.2, 0.12), "mouth", h)
    return P


def make_carrot(name="Carrot", loc=(0, 0, 0), rot_z=0.0, coll=None, disguise=False):
    """CARROT, double agent: a tall orange carrot body (cone, ridges) with a
    face, bushy green leaves on top, little arms and legs. disguise=True adds
    a Meanie helmet with a red visor (p.disguise, to pop off later)."""
    orange, dark = (1.0, 0.5, 0.08), (0.8, 0.36, 0.04)
    P = _rig(name, dict(skin=orange, nose=orange, shirt=orange, pants=orange, shoes=dark, belt=orange,
                        hair=dark, ridge=dark, leaf=(0.25, 0.7, 0.2), leaf2=(0.18, 0.55, 0.15),
                        mouth=(0.4, 0.1, 0.02), helm=(0.12, 0.12, 0.14)), loc, rot_z, coll,
             leg_len=0.5, leg_w=0.16, torso=(0.5, 0.42, 0.5), arm_len=0.55, arm_w=0.13, head=(0.56, 0.5, 0.5))
    _drop(P, "neck", "brow-1", "brow1")
    h, t = P.head, P.torso
    cone = cyl(f"{name}_cone", 0.36, 1.05, (0, 0, 0.32), mat(f"{name}_orange", orange), n=8, r2=0.1,
               parent=t, coll=coll)
    cone.rotation_euler[0] = math.pi
    for k, z in enumerate((0.15, 0.35, 0.55)):
        P.b(f"ridge{k}", (0.3 - k * 0.07, 0.04, 0.03), (0.04, -0.27 + k * 0.05, z), "ridge", t)
    for k, (x, ang, col) in enumerate(((-0.12, -25, "leaf"), (0, 0, "leaf2"), (0.12, 25, "leaf"),
                                      (-0.06, -10, "leaf2"), (0.06, 12, "leaf2"))):
        lf = P.b(f"leaf{k}", (0.1, 0.08, 0.5), (x, 0, 0.72), col, h)
        lf.rotation_euler[1] = math.radians(ang)
    P.b("cmouth", (0.16, 0.03, 0.04), (0, -0.26, 0.14), "mouth", h)
    P.disguise = None
    if disguise:
        d = empty(f"{name}_disguise", (0, 0, 0), parent=h, coll=coll)
        box(f"{name}_dhelm", (0.62, 0.56, 0.26), (0, 0.01, 0.48), mat(f"{name}_helm", (0.12, 0.12, 0.14)),
            parent=d, coll=coll)
        box(f"{name}_dvisor", (0.5, 0.04, 0.07), (0, -0.28, 0.3), mat("meanie_visor", (1.0, 0.08, 0.05), emit=4.0),
            parent=d, coll=coll)
        P.disguise = d
    return P


def make_director(name="Director", loc=(0, 0, 0), rot_z=0.0, coll=None):
    """DIRECTOR C, the agency boss: blue (Cool Man), grey three-piece suit,
    eyepatch, silver hair."""
    P = _rig(name, dict(skin=(0.35, 0.62, 1.0), nose=(0.3, 0.55, 0.95), shirt=(0.36, 0.37, 0.4),
                        pants=(0.36, 0.37, 0.4), hair=(0.85, 0.85, 0.88), patch=(0.02, 0.02, 0.02),
                        collar=(0.95, 0.95, 0.95), tie=(0.6, 0.08, 0.1)), loc, rot_z, coll,
             torso=(0.7, 0.42, 0.74))
    h, t = P.head, P.torso
    P.b("hair", (0.41, 0.39, 0.08), (0, 0.01, 0.45), "hair", h)
    P.b("patch", (0.11, 0.04, 0.1), (0.09, -0.19, 0.27), "patch", h)
    P.b("strap", (0.4, 0.03, 0.03), (0, -0.19, 0.31), "patch", h).rotation_euler[1] = math.radians(-12)
    P.b("collar", (0.24, 0.03, 0.22), (0, -0.21, 0.6), "collar", t)
    P.b("tie", (0.07, 0.04, 0.38), (0, -0.23, 0.44), "tie", t)
    return P


def make_someone(name="Someone", loc=(0, 0, 0), rot_z=0.0, coll=None):
    """SOMEONE, the mastermind: big round orange head (as drawn), long black
    coat with a high collar, gold monocle."""
    P = _rig(name, dict(skin=(1.0, 0.62, 0.25), nose=(0.95, 0.55, 0.2), shirt=(0.05, 0.04, 0.06),
                        pants=(0.05, 0.04, 0.06), gold=(1.0, 0.8, 0.2), lining=(0.6, 0.05, 0.08),
                        mouth=(0.35, 0.08, 0.02)), loc, rot_z, coll,
             torso=(0.7, 0.42, 0.8))
    _drop(P, "headbox", "nose", "brow-1", "brow1", "eye-1", "eye1")
    h, t = P.head, P.torso
    head = ico(f"{name}_ball", 0.36, (0, 0, 0.34), mat(f"{name}_skinball", (1.0, 0.62, 0.25)), parent=h,
               coll=coll, subdiv=2)
    head.scale = (1.1, 1.0, 0.95)
    for s in (-1, 1):
        P.b(f"seye{s}", (0.08, 0.03, 0.06), (s * 0.13, -0.35, 0.4), "eyes", h)
        P.b(f"sbrow{s}", (0.13, 0.03, 0.03), (s * 0.13, -0.35, 0.49), "eyes", h).rotation_euler[1] = \
            math.radians(s * 20)
    P.b("smouth", (0.2, 0.03, 0.03), (0, -0.35, 0.2), "mouth", h)
    mono = cyl(f"{name}_monocle", 0.08, 0.02, (0.13, -0.38, 0.4), mat(f"{name}_goldm", (1.0, 0.8, 0.2), metal=0.8,
               rough=0.3), n=10, parent=h, coll=coll)
    mono.rotation_euler[0] = math.pi / 2
    P.b("coat", (0.74, 0.46, 0.6), (0, 0, -0.25), "shirt", t)
    P.b("hicollar", (0.8, 0.46, 0.26), (0, 0.04, 0.8), "lining", t)
    return P


def add_arms(P, drop=0.3, sleeve="shirt", coll=None, color=None):
    """Bolt on a second pair of arms just below the first (bought from Jelly,
    the arms dealer). Returns an object with .arm_l/.arm_r, so arm(), arms_up()
    work on it: arm(add_arms(p), "r", f, -90). color: sleeve color of the new arms."""
    class Extra:
        pass
    E = Extra()
    TW, TH = P.c["torso"][0], P.c["torso"][2]
    AL, AW = P.c["arm_len"], P.c["arm_w"]
    for side, attr in ((1, "arm_l"), (-1, "arm_r")):
        piv = empty(f"{P.name}_x{attr}", (side * (TW / 2 + AW / 2), 0, TH - 0.06 - drop), P.torso, coll)
        sm = mat(f"xarm_{color}", color) if color else P.mats[sleeve]
        box(f"{P.name}_x{attr}_m", (AW, AW * 1.1, AL), (0, 0, -AL / 2 + AW / 2), sm, parent=piv, coll=coll)
        box(f"{P.name}_x{attr}_hand", (AW * 0.9, AW * 0.9, 0.14), (0, 0, -AL + AW / 2 - 0.05), P.mats["skin"],
            parent=piv, coll=coll)
        piv.rotation_euler[1] = math.radians(side * 25)
        setattr(E, attr, piv)
    E.torso = P.torso
    return E


# ---------------------------------------------------------------- moves
def run(p, start, end, period=8, swing=55):
    """Fast run: big limb swings, leaning forward."""
    walk(p, start, end, period=period, swing=swing)
    lean(p, start, 14, frames=4)
    lean(p, end, 0, frames=4)


def lean(p, f, deg, frames=6):
    p.torso.keyframe_insert("rotation_euler", index=0, frame=max(1, f - frames))
    _rot_key(p.torso, 0, -deg, f)


def arm(p, side, f, deg, frames=5, roll=0):
    """Swing an arm on X (negative = forward/up) to deg at frame f."""
    a = p.arm_r if side == "r" else p.arm_l
    a.keyframe_insert("rotation_euler", index=0, frame=max(1, f - frames))
    a.keyframe_insert("rotation_euler", index=1, frame=max(1, f - frames))
    _rot_key(a, 0, deg, f)
    _rot_key(a, 1, roll, f)


def arms_up(p, f, frames=5, deg=-170):
    arm(p, "l", f, deg, frames, roll=-15)
    arm(p, "r", f, deg, frames, roll=15)


def look(p, f, deg, frames=6, tilt=0):
    """Turn the head (deg about Z, + = to the character's left)."""
    p.head.keyframe_insert("rotation_euler", frame=max(1, f - frames))
    p.head.rotation_euler[2] = math.radians(deg)
    p.head.rotation_euler[0] = math.radians(tilt)
    p.head.keyframe_insert("rotation_euler", frame=f)


def turn(p, f, deg, frames=8):
    """Turn the whole body to face deg (root Z)."""
    p.root.keyframe_insert("rotation_euler", index=2, frame=max(1, f - frames))
    p.root.rotation_euler[2] = math.radians(deg)
    p.root.keyframe_insert("rotation_euler", index=2, frame=f)


def hand_pos(p, side="r"):
    a = p.arm_r if side == "r" else p.arm_l
    return a, (0, -0.05, -p.c["arm_len"] + p.c["arm_w"] / 2 - 0.12)


def hold(p, obj, side="r", offset=(0, 0, 0), rot=(0, 0, 0)):
    """Put a prop in a hand (parented, so it follows arm swings)."""
    a, (x, y, z) = hand_pos(p, side)
    obj.parent = a
    obj.location = (x + offset[0], y + offset[1], z + offset[2])
    obj.rotation_euler = [math.radians(r) for r in rot]
    return obj


def wobble(p, f0, f1, amp=0.08, period=10, seed=0):
    """Jelly wobble: the body squashes and stretches, the head lags behind."""
    rnd = random.Random(seed)
    ph = rnd.uniform(0, 6)
    for f in range(f0, f1 + 1, 2):
        s = math.sin(2 * math.pi * f / period + ph)
        p.body.scale = (1 + amp * s, 1 + amp * s * 0.5, 1 - amp * s)
        p.body.keyframe_insert("scale", frame=f)
        p.head.rotation_euler[1] = math.radians(6 * math.sin(2 * math.pi * f / period + ph - 1.2))
        p.head.keyframe_insert("rotation_euler", index=1, frame=f)


def bounce(p, f0, f1, amp=0.05, period=16):
    """Idle bounce on the toes (keeps blocky people alive while they talk)."""
    z0 = p.root.location.z
    for f in range(f0, f1 + 1, 2):
        p.root.location.z = z0 + amp * abs(math.sin(math.pi * f / period))
        p.root.keyframe_insert("location", index=2, frame=f)
