"""Shot 10: "So the President sends his top CIA officer, played by Rob
Gronkowski, to Amity Island." A black helicopter swoops in and lands on the
end of the Amity pier, rotor thrashing. Out climbs the agent: huge, black
suit, shades. He strides up to Brody and Jesse and gives a big thumbs up."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import reset_scene, add_sun, add_camera, key_camera, add_shake, render, FPS, shot_seconds
from jaws.world import make_ocean, make_island, splash
from jaws.people import make_brody, make_jesse, walk
from jaws.spy import make_helicopter, make_agent, spin
from _sets import move, face

F = int(shot_seconds("shot10", 4.7) * FPS)
reset_scene(F)
add_sun((50, 0, -35), energy=2.3)
make_ocean()
isl = make_island()
dx, dy, dz = isl["dock_end"]                  # (10, -62, 1.45)
LAND = int(F * 0.38)
OUT = int(F * 0.48)                            # "...top CIA officer"
h = make_helicopter("Heli", (dx - 30, dy - 25, 26), rot_z=40)
move(h["root"], [(1, (dx - 30, dy - 25, 26)), (int(LAND * 0.7), (dx - 2, dy - 4, 6)), (LAND, (dx + 3, dy + 0.5, dz))])
face(h["root"], 1, 40)
face(h["root"], LAND, 180)
spin(h["rotor"], 2, 1, F, rpm=300)
spin(h["trotor"], 1, 1, F, rpm=900)
for k in range(3):
    splash(f"Wash{k}", (dx + 3 + k * 2 - 2, dy - 4, 0.2), int(LAND * 0.6) + k * 4, count=10, size=0.4, power=4)
# heli faces -X after landing (rot 180): its left door faces +Y, toward the island
a = make_agent("Agent", loc=(dx + 3.2, dy + 1.8, dz), rot_z=180)
a.root.scale = (0.001,) * 3
a.root.keyframe_insert("scale", frame=OUT - 1)
a.root.scale = (1, 1, 1)
a.root.keyframe_insert("scale", frame=OUT)
STOP = OUT + int(F * 0.28)
move(a.root, [(OUT, (dx + 3.2, dy + 1.8, dz)), (STOP, (dx + 0.6, dy + 7.0, dz))], linear=True)
walk(a, OUT, STOP, period=14)
face(a.root, STOP, 180)
face(a.root, STOP + 6, 100)                   # turns to the camera
face(a.arm_r, STOP + 4, 0, axis=0)
face(a.arm_r, STOP + 9, -90, axis=0)           # thumbs up (well, fist out)
face(a.head, STOP + 9, 15, axis=0)
b = make_brody("Brody", loc=(dx - 1.4, dy + 10.5, dz), rot_z=15)
j = make_jesse("Jesse", loc=(dx + 1.4, dy + 11.2, dz), rot_z=-10)
for p in (b, j):
    face(p.head, 1, -15, axis=0)               # looking up at the chopper
    face(p.head, LAND, 0, axis=0)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (dx + 15, dy + 8, 4.5), (dx - 10, dy - 10, 12))
key_camera(cam, LAND, (dx + 15, dy + 6, 4.0), (dx + 1.5, dy + 3, 3.2))
key_camera(cam, F, (dx + 13, dy + 6, 3.5), (dx + 0.5, dy + 7, 2.6))
add_shake(cam, LAND - 2, LAND + 6, strength=0.15, rot_strength=0.01)
render(os.environ.get("JAWS_OUT", "renders/shot10_cia"))
