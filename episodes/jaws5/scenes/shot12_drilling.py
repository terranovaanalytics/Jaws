"""Shot 12: at the Flying Horses. The ride screeches to a stop, the kids get
kicked off and run, a drill rig drops from the sky, Brody and Jesse drill
straight through the carousel floor."""
import math, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import (reset_scene, add_sun, add_camera, key_camera, add_shake, linear_keys,
                         render, FPS, shot_seconds, box, mat)
from jaws.props import make_carousel, animate_carousel, make_drill
from jaws.world import make_extra, splash
from jaws.people import make_brody, make_jesse, walk, point

F = int(shot_seconds("shot12", 7.0) * FPS)
reset_scene(F, world_color=(0.45, 0.75, 1.0))
add_sun((45, 0, -30), energy=2.4)
box("Ground", (200, 200, 1), (0, 0, -0.5), mat("grass", (0.30, 0.72, 0.25)))
box("Path", (6, 40, 0.1), (0, -24, 0.02), mat("path", (0.85, 0.80, 0.68)))

c = make_carousel()
STOP = int(F * 0.22)
RPM = 4.0
animate_carousel(c, 1, F, rpm=RPM, stop_at=STOP)


def rotor_angle(f):
    return (min(f, STOP) - 1) / 24 * RPM / 60 * 2 * math.pi


# kids ride along with the platform, then bail in every direction
rnd = random.Random(12)
for i in range(8):
    a0 = 2 * math.pi * i / 8 + 0.2
    r = 4.6
    kid = make_extra(f"Kid{i}", seed=i, scale=0.75)
    for f in range(1, STOP + 1, 2):
        a = a0 + rotor_angle(f)
        kid.location = (r * math.cos(a), r * math.sin(a), 0.75)
        kid.rotation_euler[2] = a
        kid.keyframe_insert("location", frame=f)
        kid.keyframe_insert("rotation_euler", index=2, frame=f)
    a = a0 + rotor_angle(STOP)
    go = STOP + 6 + rnd.randint(0, 8)
    out = a + rnd.uniform(-0.6, 0.6)
    kid.keyframe_insert("location", frame=go)
    kid.rotation_euler[2] = out + math.pi / 2       # face where they run
    kid.keyframe_insert("rotation_euler", index=2, frame=go)
    kid.location = (30 * math.cos(out), 30 * math.sin(out), 0)
    kid.keyframe_insert("location", frame=go + 40)
    linear_keys(kid)

# drill rig falls from the sky onto the platform
DROP = STOP + 22
drill, bit = make_drill(loc=(2.4, -2.0, 30))
drill.keyframe_insert("location", frame=1)
drill.keyframe_insert("location", frame=DROP - 8)
drill.location.z = 0.75
drill.keyframe_insert("location", frame=DROP)
for f in range(DROP, F + 1, 2):
    bit.rotation_euler[2] = math.radians((f - DROP) * 50)
    bit.location.z = 3.9 - min(2.2, (f - DROP) / 24 * 1.4)
    bit.keyframe_insert("rotation_euler", index=2, frame=f)
    bit.keyframe_insert("location", index=2, frame=f)
dirt = (0.5, 0.33, 0.2)
for k in range(4):
    splash(f"Dust{k}", (2.4, -2.0, 0.9), DROP + 8 + k * 14, count=10, size=0.3, power=4, seed=k, color=dirt)

b = make_brody("Brody", loc=(-1.0, -12, 0), rot_z=0)
j = make_jesse("Jesse", loc=(6.0, -12, 0), rot_z=0)
for p, tx in ((b, -0.2), (j, 5.0)):
    p.root.keyframe_insert("location", frame=1)
    p.root.location = (tx, -7.2, 0)
    p.root.keyframe_insert("location", frame=STOP + 10)
    linear_keys(p.root)
    walk(p, 1, STOP + 6)
point(b, DROP + 4, side="r", hold=40)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (4, -26, 5), (1.5, 0, 3.5))
key_camera(cam, F, (3, -19, 3.8), (1.5, 0, 2.2))
add_shake(cam, DROP, DROP + 8, strength=0.5, rot_strength=0.04)
add_shake(cam, DROP + 10, F, strength=0.05, rot_strength=0.004, seed=3)
render(os.environ.get("JAWS_OUT", "renders/shot12_drilling"))
