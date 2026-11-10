"""Shot 12: "And there's one remaining problem, which is that the plan is
still in motion. And there's only one man who can stop it. Police Chief
Brody." Underwater, red-lit: a Soviet sub keeps pumping sharks out of its
torpedo tubes. Cut: Amity pier at dusk, Brody alone in a spotlight; slow
push-in, and on his name he turns to camera."""
import math, os, sys, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import bpy
from jaws.common import reset_scene, add_camera, key_camera, linear_keys, render, FPS, shot_seconds, mat, fog
from jaws.props import underwater
from jaws.fireworks import dusk
from jaws.world import make_ocean, make_island
from jaws.shark import make_shark, swim_wag
from jaws.people import make_brody
from jaws.soviet import make_sub

F = int(shot_seconds("shot12", 7.3) * FPS)
CUT = int(F * 0.52)             # "And there's only one man who can stop it."
TURN = int(F * 0.83)            # "Police Chief Brody."
s = reset_scene(F)
# --- the pier at dusk (main world)
dusk(s)
make_ocean(color=(0.04, 0.12, 0.22))
isl = make_island()
dx, dy, dz = isl["dock_end"]
b = make_brody("Brody", loc=(dx, dy + 0.5, dz), rot_z=180)          # looking out to sea... away from us
b.root.keyframe_insert("rotation_euler", index=2, frame=TURN)
b.root.rotation_euler[2] = 0                                          # turns to camera
b.root.keyframe_insert("rotation_euler", index=2, frame=TURN + 6)
for a in (b.arm_l, b.arm_r):                                          # hands on hips
    a.rotation_euler = (0, 0, math.radians(35 if a is b.arm_l else -35))
sp = bpy.data.lights.new("Spot", "SPOT")
sp.energy, sp.spot_size, sp.spot_blend, sp.color = 4000, math.radians(22), 0.3, (1.0, 0.95, 0.85)
so = bpy.data.objects.new("Spot", sp)
so.location = (dx, dy + 0.5, dz + 12)
s.collection.objects.link(so)
# --- underwater, far away, the sub at work
UX = -800.0
sub = make_sub("Sub", (UX, 20, -10), rot_z=180)                      # stern (tubes) toward +X
red = bpy.data.lights.new("SubRed", "POINT")
red.energy, red.color = 9000, (1.0, 0.15, 0.08)
ro = bpy.data.objects.new("SubRed", red)
ro.location = (UX + 4, 12, -4)
s.collection.objects.link(ro)
rnd = random.Random(12)
from jaws.common import box
box("SeaFloor", (200, 200, 1), (UX, 20, -22), mat("seafloor", (0.30, 0.25, 0.18)))
box("DeepWater", (240, 240, 70), (UX, 20, -12), mat("deep_water", (0.03, 0.13, 0.20), emit=0.6))  # inside = murk
fill = bpy.data.lights.new("SubFill", "POINT")
fill.energy, fill.color = 6000, (0.4, 0.7, 0.9)
fo = bpy.data.objects.new("SubFill", fill)
fo.location = (UX + 30, 0, 6)
s.collection.objects.link(fo)
for i in range(24):                                                   # an endless stream of sharks
    sh = make_shark(f"Out{i}", scale=rnd.uniform(1.6, 2.2))
    f0 = int(i * CUT / 14) - 10
    y = 20 + rnd.uniform(-2, 2)
    for f in (f0, f0 + 60):
        t = (f - f0) / 60
        sh.root.location = (UX + 17 + 26 * t, y + rnd.uniform(-1, 1) * t * 8, -10 + rnd.uniform(-2, 3) * t)
        sh.root.keyframe_insert("location", frame=f)
    linear_keys(sh.root)
    sh.root.scale = (0.001,) * 3
    sh.root.keyframe_insert("scale", frame=max(1, f0 - 1))
    sh.root.scale = (2.0,) * 3
    sh.root.keyframe_insert("scale", frame=max(2, f0 + 2))
    swim_wag(sh, 1, CUT, period=10, seed=i)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (UX + 24, 2, -9), (UX + 12, 20, -6))
key_camera(cam, CUT - 1, (UX + 27, 5, -9), (UX + 18, 20, -6))
key_camera(cam, CUT, (dx + 0.4, dy - 9.5, dz + 2.0), (dx, dy, dz + 1.7))
key_camera(cam, F, (dx + 0.2, dy - 4.2, dz + 1.9), (dx, dy, dz + 1.9))
for fc in cam.animation_data.action.fcurves:
    for kp in fc.keyframe_points:
        if int(kp.co[0]) == CUT - 1:
            kp.interpolation = "CONSTANT"
render(os.environ.get("JAWS_OUT", "renders/shot12_one_man"))
