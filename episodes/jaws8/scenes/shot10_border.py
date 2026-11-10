"""Shot 10: "...out the back of a truck across the border to Finland onto a
plane home." Snowy forest road: the truck smashes through the USSR/Finland
boom gate (it flips up). Cut: a four-prop plane lifts off, headed home."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import reset_scene, add_sun, add_camera, key_camera, add_shake, linear_keys, render, FPS, \
    shot_seconds, box, mat
from jaws.soviet import make_truck, make_border_gate, make_plane, spin
from _snow import snowfall, pines

F = int(shot_seconds("shot10", 4.1) * FPS)
CRASH = int(F * 0.30)
CUT = int(F * 0.55)             # "...onto a plane home"
reset_scene(F, world_color=(0.75, 0.78, 0.82))
add_sun((60, 0, 30), energy=1.4, color=(0.95, 0.95, 1.0))
box("Snow", (600, 300, 0.2), (0, 0, -0.1), mat("snow", (0.85, 0.88, 0.94)))
box("Road", (200, 7, 0.05), (0, 0, 0.01), mat("road_slush", (0.45, 0.45, 0.46)))
pines([(x, y) for x in range(-40, 40, 7) for y in (12, 19)] + [(x + 3, -13) for x in range(-40, 40, 9)], seed=1)
gate = make_border_gate("Gate", (0, 0, 0), rot_z=0)
t = make_truck("Truck", (-38, -1.2, 0), rot_z=0)
r = t["root"]
r.keyframe_insert("location", index=0, frame=1)
r.location.x = 30
r.keyframe_insert("location", index=0, frame=CUT + 6)
linear_keys(r)
for w in t["wheels"]:
    spin(w, 1, CUT, axis=2, rps=-3)
bm = gate["boom"]
bm.keyframe_insert("rotation_euler", index=0, frame=CRASH)
bm.rotation_euler[0] = math.radians(100)              # smashed up
bm.keyframe_insert("rotation_euler", index=0, frame=CRASH + 3)
bm.rotation_euler[0] = math.radians(80)
bm.keyframe_insert("rotation_euler", index=0, frame=CRASH + 8)
# the airfield (far away), cut to at CUT
AX = 1000.0
box("Runway", (300, 14, 0.05), (AX, 0, 0.02), mat("runway", (0.30, 0.30, 0.32)))
for k in range(20):
    box(f"RwLine{k}", (4, 0.4, 0.06), (AX - 140 + k * 14, 0, 0.03), mat("rw_line", (0.95, 0.95, 0.9)))
pines([(AX + x, y) for x in range(-60, 80, 8) for y in (26, 34)], seed=2)
pl = make_plane("Plane", (AX - 30, 0, 2.2), rot_z=0, scale=0.8)
pr = pl["root"]
pr.keyframe_insert("location", frame=CUT)
pr.keyframe_insert("rotation_euler", index=1, frame=CUT)
pr.location = (AX + 25, 0, 16)
pr.rotation_euler[1] = math.radians(-14)              # nose up
pr.keyframe_insert("location", frame=F + 4)
pr.keyframe_insert("rotation_euler", index=1, frame=F + 4)
for p in pl["props"]:
    spin(p, CUT, F, axis=0, rps=8)
snowfall((0, -4, 0), (14, 8, 8), 1, CUT, n=100, seed=10)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=24)
key_camera(cam, 1, (10, 9.2, 2.4), (-8, 0, 1.6))
key_camera(cam, CUT - 1, (11, 9.4, 2.4), (3, 0, 1.6))
key_camera(cam, CUT, (AX - 10, -30, 2.0), (AX - 8, 0, 4))
key_camera(cam, F, (AX - 8, -30, 2.0), (AX + 14, 0, 11))
for fc in cam.animation_data.action.fcurves:
    for kp in fc.keyframe_points:
        if int(kp.co[0]) == CUT - 1:
            kp.interpolation = "CONSTANT"
add_shake(cam, CRASH - 1, CRASH + 8, strength=0.15, rot_strength=0.02)
render(os.environ.get("JAWS_OUT", "renders/shot10_border"))
