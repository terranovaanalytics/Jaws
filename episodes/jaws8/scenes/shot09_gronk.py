"""Shot 9: "So, CIA officer Rob Gronkowski smuggles him and Chief
Oceanographer Jesse, played by Jesse Plemons..." Night, snow, a yard behind
the Kremlin: huge CIA officer Gronk waits at the back of a Soviet army
truck, waves Brody and Jesse over, they climb in, thumbs up."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import bpy
from jaws.common import reset_scene, add_camera, key_camera, render, FPS, shot_seconds, box, mat
from jaws.fireworks import dusk
from jaws.people import make_brody, make_jesse, walk
from jaws.soviet import make_gronk, make_truck, make_kremlin
from _interior import lamp
from _snow import snowfall

F = int(shot_seconds("shot09", 6.3) * FPS)
ARRIVE = int(F * 0.58)
IN = int(F * 0.78)
s = reset_scene(F)
dusk(s, horizon=(0.22, 0.18, 0.30), mid=(0.09, 0.08, 0.18), zenith=(0.02, 0.02, 0.06), sun=False,
     ambient=0.25, ambient_color=(0.5, 0.55, 0.9))
moon = bpy.data.lights.new("Moon", "SUN")
moon.energy, moon.color = 0.7, (0.6, 0.7, 1.0)
mo = bpy.data.objects.new("Moon", moon)
mo.rotation_euler = (math.radians(55), 0, math.radians(-40))
s.collection.objects.link(mo)
box("Snow", (300, 300, 0.2), (0, 0, -0.1), mat("snow_night", (0.62, 0.66, 0.76)))
k = make_kremlin(loc=(10, 60, 0), night=True)
lamp("StarGlow", (10, 54, 42), 3000, color=(1.0, 0.15, 0.1), radius=2)
lamp("YardLamp", (-6, 6, 6), 700, color=(1.0, 0.78, 0.5))
t = make_truck("Truck", (0, 6, 0), rot_z=0)
g = make_gronk("Gronk", (-3.0, 3.2, 0), rot_z=-55)
b = make_brody("Brody", (-13, 1.5, 0), rot_z=90)
j = make_jesse("Jesse", (-14.4, 2.4, 0), rot_z=90)
for p, dest in ((b, (-5.4, 5.2)), (j, (-6.2, 6.3))):
    walk(p, 1, ARRIVE, period=10, swing=32)
    p.root.keyframe_insert("location", frame=1)
    p.root.location = (dest[0], dest[1], 0)
    p.root.keyframe_insert("location", frame=ARRIVE)
    p.root.location = (-2.6, dest[1] - 0.2, 1.4)                   # hop up into the bed
    p.root.keyframe_insert("location", frame=IN)
g.arm_l.keyframe_insert("rotation_euler", frame=2)                  # "c'mon c'mon" wave
for k_ in range(4):
    g.arm_l.rotation_euler = (math.radians(-110 if k_ % 2 == 0 else -70), 0, 0)
    g.arm_l.keyframe_insert("rotation_euler", frame=8 + k_ * 9)
g.arm_l.rotation_euler = (0, 0, 0)
g.arm_l.keyframe_insert("rotation_euler", frame=8 + 4 * 9 + 6)
g.arm_r.keyframe_insert("rotation_euler", frame=IN)
g.arm_r.rotation_euler = (math.radians(-80), 0, math.radians(-10))  # thumbs up to camera
g.arm_r.keyframe_insert("rotation_euler", frame=IN + 6)
g.head.rotation_euler[2] = math.radians(-30)
g.head.keyframe_insert("rotation_euler", index=2, frame=IN + 2)
snowfall((-5, 2, 0), (9, 8, 9), 1, F, n=160, seed=9)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (-10.5, -6.5, 2.0), (-6.0, 4.5, 2.0))
key_camera(cam, F, (-9.0, -4.5, 1.9), (-4.8, 4.8, 1.9))
render(os.environ.get("JAWS_OUT", "renders/shot09_gronk"))
