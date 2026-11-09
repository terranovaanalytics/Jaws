"""Shared set for the cave shots (10, 11, 13): the Jaws 5 cutaway diagram with
the bookstore on top instead of the carousel, plus a path-follow helper.
Not a shot itself."""
import math
from jaws.common import reset_scene, add_sun, mat, text, box
from jaws.props import make_cave_cutaway
from jaws.town import make_bookstore

TUNNEL = (15.0, -12.0)        # where the tunnel meets the open sea (x, z)


def build_cave(F, drained=False):
    s = reset_scene(F, world_color=(0.45, 0.75, 1.0))
    add_sun((40, 0, 20), energy=2.4)
    if drained:               # pumped dry: dark rock where the water tint was
        mat("cave_back", (0.20, 0.17, 0.15), flat=0.3)
    cave = make_cave_cutaway()
    store = make_bookstore("Bookstore", loc=(0, 1.5, 0))
    return s, cave, store


def follow(obj, pts, f0, f1, step=2, bank=True):
    """Move obj along a polyline of (x, y, z) points between frames f0 and f1
    at constant speed, nose (+X) pointing along the direction of travel in
    the XZ plane (side-on cutaway)."""
    seg = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    total = sum(seg)

    def at(u):
        d = u * total
        for (a, b), L in zip(zip(pts, pts[1:]), seg):
            if d <= L or L == seg[-1] and (a, b) == (pts[-2], pts[-1]):
                t = d / L if L else 0
                return [a[k] + (b[k] - a[k]) * t for k in range(3)], b
            d -= L
        return list(pts[-1]), pts[-1]

    for f in range(f0, f1 + 1, step):
        u = (f - f0) / max(1, f1 - f0)
        p, _ = at(u)
        q, _ = at(min(1.0, u + 0.01))
        if u >= 0.99:
            q2, _ = at(0.99)
            dx, dz = p[0] - q2[0], p[2] - q2[2]
        else:
            dx, dz = q[0] - p[0], q[2] - p[2]
        obj.location = p
        if abs(dx) + abs(dz) > 1e-6:
            obj.rotation_euler = (0, -math.atan2(dz, abs(dx)), 0 if dx > 0 else math.pi)
        obj.keyframe_insert("location", frame=f)
        obj.keyframe_insert("rotation_euler", frame=f)


def label(name, body, loc, size=1.0, color=(1, 1, 1)):
    return text(name, body, loc, size, mat(f"label_{color}", color, emit=1.0), extrude=0.05, bold=True)
