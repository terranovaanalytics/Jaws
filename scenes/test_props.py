"""Model test: carousel, drill, pump, bait (and radar in a second still via JAWS_TEST=radar)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, box, mat, render
from jaws.props import (make_carousel, make_drill, make_pump, make_bait, make_radar,
                        radar_land, dot_line, radar_sweep)

if os.environ.get("JAWS_TEST") == "radar":
    reset_scene(1, world_color=(0.05, 0.06, 0.05))
    add_sun((60, 0, 0), energy=1.0)
    r = make_radar()
    radar_land(r, "amity", (0, 0), 1.0, 0.7, label="AMITY")
    dot_line(r, "line", (3.2, 2.2), (0.6, 0.4), 6, 1, 2)
    add_camera((0, -16, 0.8), (0, 0, 0.8), lens=35)
else:
    reset_scene(1, world_color=(0.45, 0.75, 1.0))
    add_sun((50, 0, -30))
    box("Ground", (80, 80, 1), (0, 0, -0.5), mat("grass", (0.30, 0.72, 0.25)))
    make_carousel(loc=(0, 4, 0))
    make_drill(loc=(-5, -6, 0))
    make_pump(loc=(5, -6, 0))
    make_bait(loc=(0, -9, 1))
    add_camera((0, -28, 7), (0, 0, 4), lens=30)
render(os.environ.get("JAWS_OUT", "renders/test_props"), still=True)
