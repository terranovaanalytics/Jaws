"""Shot 12: "They follow it up the coast, all the way to Maine, and capture
the whole crew." Pine-and-granite Maine coast, WELCOME TO MAINE sign, a
lighthouse. The green trail leads straight to the Russian sub, surfaced in
the cove. The boat pulls up, the agent points, and the whole crew on deck
throws their hands up."""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "..", "..", "..", "lib"), HERE]
from jaws.common import add_camera, key_camera, render, FPS, shot_seconds
from jaws.world import bob
from jaws.spy import make_russian
from _sets import cove, deck_z, trail, move, hands_up, face
from _crew import boat_crew

F = int(shot_seconds("shot12", 3.8) * FPS)
c = cove(F)
sub = c["sub"]
SY = 30
pts = [(-120 + k * 8, SY - 12 + 3 * math.sin(k)) for k in range(12)] + [(-28, SY - 4)]
trail("Trail", pts)
boat, crew = boat_crew((-50, SY - 12, 0), rot_z=10)
ARRIVE = int(F * 0.55)
move(boat, [(1, (-50, SY - 12, 0)), (ARRIVE, (-14, SY - 8.5, 0))])
bob(boat, 1, F, period=40, roll=3, pitch=1.5, heave=0.2)
UP = int(F * 0.70)                           # "...capture the whole crew"
face(crew["agent"].arm_r, ARRIVE, 0, axis=0)
face(crew["agent"].arm_r, ARRIVE + 5, -88, axis=0)
dz = deck_z(sub)
for i in range(7):
    x = -13 + i * 2.2 if i < 4 else 10 + (i - 4) * 2.2
    r = make_russian(f"Crew{i}", loc=(x, SY - 0.2, dz), rot_z=0, seed=i)
    hands_up(r, UP + (i % 3) * 2)
cam = add_camera((0, 0, 0), (0, 0, 0), lens=24)
key_camera(cam, 1, (-40, -8, 7), (-34, 70, 7))
key_camera(cam, int(F * 0.5), (-28, -12, 6), (-10, 40, 4))
key_camera(cam, F, (-9, -4, 5), (-2, 30, 4.5))
render(os.environ.get("JAWS_OUT", "renders/shot12_maine"))
