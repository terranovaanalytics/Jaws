"""Shot 16: "A whole new mystery to solve." Brody and Jesse from behind at
the end of the pier, the harbor smoldering. Far out on the horizon, a green
glow pulses. Slow pull back."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import add_camera, key_camera, render, FPS, shot_seconds, ico, mat
from jaws.fireworks import flash_light
from jaws.people import make_brody, make_jesse
from _harbor import build_harbor, BARGE, tip_barge, harbor_ablaze

F = int(shot_seconds("shot16", 3.9) * FPS)
h = build_harbor(F, extras=False)
tip_barge(h["barge"])
harbor_ablaze(h, 1, F, sails=4)
dx, dy, dz = h["dock_end"]
b = make_brody("Brody", loc=(dx - 0.8, dy - 0.6, dz), rot_z=0)
j = make_jesse("Jesse", loc=(dx + 0.8, dy - 0.6, dz), rot_z=0)
j.head.rotation_euler[2] = math.radians(12)
glow = ico("RadGlow", 70, (dx - 6, -320, -5), mat("rad_glow", (0.45, 1.0, 0.3), emit=2.0), subdiv=2)
glow.scale = (3.0, 1, 0.5)
for f in range(1, F + 1, 4):
    k = 0.75 + 0.25 * math.sin(f / FPS * 5)
    glow.scale = (3.0 * k, 1, 0.5 * k)
    glow.keyframe_insert("scale", frame=f)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=30)
key_camera(cam, 1, (dx + 0.2, dy + 3.2, dz + 2.6), (dx - 6, dy - 120, 2))
key_camera(cam, F, (dx + 0.3, dy + 6.0, dz + 3.0), (dx - 6, dy - 120, 3))
render(os.environ.get("JAWS_OUT", "renders/shot16_mystery"))
