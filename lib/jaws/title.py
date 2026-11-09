"""Shared title-card builder: big chunky "JAWS" + number bursting out of a
sunset ocean while a fin circles. Used by the opening and the end card."""
import math
from .common import (reset_scene, add_sun, add_camera, key_camera, add_shake, FPS, text, mat)
from .world import make_ocean, splash
from .shark import make_shark, swim_wag


def build_title(F, number="5", subtitle=None):
    reset_scene(F, world_color=(0.95, 0.55, 0.25))           # sunset orange sky
    add_sun((70, 0, -20), energy=2.6, color=(1.0, 0.85, 0.7))
    make_ocean(color=(0.05, 0.25, 0.50))
    red = mat("title_red", (0.9, 0.05, 0.05), flat=0.8)
    white = mat("title_white", (1, 1, 1), flat=0.9)
    t = text("Title", "JAWS", (0, 0, 0), 7.0, red, extrude=0.8, bold=True)
    n = text("TitleNum", number, (0, -0.8, 0), 12.0, white, extrude=1.0, bold=True)
    UP = min(int(F * 0.35), 30)
    for o, z0, z1 in ((t, -8, 11.5), (n, -14, 3.5)):
        o.location.z = z0
        o.keyframe_insert("location", index=2, frame=1)
        o.location.z = z1 + 0.6
        o.keyframe_insert("location", index=2, frame=UP)
        o.location.z = z1
        o.keyframe_insert("location", index=2, frame=UP + 4)
    if subtitle:
        st = text("Subtitle", subtitle, (0, -2, 16.5), 1.6, mat("title_yellow", (1, 0.9, 0.2), flat=0.9),
                  extrude=0.2, bold=True)
        st.scale = (0.001,) * 3
        st.keyframe_insert("scale", frame=UP + 6)
        st.scale = (1, 1, 1)
        st.keyframe_insert("scale", frame=UP + 10)
    splash("Rise", (0, -1, 0), UP - 6, count=24, size=0.8, power=10, life=28)
    sh = make_shark("Fin", scale=4)
    for f in range(1, F + 1, 2):
        a = -1.5 + f / FPS * 1.6
        sh.root.location = (11 * math.cos(a), 6 * math.sin(a) - 2, -2.2)
        sh.root.rotation_euler[2] = a + math.pi / 2
        sh.root.keyframe_insert("location", frame=f)
        sh.root.keyframe_insert("rotation_euler", index=2, frame=f)
    swim_wag(sh, 1, F, period=10)
    cam = add_camera((0, 0, 0), (0, 0, 0), lens=30)
    key_camera(cam, 1, (0, -27, 3), (0, 0, 7))
    key_camera(cam, F, (0, -24, 2.5), (0, 0, 7))
    add_shake(cam, UP, UP + 8, strength=0.4, rot_strength=0.03)
