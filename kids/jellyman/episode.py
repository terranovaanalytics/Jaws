"""Attack of the Jelly Man: config read by tools/assemble.py (run it with the
path: python3 tools/assemble.py kids/jellyman --render).

The title card plays under the false starts ("Okay, once upon a time... I mean...").
"""

CUES = [
    ("shot01_jelly", "there was a jelly man", -2.0),       # from "Oh, once upon a time"
    ("shot02_banana", "but a super hero banana", 0),
    ("shot03_aliens", "and then two space alien", 0),
    ("shot04_eat", "and then they ate the", 0),
    ("shot05_forcefield", "a little guy in a force", -0.4),
    ("shot06_run", "he was trapped and run", -0.6),
    ("shot07_cherry", "but then cherry super hero came", 0),
    ("shot08_spaceship", "and he stayed on the", 0),
    ("shot09_kid", "he especially saved the little", 0),
    ("shot10_carrot", "a carrot saved all of", -0.9),
    ("shot11_eaten", "a carrot got eaten up", -0.8),
    ("shot12_inside", "because he was in somewhere", 0),
    ("shot13_someone", "and then he saw someone", 0),
    ("shot14_cronchisk", "he needed the cronchisk", 0),
    ("shot15_mean_cherry", "but another mean cherry guy", 0),
    ("shot16_home", "and all the alien guys", 0),
    ("shot17_end", "the end", 0),
]
FIXES = {"meetings": "meanies"}
PHRASE_FIXES = []
SAID = []

TITLE = "shot00_title"
DEFAULTS = {TITLE: 10.7, "shot01_jelly": 6.8, "shot02_banana": 6.5, "shot03_aliens": 5.1, "shot04_eat": 4.9,
            "shot05_forcefield": 7.7, "shot06_run": 3.1, "shot07_cherry": 5.9, "shot08_spaceship": 8.5,
            "shot09_kid": 8.2, "shot10_carrot": 6.0, "shot11_eaten": 5.6, "shot12_inside": 4.6,
            "shot13_someone": 5.7, "shot14_cronchisk": 3.6, "shot15_mean_cherry": 7.9, "shot16_home": 2.9,
            "shot17_end": 2.9}

WHISPER_PROMPT = ("Once upon a time there was a jelly man. Superhero banana guy. Space alien guys. "
                  "Force field. Cherry superhero. The meanies. Spaceship. A carrot.")
CAST = []
