"""Operation Cronchisk: the recurring sets, shared by the shot scripts.

Each builder makes the environment and lights; the shot adds the cast and
the camera. Everyone faces -Y, the camera sits at -Y looking +Y.
"""
import math
import random

from jaws.common import box, cyl, ico, empty, mat, text, FPS
from jaws import ops as O
from jaws.world import make_ocean
from jaws.agents import glass


def skyline(y=60, seed=4, n=18, lit=0.35):
    """Distant city: dark blocks with scattered warm windows."""
    rnd = random.Random(seed)
    dark = mat("sky_bldg", (0.05, 0.06, 0.1))
    win = mat("sky_win", (1.0, 0.8, 0.45), emit=3.0)
    for i in range(n):
        x = -45 + i * 5 + rnd.uniform(-1, 1)
        w, h = rnd.uniform(3, 5), rnd.uniform(6, 22)
        box(f"Bldg{i}", (w, 3, h), (x, y + rnd.uniform(0, 8), h / 2 - 1), dark)
        for k in range(int(h / 1.6)):
            for j in range(3):
                if rnd.random() < lit:
                    box(f"Win{i}_{k}_{j}", (0.4, 0.05, 0.5), (x - w / 3 + j * w / 3, y - 1.55, 0.5 + k * 1.6), win)


def harbor_ext(F, rain=True):
    """Rainy neon harbor at night: dock, black water, a warehouse with a
    flickering pink PIER 9 sign, crates, a lamp post, a city skyline."""
    from jaws.common import reset_scene
    sc = reset_scene(F, world_color=(0.04, 0.05, 0.12))
    O.night(sc, moon=0.35)
    make_ocean(color=(0.02, 0.04, 0.09), wave=0.2)
    O.make_dock("Dock", (0, 4, 0.6), size=(18, 12))
    wh = empty("WH", (2, 13, 0.6))
    box("WH_body", (14, 8, 7), (0, 0, 3.5), mat("whx_wall", (0.16, 0.17, 0.2)), parent=wh)
    box("WH_roof", (14.6, 8.6, 0.4), (0, 0, 7.2), mat("whx_roof", (0.08, 0.08, 0.1)), parent=wh)
    box("WH_door", (3.6, 0.1, 4.2), (-2, -4.02, 2.1), mat("whx_door_lit", (1.0, 0.75, 0.4), emit=1.6), parent=wh)
    for k in range(5):
        box(f"WH_rib{k}", (0.12, 0.12, 7), (-7 + k * 3.5, -4.05, 3.5), mat("whx_rib", (0.1, 0.1, 0.12)), parent=wh)
    O.make_neon_sign("Neon", "PIER 9", (2.5, 8.85, 6.0), size=1.1, color=(1.0, 0.15, 0.55), energy=500,
                     flicker=(int(F * 0.2), int(F * 0.45)))
    O.point_light("DoorGlow", (0, 8.0, 2.5), 900, (1.0, 0.7, 0.4), radius=1.5)
    O.make_lamp_post("Lamp", (-5, 0.5, 0.6), energy=600)
    for i, (x, y, sz, r) in enumerate(((-7, 6, 1.2, 10), (-6, 7.2, 1.0, -20), (-7.2, 7.4, 0.9, 5),
                                       (6.5, 3, 1.3, 15), (7.5, 4.5, 1.0, -8))):
        O.make_crate(f"Crate{i}", (x, y, 0.6), sz, r)
    skyline()
    if rain:
        O.rain("Rain", (0, 2, 0.6), 1, F, size=(22, 18), height=14, count=420, seed=1)
    return sc


def warehouse_int(F, rain=False):
    """Inside PIER 9: brick, beams, one hanging lamp over a crate (the deal)."""
    from jaws.common import reset_scene
    sc = reset_scene(F, world_color=(0.02, 0.02, 0.04))
    O.dark_room(sc, ambient=0.12)
    O.make_warehouse("WH", (0, 2, 0), w=16, d=12, h=7)
    O.make_crate("DealCrate", (0, 0.5, 0), 1.1)
    for i, (x, y, sz, r) in enumerate(((-5, 4, 1.6, 10), (-5.5, 5.5, 1.3, 0), (-3.8, 6.4, 1.2, 30),
                                       (5, 5, 1.8, -10), (5.2, 3.4, 1.2, 25), (4, 6.5, 1.5, 0))):
        O.make_crate(f"Crate{i}", (x, y, 0), sz, r, color=[(0.5, 0.36, 0.2), (0.3, 0.38, 0.25)][i % 2])
    iron = mat("lamp_iron", (0.08, 0.08, 0.09))
    cyl("HangCord", 0.02, 2.5, (0, 0.5, 5.8), iron, n=4)
    cyl("HangShade", 0.6, 0.4, (0, 0.5, 4.4), iron, n=10, r2=0.15)
    ico("HangBulb", 0.15, (0, 0.5, 4.2), mat("hang_bulb", (1.0, 0.85, 0.6), emit=8.0))
    O.spot_light("HangSpot", (0, 0.5, 4.1), (0, 0.5, 0), 2600, (1.0, 0.85, 0.65), angle=70, blend=0.5)
    O.point_light("Fill", (-3, -6, 3), 250, (0.4, 0.5, 1.0), radius=2, shadow=False)
    # skylight in the roof
    box("Skylight", (3, 3, 0.05), (0, 0.5, 7.0), glass("skylight_m", (0.5, 0.6, 0.9), 0.35, 0.5))
    return sc


def desert(F, sunset_sky=False):
    from jaws.common import reset_scene, add_sun
    sc = reset_scene(F, world_color=(0.45, 0.68, 0.95))
    if sunset_sky:
        O.sunset(sc, energy=2.6, rot=(74, 0, 150))
        O.make_desert(color=(0.88, 0.55, 0.35))
    else:
        add_sun((48, 0, 30), energy=2.6, color=(1.0, 0.95, 0.85))
        O.make_desert()
    return sc


def lab_int(F, alarm=False):
    """Inside the desert lab: white panels, a workbench, the vault wall."""
    from jaws.common import reset_scene
    sc = reset_scene(F, world_color=(0.6, 0.65, 0.7))
    O.dark_room(sc, ambient=0.22)
    box("LabFloor", (20, 16, 0.2), (0, 2, -0.1), mat("lab_floor", (0.7, 0.72, 0.74), rough=0.3, metal=0.1))
    for i in range(-4, 5):
        box(f"LabTile{i}", (0.04, 16, 0.01), (i * 2, 2, 0.005), mat("lab_grout", (0.5, 0.52, 0.55)))
    box("LabBack", (20, 0.3, 7), (0, 7, 3.5), mat("lab_wall", (0.72, 0.75, 0.78)))
    for s in (-1, 1):
        box(f"LabSide{s}", (0.3, 16, 7), (s * 10, 2, 3.5), mat("lab_wall", (0.72, 0.75, 0.78)))
    for i in range(4):
        box(f"LabLight{i}", (3, 0.4, 0.08), (-6 + i * 4, 2, 6.9), mat("lab_light", (1, 1, 1), emit=5.0))
        O.point_light(f"LabL{i}", (-6 + i * 4, 2, 6.2), 180, (0.95, 0.97, 1.0), radius=1.5, shadow=i % 2 == 0)
    return sc


def lair(F, purple=True):
    """Jelly's lair inside the mesa: dark steel walls, purple accent strips,
    a big purple J emblem, grated floor."""
    from jaws.common import reset_scene
    sc = reset_scene(F, world_color=(0.03, 0.02, 0.05))
    O.dark_room(sc, ambient=0.16)
    steel = mat("lair_steel", (0.22, 0.22, 0.27), metal=0.4, rough=0.5)
    dark = mat("lair_dark", (0.1, 0.1, 0.13))
    accent = mat("lair_accent", (0.75, 0.3, 1.0), emit=4.0)
    box("LairFloor", (24, 20, 0.2), (0, 3, -0.1), mat("lair_floor", (0.18, 0.18, 0.21), rough=0.35, metal=0.4))
    for i in range(-6, 7):
        box(f"LairGrate{i}", (0.06, 20, 0.02), (i * 1.8, 3, 0.01), dark)
    box("LairBack", (24, 0.3, 9), (0, 8, 4.5), steel)
    for s in (-1, 1):
        box(f"LairSide{s}", (0.3, 20, 9), (s * 12, 3, 4.5), steel)
    for i in range(-5, 6):
        box(f"LairRib{i}", (0.5, 0.4, 9), (i * 2.2, 7.8, 4.5), dark)
    for z in (0.6, 6.5):
        box(f"LairStrip{z}", (24, 0.1, 0.12), (0, 7.6, z), accent)
    em = empty("Emblem", (0, 7.55, 4.6))
    cyl("EmblemDisc", 1.8, 0.1, (0, 0, 0), dark, n=20, rot=(90, 0, 0), parent=em)
    cyl("EmblemRing", 1.9, 0.08, (0, 0.02, 0), accent, n=20, rot=(90, 0, 0), parent=em)
    text("EmblemJ", "J", (0, -0.1, 0), 2.6, mat("lair_j", (0.75, 0.3, 1.0), emit=3.0), parent=em, bold=True,
         extrude=0.1)
    if purple:
        O.point_light("LairPurple", (0, 4, 6.5), 1500, (0.75, 0.35, 1.0), radius=3, shadow=False)
    O.point_light("LairKey", (-4, -4, 5), 700, (0.85, 0.9, 1.0), radius=1.5)
    return sc
