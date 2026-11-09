"""Shot 8: "Brody knows he can't communicate this from inside Russia. He's
gotta get out." A Kremlin hallway, red alarm light flashing: Brody (in the
ushanka) backs against the wall, sweating, looking left... right... and runs."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import reset_scene, add_camera, key_camera, add_shake, render, FPS, shot_seconds
from jaws.people import make_brody, walk
from jaws.soviet import _hat_ushanka, alarm_light, sweat
from _interior import build_hallway

F = int(shot_seconds("shot08", 3.4) * FPS)
RUN = int(F * 0.80)             # "He's gotta get out."
reset_scene(F, world_color=(0.05, 0.04, 0.04))
X, Y, Z = build_hallway()
b = make_brody("Brody", loc=(X - 1.75, Y + 6, Z), rot_z=90)   # back to the left wall, facing across
_hat_ushanka(b, "Brody", color=(0.42, 0.30, 0.20))
alarm_light("Alarm", (X, Y + 9, Z + 4.6), 1, F, period=10, energy=1500)
alarm_light("Alarm2", (X, Y + 2, Z + 4.6), 1, F, period=10, energy=900)
for f, yaw in ((1, 0), (int(F * 0.2), 60), (int(F * 0.45), -60), (int(F * 0.65), 0)):  # left... right...
    b.head.rotation_euler[2] = math.radians(yaw)
    b.head.keyframe_insert("rotation_euler", index=2, frame=f)
    b.head.keyframe_insert("rotation_euler", index=2, frame=f + 6 if f > 1 else 1)
sweat("Sweat", b.head, 4, F, every=6)
b.root.keyframe_insert("location", frame=RUN)
b.root.keyframe_insert("rotation_euler", index=2, frame=RUN)
b.root.rotation_euler[2] = math.radians(10)
b.root.keyframe_insert("rotation_euler", index=2, frame=RUN + 3)
b.root.location = (X - 1.0, Y + 1.0, Z)               # bolts toward camera
b.root.keyframe_insert("location", frame=F + 6)
for limb in (b.leg_l, b.leg_r, b.arm_l, b.arm_r):     # stand still until he bolts
    limb.keyframe_insert("rotation_euler", index=0, frame=1)
    limb.keyframe_insert("rotation_euler", index=0, frame=RUN - 1)
walk(b, RUN, F, period=6, swing=45)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=26)
key_camera(cam, 1, (X + 1.4, Y - 0.5, Z + 1.8), (X - 1.6, Y + 6, Z + 1.7))
key_camera(cam, F, (X + 1.2, Y + 1.6, Z + 1.8), (X - 1.6, Y + 6, Z + 1.8))
add_shake(cam, 1, F, strength=0.02, rot_strength=0.004)
render(os.environ.get("JAWS_OUT", "renders/shot08_get_out"))
