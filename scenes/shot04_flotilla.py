"""Shot 4: Chief Brody leads a flotilla of tiny boats out of Amity Harbor,
Dunkirk style, pointing heroically out to sea. Camera tracks alongside."""
import math, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, key_camera, linear_keys, render, FPS, shot_seconds
from jaws.world import make_ocean, make_island, make_small_boat, bob, make_extra
from jaws.people import make_brody

F = int(shot_seconds("shot04", 7.0) * FPS)
reset_scene(F, world_color=(0.45, 0.75, 1.0))
add_sun((45, 0, 40), energy=2.4)
make_ocean()
make_island()

rnd = random.Random(4)
Y0, Y1 = -66.0, -96.0          # lead boat sails out of the harbor toward -Y
X = 30.0           # east of the pier so nobody starts inside it


def sail(obj, dx, dy, phase):
    for f, y in ((1, Y0), (F, Y1)):
        obj.location = (X + dx, y + dy, 0)
        obj.keyframe_insert("location", frame=f)
    linear_keys(obj)
    bob(obj, 1, F, roll=4, pitch=3, heave=0.2, phase=phase)


lead = make_small_boat("LeadBoat", rot_z=-90, color=(0.95, 0.95, 0.95), seed=0)
lead.scale = (1.6,) * 3
sail(lead, 0, 0, 0)
brody = make_brody("Brody", loc=(0.3, 0, 0.62), rot_z=90)   # faces -Y once boat turns
brody.root.parent = lead
brody.root.scale = (1 / 1.6,) * 3
brody.root.location = (0.6, 0, 0.62)
brody.root.rotation_euler[2] = math.radians(90)             # face the bow (+X local)
brody.arm_r.rotation_euler[0] = math.radians(-100)          # pointing out to sea
brody.arm_l.rotation_euler[1] = math.radians(-20)

k = 0
for row in range(1, 6):
    for side in (-1, 1):
        for extra in range(1 if row < 3 else 2):
            dx = side * (row * 2.6 + extra * 3 + rnd.uniform(-0.6, 0.6))
            dy = row * 7 + extra * 3.5 + rnd.uniform(-1, 1)
            b = make_small_boat(f"Boat{k}", rot_z=-90, seed=k + 1)
            sail(b, dx, dy, phase=k * 7)
            if rnd.random() < 0.6:
                p = make_extra(f"Sailor{k}", (0, 0, 0.6), seed=k)
                p.parent = b
                p.location = (-0.8, 0, 0.6)
            k += 1

cam = add_camera((0, 0, 0), (0, 0, 0), lens=30)
for f, y in ((1, Y0), (F, Y1)):
    # ahead of the fleet, looking back at it: Brody leads straight at us
    key_camera(cam, f, (X + 3, y - 20 + (4 if f == F else 0), 8 - (1.5 if f == F else 0)), (X, y + 14, 0))
linear_keys(cam)
render(os.environ.get("JAWS_OUT", "renders/shot04_flotilla"))
