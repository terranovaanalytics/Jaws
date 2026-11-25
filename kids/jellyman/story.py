"""Attack of the Jelly Man: the characters, as drawn (drawings/NN.jpg).

CUTOUTS is read by tools/cutout.py (drawing -> cutouts/NN.png) and by the
scenes (lib/jaws/kids.py: puppet(key)). color = fill for closed shapes,
ink = line color, height = puppet height in Blender units.
"""
TITLE = "ATTACK OF THE JELLY MAN"

INK = (0.05, 0.10, 0.13)
CUTOUTS = {
    "01": dict(name="Jelly Man", color=(0.80, 0.45, 0.95), height=3.2, close=28, erase=[(0.9, 0, 1, 1)]),
    "02": dict(name="Superhero Banana Guy", color=(1.00, 0.86, 0.15), height=2.6, thresh=0.16),
    "03": dict(name="Space Alien", color=(0.45, 0.92, 0.30), height=3.0, erase=[(0, 0.36, 0.2, 0.7)]),
    "04": dict(name="Force Field Guy", color=(0.55, 0.92, 1.00), height=3.0, fill_alpha=0.55, close=16, gutter=0.7),
    "05": dict(name="Cherry Superhero", color=(0.92, 0.10, 0.16), height=2.8, erase=[(0, 0.9, 1, 1)]),
    "06": dict(name="Meanie", color=(0.55, 0.32, 0.78), height=2.2, close=14, erase=[(0, 0.88, 0.5, 1)]),
    "07": dict(name="Spaceship", color=(0.72, 0.76, 0.86), height=4.0),
    "08": dict(name="Little Kid", color=(1.00, 0.78, 0.58), height=1.7, close=22),
    "09": dict(name="Carrot", color=(1.00, 0.50, 0.08), height=2.6, solid=True, close=12,
               top_color=(0.25, 0.70, 0.20), top_split=0.30),
    "10": dict(name="Cool Man", color=(0.35, 0.65, 1.00), height=2.8),
    "11": dict(name="Someone", color=(1.00, 0.62, 0.25), height=2.4, rotate=-90, thresh=0.16, erase=[(0.55, 0.92, 1, 1), (0.86, 0, 1, 1), (0.78, 0.86, 1, 1)]),
    "12": dict(name="Mean Cherry Guy", color=(0.55, 0.04, 0.16), height=2.8, erase=[(0, 0.92, 1, 1)]),
}
for _c in CUTOUTS.values():
    _c.setdefault("ink", INK)
