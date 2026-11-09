"""Shot 2: a shark fin zooms in, the shark breaches and rams the ferry.
Impact shake, splash, passengers tumble off, ferry lists and starts sinking."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import (reset_scene, add_sun, add_camera, key_camera, add_shake,
                         linear_keys, render, FPS, JANK, box, mat, shot_seconds)
from jaws.world import (make_ocean, make_island, make_ferry, bob, make_extra, splash,
                        make_ragdoll_extra, rigid, bake_physics)
from jaws.shark import make_shark, open_jaw, swim_wag

F = int(shot_seconds("shot02", 7.0) * FPS)
HIT = max(34, int(F * 0.37))  # frame of impact

reset_scene(F, world_color=(0.45, 0.75, 1.0))
add_sun((50, 0, -25), energy=2.4)
make_ocean()
isl = make_island()
isl["root"].location = (40, 160, 0)   # Amity in the background

ferry = make_ferry("Ferry", loc=(0, 0, 0), rot_z=0)
bob(ferry, 1, HIT)
# after impact: list toward camera, bow dips, sink
SINK = [(HIT, 0, 0, 0), (HIT + 4, 9, -2, -0.3), (HIT + 10, 6, -1, -0.5),
        (HIT + 30, 16, 3, -1.4), (F, 26, 6, -3.6)]
for f, roll, pitch, z in SINK:
    ferry.rotation_euler = (math.radians(roll), math.radians(pitch), 0)
    ferry.location.z = z
    ferry.keyframe_insert("rotation_euler", frame=f)
    ferry.keyframe_insert("location", index=2, frame=f)
if JANK >= 3:   # BUG: the ferry's physics have a seizure while it sinks
    add_shake(ferry, HIT + 20, F, strength=0.25, rot_strength=0.06, seed=9)

# shark: fin cuts toward the ferry, then breaches into the hull
S = 5.0
shark = make_shark("Shark", scale=S)
# fin crosses the foreground left->right (profile to camera), then breaches
path = [(1, (-12.5, -13, -2.3), 0, 22), (HIT - 22, (-7, -11, -2.3), 0, 22),
        (HIT - 10, (-4.5, -9.0, -0.8), -25, 28), (HIT, (-1.5, -6.6, 1.6), -30, 32),
        (HIT + 14, (0.5, -8.5, -3.0), 35, 32), (HIT + 40, (1.5, -10, -11), 60, 32)]
if JANK >= 3:   # BUG: no collision. The shark just swims straight through the ferry
    path = path[:4] + [(HIT + 22, (6, 3, 1.6), -30, 32), (HIT + 34, (9, 7, -1), 20, 32),
                       (HIT + 50, (11, 10, -8), 40, 32)]
for f, loc, pitch, yaw in path:
    shark.root.location = loc
    shark.root.rotation_euler = (0, math.radians(pitch), math.radians(yaw))
    shark.root.keyframe_insert("location", frame=f)
    shark.root.keyframe_insert("rotation_euler", frame=f)
open_jaw(shark, HIT - 18, 0.0)
open_jaw(shark, HIT - 8, 1.0)
open_jaw(shark, HIT, 1.0)
open_jaw(shark, HIT + 3, 0.2)
swim_wag(shark, 1, F, period=8, angle=28)

splash("Wake", (-4.5, -9.0, 0), HIT - 12, count=10, size=0.5, power=5, seed=2)
splash("Hit", (0, -4.3, 1.0), HIT, count=22, size=0.8, power=9, life=30, seed=3)
splash("Fall", (0.5, -8.5, 0), HIT + 14, count=14, size=0.7, power=7, seed=4)

# passengers on the stern deck get flung overboard toward camera
if JANK >= 2:
    # real (bad) physics: a hidden paddle punches up through the deck at impact
    deck = box("DeckCollider", (16, 7, 1.0), (-6, 0, 1.35), None)
    deck.hide_render = True
    rigid(deck, "PASSIVE").kinematic = True
    paddle = box("Paddle", (9, 3.5, 0.6), (-6.5, -0.2, 1.2), None)
    paddle.hide_render = True
    rigid(paddle, "PASSIVE").kinematic = True
    for f, z, y in [(1, 1.2, -0.2), (HIT + 2, 1.2, -0.2), (HIT + 5, 3.6, -3.5), (HIT + 6, -20, -3.5)]:
        paddle.location.z, paddle.location.y = z, y
        paddle.keyframe_insert("location", frame=f)
    for f, z in [(HIT + 6, 1.35), (HIT + 7, -30)]:
        deck.location.z = z
        deck.keyframe_insert("location", index=2, frame=f)
    linear_keys(paddle)
    bpy_scene = __import__("bpy").context.scene
    for i in range(7):
        x = -10 + i * 1.5
        p = make_ragdoll_extra(f"Tourist{i}", (x, -1.4 + (i % 2) * 1.1, 3.25), seed=i, scale=1.5)
        rb = rigid(p, "ACTIVE", mass=1, bounce=0.9 if JANK >= 3 else 0.2)
        rb.use_deactivation = rb.use_start_deactivated = True   # stand still until hit
    if JANK >= 3:
        # BUG: the ocean is a trampoline
        tramp = box("Trampoline", (200, 200, 1), (0, 0, -0.6), None)
        tramp.hide_render = True
        rigid(tramp, "PASSIVE", bounce=0.95)
        # BUG: one tourist T-poses and glides across the water like nothing happened
        g = make_ragdoll_extra("Glider", (-14, -12, 1.25), seed=8, scale=1.5)
        g.keyframe_insert("location", frame=1)
        g.location.x = 10
        g.keyframe_insert("location", frame=F)
        linear_keys(g)
        # BUG: a car stays hovering exactly where the deck used to be
        cm = mat("car0", (0.9, 0.2, 0.2))
        box("FloatingCar", (2.8, 1.5, 0.8), (-10, -1.5, 2.3), cm)
        box("FloatingCarTop", (1.5, 1.4, 0.6), (-10.2, -1.5, 3.0), cm)
        ferry_car = __import__("bpy").data.objects.get("Ferry_car0")
        if ferry_car:
            ferry_car.hide_render = True
        __import__("bpy").data.objects["Ferry_carTop0"].hide_render = True
    bpy_scene.rigidbody_world.substeps_per_frame = 20
    bake_physics()
else:
    for i in range(6):
        x = -9 + i * 1.6
        p = make_extra(f"Tourist{i}", (x, -1.5 + (i % 2), 1.85), seed=i, scale=1.5)
        start = HIT + 4 + i * 5
        p.keyframe_insert("location", frame=start)
        p.keyframe_insert("rotation_euler", frame=start)
        for k in range(0, 26, 3):
            t = k / 24
            p.location = (x + 0.5 * t, -1.5 - 7 * t, 2.2 + 5 * t - 9 * t * t)
            p.rotation_euler = (math.radians(-400 * t), math.radians(120 * t * (1 if i % 2 else -1)), 0)
            p.keyframe_insert("location", frame=start + k)
            p.keyframe_insert("rotation_euler", frame=start + k)
        splash(f"Plop{i}", (x + 0.5, -1.5 - 7 * 1.0, 0), start + 22, count=6, size=0.35,
               power=4, life=16, seed=10 + i)

cam = add_camera((-6, -34, 7), (-4, -8, 1), lens=30)
key_camera(cam, 1, (-7, -34, 7), (-5, -9, 0.5))
key_camera(cam, HIT, (-4, -29, 6), (-1, -5, 1.8))
key_camera(cam, F, (-3, -26, 5.5), (0, -3, 0.5))
linear_keys(cam)
add_shake(cam, HIT, HIT + 30, strength=0.35, rot_strength=0.03)
render(os.environ.get("JAWS_OUT", "renders/shot02_ferry_rammed"))
