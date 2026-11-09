"""Jaws 6 episode config, read by tools/assemble.py.

CUES: (shot, phrase where that shot starts, nudge in seconds). Phrases are
matched against what was actually said first, then against script.md.
Avoid "shark" in cues: Whisper may hear it as "shock".
The title card plays under the intro line ("Me and my kid are rebooting...").
"""

CUES = [
    ("shot01_recap", "now remember in jaws 5", 0),
    ("shot02_reviews", "the audience loved it", 0),
    ("shot03_fourth", "so we're running it back", 0),
    ("shot04_brody_dock", "police chief brody played by pedro", 0),
    ("shot05_barge_rammed", "rams the fireworks barge", -0.4),
    ("shot06_rockets", "and every rock and fire", 0.3),
    ("shot07_war1812", "it looks like the friggin", 0),
    ("shot08_brody_jesse", "police chief brody and chief oceanographer", 0),
    ("shot09_radar", "are back and the radar", -0.4),
    ("shot10_mech_cave", "so police chief brody hops", 0),
    ("shot11_same_plan", "same plan same execution", 0),
    ("shot12_bookstore", "kick the kids out", 0),
    ("shot13_hunch", "they realize something big", 0),
    ("shot14_tests", "he runs some tests", 0),
    ("shot15_mutants", "these were radioactive mutant", 0),
    ("shot16_mystery", "now police chief brody and jesse have", 0),
    ("shot17_endcard", "and that sets us up", 0),
]
# Caption fixes for words Whisper reliably mishears in this recording.
FIXES = {"shock": "shark", "shocks": "sharks", "shock's": "shark's", "edgerton": "Edgartown",
         "edgertown": "Edgartown"}
PHRASE_FIXES = [(r"\b9\s*-\s*11\b", "911")]
# Whole-phrase corrections from the narrator: (what Whisper heard, what was said).
SAID = [("from the dark", "from the dock"), ("every rock and fire", "every rocket fires")]

TITLE = "shot00_title"
DEFAULTS = {TITLE: 5.0, "shot01_recap": 6.6, "shot02_reviews": 2.8, "shot03_fourth": 6.6,
            "shot04_brody_dock": 3.6, "shot05_barge_rammed": 4.5, "shot06_rockets": 4.9,
            "shot07_war1812": 5.8, "shot08_brody_jesse": 5.0, "shot09_radar": 4.0,
            "shot10_mech_cave": 7.1, "shot11_same_plan": 4.4, "shot12_bookstore": 4.5,
            "shot13_hunch": 4.9, "shot14_tests": 5.9, "shot15_mutants": 4.1,
            "shot16_mystery": 4.2, "shot17_endcard": 2.4}

# Vocabulary hint for Whisper (names, places, words it might mishear).
WHISPER_PROMPT = ("Jaws 6. Great white sharks. Shark 911. Rotten Tomatoes score 99. Fourth of July "
                  "fireworks barge in Edgartown Harbor. Police Chief Brody, played by Pedro Pascal. "
                  "Chief oceanographer Jesse, played by Jesse Plemons. Mechanical shark sub. "
                  "Edgartown Bookstore. Radioactive mutant sharks.")

# Cast photo cards (assets/cast/): (image, phrase where it pops up, phrase where it
# goes or None, seconds held after the phrase). The original 1975 Brody on "Police
# Chief Brody", then the actor on "played by ...".
CAST = [
    ("assets/cast/brody_1975.jpg", "police chief brody played by", "played by pedro", 0),
    ("assets/cast/pedro_pascal.jpg", "played by pedro pascal", None, 0.5),
    # not cast, same card: the owner's War of 1812 painting on the line
    ("assets/cast/war_of_1812.jpg", "friggin war of 1812", "stop the recording", 0),
    ("assets/cast/jesse_plemons.jpg", "played by jesse plemons", None, 0.5),
]
