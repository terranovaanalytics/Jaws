"""Model test (Jaws 7): nuclear sub, plane, helicopter, White House, pines,
radio + jammer, the President, the CIA agent, Russian sailors, Brody."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, box, mat, render
from jaws.spy import (make_nuke_sub, make_plane, make_helicopter, make_white_house, make_pine, make_radio,
                      make_jammer, make_president, make_agent, make_russian, open_hatch)
from jaws.people import make_brody

s = reset_scene(30, world_color=(0.45, 0.75, 1.0))
add_sun((50, 0, -30))
make_white_house(loc=(0, 70, 0))
sub = make_nuke_sub("Sub", (-6, 22, -1.0), rot_z=-170, scale=0.6)
open_hatch(sub, 1)
make_plane("Plane", (14, 10, 9), rot_z=200)
make_helicopter("Heli", (14, 4, 0), rot_z=210)
for k in range(4):
    make_pine(f"Pine{k}", (-22 + k * 3, 30, 0), h=7 + k, seed=k)
make_radio("Radio", (-9, -4, 0))
make_jammer("Jam", (-6.5, -4, 0))
make_president("P", (-3, -4, 0))
make_agent("A", (-1, -4, 0))
make_russian("R", (1, -4, 0))
make_russian("R2", (2.5, -4, 0), seed=1)
make_brody("B", (4.5, -4, 0))
add_camera((0, -24, 7), (0, 10, 4), lens=26)
s.frame_set(20)
render(os.environ.get("JAWS_OUT", "renders/test_spy"), still=True)
