"""Shot 14: Jesse's lab. A shark lies on the table, Jesse waves the Geiger
counter over it... the needle pegs, CLICK CLICK CLICK, the shark glows
green, the warning light spins, Brody jumps back. Radioactive."""
import math, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import bpy
from jaws.common import (reset_scene, add_camera, key_camera, add_shake, render, FPS, shot_seconds,
                         box, cyl, mat, text)
from jaws.shark import make_shark, open_jaw
from jaws.people import make_brody, make_jesse
from jaws.props import make_rad_sign, make_geiger, needle_swing, make_beaker, blink
from jaws.town import pop_in

F = int(shot_seconds("shot14", 5.9) * FPS)
REV = int(F * 0.41)
reset_scene(F, world_color=(0.06, 0.07, 0.08))


def plight(name, loc, energy, color=(1, 0.95, 0.85), size=0.5):
    d = bpy.data.lights.new(name, "POINT")
    d.energy, d.color, d.shadow_soft_size = energy, color, size
    o = bpy.data.objects.new(name, d)
    o.location = loc
    bpy.context.scene.collection.objects.link(o)
    return d


plight("Lamp", (0, -1.5, 5.5), 350)
plight("Fill", (2, -9, 3), 300, (0.8, 0.85, 1.0), size=2)
box("Floor", (20, 14, 0.5), (0, 0, -0.25), mat("lab_floor", (0.55, 0.55, 0.52)))
box("BackWall", (20, 0.5, 8), (0, 4, 4), mat("lab_wall", (0.62, 0.68, 0.62)))
box("SideWall", (0.5, 14, 8), (-7, 0, 4), mat("lab_wall", (0.62, 0.68, 0.62)))
for x in range(-6, 7, 2):                            # tile line on the wall
    box(f"Tile{x}", (0.05, 0.05, 8), (x, 3.74, 4), mat("lab_tile", (0.5, 0.56, 0.5)))
cyl("Shade", 0.8, 0.6, (0, -1.5, 6.0), mat("lamp_shade", (0.2, 0.25, 0.22)), n=8, r2=0.3)
box("Table", (5.5, 2.4, 0.2), (0, 0, 1.6), mat("steel", (0.7, 0.72, 0.74), metal=0.6, rough=0.4))
for x in (-2.5, 2.5):
    for y in (-1, 1):
        box(f"Leg{x}{y}", (0.15, 0.15, 1.6), (x, y, 0.8), mat("steel", (0.7, 0.72, 0.74)))
gray = make_shark("Specimen", (0, 0, 2.15), rot_z=180, scale=2.2)
glow = make_shark("SpecimenRad", (0, 0, 2.15), rot_z=180, scale=2.2, variant="rad")
for o in gray.parts:
    o.keyframe_insert("hide_render", frame=REV - 1)
    o.hide_render = True
    o.keyframe_insert("hide_render", frame=REV)
for o in glow.parts:
    o.hide_render = True
    o.keyframe_insert("hide_render", frame=1)
    o.keyframe_insert("hide_render", frame=REV - 1)
    o.hide_render = False
    o.keyframe_insert("hide_render", frame=REV)
for sh in (gray, glow):
    open_jaw(sh, 1, 0.3)
g = plight("RadLight", (0, -0.8, 3.2), 0, (0.45, 1.0, 0.3), size=1.0)
g.keyframe_insert("energy", frame=REV - 1)
for f in range(REV, F + 1, 3):
    g.energy = 500 + 150 * math.sin(f)
    g.keyframe_insert("energy", frame=f)
make_rad_sign("Sign", (-3.5, 3.72, 5.0), size=0.9)
for i, (x, c) in enumerate([(4.6, (0.4, 1.0, 0.3)), (5.1, (0.3, 0.6, 1.0)), (5.6, (1.0, 0.5, 0.2))]):
    make_beaker(f"Beaker{i}", (x, 2.8, 1.8), color=c)
box("Bench", (3.0, 1.4, 0.2), (5.0, 2.9, 1.7), mat("steel", (0.7, 0.72, 0.74)))
# spinning warning light on the wall
wl = cyl("WarnBase", 0.3, 0.2, (2.0, 3.6, 6.4), mat("warn_base", (0.2, 0.2, 0.2)), n=8, rot=(90, 0, 0))
wr = cyl("WarnLamp", 0.35, 0.5, (2.0, 3.4, 6.4), mat("warn_red", (1.0, 0.1, 0.05), emit=5.0), n=8, rot=(90, 0, 0))
blink(wr, REV, F, period=8, on=4)
wd = plight("WarnLight", (2.0, 3.0, 6.4), 0, (1.0, 0.15, 0.1), size=0.3)
for f in range(REV, F + 1, 4):
    wd.energy = 400 if (f // 4) % 2 == 0 else 0
    wd.keyframe_insert("energy", frame=f)
    wd.keyframe_insert("energy", frame=f + 3)

j = make_jesse("Jesse", loc=(1.2, -2.0, 0), rot_z=20)
gc, needle, wand = make_geiger()
gc.parent = j.arm_l
gc.location = (0, -0.05, -0.85)
gc.rotation_euler = (math.radians(90), 0, 0)
j.arm_l.rotation_euler[0] = math.radians(-70)
j.arm_r.rotation_euler = (math.radians(-60), 0, 0)
for f in range(1, REV, 8):                           # sweeping the wand over the shark
    j.arm_r.rotation_euler[2] = math.radians(-20 if (f // 8) % 2 else 15)
    j.arm_r.keyframe_insert("rotation_euler", frame=f)
needle_swing(needle, REV - 2, F)
b = make_brody("Brody", loc=(-2.0, -2.4, 0), rot_z=-15)
b.root.keyframe_insert("location", frame=REV + 2)
b.root.location = (-2.3, -2.9, 0.35)
b.root.keyframe_insert("location", frame=REV + 6)
b.root.location.z = 0
b.root.keyframe_insert("location", frame=REV + 10)
for arm in (b.arm_l, b.arm_r):
    arm.keyframe_insert("rotation_euler", frame=REV + 2)
    arm.rotation_euler[0] = math.radians(-150)
    arm.keyframe_insert("rotation_euler", frame=REV + 6)
rnd = random.Random(14)
ink = mat("click_yellow", (1.0, 0.95, 0.3), emit=1.5)
for k in range(7):
    t = text(f"Click{k}", "CLICK", (rnd.uniform(-1.5, 3.5), -2.6, rnd.uniform(3.6, 5.6)), 0.55, ink, bold=True,
             rot=(90, 0, rnd.uniform(-20, 20)))
    pop_in(t, REV + k * 6, out_frame=REV + k * 6 + 14)
big = text("RadWord", "RADIOACTIVE!", (0, -2.2, 6.6), 0.9, mat("rad_word", (0.5, 1.0, 0.3), emit=2.0),
           extrude=0.1, bold=True)
pop_in(big, REV + 8)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (-0.8, -11.5, 4.0), (0, 0, 3.0))
key_camera(cam, REV, (-0.6, -9.8, 3.9), (0, 0, 3.0))
key_camera(cam, F, (-0.5, -11.5, 4.3), (0, 0, 3.8))
add_shake(cam, REV, REV + 14, strength=0.2, rot_strength=0.02)
render(os.environ.get("JAWS_OUT", "renders/shot14_tests"))
