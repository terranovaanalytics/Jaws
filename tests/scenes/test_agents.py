"""Test still: the Operation Cronchisk cast lineup (lib/jaws/agents.py)."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, render, box, mat
from jaws import agents as A

reset_scene(1, world_color=(0.5, 0.6, 0.75))
add_sun((55, 0, 25), energy=2.4)
box("Floor", (60, 60, 1), (0, 0, -0.5), mat("floor", (0.55, 0.55, 0.5)))
makers = [A.make_jelly, A.make_banana, A.make_twin, A.make_blip, A.make_cherry, A.make_meanie,
          A.make_pocket, A.make_carrot, A.make_director, A.make_someone, A.make_dark_cherry]
for i, mk in enumerate(makers):
    row, col = divmod(i, 6)
    p = mk(mk.__name__[5:], loc=((col - 2.5) * 1.55, row * 3.0, 0))
A.make_carrot("Disguised", loc=(4.6, 3.0, 0), disguise=True)
add_camera((0, -9, 3.0), (0, 1.5, 1.4), lens=24)
render(os.environ.get("JAWS_OUT", "renders/test_agents"), still=True)
