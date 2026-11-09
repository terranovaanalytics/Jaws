"""Shared Kremlin interiors (shots 5, 6, 8): the war room where Brezhnev
explains the plan, and a long hallway. Built far from the origin so a shot
can also have the exterior Kremlin and cut between the two. Not a shot."""
import math
import bpy
from jaws.common import box, cyl, mat, text
from jaws.soviet import make_brezhnev, make_chalkboard, make_soviet_flag

ROOM = (400.0, 0.0, 0.0)


def lamp(name, at, energy=900, color=(1.0, 0.82, 0.55), radius=0.5):
    d = bpy.data.lights.new(name, "POINT")
    d.energy, d.color, d.shadow_soft_size = energy, color, radius
    o = bpy.data.objects.new(name, d)
    o.location = at
    bpy.context.scene.collection.objects.link(o)
    return o


def build_war_room():
    """Back wall at y=+5, door on the left (x=-4), chalkboard center-right,
    Brezhnev beside it. Returns dict with brezhnev, board, door (x, y)."""
    X, Y, Z = ROOM
    wall = mat("room_wall", (0.55, 0.16, 0.12))
    panel = mat("room_panel", (0.32, 0.20, 0.12))
    carpet = mat("room_carpet", (0.50, 0.08, 0.07))
    floor = mat("room_floor", (0.35, 0.24, 0.14))
    gold = mat("gold", (1.0, 0.78, 0.15), emit=0.3)
    box("RoomFloor", (30, 30, 0.2), (X, Y, Z - 0.1), floor)
    box("RoomCarpet", (8, 12, 0.03), (X + 1, Y, Z + 0.01), carpet)
    box("RoomBack", (30, 0.4, 9), (X, Y + 5.2, Z + 4.5), wall)
    box("RoomWainscot", (30, 0.45, 1.4), (X, Y + 5.0, Z + 0.7), panel)
    box("RoomLeft", (0.4, 20, 9), (X - 6.0, Y - 4, Z + 4.5), wall)
    # doorway in the left wall, near the camera
    box("DoorGap", (0.5, 1.6, 3.0), (X - 6.0, Y - 1.2, Z + 1.5), mat("door_dark", (0.03, 0.02, 0.02)))
    for dy in (-2.05, -0.35):
        box(f"DoorJamb{dy}", (0.55, 0.18, 3.2), (X - 6.0, Y + dy, Z + 1.6), panel)
    box("DoorHead", (0.55, 1.9, 0.2), (X - 6.0, Y - 1.2, Z + 3.2), panel)
    make_soviet_flag("RoomFlag", (X - 2.5, Y + 4.7, Z + 1.0), size=2.4, pole=6.0, wave=False)
    # portrait frames on the back wall
    for k, x in enumerate((-4.6, 4.8)):
        box(f"Frame{k}", (1.6, 0.1, 2.0), (X + x, Y + 4.95, Z + 4.6), gold)
        box(f"Pic{k}", (1.3, 0.12, 1.7), (X + x, Y + 4.94, Z + 4.6), mat("pic_dark", (0.20, 0.18, 0.15)))
    # long table with red phone
    wood = mat("table_wood", (0.30, 0.18, 0.10))
    box("Table", (4.0, 1.6, 0.12), (X + 3.4, Y - 2.4, Z + 1.0), wood)
    for dx in (-1.8, 1.8):
        for dy in (-0.6, 0.6):
            box(f"TLeg{dx}{dy}", (0.12, 0.12, 1.0), (X + 3.4 + dx, Y - 2.4 + dy, Z + 0.5), wood)
    box("Phone", (0.35, 0.25, 0.15), (X + 2.6, Y - 2.4, Z + 1.14), mat("phone_red", (0.9, 0.08, 0.06)))
    board = make_chalkboard("Board", (X + 1.8, Y + 3.2, Z), w=4.6, h=2.8)
    brez = make_brezhnev("Brezhnev", (X + 0.4, Y + 1.8, Z), rot_z=-20)
    lamp("RoomKey", (X - 2, Y - 5, Z + 6), 2500)
    lamp("RoomFill", (X + 4, Y - 1, Z + 5), 800, color=(1.0, 0.9, 0.75))
    lamp("RoomBack", (X, Y + 3.5, Z + 7.5), 600, color=(1.0, 0.7, 0.45))
    return dict(brezhnev=brez, board=board, door=(X - 6.0, Y - 1.2))


def build_hallway():
    """Long red-carpet hallway along +Y from y=0 to 40, walls at x=+-2.2."""
    X, Y, Z = ROOM[0] + 100, 0.0, 0.0
    wall = mat("hall_wall", (0.62, 0.55, 0.42))
    panel = mat("room_panel", (0.32, 0.20, 0.12))
    carpet = mat("room_carpet", (0.50, 0.08, 0.07))
    floor = mat("room_floor", (0.35, 0.24, 0.14))
    gold = mat("gold", (1.0, 0.78, 0.15), emit=0.3)
    box("HallFloor", (6, 60, 0.2), (X, Y + 20, Z - 0.1), floor)
    box("HallCarpet", (2.0, 60, 0.03), (X, Y + 20, Z + 0.01), carpet)
    for s in (-1, 1):
        box(f"HallWall{s}", (0.3, 60, 5), (X + s * 2.4, Y + 20, Z + 2.5), wall)
        box(f"HallWain{s}", (0.35, 60, 1.1), (X + s * 2.35, Y + 20, Z + 0.55), panel)
        for k in range(6):
            y = Y + 4 + k * 6
            box(f"HallFrame{s}{k}", (0.1, 1.4, 1.7), (X + s * 2.23, y, Z + 2.6), gold)
            box(f"HallPic{s}{k}", (0.12, 1.1, 1.4), (X + s * 2.22, y, Z + 2.6), mat("pic_dark", (0.20, 0.18, 0.15)))
    box("HallCeil", (5, 60, 0.2), (X, Y + 20, Z + 5.0), wall)
    box("HallEnd", (5, 0.3, 5), (X, Y + 45, Z + 2.5), mat("door_dark", (0.03, 0.02, 0.02)))
    for k in range(4):
        lamp(f"HallLamp{k}", (X, Y + 2 + k * 9, Z + 4.4), 250)
    return (X, Y, Z)
