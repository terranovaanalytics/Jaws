"""Jaws 7 episode config, read by tools/assemble.py.

CUES: (shot, phrase where that shot starts, nudge in seconds). Phrases are
matched against what was actually said first, then against script.md.
Avoid "shark" in cues: Whisper may hear it as "shock".
The title card plays under the intro line ("Me and my kid are rebooting...").
Note: a single Whisper pass skipped 4-30 s of this recording; audio/transcript.json
was built from a chunked pass. Don't delete it unless you check that stretch again.
"""

CUES = [
    ("shot01_reviews", "jaws 5 and jaws 6 had", 0),
    ("shot02_recap", "okay buddy", 0),
    ("shot03_line", "now jaws 7 are you ready", 0),
    ("shot04_brody_sub", "but this time police chief", 0),
    ("shot05_follow", "and follows the", 0),
    ("shot06_nuke_sub", "and at the end of the line", 0),
    ("shot07_russians", "and guess who it is", 0),
    ("shot08_dc", "brody gets on a plane", 0),
    ("shot09_president", "mr president played by", 0),
    ("shot10_cia", "so the president sends", 0),
    ("shot11_trail", "and they go looking", 0),
    ("shot12_maine", "they follow it up the coast", 0),
    ("shot13_jam", "but first they jam", 0),
    ("shot14_one_guy", "they keep one russian", 0),
    ("shot15_hatch", "and then police chief brody jesse", 0),
    ("shot16_russia", "brody looks back and says", 0),
    ("shot17_endcard", "and that sets us up", 0),
]
# Caption fixes for words Whisper reliably mishears in this recording.
FIXES = {"shock": "shark", "shocks": "sharks", "shock's": "shark's", "jaws": "Jaws"}
PHRASE_FIXES = []
# Whole-phrase corrections from the narrator: (what Whisper heard, what was said).
SAID = [("are not to be radioactive now", "turned out to be radioactive. Now")]

TITLE = "shot00_title"
DEFAULTS = {TITLE: 4.7, "shot01_reviews": 7.9, "shot02_recap": 2.9, "shot03_line": 4.5,
            "shot04_brody_sub": 5.3, "shot05_follow": 3.4, "shot06_nuke_sub": 4.5,
            "shot07_russians": 2.4, "shot08_dc": 4.4, "shot09_president": 6.0,
            "shot10_cia": 5.3, "shot11_trail": 4.4, "shot12_maine": 4.5, "shot13_jam": 3.0,
            "shot14_one_guy": 3.8, "shot15_hatch": 4.4, "shot16_russia": 3.3,
            "shot17_endcard": 1.6}

# Vocabulary hint for Whisper (names, places, words it might mishear).
WHISPER_PROMPT = ("Jaws 7. Great white sharks. Police Chief Brody, played by Pedro Pascal. "
                  "Chief oceanographer Jesse. Mechanical shark sub. Nuclear submarine. The Russians. "
                  "The White House. Mr. President, played by Tom Brady. CIA officer, played by "
                  "Rob Gronkowski. Gronk. Amity Island. Maine. Radioactive mutant sharks.")

# Cast photo cards (assets/cast/): (image, phrase where it pops up, phrase where it
# goes or None, seconds held after the phrase).
CAST = [
    ("assets/cast/brody_1975.jpg", "police chief brody played by", "played by pedro", 0),
    ("assets/cast/pedro_pascal.jpg", "played by pedro pascal", None, 0.6),
    ("assets/cast/tom_brady.jpg", "played by tom brady", None, 1.5),
    ("assets/cast/gronk.jpg", "played by rob gronkowski", None, 0.9),
]
