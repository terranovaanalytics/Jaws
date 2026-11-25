"""Shot 06: the lab vault. The Twins eat through the steel door, chomp by chomp."""
import os, sys
os.environ.setdefault("JAWS_LOOK", "sunny")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import math
from jaws.common import render, add_camera, key_camera, add_shake, FPS, shot_seconds, mat, box, cyl, ico, empty, text
from jaws import agents as A, ops as O
import sets as S

F = int(shot_seconds("shot06_vault", 4.5) * FPS)
S.lab_int(F)
v = O.make_vault_door("Vault", (0, 5.2, 0), r=2.0)
twins = [A.make_twin(f"Twin{s}", (s * 0.75, 3.2, 0), rot_z=180 - s * 15) for s in (-1, 1)]
times = [int(F * t / 4.5) for t in (1.0, 1.6, 2.2, 2.8)]
order = [0, 4, 1, 5, 2, 6, 3, 7]
for i, f in enumerate(times):
    for k, t in enumerate(twins):
        ff = f + k * 3
        A.lean(t, ff - 1, 32, frames=4)
        A.lean(t, ff + 5, 0, frames=5)
        O.hide_at(v["chunks"][order[i * 2 + k]], ff)
    w = text(f"Chomp{i}", "CHOMP!", ((-1) ** i * 0.7, 2.8, 4.5 + (i % 2) * 0.4), 0.5,
             mat("chomp_txt", (1.0, 0.85, 0.1), emit=2.0), bold=True, extrude=0.06, rot=(90, 0, 25))
    O.show_at(w, f, f + 10)
CL = int(F * 3.6 / 4.5)
hub = v["hub"]
O.move(hub, CL - 4, CL + 4, tuple(hub.location), (0, -1.2, 0.3))
for t in twins:
    A.look(t, CL + 8, 0, tilt=-15)
    A.arm(t, "r", CL + 10, -30)
O.point_light("VaultGlow", (0, 6.5, 2.2), 0, (1.0, 0.85, 0.4), radius=1, shadow=False)
cam = add_camera((4.5, -2, 2.4), (0, 4, 2.0), lens=30)
key_camera(cam, 1, (4.8, -2.4, 2.3), (0, 4.2, 2.1))
key_camera(cam, F, (3.6, -1.0, 2.1), (0, 4.4, 2.0))
for f in times:
    add_shake(cam, f, f + 4, strength=0.06, rot_strength=0.008, seed=f)
render(os.environ.get("JAWS_OUT", "renders/shot06_vault"))
