"""Shot 11: "Same plan, same execution." In the cave: the mech spits out the
giant ham, the sharks pile on it; the mech zips out through the tunnel,
the dynamite blinks... KABOOM, boulders seal the entrance."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import add_camera, key_camera, add_shake, render, FPS, shot_seconds, mat, box, cyl
from jaws.shark import make_shark, swim_wag, open_jaw, chomp
from jaws.props import make_bait, explosion, blink
from jaws.world import splash
from _cave import build_cave, follow, TUNNEL

F = int(shot_seconds("shot11", 4.4) * FPS)
s, cave, store = build_cave(F)
tx, tz = TUNNEL
DROP = int(F * 0.22)
LEAVE = DROP + 14
BOOM = int(F * 0.73)
mech = make_shark("Mech", scale=2.4, variant="mech")
mech.root.location = (8, 1.6, -9.5)
mech.root.rotation_euler[2] = math.pi
mech.root.keyframe_insert("location", frame=1)
mech.root.keyframe_insert("rotation_euler", frame=1)
mech.root.location = (5, 1.6, -9.5)
mech.root.keyframe_insert("location", frame=DROP)
follow(mech.root, [(5, 1.6, -9.5), (8, 1.6, -11), (tx - 4, 1.6, tz + 0.5), (tx + 14, 1.6, tz + 1)], LEAVE, BOOM - 4)
mech.root.keyframe_insert("rotation_euler", frame=LEAVE - 2)
open_jaw(mech, DROP - 4, 0)
open_jaw(mech, DROP, 1)
open_jaw(mech, DROP + 8, 1)
open_jaw(mech, DROP + 12, 0)
swim_wag(mech, 1, F, period=12, angle=12)
ham = make_bait("Ham", loc=(3.6, 1.2, -9.8))
ham.scale = (0.001,) * 3
ham.keyframe_insert("scale", frame=DROP - 1)
ham.scale = (1.2,) * 3
for f, x, z, spin in [(DROP, 3.6, -9.8, 0), (DROP + 8, 2.8, -11.5, 50), (DROP + 22, 2.4, -14.0, 120), (F, 2.4, -14.2, 130)]:
    ham.location = (x, 1.2, z)
    ham.rotation_euler = (0, math.radians(spin), 0)
    ham.keyframe_insert("location", frame=f)
    ham.keyframe_insert("rotation_euler", frame=f)
    ham.keyframe_insert("scale", frame=f)
rnd = random.Random(11)
for i in range(10):
    sh = make_shark(f"Hungry{i}", scale=rnd.uniform(1.3, 1.6))
    a = 2 * math.pi * i / 10
    start = (-2 + math.cos(a) * 8, rnd.uniform(0, 4), -10 + math.sin(a) * 4)
    end = (2.4 + math.cos(a) * 2.2, start[1] * 0.5, -13.2 + math.sin(a) * 1.0)
    sh.root.location = start
    sh.root.rotation_euler[2] = 0 if end[0] > start[0] else math.pi
    sh.root.keyframe_insert("location", frame=1)
    sh.root.keyframe_insert("location", frame=DROP + 6 + rnd.randint(0, 6))
    sh.root.location = end
    sh.root.keyframe_insert("location", frame=DROP + 24 + rnd.randint(0, 6))
    for f in range(DROP + 30, F + 1, 4):
        sh.root.location = (end[0] + rnd.uniform(-0.5, 0.5), end[1], end[2] + rnd.uniform(-0.4, 0.4))
        sh.root.keyframe_insert("location", frame=f)
    swim_wag(sh, 1, F, period=6, angle=30, seed=i)
    chomp(sh, DROP + 20, F, period=6)
splash("Frenzy", (2.4, 1.0, -13.2), DROP + 26, count=18, size=0.4, power=5, life=30, seed=3, color=(0.8, 0.9, 1.0))
# dynamite at the tunnel mouth, then the blast and the rockfall
dyn = mat("dynamite", (0.85, 0.08, 0.08))
sticks = [cyl(f"Stick{i}", 0.3, 2.0, (tx - 1.0 + i * 0.6, -1.5, tz - 2.6), dyn, n=6) for i in range(3)]
lamp = cyl("Lamp", 0.22, 0.2, (tx - 0.4, -1.8, tz - 1.4), mat("lamp_red", (1, 0.1, 0.1), emit=5), n=6, rot=(90, 0, 0))
blink(lamp, 1, BOOM - 1, period=6, on=3)
for o in sticks:
    o.keyframe_insert("hide_render", frame=BOOM - 1)
    o.hide_render = True
    o.keyframe_insert("hide_render", frame=BOOM)
explosion("Boom", (tx, 0, tz), BOOM, size=6, count=22, life=20)
rock = mat("cave_rock", (0.28, 0.27, 0.30))
for i in range(8):
    b = box(f"Boulder{i}", [rnd.uniform(2.0, 3.0)] * 3, (0, 0, 0), rock)
    bx, bz = tx - 1 + (i % 3) * 1.6, tz - 2 + (i // 3) * 2.0
    st = BOOM + 2 + i
    b.location = (bx + rnd.uniform(-2, 2), 1.5, -1)
    b.keyframe_insert("location", frame=1)
    b.keyframe_insert("location", frame=st)
    b.location = (bx, 1.5, bz)
    b.rotation_euler = (rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1))
    b.keyframe_insert("location", frame=st + 6)
    b.keyframe_insert("rotation_euler", frame=st + 6)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (4, -28, -10), (4, 0, -11))
key_camera(cam, BOOM - 8, (6, -30, -10), (6.5, 0, -11))
key_camera(cam, F, (8, -31, -10), (8, 0, -11))
add_shake(cam, DROP + 26, BOOM - 4, strength=0.06, rot_strength=0.006)
add_shake(cam, BOOM, BOOM + 24, strength=0.6, rot_strength=0.05, seed=4)
render(os.environ.get("JAWS_OUT", "renders/shot11_same_plan"))
