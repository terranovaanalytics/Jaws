"""Operation Cronchisk: a blocky spy thriller remake of Attack of the Jelly Man.

No narration: trailer-style text cards + a synthesized spy score and sound
effects, put together by tools/trailer.py (python3 tools/trailer.py kids/cronchisk).
SHOTS sets each shot's length (written to timing.json for the scenes).
"""
TITLE = "OPERATION CRONCHISK"

SHOTS = [
    ("shot00_harbor", 6.0),
    ("shot01_jelly", 5.0),
    ("shot02_banana", 5.5),
    ("shot03_titles", 5.0),
    ("shot04_briefing", 5.0),
    ("shot05_twins", 4.5),
    ("shot06_vault", 4.5),
    ("shot07_bubble", 4.5),
    ("shot08_escape", 4.0),
    ("shot09_cherry", 5.0),
    ("shot10_orbiter", 5.0),
    ("shot11_brig", 5.0),
    ("shot12_swap", 5.5),
    ("shot13_gulp", 5.0),
    ("shot14_help", 4.0),
    ("shot15_someone", 5.5),
    ("shot16_countdown", 5.0),
    ("shot17_dark_cherry", 5.0),
    ("shot18_getaway", 5.0),
    ("shot19_end", 6.5),
]

# Trailer text: (shot, start offset s, duration s, text). Kept in the lower-middle
# of the frame, like a movie trailer.
CARDS = [
    ("shot00_harbor", 0.6, 2.6, "MIDNIGHT. PIER 9."),
    ("shot00_harbor", 3.4, 2.4, "AN ARMS DEALER..."),
    ("shot01_jelly", 1.0, 3.6, "...AND A CRYSTAL\nTHAT COULD RULE THE WORLD"),
    ("shot02_banana", 0.4, 2.0, "ONE AGENT"),
    ("shot02_banana", 2.6, 2.6, "STOOD IN HIS WAY"),
    ("shot04_briefing", 0.4, 4.4, "BUT JELLY HAD HIRED\nHELP"),
    ("shot05_twins", 0.8, 3.4, "THE TWINS"),
    ("shot06_vault", 0.5, 3.6, "THEY EAT\nANYTHING"),
    ("shot07_bubble", 0.4, 3.8, "THEY TOOK THE SCIENTIST\nWHO BUILT IT"),
    ("shot08_escape", 0.6, 3.0, "HE RAN"),
    ("shot09_cherry", 0.6, 3.8, "THE AGENCY SENT\nBACKUP"),
    ("shot10_orbiter", 1.0, 3.6, "SHE HELD ON"),
    ("shot11_brig", 0.6, 3.8, "SHE SAVED THE KID"),
    ("shot12_swap", 0.5, 4.4, "THE DOUBLE AGENT\nDISARMED THEM ALL"),
    ("shot13_gulp", 0.4, 2.2, "UNTIL..."),
    ("shot15_someone", 0.6, 4.2, "SOMEONE ELSE\nWAS PULLING THE STRINGS"),
    ("shot16_countdown", 0.4, 4.2, "HE NEEDED\nTHE CRONCHISK"),
    ("shot17_dark_cherry", 2.2, 2.6, "NOT TODAY"),
    ("shot18_getaway", 0.6, 4.0, "THE TWINS\nWENT THEIR OWN WAY"),
]

# Sound effects: (shot, offset s, kind). Kinds: see tools/trailer.py SFX.
SFX = [
    ("shot00_harbor", 0.0, "rain"),
    ("shot01_jelly", 1.2, "latch"),
    ("shot02_banana", 0.5, "glass"),
    ("shot02_banana", 1.0, "thud"),
    ("shot02_banana", 3.1, "slurp"),
    ("shot03_titles", 0.2, "whoosh"),
    ("shot03_titles", 1.9, "boom"),
    ("shot05_twins", 0.2, "hum"),
    ("shot06_vault", 1.0, "chomp"),
    ("shot06_vault", 1.6, "chomp"),
    ("shot06_vault", 2.2, "chomp"),
    ("shot06_vault", 2.8, "chomp"),
    ("shot06_vault", 3.6, "clang"),
    ("shot07_bubble", 0.3, "alarm"),
    ("shot08_escape", 0.2, "glass"),
    ("shot08_escape", 0.2, "alarm"),
    ("shot09_cherry", 0.2, "whoosh"),
    ("shot09_cherry", 3.0, "thud"),
    ("shot10_orbiter", 0.3, "jet"),
    ("shot11_brig", 1.4, "zap"),
    ("shot11_brig", 2.2, "clang"),
    ("shot12_swap", 1.0, "pop"),
    ("shot12_swap", 1.7, "pop"),
    ("shot12_swap", 2.4, "pop"),
    ("shot12_swap", 3.1, "pop"),
    ("shot12_swap", 3.8, "pop"),
    ("shot13_gulp", 2.5, "gulp"),
    ("shot14_help", 0.3, "bubbles"),
    ("shot14_help", 1.0, "radio"),
    ("shot15_someone", 2.4, "creak"),
    ("shot15_someone", 3.2, "sting"),
    ("shot16_countdown", 1.4, "power"),
    ("shot16_countdown", 2.0, "beeps"),
    ("shot17_dark_cherry", 1.0, "whoosh"),
    ("shot17_dark_cherry", 1.6, "powerdown"),
    ("shot18_getaway", 1.0, "boom"),
    ("shot18_getaway", 1.6, "boom"),
    ("shot19_end", 0.0, "waves"),
    ("shot19_end", 1.2, "clink"),
]

# Music: sections of the score by shot (see tools/trailer.py): intro (tense, sparse),
# drive (main spy groove), break (drop to a pulse), climax (full), end (big final chord).
MUSIC = [
    ("shot00_harbor", "intro"),
    ("shot03_titles", "hit"),
    ("shot04_briefing", "drive"),
    ("shot13_gulp", "break"),
    ("shot15_someone", "tension"),
    ("shot17_dark_cherry", "climax"),
    ("shot19_end", "end"),
]
