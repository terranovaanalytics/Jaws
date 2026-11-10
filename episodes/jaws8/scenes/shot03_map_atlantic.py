"""Shot 3: "For the first time ever, Police Chief Brody is leaving the United
States. They sail all the way to Leningrad." Old-movie travel map: a dashed
red line crawls from Amity across the Atlantic to Leningrad, a tiny sub icon
leading it. The camera tracks the icon across the map."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from jaws.common import reset_scene, add_sun, add_camera, key_camera, render, FPS, shot_seconds, mat, text
from jaws.soviet import make_map_table, pin, dotted_path, follow_path, path_point, make_sub
from jaws.town import pop_in

F = int(shot_seconds("shot03", 5.9) * FPS)
GO = int(F * 0.30)              # "...leaving the United States"
ARRIVE = int(F * 0.86)          # "...Leningrad"
reset_scene(F, world_color=(0.12, 0.10, 0.08))
add_sun((35, 10, 20), energy=1.6)
m = make_map_table()
P = m["places"]
route = [P["amity"], (-6, 5.5), (-1, 8.3), (4, 9.2), (9.5, 9.6), (12.2, 9.4), P["leningrad"]]
pin("PinAmity", P["amity"], parent=m["root"], color=(0.2, 0.4, 0.9))
pl = pin("PinLen", P["leningrad"], parent=m["root"])
pop_in(pl, ARRIVE, scale=1.0)
lm = mat("map_label", (0.10, 0.08, 0.06))
t = text("LblAmity", "AMITY", (P["amity"][0] - 1.6, P["amity"][1] - 0.9, 0.1), 0.7, lm, rot=(0, 0, 0),
         parent=m["root"], bold=True)
t2 = text("LblLen", "LENINGRAD", (P["leningrad"][0] - 1.0, P["leningrad"][1] - 1.1, 0.1), 0.7, lm, rot=(0, 0, 0),
          parent=m["root"], bold=True)
pop_in(t2, ARRIVE + 2)
dotted_path("Route", route, GO, ARRIVE, parent=m["root"], step=0.7)
icon = make_sub("Icon", (0, 0, 0), scale=0.07)
icon["root"].parent = m["root"]
follow_path(icon["root"], route, GO, ARRIVE, z=0.2)
icon["root"].location = (*P["amity"], 0.2)
icon["root"].keyframe_insert("location", frame=1)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=30)
for f in (1, GO, int(F * 0.5), int(F * 0.7), ARRIVE, F):
    t = 0 if f <= GO else min(1, (f - GO) / (ARRIVE - GO))
    x, y, _ = path_point(route, t)
    if f == F:
        x += 0.5
    key_camera(cam, f, (x + 0.5, y - 9.5, 14.0 - 1.0 * (f / F)), (x + 0.5, y - 0.5, 0))
render(os.environ.get("JAWS_OUT", "renders/shot03_map_atlantic"))
