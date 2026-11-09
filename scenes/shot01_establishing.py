"""Shot 1: Amity Island establishing shot. Sunny. Ferry chugs toward the harbor.
Camera: slow push-in. Gulls flap by."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, key_camera, linear_keys, render, FPS
from jaws.world import make_ocean, make_island, make_ferry, bob, make_gull, flap

SECONDS = 6.0
F = int(SECONDS * FPS)

reset_scene(F, world_color=(0.45, 0.75, 1.0))
add_sun((48, 0, -30), energy=2.4)
make_ocean()
isl = make_island()

ferry = make_ferry("Ferry", loc=(-30, -108, 0), rot_z=40)
ferry.keyframe_insert("location", index=0, frame=1)
ferry.keyframe_insert("location", index=1, frame=1)
ferry.location.x, ferry.location.y = -19, -98
ferry.keyframe_insert("location", index=0, frame=F)
ferry.keyframe_insert("location", index=1, frame=F)
linear_keys(ferry)
bob(ferry, 1, F)

for i, (x, y, z) in enumerate([(-40, -100, 24), (-46, -96, 26), (-35, -94, 27)]):
    g, wings = make_gull(f"Gull{i}", (x, y, z))
    g.keyframe_insert("location", frame=1)
    g.location.x += 22
    g.location.y += 6
    g.keyframe_insert("location", frame=F)
    linear_keys(g)
    flap(wings, 1, F, phase=i * 3)

cam = add_camera((-24, -170, 34), (-8, -60, 0), lens=28)
key_camera(cam, 1, (-24, -170, 34), (-8, -60, 0))
key_camera(cam, F, (-20, -140, 27), (-10, -62, 0))
linear_keys(cam)
render(os.environ.get("JAWS_OUT", "renders/shot01_establishing"))
