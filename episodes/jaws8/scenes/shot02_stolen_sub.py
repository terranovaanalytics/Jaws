"""Shot 2: "And Police Chief Brody, played by Pedro Pascal, just stole that
sub and he's headed to Russia. Let's go." The (placeholder) Soviet sub slides
out of Amity harbor, Brody standing in the hatch. He salutes; on "Let's go"
he drops inside and the sub dives."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, key_camera, add_shake, render, FPS, shot_seconds
from jaws.world import make_ocean, make_island, make_gull, flap, splash
from jaws.people import make_brody
from jaws.soviet import make_sub

F = int(shot_seconds("shot02", 5.2) * FPS)
SALUTE = int(F * 0.45)          # "...just stole that sub"
GO = int(F * 0.84)              # "Let's go."
reset_scene(F)
add_sun((60, 0, 40))
make_ocean()
isl = make_island()
sub = make_sub("Sub", (26, -64, 0), rot_z=-90)
r = sub["root"]
r.keyframe_insert("location", frame=1)
r.location.y = -74
r.keyframe_insert("location", frame=GO)
r.location = (26, -79, -7)
r.rotation_euler[1] = math.radians(12)            # nose down (bow is local +X)
r.keyframe_insert("location", frame=F + 8)
r.keyframe_insert("rotation_euler", index=1, frame=F + 8)
r.rotation_euler[1] = 0
r.keyframe_insert("rotation_euler", index=1, frame=GO)
hx, hy, hz = sub["hatch"]
b = make_brody("Brody", loc=(hx, hy, hz - 0.9), rot_z=90)
b.root.parent = r
b.root.keyframe_insert("location", index=2, frame=GO + 2)
b.root.location.z = hz - 3.2
b.root.keyframe_insert("location", index=2, frame=GO + 8)
b.arm_r.keyframe_insert("rotation_euler", frame=SALUTE - 6)
b.arm_r.rotation_euler = (math.radians(-150), 0, math.radians(-35))
b.arm_r.keyframe_insert("rotation_euler", frame=SALUTE)
b.arm_r.keyframe_insert("rotation_euler", frame=GO - 6)
b.arm_r.rotation_euler = (math.radians(-170), 0, 0)            # "let's go!" fist pump
b.arm_r.keyframe_insert("rotation_euler", frame=GO)
b.head.rotation_euler[2] = math.radians(-30)                 # looking at camera...
b.head.keyframe_insert("rotation_euler", index=2, frame=SALUTE)
splash("Dive", (26, -86, 0), GO + 6, count=18, size=0.7, power=7, life=24)
for k in range(3):
    g, w = make_gull(f"Gull{k}", (10 + k * 5, -70 - k * 3, 12 + k))
    g.keyframe_insert("location", frame=1)
    g.location.x += 18
    g.keyframe_insert("location", frame=F)
    flap(w, 1, F, phase=k * 3)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=32)
key_camera(cam, 1, (20.5, -74, 6.3), (26, -66.5, 4.4))
key_camera(cam, GO, (19.5, -84, 5.8), (26, -76.0, 4.2))
key_camera(cam, F, (17.5, -88, 4.0), (26, -82, 1.5))
add_shake(cam, GO + 4, F, strength=0.06)
render(os.environ.get("JAWS_OUT", "renders/shot02_stolen_sub"))
