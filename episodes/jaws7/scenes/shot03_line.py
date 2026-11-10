"""Shot 3: "Now Jaws 7, are you ready? Let's go. We got another line of
sharks." Underwater, murky green: a rock arch on the sea floor glowing from
inside. ARE YOU READY? hangs in the water; on "Let's go" it pops and a line
of glowing mutant sharks streams out of the cave, past the camera."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import add_camera, key_camera, render, FPS, shot_seconds, box, mat, text
from jaws.shark import make_shark, swim_wag
from jaws.town import pop_in
from _sets import deep, glow_light

F = int(shot_seconds("shot03", 4.5) * FPS)
s = deep(F, color=(0.03, 0.13, 0.12), start=10, depth=70, floor_z=-20)
GO = int(F * 0.42)
rock = mat("arch_rock", (0.28, 0.30, 0.30))
glow = mat("cave_glow", (0.45, 1.0, 0.3), emit=3.5)
CX, CY = 0, 34
for side in (-1, 1):                                    # the arch
    box(f"Pillar{side}", (5, 6, 11), (CX + side * 6.5, CY, -14.5), rock, rot=(0, side * 6, 0))
box("Lintel", (19, 7, 4), (CX, CY, -8.0), rock, rot=(0, 3, 0))
box("Back", (10, 1, 10), (CX, CY + 3.5, -15), glow)
box("Mound", (30, 14, 6), (CX, CY + 7, -17), rock)
glow_light("CaveLight", (CX, CY - 2, -13), (0.45, 1.0, 0.3), 9000, radius=3)
yel = mat("ready_yellow", (1, 0.85, 0.1), emit=2.5)
q = text("Ready", "ARE YOU", (0, 9, -2.2), 1.7, yel, extrude=0.25, bold=True)
q2 = text("Ready2", "READY?", (0, 9, -4.4), 2.3, yel, extrude=0.3, bold=True)
pop_in(q, 4, out_frame=GO)
pop_in(q2, 8, out_frame=GO)
N = 9
for i in range(N):
    sh = make_shark(f"Mutant{i}", scale=2.3, variant="rad")
    f0 = GO + i * 5
    side = -1 if i % 2 else 1
    a = (CX + side * 0.6, CY + 1, -14)                  # out of the cave, over the camera's shoulder
    b = (CX + side * 5 - 3, -8, -5 + (i % 3) * 0.8)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    sh.root.rotation_euler = (0, math.radians(-12), ang)
    sh.root.location = a
    sh.root.scale = (0.001,) * 3
    sh.root.keyframe_insert("scale", frame=1)
    sh.root.keyframe_insert("scale", frame=f0 - 1)
    sh.root.scale = (2.3,) * 3
    sh.root.keyframe_insert("scale", frame=f0)
    for f, p in ((f0, a), (f0 + int(1.8 * FPS), b)):
        sh.root.location = p
        sh.root.keyframe_insert("location", frame=f)
    for fc in sh.root.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    swim_wag(sh, 1, F, period=9, angle=26, seed=i)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (0, -6, -6), (0, 30, -8))
key_camera(cam, F, (0, -2, -7), (0, 30, -10))
render(os.environ.get("JAWS_OUT", "renders/shot03_line"))
