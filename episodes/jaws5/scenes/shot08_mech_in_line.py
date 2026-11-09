"""Shot 8: underwater. A single-file line of great whites... and one of them
is Brody's riveted mechanical shark sub with a glowing porthole."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import reset_scene, add_camera, key_camera, linear_keys, render, FPS, shot_seconds
from jaws.props import underwater
from jaws.shark import make_shark, swim_wag

F = int(shot_seconds("shot08", 7.0) * FPS)
s = reset_scene(F)
underwater(s)

S = 3.0
SPEED = 3.0                    # m/s along +X
MECH = 4
for i in range(9):
    x0 = -i * 8.5
    sh = make_shark(f"Shark{i}", scale=S, variant="mech" if i == MECH else "real")
    for f in (1, F):
        sh.root.location = (x0 + SPEED * (f - 1) / FPS, 0, -8 + 0.6 * math.sin(i))
        sh.root.keyframe_insert("location", frame=f)
    linear_keys(sh.root)
    swim_wag(sh, 1, F, period=14 if i == MECH else 12, angle=10 if i == MECH else 22, seed=i)

# camera tracks alongside, sliding back along the line to land on the mech
mx0 = -MECH * 8.5
cam = add_camera((0, 0, 0), (0, 0, 0), lens=30)
key_camera(cam, 1, (-12, -17, -6), (-12, 0, -8))
key_camera(cam, F, (mx0 + SPEED * F / FPS + 1, -11, -7), (mx0 + SPEED * F / FPS, 0, -8))
render(os.environ.get("JAWS_OUT", "renders/shot08_mech_in_line"))
