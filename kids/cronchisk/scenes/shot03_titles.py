"""Shot 03: title sequence. Black, the Cronchisk spinning, laser sweeps, agent silhouettes, OPERATION CRONCHISK."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S
import bpy

F = int(shot_seconds("shot03_titles", 5.0) * FPS)
from jaws.common import reset_scene
sc = reset_scene(F, world_color=(0.0, 0.0, 0.0))
O.dark_room(sc, ambient=0.02)
HIT = int(F * 0.38)
box("Floor", (40, 40, 0.2), (0, 4, -0.1), mat("title_floor", (0.03, 0.02, 0.04), rough=0.15, metal=0.5))
gem = O.make_cronchisk("Gem", (0, 0, 3.0), size=1.2, light=900)
for f, z in ((1, 2.6), (F, 3.2)):
    gem.location.z = z
    gem.keyframe_insert("location", index=2, frame=f)
gem.rotation_euler[2] = 0
gem.keyframe_insert("rotation_euler", index=2, frame=1)
gem.rotation_euler[2] = 4 * math.pi
gem.keyframe_insert("rotation_euler", index=2, frame=F)
for fc in gem.animation_data.action.fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = "LINEAR"
black = mat("silhouette", (0.01, 0.01, 0.015), flat=0.0)
heroes = [A.make_banana("SilB", (-2.0, 1.2, 0), rot_z=-20), A.make_cherry("SilC", (2.0, 1.2, 0), rot_z=20)]
for p in heroes:
    for o in p.root.children_recursive:
        if o.type == "MESH":
            o.data.materials.clear()
            o.data.materials.append(black)
    A.arm(p, "r", 20, -60, frames=10)
for s in (-1, 1):
    O.spot_light(f"Rim{s}", (s * 4, 5, 6), (s * 2, 1.2, 1.5), 3000, O.PINK, angle=40)
# laser sweeps: thin glowing bars rotating across the frame
for k in range(4):
    las = box(f"Laser{k}", (30, 0.03, 0.03), (0, 3 + k * 0.3, 1.5 + k * 1.3), mat(f"laser{k}", [(1, 0.1, 0.4), (1, 0.6, 0.9)][k % 2], emit=8.0))
    las.visible_shadow = False
    for f, a in ((1, -30 + k * 20), (F, 30 - k * 25)):
        las.rotation_euler[1] = math.radians(a)
        las.keyframe_insert("rotation_euler", index=1, frame=f)
pink = mat("title_pink", O.PINK, emit=2.5)
white = mat("title_white", (1, 1, 1), emit=1.5)
t1 = text("T_op", "OPERATION", (0, -1.5, 6.4), 0.72, white, extrude=0.08, bold=True)
t2 = text("T_cr", "CRONCHISK", (0, -1.5, 5.3), 1.0, pink, extrude=0.18, bold=True)
O.show_at(t1, HIT - 8)
for o, f in ((t2, HIT),):
    for df, k in ((-1, 0.001), (0, 0.001), (3, 1.25), (6, 1.0)):
        o.scale = (k,) * 3
        o.keyframe_insert("scale", frame=f + df)
flash = O.point_light("Flash", (0, -3, 5), 0, (1, 0.6, 0.9), radius=2, shadow=False)
for f, e in ((HIT - 1, 0), (HIT, 6000), (HIT + 10, 0)):
    flash.data.energy = e
    flash.data.keyframe_insert("energy", frame=f)
cam = add_camera((0, -12, 3.5), (0, 0, 3.5), lens=35)
key_camera(cam, 1, (0, -13, 3.0), (0, 0, 3.6))
key_camera(cam, F, (0, -11, 3.4), (0, 0, 3.9))
add_shake(cam, HIT, HIT + 8, strength=0.2, rot_strength=0.015)
render(os.environ.get("JAWS_OUT", "renders/shot03_titles"))
