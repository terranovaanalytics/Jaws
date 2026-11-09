"""Shot 8: Brody and Jesse on the pier, the harbor burning behind them. Slow
push-in; they look at each other... they know exactly what happened."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import bpy
from jaws.common import add_camera, key_camera, render, FPS, shot_seconds
from jaws.people import make_brody, make_jesse
from _harbor import build_harbor, BARGE, tip_barge, harbor_ablaze, chaos_bursts

F = int(shot_seconds("shot08", 5.0) * FPS)
h = build_harbor(F)
tip_barge(h["barge"])
harbor_ablaze(h, 1, F)
chaos_bursts(1, F, every=12, seed=8)
dx, dy, dz = h["dock_end"]
b = make_brody("Brody", loc=(dx - 0.6, dy + 0.8, dz), rot_z=180)
j = make_jesse("Jesse", loc=(dx + 0.6, dy + 0.8, dz), rot_z=180)
LOOK = int(F * 0.45)
BACK = int(F * 0.8)
for p, yaw in ((b, -35), (j, 35)):                   # turn to each other... then to camera
    p.head.keyframe_insert("rotation_euler", frame=LOOK - 6)
    p.head.rotation_euler[2] = math.radians(yaw)
    p.head.keyframe_insert("rotation_euler", frame=LOOK)
    p.head.keyframe_insert("rotation_euler", frame=BACK - 4)
    p.head.rotation_euler = (math.radians(-6), 0, 0)
    p.head.keyframe_insert("rotation_euler", frame=BACK + 2)
# warm fire light on their faces from the burning harbor (behind the camera's
# view they would be backlit only)
d = bpy.data.lights.new("FaceFire", "POINT")
d.color, d.use_shadow = (1.0, 0.55, 0.25), False
o = bpy.data.objects.new("FaceFire", d)
o.location = (dx + 2, dy + 5, dz + 2.5)
bpy.context.scene.collection.objects.link(o)
for f in range(1, F + 1, 3):
    d.energy = 60 + 25 * math.sin(f * 1.7) * math.sin(f * 0.6)
    d.keyframe_insert("energy", frame=f)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=35)
key_camera(cam, 1, (dx + 0.5, dy + 6.5, dz + 1.9), (dx, dy, dz + 2.3))
key_camera(cam, F, (dx + 0.1, dy + 5.0, dz + 1.85), (dx, dy, dz + 1.95))
render(os.environ.get("JAWS_OUT", "renders/shot08_brody_jesse"))
