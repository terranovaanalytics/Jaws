"""Shot 15: "Radioactive mutant sharks the whole time. But where are they
coming from?" Underwater, murky green: a swarm of glowing sharks streams
past; the camera tilts down to a crack in the sea floor glowing green."""
import math, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import bpy
from jaws.common import reset_scene, add_camera, key_camera, linear_keys, render, FPS, shot_seconds, box, mat
from jaws.props import underwater
from jaws.shark import make_shark, swim_wag

F = int(shot_seconds("shot15", 4.1) * FPS)
s = reset_scene(F)
underwater(s, color=(0.03, 0.15, 0.13), start=8, depth=60)
rnd = random.Random(15)
for i in range(32):
    sh = make_shark(f"Mutant{i}", scale=rnd.uniform(1.8, 2.6), variant="rad")
    y = rnd.uniform(4, 26)
    z = rnd.uniform(-12, -3)
    x0 = rnd.uniform(-30, 4)
    v = rnd.uniform(6, 9)
    for f in (1, F):
        sh.root.location = (x0 + v * (f - 1) / FPS, y, z + 0.5 * math.sin(i))
        sh.root.keyframe_insert("location", frame=f)
    linear_keys(sh.root)
    swim_wag(sh, 1, F, period=10, angle=24, seed=i)
glow = mat("crack_glow", (0.45, 1.0, 0.3), emit=4.0)
dark = mat("crack_dark", (0.02, 0.05, 0.03))
for k in range(9):                                  # zig-zag crack
    x = -12 + k * 3
    box(f"Crack{k}", (3.4, 1.0, 0.1), (x, 14 + (2 if k % 2 else -2) * 0.5, -19.95), glow, rot=(0, 0, 30 if k % 2 else -30))
    box(f"Lip{k}", (3.6, 0.6, 0.6), (x, 13 + (2 if k % 2 else -2) * 0.5, -19.8), dark, rot=(0, 0, 30 if k % 2 else -30))
d = bpy.data.lights.new("CrackLight", "POINT")
d.color, d.energy = (0.45, 1.0, 0.3), 6000
o = bpy.data.objects.new("CrackLight", d)
o.location = (0, 14, -17)
s.collection.objects.link(o)
for f in range(1, F + 1, 4):
    d.energy = 5000 + 2000 * math.sin(f / 5)
    d.keyframe_insert("energy", frame=f)
T = int(F * 0.6)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (0, -18, -7), (0, 10, -7))
key_camera(cam, T, (0, -16, -7), (0, 10, -8))
key_camera(cam, F, (0, -4, -8), (0, 14, -20))
render(os.environ.get("JAWS_OUT", "renders/shot15_mutants"))
