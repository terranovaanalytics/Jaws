"""Shot 2: "The audience loved it. Rotten Tomatoes score 99." The old theater
showing JAWS 5, bulbs chasing, a crowd cheering out front. A giant tomato
pops in over the marquee and a critics' score spins up to 99%. (Generic
tomato and number, no real logo.)"""
import math, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, key_camera, render, FPS, shot_seconds, box, mat, text
from jaws.town import make_marquee, chase_bulbs, make_tomato, pop_in
from jaws.world import make_extra

F = int(shot_seconds("shot02", 2.9) * FPS)
reset_scene(F, world_color=(0.45, 0.75, 1.0))
add_sun((45, 0, -30), energy=2.4)
box("Street", (200, 200, 1), (0, 0, -0.5), mat("asphalt", (0.30, 0.30, 0.32)))
box("Sidewalk", (40, 6, 0.3), (0, -4, 0.15), mat("sidewalk", (0.72, 0.70, 0.66)))
for x in (-14, 14):
    box(f"Neighbor{x}", (12, 6, 9 + abs(x) * 0.1), (x, 3, 4.6), mat(f"nb{x}", (0.75, 0.68, 0.55) if x < 0 else (0.55, 0.6, 0.62)))
c = make_marquee(loc=(0, 0, 0), title="JAWS 5")
chase_bulbs(c["bulbs"], 1, F)
rnd = random.Random(2)
for i in range(16):                              # cheering crowd, hopping
    e = make_extra(f"Fan{i}", (-6.5 + i * 0.85 + rnd.uniform(-0.2, 0.2), -4.5 + rnd.uniform(-1.2, 1.2), 0.3), seed=i)
    e.rotation_euler[2] = math.radians(180 + rnd.uniform(-20, 20))
    ph = rnd.randint(0, 6)
    for f in range(1, F + 1, 3):
        e.location.z = 0.3 + (0.35 if (f // 3 + ph) % 2 else 0)
        e.keyframe_insert("location", index=2, frame=f)
POP = int(F * 0.35)
tom = make_tomato("Tomato", (-4.6, -3.2, 10.0), size=1.9)
pop_in(tom, POP - 6)
white = mat("score_white", (1, 1, 1), emit=1.2)
steps = [12, 34, 58, 77, 91, 99]
objs = []
for k, n in enumerate(steps):
    o = text(f"Score{n}", f"{n}%", (4.0, -3.2, 10.0), 2.6, white, extrude=0.25, bold=True)
    objs.append(o)
for k, o in enumerate(objs):                     # the number spins up and lands on 99
    on = POP + k * 3
    off = POP + (k + 1) * 3 if k < len(objs) - 1 else F + 1
    o.hide_render = True
    o.keyframe_insert("hide_render", frame=1)
    o.hide_render = False
    o.keyframe_insert("hide_render", frame=on)
    o.hide_render = True
    o.keyframe_insert("hide_render", frame=off)
pop_in(objs[-1], POP + 15, overshoot=1.35)
cap = text("Critics", "CRITICS", (4.0, -3.2, 8.2), 0.9, mat("score_yellow", (1, 0.9, 0.2), emit=1.0), bold=True)
pop_in(cap, POP)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=24)
key_camera(cam, 1, (0, -23, 3), (0, 0, 7.5))
key_camera(cam, F, (0, -19, 3.5), (0, 0, 8.0))
render(os.environ.get("JAWS_OUT", "renders/shot02_reviews"))
