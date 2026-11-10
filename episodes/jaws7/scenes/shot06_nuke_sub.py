"""Shot 6: "And at the end of the line, he finds a giant frickin' nuclear
submarine." Behind the line in the black deep; the sharks swim toward a dim
green glow... the floodlights bang on: a gigantic submarine, sharks filing
into a glowing bay in its side. Camera drifts back and up to show the size."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import add_camera, key_camera, add_shake, render, FPS, shot_seconds
from jaws.shark import make_shark, swim_wag
from _deepsub import build_deepsub, BAY

F = int(shot_seconds("shot06", 4.0) * FPS)
ON = int(F * 0.5)                          # "...he finds a giant..."
s, sub = build_deepsub(F, lights_on=ON)
for i in range(9):
    mech = i == 5
    sh = make_shark(f"S{i}", scale=2.0, variant="mech" if mech else "rad")
    a = (2 - i * 6.0, 18 + i * 0.6, -9 + 0.6 * math.sin(i))
    b = BAY
    L = math.dist(a, b)
    v = 7.0
    t_arrive = 1 + int(L / v * FPS)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    sh.root.rotation_euler = (0, 0, ang)
    p_end = b if t_arrive <= F else tuple(a[k] + (b[k] - a[k]) * (F - 1) / (t_arrive - 1) for k in range(3))
    sh.root.location = a
    sh.root.keyframe_insert("location", frame=1)
    sh.root.location = p_end
    sh.root.keyframe_insert("location", frame=min(F, t_arrive))
    if t_arrive < F:                       # swallowed by the bay
        sh.root.keyframe_insert("scale", frame=t_arrive - 1)
        sh.root.scale = (0.001,) * 3
        sh.root.keyframe_insert("scale", frame=t_arrive)
    for fc in sh.root.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    swim_wag(sh, 1, F, period=14 if mech else 10, angle=10 if mech else 24, seed=i)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=20)
key_camera(cam, 1, (-14, 16, -9), (20, 46, -7))
key_camera(cam, ON, (-12, 18, -10), (26, 48, -3))
key_camera(cam, F, (-8, 22, -13), (40, 50, 5))
add_shake(cam, ON, ON + 6, strength=0.2, rot_strength=0.015)
render(os.environ.get("JAWS_OUT", "renders/shot06_nuke_sub"))
