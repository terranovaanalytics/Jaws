"""Shot 1: "Jaws 5 and Jaws 6 had nearly perfect audience scores, but Jaws 6
took a hit with the critics. One guy said, 'it's just Jaws 5 but under a
bookstore.'" The theater again, JAWS 6 on the marquee, the crowd hopping.
Two popcorn buckets pop up with audience scores; then a tomato splats and the
critics' number tumbles; then a critic's quote card slams in. (Generic
popcorn, tomato and numbers: no real logos.)"""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import reset_scene, add_sun, add_camera, key_camera, add_shake, render, FPS, shot_seconds, box, cyl, ico, mat, text, empty
from jaws.town import make_marquee, chase_bulbs, make_tomato, pop_in
from jaws.world import make_extra

F = int(shot_seconds("shot01", 7.7) * FPS)
reset_scene(F, world_color=(0.45, 0.75, 1.0))
add_sun((45, 0, -30), energy=2.4)
box("Street", (200, 200, 1), (0, 0, -0.5), mat("asphalt", (0.30, 0.30, 0.32)))
box("Sidewalk", (40, 6, 0.3), (0, -4, 0.15), mat("sidewalk", (0.72, 0.70, 0.66)))
for x in (-14, 14):
    box(f"Neighbor{x}", (12, 6, 9 + abs(x) * 0.1), (x, 3, 4.6), mat(f"nb{x}", (0.75, 0.68, 0.55) if x < 0 else (0.55, 0.6, 0.62)))
c = make_marquee(loc=(0, 0, 0), title="JAWS 6")
chase_bulbs(c["bulbs"], 1, F)
CRIT = int(F * 0.52)          # "...took a hit with the critics"
QUOTE = int(F * 0.66)         # "One guy said..."
rnd = random.Random(2)
for i in range(16):                              # cheering crowd, hopping (until the critics)
    e = make_extra(f"Fan{i}", (-6.5 + i * 0.85 + rnd.uniform(-0.2, 0.2), -4.5 + rnd.uniform(-1.2, 1.2), 0.3), seed=i)
    e.rotation_euler[2] = math.radians(180 + rnd.uniform(-20, 20))
    ph = rnd.randint(0, 6)
    for f in range(1, F + 1, 3):
        e.location.z = 0.3 + (0.35 if (f // 3 + ph) % 2 and f < CRIT else 0)
        e.keyframe_insert("location", index=2, frame=f)


def popcorn(name, loc, size=1.0):
    root = empty(name, loc)
    red = mat("pop_red", (0.85, 0.12, 0.10), emit=0.4)
    white = mat("pop_white", (0.96, 0.95, 0.9), emit=0.4)
    for k in range(8):                           # striped tub (alternating panels)
        a = k * math.pi / 4
        p = box(f"{name}_p{k}", (0.62 * size, 0.1 * size, 1.5 * size),
                (0.75 * size * math.cos(a), 0.75 * size * math.sin(a), 0), red if k % 2 else white, parent=root)
        p.rotation_euler = (0, 0, a + math.pi / 2)
    corn = mat("pop_corn", (1.0, 0.92, 0.6), emit=0.6)
    r2 = random.Random(len(name))
    for k in range(14):
        ico(f"{name}_c{k}", 0.24 * size, (r2.uniform(-0.6, 0.6) * size, r2.uniform(-0.6, 0.6) * size,
            (0.8 + r2.uniform(0, 0.5)) * size), corn, parent=root, subdiv=0)
    return root


white = mat("score_white", (1, 1, 1), emit=1.2)
yellow = mat("score_yellow", (1, 0.9, 0.2), emit=1.0)
for k, (lbl, n, x) in enumerate((("JAWS 5", "99%", -4.2), ("JAWS 6", "98%", 4.2))):
    f0 = int(F * (0.06 + k * 0.14))
    tub = popcorn(f"Pop{k}", (x, -3.2, 12.6), 1.1)
    pop_in(tub, f0, out_frame=CRIT)
    num = text(f"PopN{k}", n, (x, -3.2, 10.4), 2.2, white, extrude=0.2, bold=True)
    pop_in(num, f0 + 3, out_frame=CRIT)
    lab = text(f"PopL{k}", lbl, (x, -3.2, 8.9), 0.9, yellow, bold=True)
    pop_in(lab, f0 + 3, out_frame=CRIT)
aud = text("AudLbl", "AUDIENCE", (0, -3.2, 15.2), 1.3, yellow, extrude=0.1, bold=True)
pop_in(aud, int(F * 0.04), out_frame=CRIT)

# the critics: tomato thuds in, the score tumbles 98 -> 41
tom = make_tomato("Tomato", (-4.0, -3.2, 12.0), size=1.9)
pop_in(tom, CRIT, out_frame=QUOTE)
steps = [98, 90, 77, 63, 52, 41]
objs = [text(f"Crit{n}", f"{n}%", (3.6, -3.2, 12.0), 2.6, white, extrude=0.25, bold=True) for n in steps]
for k, o in enumerate(objs):
    on = CRIT + 2 + k * 3
    off = CRIT + 2 + (k + 1) * 3 if k < len(objs) - 1 else QUOTE
    o.hide_render = True
    o.keyframe_insert("hide_render", frame=1)
    o.hide_render = False
    o.keyframe_insert("hide_render", frame=on)
    o.hide_render = True
    o.keyframe_insert("hide_render", frame=off)
cl = text("CritLbl", "CRITICS", (3.6, -3.2, 10.0), 0.9, yellow, bold=True)
pop_in(cl, CRIT, out_frame=QUOTE)

# one guy's review, on a newspaper-ish card
card = empty("Quote", (0, -4.0, 11.6))
box("QuoteCard", (9.6, 0.2, 5.2), (0, 0, 0), mat("quote_paper", (0.96, 0.94, 0.86), emit=0.7), parent=card)
box("QuoteBar", (9.6, 0.25, 0.7), (0, -0.02, 2.2), mat("quote_red", (0.75, 0.1, 0.1), emit=0.6), parent=card)
ink = mat("quote_ink", (0.05, 0.05, 0.05))
text("QuoteHead", "THE CRITIC SAYS", (0, -0.18, 2.2), 0.5, mat("quote_white", (1, 1, 1), emit=1.0), bold=True, parent=card)
for k, line in enumerate(('"IT\'S JUST JAWS 5', 'BUT UNDER', 'A BOOKSTORE."')):
    text(f"QuoteL{k}", line, (0, -0.15, 1.05 - k * 1.05), 0.85, ink, bold=True, parent=card)
text("QuoteBy", "- ONE GUY", (2.4, -0.15, -2.1), 0.5, ink, bold=True, parent=card)
pop_in(card, QUOTE, overshoot=1.15)
card.rotation_euler = (0, math.radians(3), 0)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=24)
key_camera(cam, 1, (0, -23, 3), (0, 0, 8.0))
key_camera(cam, F, (0, -19.5, 3.5), (0, 0, 8.5))
add_shake(cam, CRIT, CRIT + 6, strength=0.25, rot_strength=0.02)
render(os.environ.get("JAWS_OUT", "renders/shot01_reviews"))
