"""Model test: bookstore, cinema marquee, sailboat, flag, PA pole, comic
symbols, tomato, radiation sign, Geiger counter, beakers, radioactive shark."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, box, mat, render
from jaws.town import (make_bookstore, make_marquee, make_sailboat, make_flag, make_pa_pole, bunting,
                       question_mark, light_bulb, make_tomato, music_notes)
from jaws.props import make_rad_sign, make_geiger, make_beaker
from jaws.shark import make_shark

s = reset_scene(30, world_color=(0.45, 0.75, 1.0))
add_sun((50, 0, -30))
box("Ground", (200, 200, 1), (0, 0, -0.5), mat("grass", (0.30, 0.72, 0.25)))
make_bookstore(loc=(-8, 10, 0))
make_marquee(loc=(9, 12, 0))
make_sailboat("Sail", (-10, -6, 0), rot_z=20)
make_flag(loc=(0, -2, 0), size=1.5)
make_pa_pole(loc=(4, -1, 0))
music_notes("Notes", (3.1, -2.2, 6.1), 1, 30)
bunting("Bunt", (-13, 6.4, 5), (-3, 6.4, 5))
question_mark("Q", (-2, -6, 3), 1.5)
light_bulb("Bulb", (0, -6, 3), 1.0)
make_tomato(loc=(2.5, -6, 2.8))
make_rad_sign(loc=(5.5, -6, 3), size=0.9)
g, n, w = make_geiger()
g.location = (8, -6, 3)
make_beaker("Bk", (9, -6, 1.5))
make_shark("Rad", (6, -9, 1.2), rot_z=200, scale=2.5, variant="rad")
add_camera((0, -26, 6), (0, 0, 4), lens=26)
s.frame_set(20)
render(os.environ.get("JAWS_OUT", "renders/test_town"), still=True)
