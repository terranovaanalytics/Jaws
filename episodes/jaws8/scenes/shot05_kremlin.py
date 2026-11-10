"""Shot 5: "Police Chief Brody sneaks into the freaking Kremlin and he hears
Soviet leader Brezhnev, played by Bill Belichick, explain the plan."
Night: Brody (in his ushanka) tiptoes along the Kremlin wall under the red
star. Cut inside: he peeks through a doorway at Brezhnev, in a cut-off
hoodie and medals, chalk in hand at the board."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
import bpy
from jaws.common import reset_scene, add_camera, key_camera, render, FPS, shot_seconds, box, mat
from jaws.fireworks import dusk
from jaws.people import make_brody, walk
from jaws.soviet import make_kremlin, _hat_ushanka
from _interior import build_war_room, lamp, ROOM

F = int(shot_seconds("shot05", 7.2) * FPS)
CUT = int(F * 0.40)             # "...and he hears Soviet leader Brezhnev"
POINT = int(F * 0.80)           # "...explain the plan"
s = reset_scene(F)
dusk(s, horizon=(0.20, 0.14, 0.28), mid=(0.08, 0.07, 0.18), zenith=(0.02, 0.02, 0.06), sun=False,
     ambient=0.18, ambient_color=(0.45, 0.5, 0.9))
moon = bpy.data.lights.new("Moon", "SUN")
moon.energy, moon.color = 0.6, (0.6, 0.7, 1.0)
mo = bpy.data.objects.new("Moon", moon)
mo.rotation_euler = (math.radians(55), 0, math.radians(-30))
s.collection.objects.link(mo)
box("Square", (300, 200, 0.2), (0, -60, -0.1), mat("cobbles", (0.28, 0.27, 0.28)))
k = make_kremlin(night=True)
lamp("StarGlow", (0, -6, 42), 3000, color=(1.0, 0.15, 0.1), radius=2)
lamp("GateLamp", (-8, -8, 6), 1200, color=(1.0, 0.75, 0.45))
# --- outside: tiptoe along the wall
b = make_brody("Brody", loc=(-14, -2.4, 0), rot_z=90)
_hat_ushanka(b, "Brody", color=(0.42, 0.30, 0.20))
b.torso.rotation_euler[0] = math.radians(14)                  # sneaky crouch
b.arm_l.rotation_euler[0] = math.radians(-50)
walk(b, 1, CUT, period=16, swing=18)
b.root.keyframe_insert("location", index=0, frame=1)
b.root.location.x = -8.5
b.root.keyframe_insert("location", index=0, frame=CUT)
b.head.rotation_euler[2] = math.radians(-35)                  # glance at camera
b.head.keyframe_insert("rotation_euler", index=2, frame=int(CUT * 0.5))
# --- inside
room = build_war_room()
z = room["brezhnev"]
X, Y, Z = ROOM
box("Column", (0.9, 0.9, 9), (X - 4.3, Y - 2.6, Z + 4.5), mat("room_panel", (0.32, 0.20, 0.12)))
p = make_brody("Peek", loc=(X - 4.0, Y - 3.4, Z), rot_z=200)  # back to us, hiding behind the column
_hat_ushanka(p, "Peek", color=(0.42, 0.30, 0.20))
p.root.keyframe_insert("rotation_euler", index=1, frame=CUT)
p.root.rotation_euler[1] = math.radians(-14)                   # leans out to look
p.root.keyframe_insert("rotation_euler", index=1, frame=CUT + 10)
z.arm_r.rotation_euler = (math.radians(-30), 0, 0)
z.arm_r.keyframe_insert("rotation_euler", frame=POINT - 6)
z.arm_r.rotation_euler = (math.radians(-100), 0, math.radians(-50))   # chalk at the board
z.arm_r.keyframe_insert("rotation_euler", frame=POINT)
z.head.rotation_euler[2] = math.radians(-10)
z.head.keyframe_insert("rotation_euler", index=2, frame=POINT - 6)
z.head.rotation_euler[2] = math.radians(-50)
z.head.keyframe_insert("rotation_euler", index=2, frame=POINT)
box("Chalk", (0.05, 0.05, 0.14), (0, -0.05, -0.62), mat("chalk", (0.92, 0.92, 0.88), emit=0.6), parent=z.arm_r)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=24)
key_camera(cam, 1, (-14, -10, 1.2), (-11, 0, 3.6))
key_camera(cam, CUT - 1, (-11.5, -9.5, 1.2), (-8.5, 0, 3.8))
key_camera(cam, CUT, (X - 5.2, Y - 8.6, Z + 2.3), (X - 1.0, Y + 1.8, Z + 1.5))
key_camera(cam, F, (X - 4.8, Y - 7.0, Z + 2.2), (X - 0.6, Y + 1.8, Z + 1.6))
for fc in cam.animation_data.action.fcurves:          # hard cut at CUT
    for kp in fc.keyframe_points:
        if int(kp.co[0]) in (CUT - 1,):
            kp.interpolation = "CONSTANT"
render(os.environ.get("JAWS_OUT", "renders/shot05_kremlin"))
