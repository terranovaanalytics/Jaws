"""Shot 6: chief oceanographer Jesse arrives on the Amity dock. Red beanie in
summer. Walks up, stops, slow push-in, he looks at the camera."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
from jaws.common import (reset_scene, add_sun, add_camera, key_camera, linear_keys, render,
                         FPS, shot_seconds, box, mat, text)
from jaws.world import make_ocean, make_island, make_small_boat, bob, make_gull, flap
from jaws.people import make_jesse, walk

F = int(shot_seconds("shot06", 6.0) * FPS)
reset_scene(F, world_color=(0.45, 0.75, 1.0))
add_sun((40, 0, 50), energy=2.4)
make_ocean()
isl = make_island()
dx, dy, dz = isl["dock_end"]          # T end of the pier

# Jesse walks down the pier toward the T (toward -Y)
j = make_jesse("Jesse", loc=(dx, dy + 14, dz), rot_z=0)
STOP = int(F * 0.55)
j.root.keyframe_insert("location", frame=1)
j.root.location.y = dy + 1.5
j.root.keyframe_insert("location", frame=STOP)
linear_keys(j.root)
walk(j, 1, STOP - 4, period=12, swing=30)
for limb in (j.leg_l, j.leg_r, j.arm_l, j.arm_r):
    limb.rotation_euler[0] = 0
    limb.keyframe_insert("rotation_euler", index=0, frame=STOP)
# beat... then a slow, judgmental head tilt
j.head.keyframe_insert("rotation_euler", frame=STOP + 6)
j.head.rotation_euler = (math.radians(-8), math.radians(14), 0)
j.head.keyframe_insert("rotation_euler", frame=STOP + 16)

# dock dressing: sign, moored boats, gull
sign_m = mat("sign_board", (0.95, 0.95, 0.9))
box("SignBoard", (4.2, 0.2, 1.1), (dx - 4.5, dy + 6, dz + 2.6), sign_m)
box("SignPost", (0.2, 0.2, 2.4), (dx - 4.5, dy + 6.1, dz + 1.1), mat("dock_post", (0.30, 0.22, 0.14)))
text("SignText", "AMITY HARBOR", (dx - 4.5, dy + 5.88, dz + 2.6), 0.55, mat("sign_ink", (0.1, 0.2, 0.5)))
for i, (ox, oy) in enumerate([(6, -1), (-6.5, 0.5), (7, 6)]):
    b = make_small_boat(f"Moored{i}", loc=(dx + ox, dy + oy, 0), rot_z=90 * (1 if i % 2 else -1), seed=i + 2)
    bob(b, 1, F, phase=i * 13)
g, wings = make_gull("Gull", (dx - 8, dy + 4, dz + 8))
g.keyframe_insert("location", frame=1)
g.location = (dx + 10, dy + 2, dz + 9)
g.keyframe_insert("location", frame=F)
linear_keys(g)
flap(wings, 1, F)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=35)
key_camera(cam, 1, (dx - 1.5, dy - 9, dz + 2.0), (dx, dy + 6, dz + 2.0))
key_camera(cam, STOP, (dx - 1.0, dy - 6, dz + 2.1), (dx, dy + 2, dz + 2.0))
key_camera(cam, F, (dx - 0.5, dy - 3.8, dz + 2.6), (dx, dy + 1.5, dz + 2.45))
render(os.environ.get("JAWS_OUT", "renders/shot06_jesse_arrives"))
