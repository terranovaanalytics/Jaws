"""Test still: every puppet lined up in the storybook land."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import render, add_camera
from jaws import kids as K

K.start(1)
K.make_land(seed=2)
K.make_sun_disc()
keys = ["01", "02", "03", "04", "05", "06", "08", "09", "10", "11", "12"]
for i, k in enumerate(keys):
    row, col = divmod(i, 4)
    K.puppet(k, ((col - 1.5) * 2.6, row * 3.0, 0), height=2.3)
K.puppet("07", (6, 9, 2), height=4)
add_camera((0, -16, 4.5), (0, 3, 3.2), lens=32)
render(os.environ.get("JAWS_OUT", "renders/_lineup"), still=True)
