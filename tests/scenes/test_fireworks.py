"""Model test: dusk sky, Amity at night, fireworks barge, bursts, a fire."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
from jaws.common import reset_scene, add_camera, render
from jaws.world import make_ocean, make_island
from jaws.fireworks import dusk, make_barge, firework, fire, burst

s = reset_scene(40)
dusk(s)
make_ocean(color=(0.04, 0.12, 0.22))
make_island()
b = make_barge("Barge", (0, -85, 0), rot_z=10)
firework("FW1", (0, -85, 2), (-8, -80, 30), 1, rise=20, seed=1)
firework("FW2", (0, -85, 2), (10, -78, 36), 6, rise=18, seed=2)
burst("B3", (2, -70, 22), 26, seed=3, ring=True)
fire("Fire", (-12, -95, 0.5), 1, 40, size=1.2)
add_camera((-6, -150, 10), (0, -80, 14), lens=30)
s.frame_set(30)
render(os.environ.get("JAWS_OUT", "renders/test_fireworks"), still=True)
