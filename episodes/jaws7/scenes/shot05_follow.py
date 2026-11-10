"""Shot 5: "...and follows the sharks out of the cave, way into deep water."
Tracking alongside the conga line of glowing mutants, Brody's mech shark
tucked in the middle, sliding deeper and darker."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import add_camera, key_camera, render, FPS, shot_seconds
from jaws.shark import make_shark, swim_wag
from _sets import deep

F = int(shot_seconds("shot05", 3.3) * FPS)
s = deep(F, color=(0.015, 0.07, 0.09), start=6, depth=45, floor_z=-60)
SPEED, DROP = 4.0, 1.6                     # m/s forward, m/s down
MECH = 3
for i in range(8):
    x0 = -i * 8.0
    mech = i == MECH
    sh = make_shark(f"S{i}", scale=3.0, variant="mech" if mech else "rad")
    sh.root.rotation_euler[1] = math.radians(12)            # nose down
    for f in (1, F):
        t = (f - 1) / FPS
        sh.root.location = (x0 + SPEED * t, 0.5 * math.sin(i), -8 - DROP * t + 0.5 * math.cos(i * 2))
        sh.root.keyframe_insert("location", frame=f)
    for fc in sh.root.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    swim_wag(sh, 1, F, period=14 if mech else 10, angle=10 if mech else 24, seed=i)
mx = -MECH * 8.0
T = F / FPS
cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (mx - 4, -17, -5), (mx + 2, 0, -8.5))
key_camera(cam, F, (mx + SPEED * T - 1, -15, -6 - DROP * T), (mx + SPEED * T + 3, 0, -9 - DROP * T))
for fc in cam.animation_data.action.fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = "LINEAR"
render(os.environ.get("JAWS_OUT", "renders/shot05_follow"))
