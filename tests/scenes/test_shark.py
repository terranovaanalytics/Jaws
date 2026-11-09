"""Model test: great white (jaw open) + mech sub behind it."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, box, mat, render
from jaws.shark import make_shark, open_jaw

reset_scene(1, world_color=(0.35, 0.65, 0.92))
add_sun((55, 0, 40))
box("Floor", (40, 40, 0.1), (0, 0, -1.2), mat("sand", (0.93, 0.83, 0.55)))
s = make_shark("Shark", loc=(0.3, 0, 0.6), rot_z=-35)
open_jaw(s, 1, 1.0)
m = make_shark("MechShark", loc=(-0.3, 2.4, 1.5), rot_z=-150, variant="mech", scale=0.9)
open_jaw(m, 1, 0.3)
add_camera((1.6, -4.6, 1.3), (0.0, 0.9, 0.95), lens=32)
render(os.environ.get("JAWS_OUT", "renders/test_shark"), still=True)
