"""Shot 6: "And the plan is, make every American scared to go in the water.
Nobody joins the Navy. Nobody joins the Coast Guard." The chalkboard, coach
style: O's on the beach, X's (sharks) in the water, arrows sending every O
running inland. Cut to the beach: empty Navy and Coast Guard recruiting
booths, a tumbleweed, fins circling offshore."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import reset_scene, add_sun, add_camera, key_camera, render, FPS, shot_seconds, box, mat
from jaws.world import make_ocean, make_gull, flap
from jaws.shark import make_shark, swim_wag
from jaws.soviet import chalk_mark, chalk_arrow, make_recruit_booth, make_tumbleweed, roll
from _interior import build_war_room, ROOM

F = int(shot_seconds("shot06", 6.7) * FPS)
CUT = int(F * 0.56)             # "Nobody joins the Navy."
reset_scene(F, world_color=(0.75, 0.72, 0.62))
add_sun((62, 0, 30), energy=1.6)
# --- the board
room = build_war_room()
bd, z = room["board"], room["brezhnev"]
X, Y, Z = ROOM
chalk_mark(bd, "title", "THE PLAN", (0, 1.12), 0.36, frame=2)
chalk_mark(bd, "water", "~  ~  ~  ~  ~  ~", (0, -0.15), 0.5, frame=4)
chalk_mark(bd, "beach", "BEACH", (-1.6, 0.55), 0.22, frame=4)
chalk_mark(bd, "sea", "OCEAN", (-1.6, -0.95), 0.22, frame=4)
for k in range(4):                                  # the Americans
    chalk_mark(bd, f"o{k}", "O", (-0.9 + k * 0.75, 0.35), 0.42, frame=int(F * 0.08) + k * 2)
for k in range(5):                                  # the sharks
    chalk_mark(bd, f"x{k}", "X", (-1.2 + k * 0.65, -0.75), 0.42, frame=int(F * 0.16) + k * 2,
               color=(0.95, 0.30, 0.25))
for k in range(4):                                  # everybody runs away from the water
    x = -0.9 + k * 0.75
    chalk_arrow(bd, f"run{k}", (x, 0.6), (x + (k - 1.5) * 0.2, 0.85), frame=int(F * 0.30) + k * 3)
z.arm_r.rotation_euler = (math.radians(-100), 0, math.radians(-50))
for k, f in enumerate(range(int(F * 0.08), CUT, 8)):  # tap tap tap at the board
    z.arm_r.rotation_euler[0] = math.radians(-100 if k % 2 else -85)
    z.arm_r.keyframe_insert("rotation_euler", index=0, frame=f)
z.head.rotation_euler[2] = math.radians(-50)
# --- the beach, nobody enlisting
make_ocean(color=(0.10, 0.35, 0.50))
box("Sand", (200, 32, 1), (0, -4, 0.0), mat("beach", (0.95, 0.86, 0.58)))
make_recruit_booth("Navy", (-2.2, 6, 0.5), rot_z=8, sign="NAVY")
make_recruit_booth("CoastGuard", (2.6, 7.5, 0.5), rot_z=-8, sign="COAST GUARD", color=(0.85, 0.30, 0.12))
tw = make_tumbleweed("Tumble", (0, 0, 0), size=0.7)
roll(tw, (-9, 3.2, 1.0), (9, 2.6, 1.0), CUT, F + 10, radius=0.7, hops=4, hop_h=0.5)
for k in range(3):                                  # fins circling offshore
    sh = make_shark(f"Fin{k}", scale=3.0)
    for f in range(CUT - 2, F + 1, 3):
        a = f / FPS * 0.7 + k * 2.1
        sh.root.location = (-2 + 9 * math.cos(a), 17 + 3 * math.sin(a), -1.3)
        sh.root.rotation_euler[2] = a + math.pi / 2
        sh.root.keyframe_insert("location", frame=f)
        sh.root.keyframe_insert("rotation_euler", index=2, frame=f)
    swim_wag(sh, CUT, F, period=12, seed=k)
g, w = make_gull("Gull", (-6, 10, 7))
g.keyframe_insert("location", frame=CUT)
g.location.x = 8
g.keyframe_insert("location", frame=F)
flap(w, CUT, F)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=30)
bx, by, bz = X + 1.8, Y + 3.2, Z + bd["cz"]
key_camera(cam, 1, (bx - 0.4, by - 6.4, bz + 0.1), (bx - 0.1, by, bz - 0.1))
key_camera(cam, CUT - 1, (bx - 0.2, by - 5.9, bz + 0.1), (bx - 0.1, by, bz))
key_camera(cam, CUT, (0.5, -8, 2.4), (0.3, 8, 2.4))
key_camera(cam, F, (0.4, -6.5, 2.3), (0.3, 8, 2.3))
for fc in cam.animation_data.action.fcurves:
    for kp in fc.keyframe_points:
        if int(kp.co[0]) == CUT - 1:
            kp.interpolation = "CONSTANT"
render(os.environ.get("JAWS_OUT", "renders/shot06_plan"))
