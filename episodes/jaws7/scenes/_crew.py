"""Brody, Jesse and the agent standing in the little boat (shots 11-12)."""
import math
from jaws.world import make_small_boat
from jaws.people import make_brody, make_jesse
from jaws.spy import make_agent

S = 0.8


def boat_crew(loc, rot_z):
    boat = make_small_boat("Boat", loc, rot_z=rot_z, color=(0.95, 0.95, 0.95), seed=3)
    crew = {}
    for key, fn, xy, rz in (("brody", make_brody, (-1.6, -0.45), -90), ("jesse", make_jesse, (-1.7, 0.45), -90),
                            ("agent", make_agent, (1.15, 0.0), -90)):
        p = fn(key.title(), loc=(xy[0], xy[1], 0.55), rot_z=rz)
        p.root.parent = boat
        p.root.scale = (S,) * 3
        crew[key] = p
    return boat, crew
