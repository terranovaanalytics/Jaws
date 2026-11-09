"""Shot 7: "And then America, protected by an ocean, becomes defenseless
overnight. Russia, achieving naval superiority, wins the Cold War." The war
map, low over the Atlantic: little US Navy ships guard the coast... then
sink off the map one by one. A fleet of red-star ships sails across from
the east, and a big Soviet flag plants itself on the USA."""
import math, os, sys, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, key_camera, render, FPS, shot_seconds, box, mat, text, empty
from jaws.soviet import make_map_table, make_soviet_flag
from jaws.town import pop_in

F = int(shot_seconds("shot07", 7.5) * FPS)
SINK = int(F * 0.30)            # "...becomes defenseless overnight"
FLEET = int(F * 0.50)           # "Russia, achieving naval superiority"
WIN = int(F * 0.84)             # "...wins the Cold War"
reset_scene(F, world_color=(0.12, 0.10, 0.08))
add_sun((40, 10, 30), energy=1.7)
m = make_map_table()
R = m["root"]


def ship(name, loc, red):
    s = empty(name, loc, R)
    s.scale = (1.5,) * 3
    hull = mat("ship_red" if red else "ship_navy", (0.45, 0.45, 0.48) if red else (0.30, 0.36, 0.48))
    box(f"{name}_h", (1.4, 0.45, 0.25), (0, 0, 0.12), hull, parent=s)
    box(f"{name}_t", (0.4, 0.3, 0.35), (-0.1, 0, 0.4), hull, parent=s)
    if red:
        text(f"{name}_star", "★", (-0.1, 0, 0.62), 0.45, mat("soviet_red", (0.85, 0.10, 0.08), emit=0.3),
             rot=(90, 0, 0), parent=s, bold=True)
    else:
        box(f"{name}_flag", (0.18, 0.02, 0.12), (-0.1, 0, 0.66), mat("navy_flag", (0.9, 0.9, 0.9)), parent=s)
    return s


rnd = random.Random(7)
coast = [(-8.0, 4.6), (-8.4, 3.0), (-9.2, 1.6), (-9.9, 0.0), (-10.4, -1.8), (-10.8, -3.6), (-7.6, 6.2)]
for k, (x, y) in enumerate(coast):
    s = ship(f"Navy{k}", (x + 1.4, y, 0), red=False)
    s.rotation_euler[2] = math.radians(90)
    s.keyframe_insert("location", index=2, frame=SINK + k * 3)
    s.location.z = -1.8                               # glug glug
    s.rotation_euler[1] = math.radians(25)
    s.keyframe_insert("location", index=2, frame=SINK + k * 3 + 10)
    s.keyframe_insert("rotation_euler", index=1, frame=SINK + k * 3 + 10)
    s.rotation_euler[1] = 0
    s.keyframe_insert("rotation_euler", index=1, frame=SINK + k * 3)
for k in range(9):                                    # the red fleet
    row, col = divmod(k, 3)
    y0 = 1.5 + (col - 1) * 1.8 + row * 0.5
    s = ship(f"Red{k}", (12 + row * 2.0, y0, 0), red=True)
    s.rotation_euler[2] = math.radians(180)
    s.keyframe_insert("location", index=0, frame=FLEET + k)
    s.location.x = -7.2 + row * 2.2 + rnd.uniform(-0.3, 0.3)
    s.keyframe_insert("location", index=0, frame=WIN + 4)
fl = make_soviet_flag("Win", (-13.0, 0.0, 0), size=2.6, pole=5.0)
fl.parent = R
pop_in(fl, WIN, scale=1.0)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (-17, -10, 7.5), (-9.5, 1.5, 0))
key_camera(cam, FLEET, (-15.5, -10.5, 8.0), (-6, 1.5, 0))
key_camera(cam, WIN - 4, (-14.5, -11, 8.5), (-7.5, 1.5, 0.5))
key_camera(cam, F, (-15.5, -10.5, 8.5), (-9.5, 1.0, 1.2))
render(os.environ.get("JAWS_OUT", "renders/shot07_cold_war"))
