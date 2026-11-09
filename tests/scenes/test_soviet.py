"""Model test (Jaws 8): placeholder Soviet sub, Brezhnev, Gronk, disguised
soldier, truck, plane, border gate, chalkboard, recruiting booth, bubble, flag.
The Kremlin and the map table have their own frames (see camera keys)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, key_camera, box, mat, render
from jaws.people import make_brody, make_jesse
from jaws.soviet import (make_sub, make_brezhnev, make_gronk, make_soldier, make_truck, make_plane,
                         make_border_gate, make_chalkboard, chalk_mark, chalk_arrow, make_recruit_booth,
                         speech_bubble, make_soviet_flag, make_kremlin, make_map_table, pin, dotted_path,
                         make_tumbleweed)

s = reset_scene(3, world_color=(0.45, 0.75, 1.0))
add_sun((50, 0, -30))
box("Ground", (400, 400, 1), (0, 0, -0.5), mat("grass", (0.30, 0.72, 0.25)))
make_brezhnev(loc=(-1.2, -6, 0))
make_gronk(loc=(1.2, -6, 0))
make_brody(loc=(3.0, -6, 0))
make_jesse(loc=(4.4, -6, 0))
for k in range(3):
    make_soldier(f"Sol{k}", loc=(-3 - k * 1.1, -6, 0), seed=k)
speech_bubble("Bub", (-4.2, -6, 3.2), "ДА ДА!", size=0.5)
b = make_chalkboard(loc=(-9, -2, 0))
chalk_mark(b, "x", "X  X  X", (-1.5, 0.8), 0.5)
chalk_mark(b, "o", "O  O", (1.2, -0.6), 0.5)
chalk_arrow(b, "arr", (-1.5, 0.3), (1.0, -0.4))
make_recruit_booth(loc=(9, -2, 0), sign="NAVY")
make_tumbleweed("Tw", (6, -5, 0.5))
make_soviet_flag(loc=(-6, -4, 0), size=1.2, pole=4)
make_truck(loc=(-8, 8, 0), rot_z=10)
make_border_gate(loc=(6, 8, 0), rot_z=90)
make_sub(loc=(0, 30, 0), scale=0.7)
make_plane(loc=(20, 30, 0), rot_z=-30, scale=0.6)
make_kremlin(loc=(0, 160, 0))
m = make_map_table(loc=(-80, 0, 0))
pin("PA", m["places"]["amity"], parent=m["root"])
pin("PL", m["places"]["leningrad"], parent=m["root"])
dotted_path("Route", [m["places"]["amity"], (0, 6), m["places"]["leningrad"]], 1, 2, parent=m["root"])
cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (0, -20, 5), (0, 0, 3))
key_camera(cam, 2, (0, 60, 18), (0, 160, 20))
key_camera(cam, 3, (-80, -2, 45), (-80, 0, 0))
render(os.environ.get("JAWS_OUT", "renders/test_soviet"))
