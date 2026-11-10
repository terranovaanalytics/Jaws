"""End card: JAWS 9, COMING SOON."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import render, FPS, shot_seconds
from jaws.title import build_title

build_title(int(shot_seconds("shot13", 2.5) * FPS), "9", subtitle="COMING SOON")
render(os.environ.get("JAWS_OUT", "renders/shot13_endcard"))
