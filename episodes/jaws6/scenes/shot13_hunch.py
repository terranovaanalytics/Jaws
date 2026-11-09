"""Shot 13: the cave, pumped dry. Sharks flop on the floor; one is still
gnawing the wall, spitting out rock. Brody and Jesse stand in the middle of
it. "How are these sharks making caves?" A "?" pops over Jesse... then a
light bulb: he's got a hunch."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import add_camera, key_camera, render, FPS, shot_seconds, mat, box
from jaws.shark import make_shark, chomp, swim_wag
from jaws.people import make_brody, make_jesse
from jaws.town import question_mark, light_bulb, pop_in
from jaws.world import splash
from _cave import build_cave, TUNNEL

F = int(shot_seconds("shot13", 4.9) * FPS)
s, cave, store = build_cave(F, drained=True)
import bpy
for o in list(bpy.data.objects):                     # clear the floor teeth where people stand
    if o.name.startswith("Cave_tooth") and o.location.z < -10 and -9 < o.location.x < 2:
        o.hide_render = True
FLOOR = -16.0
tx, tz = TUNNEL
rock = mat("cave_rock", (0.28, 0.27, 0.30))
for i in range(6):                                   # the sealed tunnel
    box(f"Plug{i}", (2.6, 2.6, 2.6), (tx - 1 + (i % 2) * 1.8, 1.5, tz - 1.5 + (i // 2) * 2.0), rock, rot=(i * 20, i * 33, 0))
b = make_brody("Brody", loc=(-5.6, 1.0, FLOOR), rot_z=10)
j = make_jesse("Jesse", loc=(-3.2, 0.8, FLOOR), rot_z=-10)
rnd = random.Random(13)
for i, (x, y) in enumerate([(-8, 2.5), (3, 2.8), (6.5, 1.5), (-10.5, 1.2)]):   # stranded, flopping
    sh = make_shark(f"Flop{i}", (x, y, FLOOR + 0.35), rot_z=rnd.uniform(0, 360), scale=1.5)
    for f in range(1, F + 1, 4):
        sh.root.rotation_euler[0] = math.radians(70 + (25 if (f // 4 + i) % 2 else -10))
        sh.root.keyframe_insert("rotation_euler", index=0, frame=f)
    swim_wag(sh, 1, F, period=6, angle=35, seed=i)
box("Pillar", (1.6, 3.0, 12), (-10.4, 2.6, -10), mat("dirt", (0.50, 0.33, 0.20)))
g = make_shark("Gnawer", (-8.4, 2.6, -11.5), scale=1.7)  # still digging at the left wall
g.root.rotation_euler[2] = math.pi
chomp(g, 1, F, period=6)
swim_wag(g, 1, F, period=8, angle=20)
for k in range(5):
    splash(f"Chips{k}", (-9.6, 2.2, -11.5), 4 + k * 22, count=8, size=0.25, power=4, life=18, seed=k,
           color=(0.5, 0.33, 0.2))
Q = int(F * 0.41)
H = int(F * 0.78)
q = question_mark("Huh", (-3.2, 0.4, FLOOR + 3.4), 1.8)
pop_in(q, Q, out_frame=H)
bulb = light_bulb("Idea", (-3.2, 0.4, FLOOR + 3.7), 1.2)
bulb.rotation_euler[0] = math.radians(90) * 0
pop_in(bulb, H)
for p, yaw in ((b, 25), (j, -15)):                  # looking around at the walls
    for f, y in ((1, 0), (int(F * 0.3), yaw), (Q, -yaw)):
        p.head.rotation_euler[2] = math.radians(y)
        p.head.keyframe_insert("rotation_euler", index=2, frame=f)
j.head.rotation_euler = (math.radians(-10), 0, 0)
j.head.keyframe_insert("rotation_euler", frame=H)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (-5, -21, -10), (-5, 0, -12))
key_camera(cam, F, (-5, -14, -12.4), (-5, 0, -13.2))
render(os.environ.get("JAWS_OUT", "renders/shot13_hunch"))
