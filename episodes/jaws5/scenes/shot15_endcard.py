"""End card over "...and that leads us to Jaws 6": JAWS 6, COMING SOON."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import render, FPS, shot_seconds
from jaws.title import build_title

build_title(int(shot_seconds("shot15", 3.5) * FPS), "6", subtitle="COMING SOON")
render(os.environ.get("JAWS_OUT", "renders/shot15_endcard"))
