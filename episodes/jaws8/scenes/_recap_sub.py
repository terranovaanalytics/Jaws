"""PLACEHOLDER clip for the recap ("you know about the Russian nuclear sub"):
the placeholder Soviet sub glides past underwater. Swap for real Jaws 7
footage once it exists (see shot01_recap.py). Not a shot itself: render it
before shot01 with  tools/render.sh episodes/jaws8/scenes/_recap_sub.py"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import reset_scene, add_camera, key_camera, linear_keys, render, FPS
from jaws.props import underwater
from jaws.soviet import make_sub

F = int(3.0 * FPS)
s = reset_scene(F)
underwater(s, color=(0.04, 0.18, 0.30), start=10, depth=70)
sub = make_sub("Sub", (-26, 18, -8), rot_z=0, scale=1.0)
sub["root"].keyframe_insert("location", frame=1)
sub["root"].location.x = 12
sub["root"].keyframe_insert("location", frame=F)
linear_keys(sub["root"])
cam = add_camera((0, 0, 0), (0, 0, 0), lens=24)
key_camera(cam, 1, (-8, -6, -9), (-14, 18, -6))
key_camera(cam, F, (-2, -4, -9), (4, 18, -6))
render(os.environ.get("JAWS_OUT", "renders/_recap_sub"))
