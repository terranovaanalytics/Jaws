"""Shot 11: "The Russians were just starting with Amity Island, but next it's
gonna be the whole United States." The war map over the USA: Amity's pin
pulses red, then shark fins pop up all along the coast, spreading out from
Amity in a wave, down the East Coast and round the Gulf."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, key_camera, render, FPS, shot_seconds, mat, text, cyl
from jaws.soviet import make_map_table, pin
from jaws.shark import make_shark, swim_wag
from jaws.town import pop_in

F = int(shot_seconds("shot11", 4.7) * FPS)
SPREAD = int(F * 0.42)          # "...but next it's gonna be the whole United States"
reset_scene(F, world_color=(0.12, 0.10, 0.08))
add_sun((40, 10, 30), energy=1.7)
m = make_map_table()
R = m["root"]
ax, ay = m["places"]["amity"]
p = pin("PinAmity", (ax, ay), parent=R, color=(0.9, 0.1, 0.06), size=0.7)
lm = mat("map_label", (0.10, 0.08, 0.06))
text("LblAmity", "AMITY", (ax - 1.6, ay + 1.0, 0.1), 0.6, lm, rot=(0, 0, 0), parent=R, bold=True)
from jaws.common import empty, box
ring = empty("Pulse", (ax, ay, 0.1), R)
for i in range(20):                                 # a hollow ring of red dashes
    a_ = i / 20 * 2 * math.pi
    box(f"PulseD{i}", (0.12, 0.3, 0.03), (math.cos(a_), math.sin(a_), 0), mat("pulse_red", (1.0, 0.15, 0.08),
        emit=1.5), parent=ring, rot=(0, 0, math.degrees(a_)))
for k in range(4):                                  # radar-ish pulse rings around Amity
    f0 = 2 + k * int(F / 4)
    ring.scale = (0.2, 0.2, 1)
    ring.keyframe_insert("scale", frame=f0)
    ring.scale = (3.0, 3.0, 1)
    ring.keyframe_insert("scale", frame=f0 + int(F / 4) - 1)
# fins just offshore, ordered outward from Amity: up the coast, down the coast, the Gulf
coast = [(-7.9, 5.0), (-7.0, 6.6), (-8.4, 2.4), (-9.0, 1.0), (-9.7, -0.6), (-10.1, -2.2), (-10.5, -4.0),
         (-12.0, -5.2), (-13.6, -5.4), (-15.2, -5.2), (-16.8, -5.0), (-18.4, -5.3), (-6.0, 8.0)]
coast.sort(key=lambda q: math.dist(q, (ax, ay)))
for k, (x, y) in enumerate(coast):
    sh = make_shark(f"Fin{k}", (x, y, -0.32), rot_z=(k * 47) % 360, scale=1.0)
    sh.root.parent = R
    pop_in(sh.root, SPREAD + k * 3, scale=1.0)
    swim_wag(sh, SPREAD, F, period=10, seed=k)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (ax - 1.5, ay - 9, 11), (ax - 1.5, ay - 1, 0))
key_camera(cam, SPREAD, (ax - 2.5, ay - 11, 13), (ax - 2.5, ay - 2, 0))
key_camera(cam, F, (-12.5, -14, 17), (-12.5, -1.5, 0))
render(os.environ.get("JAWS_OUT", "renders/shot11_next_us"))
