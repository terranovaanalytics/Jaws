"""Jaws 8 episode config, read by tools/assemble.py.

CUES: (shot, phrase where that shot starts, nudge in seconds). Phrases are
matched against what was actually said first, then against script.md.
Avoid "shark" in cues: Whisper may hear it as "shock".
The title card plays under the intro line ("Me and my kid are rebooting...").
"""

CUES = [
    ("shot01_recap", "if you've been following along", 0),
    ("shot02_stolen_sub", "and police chief brody played by pedro", 0),
    ("shot03_map_atlantic", "for the first time ever", 0),
    ("shot04_disguise", "american soldiers dressed up", 0),
    ("shot05_kremlin", "sneaks into the freaking kremlin", -0.9),
    ("shot06_plan", "and the plan is make", 0),
    ("shot07_cold_war", "and then america protected", 0),
    ("shot08_get_out", "brody knows he can't communicate", 0),
    ("shot09_gronk", "so cia officer", 0),
    ("shot10_border", "out the back of a truck", 0),
    ("shot11_next_us", "the russians were just starting", 0),
    ("shot12_one_man", "and there's one remaining problem", 0),
    ("shot13_endcard", "and that sets us up", 0),
]
# Caption fixes for words Whisper reliably mishears in this recording.
FIXES = {"shock": "shark", "shocks": "sharks", "shock's": "shark's", "blemons": "Plemons",
         "nucleus": "nuclear"}
PHRASE_FIXES = []
# Whole-phrase corrections: (what Whisper heard, what was said).
SAID = [("jesse blemons", "jesse plemons"), ("russian nucleus sub", "russian nuclear sub")]

TITLE = "shot00_title"
DEFAULTS = {TITLE: 4.8, "shot01_recap": 6.5, "shot02_stolen_sub": 5.2, "shot03_map_atlantic": 5.8,
            "shot04_disguise": 5.9, "shot05_kremlin": 7.4, "shot06_plan": 6.7, "shot07_cold_war": 7.6,
            "shot08_get_out": 3.3, "shot09_gronk": 6.3, "shot10_border": 4.0, "shot11_next_us": 4.7,
            "shot12_one_man": 7.3, "shot13_endcard": 2.1}

# Vocabulary hint for Whisper (names, places, words it might mishear).
WHISPER_PROMPT = ("Jaws 8. Great white sharks. Police Chief Brody, played by Pedro Pascal. Chief "
                  "oceanographer Jesse, played by Jesse Plemons. Bill Belichick plays Leonid Brezhnev. "
                  "Soviet Union. Gronk, Rob Gronkowski. Amity.")

# Cast photo cards (assets/cast/): (image, phrase where it pops up, phrase where it
# goes or None, seconds held after the phrase).
CAST = [
    ("assets/cast/brody_1975.jpg", "police chief brody played by", "played by pedro", 0),
    ("assets/cast/pedro_pascal.jpg", "played by pedro pascal", None, 0.5),
    ("assets/cast/brezhnev.jpg", "soviet leader brezhnev", "played by bill", 0),
    ("assets/cast/bill_belichick.jpg", "played by bill belichick", None, 0.6),
    ("assets/cast/gronk.jpg", "rob gronkowski smuggles", "played by jesse", 0),
    ("assets/cast/jesse_plemons.jpg", "played by jesse plemons", None, 0.5),
]
