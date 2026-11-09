"""End card: JAWS 7, COMING SOON."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import render, FPS, shot_seconds
from jaws.title import build_title

build_title(int(shot_seconds("shot17", 2.6) * FPS), "7", subtitle="COMING SOON")
render(os.environ.get("JAWS_OUT", "renders/shot17_endcard"))
