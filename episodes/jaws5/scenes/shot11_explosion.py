"""Shot 11: outside the cave mouth. The mech sub zips away, the dynamite
blinks... KABOOM. Boulders crash down and seal the entrance."""
import math, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import (reset_scene, add_camera, key_camera, add_shake, linear_keys, render, FPS,
                         shot_seconds, box, cyl, mat)
from jaws.props import underwater, explosion, blink
from jaws.shark import make_shark, swim_wag

F = int(shot_seconds("shot11", 6.0) * FPS)
s = reset_scene(F)
underwater(s, start=10, depth=60)

rnd = random.Random(11)
rock = mat("wall_rock", (0.40, 0.38, 0.40))
dark = mat("tunnel_dark", (0.01, 0.03, 0.06))
# rock wall with a tunnel mouth (dark hole) at x=0, z=-14
for i in range(40):
    x, z = rnd.uniform(-22, 22), rnd.uniform(-20, 4)
    if abs(x) < 3.2 and -18 < z < -10:
        continue
    sz = rnd.uniform(3, 6)
    box(f"Wall{i}", (sz, 4, sz), (x, 4 + rnd.uniform(-1, 1), z), rock, rot=(0, rnd.uniform(0, 45), 0))
box("Hole", (6.4, 1, 8), (0, 6.5, -14), dark)
# dynamite bundle with a blinking red light
dyn = mat("dynamite", (0.85, 0.08, 0.08))
for i in range(3):
    cyl(f"Stick{i}", 0.3, 2.0, (-0.6 + i * 0.6, 1.8, -17.6), dyn, n=6)
lamp = cyl("Lamp", 0.22, 0.2, (0, 1.5, -16.4), mat("lamp_red", (1, 0.1, 0.1), emit=5), n=6, rot=(90, 0, 0))
BOOM = max(10, int(F * 0.35))
blink(lamp, 1, BOOM - 1, period=8, on=4)
for o in ("Stick0", "Stick1", "Stick2"):
    ob = s.objects[o]
    ob.keyframe_insert("hide_render", frame=BOOM - 1)
    ob.hide_render = True
    ob.keyframe_insert("hide_render", frame=BOOM)

mech = make_shark("Mech", scale=2.4, variant="mech")
mech.root.rotation_euler[2] = math.radians(-95)
for f, loc in [(1, (0.5, 3, -14)), (BOOM - 4, (1.5, -20, -11)), (F, (2, -40, -9))]:
    mech.root.location = loc
    mech.root.keyframe_insert("location", frame=f)
swim_wag(mech, 1, F, period=8, angle=14)

explosion("Boom", (0, 1.5, -15), BOOM, size=7, count=24, life=22)
# boulders tumble down and plug the hole
for i in range(9):
    b = box(f"Boulder{i}", [rnd.uniform(2.2, 3.4)] * 3, (0, 0, 0), rock)
    tx, tz = (i % 3 - 1) * 2.2 + rnd.uniform(-0.3, 0.3), -17 + (i // 3) * 2.4
    start = BOOM + 2 + i
    b.location = (tx + rnd.uniform(-2, 2), 2.5, 8 + i)
    b.keyframe_insert("location", frame=1)
    b.keyframe_insert("location", frame=start)
    b.keyframe_insert("rotation_euler", frame=start)
    b.location = (tx, 2.5, tz)
    b.rotation_euler = (rnd.uniform(-2, 2), rnd.uniform(-2, 2), rnd.uniform(-2, 2))
    b.keyframe_insert("location", frame=start + 7)
    b.keyframe_insert("rotation_euler", frame=start + 7)
    b.location.z = tz + 0.6                      # little bounce
    b.keyframe_insert("location", frame=start + 9)
    b.location.z = tz
    b.keyframe_insert("location", frame=start + 11)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (-3, -24, -12), (0, 3, -14))
key_camera(cam, F, (-2, -19, -12.5), (0, 3, -14.5))
add_shake(cam, BOOM, BOOM + 30, strength=0.6, rot_strength=0.05)
render(os.environ.get("JAWS_OUT", "renders/shot11_explosion"))
