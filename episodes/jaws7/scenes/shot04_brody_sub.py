"""Shot 4: "But this time Police Chief Brody, played by Pedro Pascal, hops in
his mechanical shark sub, blends in..." Amity pier. Brody marches to the end,
hops into the hatch on the mech shark's back, the lid slams, it sinks under
as two real fins cruise by. (Cast cards play over the top of frame.)"""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import reset_scene, add_sun, add_camera, key_camera, render, FPS, shot_seconds, cyl, mat, empty
from jaws.world import make_ocean, make_island, splash, bob
from jaws.people import make_brody, walk
from jaws.shark import make_shark, swim_wag
from _sets import move, face

F = int(shot_seconds("shot04", 5.3) * FPS)
reset_scene(F)
add_sun((50, 0, -35), energy=2.3)
make_ocean()
isl = make_island()
dx, dy, dz = isl["dock_end"]                  # (10, -62, 1.45)
SX, SY = dx + 4.2, dy - 0.5                    # the mech sub, alongside the pier end
mech = make_shark("Mech", (SX, SY, 0.1), rot_z=0, scale=3.4, variant="mech")
swim_wag(mech, 1, F, period=20, angle=6, seed=1)
metal = mat("hatch_metal", (0.55, 0.57, 0.6), rough=0.4, metal=0.7)
cyl("HatchRim", 0.15, 0.06, (0.0, 0, 0.36), metal, n=10, parent=mech.root)
cyl("HatchHole", 0.12, 0.02, (0.0, 0, 0.395), mat("hatch_hole", (0.01, 0.01, 0.01)), n=10, parent=mech.root)
hinge = empty("HatchHinge", (-0.14, 0, 0.39), parent=mech.root)
cyl("HatchLid", 0.14, 0.03, (0.14, 0, 0.0), metal, n=10, parent=hinge)
HOP = int(F * 0.48)                            # "hops in"
IN = HOP + 10
SHUT = IN + 4
SINK = int(F * 0.74)                           # "blends in"
face(hinge, 1, -110, axis=1)
face(hinge, SHUT - 2, -110, axis=1)
face(hinge, SHUT, 0, axis=1)
top = (SX, SY, 0.1 + 0.4 * 3.4)               # hatch in world space
b = make_brody("Brody", loc=(dx, dy + 12, dz), rot_z=0)
WALK_END = int(F * 0.34)
move(b.root, [(1, (dx, dy + 12, dz)), (WALK_END, (dx + 0.4, dy + 0.3, dz))], linear=True)
walk(b, 1, WALK_END)
face(b.root, WALK_END, 0)
face(b.root, WALK_END + 6, 90)                 # turn to face the sub
move(b.root, [(HOP - 4, (dx + 0.4, dy + 0.3, dz)), (HOP - 1, (dx + 0.4, dy + 0.3, dz - 0.25)),
              (HOP + 5, ((dx + SX) / 2, (dy + SY) / 2, top[2] + 2.6)), (IN - 2, (top[0], top[1], top[2] + 0.1)),
              (IN + 2, (top[0], top[1], top[2] - 2.0))])
for arm in (b.arm_l, b.arm_r):                 # arms up for the hop
    face(arm, HOP - 2, 0, axis=0)
    face(arm, HOP + 2, -170, axis=0)
b.root.keyframe_insert("scale", frame=IN)
b.root.scale = (0.001,) * 3
b.root.keyframe_insert("scale", frame=IN + 2)
# then it slips under
mech.root.keyframe_insert("location", frame=SINK)
mech.root.location.z = -3.5
mech.root.keyframe_insert("location", frame=F)
splash("Sink", (SX, SY - 1, 0.2), SINK + 4, count=16, size=0.5, power=5)
for k in range(2):                             # real sharks cruising past: it blends right in
    sh = make_shark(f"Fin{k}", scale=3.2, rot_z=0)
    y = SY + 6 + k * 5
    move(sh.root, [(int(F * 0.45), (SX - 30 - k * 8, y, -0.7)), (F, (SX + 10 - k * 8, y, -0.7))], linear=True)
    swim_wag(sh, 1, F, period=12, seed=k + 3)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=30)
key_camera(cam, 1, (dx - 4, dy - 11, 3.6), (dx + 0.5, dy + 5, 2.6))
key_camera(cam, WALK_END, (dx - 3, dy - 11, 3.4), (dx + 1.8, dy + 0.5, 2.4))
key_camera(cam, F, (dx - 2, dy - 12, 3.0), (SX - 1, SY + 2, 1.2))
render(os.environ.get("JAWS_OUT", "renders/shot04_brody_sub"))
