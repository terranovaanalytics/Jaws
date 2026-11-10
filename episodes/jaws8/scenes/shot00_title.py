"""Title card: big chunky red "JAWS 8" rises out of the ocean while a fin circles.
Plays under the intro line."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import render, FPS, shot_seconds
from jaws.title import build_title

build_title(int(shot_seconds("shot00", 5.0) * FPS), "8")
render(os.environ.get("JAWS_OUT", "renders/shot00_title"))
