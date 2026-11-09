"""Shared set for shots 6-7: the giant Russian nuclear sub hanging in the
dark deep water, a glowing green bay open in its side. Not a shot itself."""
from jaws.common import box, mat
from jaws.spy import make_nuke_sub
from _sets import deep, glow_light

SUB = (40, 50, -6)
SCALE = 2.0
BAY = (SUB[0] - 16, SUB[1] - 6.2, SUB[2] - 1)        # world spot of the shark bay door


def build_deepsub(F, lights_on=1, flood=200000):
    s = deep(F, color=(0.01, 0.05, 0.07), start=10, depth=85, floor_z=-40)
    sub = make_nuke_sub("Sub", SUB, rot_z=0, scale=SCALE)
    bay = box("Bay", (5, 0.3, 3), (-8, -3.0, -0.5), mat("bay_glow", (0.45, 1.0, 0.3), emit=4.0), parent=sub["root"])
    lights = [glow_light("BayLight", (BAY[0], BAY[1] - 4, BAY[2]), (0.45, 1.0, 0.3), 30000, radius=4),
              glow_light("SubFlood", (SUB[0] + 10, SUB[1] - 25, SUB[2] + 12), (0.8, 0.9, 1.0), flood, radius=6)]
    for L in lights:
        e = L.data.energy
        L.data.energy = 0
        L.data.keyframe_insert("energy", frame=max(1, lights_on - 1))
        L.data.energy = e
        L.data.keyframe_insert("energy", frame=lights_on)
    return s, sub
