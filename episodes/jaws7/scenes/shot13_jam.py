"""Shot 13: "But first, they jam the radios, so Russia has no idea." Inside
the sub's radio room: a big radio labelled MOSCOW. Jesse sets a homemade
jammer on the desk, its dish swings round, red light blinking; the radio's
dial dies and spits static. Question marks pop up over it."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import reset_scene, add_sun, add_camera, key_camera, render, FPS, shot_seconds, box, mat, text
from jaws.people import make_jesse
from jaws.props import blink
from jaws.spy import make_radio, make_jammer, static_burst
from jaws.town import question_mark, pop_in
from _sets import face, glow_light

F = int(shot_seconds("shot13", 3.9) * FPS)
reset_scene(F, world_color=(0.1, 0.12, 0.1))
add_sun((60, 0, 20), energy=0.8)
wall = mat("sub_room", (0.30, 0.36, 0.30))
box("Floor", (12, 10, 0.2), (0, 0, -0.1), mat("sub_floor", (0.20, 0.20, 0.20)))
box("BackWall", (12, 0.3, 5), (0, 2.6, 2.5), wall)
box("SideWall", (0.3, 10, 5), (-4, 0, 2.5), wall)
for k in range(5):
    box(f"Pipe{k}", (12, 0.2, 0.2), (0, 2.35, 3.0 + k * 0.35), mat("sub_pipe", (0.55, 0.45, 0.25), metal=0.6, rough=0.5))
box("Desk", (4.5, 1.6, 0.9), (0, 1.5, 0.45), mat("sub_desk", (0.25, 0.27, 0.25)))
glow_light("Bulb", (0, 0, 3.8), (1.0, 0.9, 0.7), 350, radius=0.5)
r = make_radio("Radio", (-0.6, 1.5, 0.9))
text("RadioLbl", "MOSCOW", (-0.6, 0.97, 2.15), 0.32, mat("radio_lbl", (0.7, 0.08, 0.06)), bold=True)
JAM = int(F * 0.30)                           # "they jam the radios"
NOIDEA = int(F * 0.66)                        # "so Russia has no idea"
w = r["window"]
w.keyframe_insert("hide_render", frame=1)
blink(w, JAM, JAM + 12, period=4, on=2)
w.hide_render = True
w.keyframe_insert("hide_render", frame=JAM + 14)
jm = make_jammer("Jammer", (1.4, 1.3, 0.9))
pop_in(jm["root"], JAM - 8)
blink(jm["light"], JAM, F, period=6, on=3)
static_burst("Static", r["speaker"], JAM + 4, F, every=3, life=8)
j = make_jesse("Jesse", loc=(2.1, 0.3, 0), rot_z=-50)
face(j.arm_r, JAM - 10, 0, axis=0)
face(j.arm_r, JAM - 4, -70, axis=0)
face(j.arm_r, JAM + 8, -10, axis=0)
for k in range(3):
    q = question_mark(f"Q{k}", (-1.3 + k * 0.7, 0.9, 2.9 + (k % 2) * 0.3), size=0.75)
    qm = mat("q_red", (0.9, 0.12, 0.08), emit=1.5)
    qm.shadow_method = "NONE"
    q.data.materials[0] = qm
    q.scale = (0.001,) * 3
    q.keyframe_insert("scale", frame=1)
    pop_in(q, NOIDEA + k * 3)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=28)
key_camera(cam, 1, (1.0, -5.8, 2.4), (0.7, 1.5, 1.7))
key_camera(cam, F, (0.8, -4.8, 2.3), (0.5, 1.5, 1.9))
render(os.environ.get("JAWS_OUT", "renders/shot13_jam"))
