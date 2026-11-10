"""Shot 4: "American soldiers dressed up as Russians. Plus, that one Russian
guy who speaks Russian so the Russians don't know what's up." Leningrad dock
at grey dusk: Brody's team marches in wearing ushankas and glued-on
mustaches (and white sneakers). Their one real Russian (the sailor kept on board in Jaws 7) chats up the two
real guards in nonsense Cyrillic; the guards nod along."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, key_camera, render, FPS, shot_seconds, box, mat
from jaws.world import make_ocean
from jaws.people import make_brody, walk
from jaws.soviet import make_soldier, make_sub, speech_bubble, make_soviet_flag, _hat_ushanka
from jaws.town import pop_in
from jaws.spy import make_russian

F = int(shot_seconds("shot04", 6.1) * FPS)
STOP = int(F * 0.38)            # they halt in front of the guards
TALK = int(F * 0.43)            # "Plus, that one Russian guy..."
NOD = int(F * 0.72)             # "...so the Russians don't know what's up"
reset_scene(F, world_color=(0.55, 0.58, 0.62))
add_sun((62, 0, -40), energy=1.6, color=(0.95, 0.95, 1.0))
make_ocean(color=(0.10, 0.22, 0.30))
stone = mat("dock_stone", (0.50, 0.50, 0.48))
box("Quay", (80, 30, 3), (0, 14, 0), stone)
# Leningrad facades: pastel palaces along the back of the quay
cols = [(0.90, 0.78, 0.45), (0.55, 0.70, 0.62), (0.85, 0.60, 0.55), (0.80, 0.80, 0.70)]
win = mat("pal_win", (0.25, 0.28, 0.32))
white = mat("pal_trim", (0.92, 0.92, 0.88))
for k in range(6):
    x = -30 + k * 12
    h = 12 + (k % 3) * 2
    box(f"Pal{k}", (11.6, 6, h), (x, 26, 1.5 + h / 2), mat(f"pal{k}", cols[k % 4]))
    box(f"PalTrim{k}", (11.8, 6.2, 0.5), (x, 26, 1.5 + h), white)
    for r in range(3):
        for c in range(4):
            box(f"PalW{k}{r}{c}", (1.2, 0.1, 1.8), (x - 4.2 + c * 2.8, 22.95, 4.5 + r * 3.6), win)
make_soviet_flag("Flag", (6, 8, 1.5), size=1.6, pole=7)
sub = make_sub("Sub", (-24, -8, 0), rot_z=10, scale=0.9)
Z = 1.5
team = []
b = make_brody("Brody", loc=(-9, 4, Z), rot_z=90)
_hat_ushanka(b, "Brody")
team.append(b)
for k in range(3):
    team.append(make_soldier(f"Sol{k}", loc=(-10.0 - k * 1.0, 4.6 - (k % 2) * 0.9, Z), rot_z=90, seed=k))
spk = make_russian("Speaker", loc=(-7.6, 3.4, Z), rot_z=90, stache=True)  # the Russian sailor kept from Jaws 7
team.append(spk)
for k, p in enumerate(team):
    walk(p, 1, STOP, period=12)
    for limb in (p.leg_l, p.leg_r, p.arm_l, p.arm_r):          # stand still once they stop
        limb.rotation_euler[0] = 0
        limb.keyframe_insert("rotation_euler", index=0, frame=STOP + 4)
    p.root.keyframe_insert("location", index=0, frame=1)
    p.root.location.x += 6.5
    p.root.keyframe_insert("location", index=0, frame=STOP)
    p.root.rotation_euler[2] = 0
    p.root.keyframe_insert("rotation_euler", index=2, frame=STOP + 4)
    p.root.rotation_euler[2] = math.radians(90)
    p.root.keyframe_insert("rotation_euler", index=2, frame=STOP)
    p.head.rotation_euler[2] = math.radians(50)               # shifty sideways glances at the guards
    p.head.keyframe_insert("rotation_euler", index=2, frame=STOP + 6)
spk.root.rotation_euler[2] = math.radians(55)
spk.root.keyframe_insert("rotation_euler", index=2, frame=STOP + 4)
guards = [make_soldier(f"Guard{k}", loc=(1.6 + k * 1.3, 2.6 + k * 0.6, Z), rot_z=-40, seed=k + 7, disguise=False,
                       coat=(0.36, 0.37, 0.40)) for k in range(2)]      # real guards: grey coats
for k, g in enumerate(guards):                      # nod nod nod
    f = NOD + k * 2
    while f < F - 2:
        g.head.rotation_euler[0] = 0
        g.head.keyframe_insert("rotation_euler", index=0, frame=f)
        g.head.rotation_euler[0] = math.radians(18)
        g.head.keyframe_insert("rotation_euler", index=0, frame=f + 4)
        f += 8
bub = speech_bubble("Bubble", (0.2, 2.6, Z + 3.4), "ДА, ТОВАРИЩ!\n"
                    "ВСЁ ХОРОШО!", size=0.5)
pop_in(bub, TALK)
spk.arm_r.keyframe_insert("rotation_euler", frame=TALK)
for k in range(4):                                  # chatty hand
    spk.arm_r.rotation_euler = (math.radians(-60 if k % 2 == 0 else -30), 0, 0)
    spk.arm_r.keyframe_insert("rotation_euler", frame=TALK + 6 + k * 7)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=22)
key_camera(cam, 1, (-4.0, -7.0, Z + 1.8), (-3.2, 4, Z + 2.4))
key_camera(cam, STOP, (-1.6, -5.0, Z + 1.6), (-1.2, 4, Z + 2.2))
key_camera(cam, F, (0.8, -2.6, Z + 1.6), (0.8, 4, Z + 2.5))
render(os.environ.get("JAWS_OUT", "renders/shot04_disguise"))
