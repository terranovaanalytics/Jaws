"""Jaws 5 episode config, read by tools/assemble.py.

CUES: (shot, phrase where that shot starts, nudge in seconds). Phrases are
matched against what was actually said first (the recording ad-libs), then
against script.md. Avoid "shark" in cues: Whisper may hear it as "shock".
"""

CUES = [
    ("shot01_establishing", "we're gonna start with jaws 5", 0),
    ("shot02_ferry_rammed", "a steamship authority ferry", 0),
    ("shot03_swarm", "people hit the water", 0),
    ("shot04_flotilla", "police chief brody still alive", 0),
    ("shot05_boats_sinking", "most of them get rammed and sunk", 0),
    ("shot06_jesse_arrives", "it makes national news", 0),
    ("shot07_radar_line", "he brings an advanced radar", 0),
    ("shot08_mech_in_line", "so police chief brody builds", 0),
    ("shot09_cave", "blends in and follows the", 0.8),
    ("shot10_bait", "they hatch a plan", 0),
    ("shot11_explosion", "blow up the cave entrance", 0),
    ("shot12_drilling", "then kick the kids off", 1.0),
    ("shot13_pump", "it's a crazy plan", 0),
    ("shot14_radar_again", "the radar goes quiet", 0),
    ("shot15_endcard", "and that leads us to jaws", 0),
]
# Caption fixes for words Whisper reliably mishears in this recording.
FIXES = {"shock": "shark", "shocks": "sharks", "shock's": "shark's", "edgerton": "Edgartown",
         "edgertown": "Edgartown",
         "zazu": "Zissou"}
PHRASE_FIXES = [(r"\b9\s*-\s*11\b", "911")]
# Whole-phrase corrections from the narrator: (what Whisper heard, what was said).
# Timing of the misheard span is spread evenly over the corrected words.
SAID = [("and the story's a heroine.", "and stories are harrowing.")]


TITLE = "shot00_title"
DEFAULTS = {TITLE: 3.0, "shot15_endcard": 3.5, "shot01_establishing": 6, "shot02_ferry_rammed": 7, "shot03_swarm": 7,
            "shot04_flotilla": 7, "shot05_boats_sinking": 7, "shot06_jesse_arrives": 6,
            "shot07_radar_line": 6, "shot08_mech_in_line": 7, "shot09_cave": 6, "shot10_bait": 6,
            "shot11_explosion": 6, "shot12_drilling": 7, "shot13_pump": 6, "shot14_radar_again": 8}

# Vocabulary hint for Whisper (names, places, words it might mishear).
WHISPER_PROMPT = ("Jaws 5. Great white sharks. Shark 911 on Amity Island. Police Chief Brody, "
                  "played by Pedro Pascal. Chief oceanographer Jesse, played by Jesse Plemons, "
                  "wears a Steve Zissou red cap. Mechanical shark submarine. Shark cave under "
                  "the Flying Horses carousel. Edgartown Harbor.")

# Cast photo cards (assets/cast/): (image, phrase where it pops up, phrase where it
# goes or None, seconds held after the phrase). The original 1975 Brody on "Police
# Chief Brody", then the actor on "played by ...".
CAST = [
    ("assets/cast/brody_1975.jpg", "police chief brody still alive", "played by pedro", 0),
    ("assets/cast/pedro_pascal.jpg", "played by pedro pascal", None, 0.5),
    ("assets/cast/jesse_plemons.jpg", "played by jesse plemons", None, 0.5),
]
