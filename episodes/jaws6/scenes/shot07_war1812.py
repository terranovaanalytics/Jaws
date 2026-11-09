"""Shot 7: "It looks like the War of 1812, and no one can stop the recording
of the national anthem." From the pier: the harbor burns, rockets skip over
the water, the flag waves. Pan to the PA speaker blasting music notes while a
guy yanks its cord, fails, and falls on his butt."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import add_camera, key_camera, add_shake, render, FPS, shot_seconds, box, mat
from jaws.world import make_extra
from jaws.town import make_pa_pole, music_notes
from _harbor import build_harbor, BARGE, tip_barge, harbor_ablaze, chaos_bursts

F = int(shot_seconds("shot07", 5.8) * FPS)
h = build_harbor(F)
tip_barge(h["barge"])
harbor_ablaze(h, 1, F)
chaos_bursts(1, F, every=5, seed=7)
dx, dy, dz = h["dock_end"]
px, py = dx - 4.5, dy - 0.5
pa = make_pa_pole("PA", (px, py, dz), rot_z=-20)
for k, (hx, hy, hz) in enumerate(pa["horns"]):
    music_notes(f"Notes{k}", (px + hx, py + hy, dz + hz), 1 + k * 3, F, every=6, seed=k, size=1.5)
# the guy tugging the cord
PULL, FALL = int(F * 0.45), int(F * 0.78)
g = make_extra("Tugger", (px + 0.9, py - 0.9, dz), seed=5, scale=1.0)
g.rotation_euler[2] = math.radians(70)
cord = box("Cord", (0.05, 0.05, 1.0), (px + 0.5, py - 0.6, dz + 0.9), mat("cable", (0.05, 0.05, 0.05)),
           rot=(0, 60, 20))
for f in range(PULL, FALL, 4):                       # heave... heave...
    g.rotation_euler[1] = math.radians(-25 if (f // 4) % 2 else -10)
    g.keyframe_insert("rotation_euler", index=1, frame=f)
g.rotation_euler[1] = math.radians(-85)              # ...and down he goes
g.keyframe_insert("rotation_euler", index=1, frame=FALL + 5)
g.keyframe_insert("location", frame=FALL)
g.location.z = dz - 0.3
g.keyframe_insert("location", frame=FALL + 5)

cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (dx + 2, dy + 2.5, dz + 4.5), (BARGE[0] + 2, BARGE[1] + 10, 5))
key_camera(cam, int(F * 0.3), (dx + 2, dy + 2.3, dz + 4.2), (BARGE[0] + 6, BARGE[1] + 14, 5))
key_camera(cam, int(F * 0.48), (dx + 2.5, dy + 4.5, dz + 2.3), (px, py, dz + 3.2))
key_camera(cam, F, (dx + 1.8, dy + 3.4, dz + 2.0), (px, py, dz + 3.0))
add_shake(cam, 1, F, strength=0.05, rot_strength=0.005)
render(os.environ.get("JAWS_OUT", "renders/shot07_war1812"))
