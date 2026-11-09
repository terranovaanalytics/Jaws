"""Model test: Chief Brody (and Jesse next to him for scale)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, box, mat, render
from jaws.people import make_brody, make_jesse
import math

reset_scene(1, world_color=(0.45, 0.72, 0.95))
add_sun((50, 0, 25))
box("Dock", (8, 8, 0.2), (0, 0, -0.1), mat("planks", (0.55, 0.40, 0.25)))
b = make_brody("Brody", loc=(-0.15, 0, 0), rot_z=-15)
b.arm_r.rotation_euler[0] = math.radians(-70)   # pointing at something offscreen
j = make_jesse("Jesse", loc=(1.0, 0.9, 0), rot_z=-30)
add_camera((0.9, -4.2, 1.6), (0.35, 0, 1.15), lens=35)
render(os.environ.get("JAWS_OUT", "renders/test_brody"), still=True)
