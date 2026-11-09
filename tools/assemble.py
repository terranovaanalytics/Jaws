#!/usr/bin/env python3
"""Assemble the final Jaws 5 reel.

    python3 tools/assemble.py            # full pipeline (needs audio/jaws5.m4a)
    python3 tools/assemble.py --render   # also re-render shots whose length changed
    python3 tools/assemble.py --silent   # no audio yet: stitch a silent draft

Steps (with audio):
  1. Transcribe the narration with Whisper (word timestamps), cached in
     audio/transcript.json.
  2. Find where each shot's cue phrase is spoken (CUES below) and write
     timing.json, which every scene reads for its length.
  3. Optionally re-render shots whose length changed (--render).
  4. Title card + shots -> one video, narration as the audio, burned-in
     captions, -> final/jaws5.mp4
"""
import argparse
import difflib
import json
import os
import re
import subprocess
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AUDIO = os.path.join(REPO, "audio", "jaws5.m4a")
TRANSCRIPT = os.path.join(REPO, "audio", "transcript.json")
TIMING = os.path.join(REPO, "timing.json")
RENDERS = os.path.join(REPO, "renders")
FINAL = os.path.join(REPO, "final")
FPS = 24

# shot -> phrase from scripts/jaws5.md where the shot should start.
# Edit these if a shot should land on a different line.
# (shot, phrase where the shot starts, nudge in seconds). Phrases are matched
# against what was actually SAID first (the recording ad-libs), then against
# scripts/jaws5.md. Avoid "shark" in cues: Whisper often hears it as "shock".
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


def apply_said(words):
    words = list(words)
    for heard, said in SAID:
        h = [norm(t) for t in heard.split()]
        n = len(h)
        for i in range(len(words) - n + 1):
            if [norm(w["w"]) for w in words[i:i + n]] == h:
                s0, e0 = words[i]["s"], words[i + n - 1]["e"]
                new = said.split()
                step = (e0 - s0) / len(new)
                words[i:i + n] = [dict(w=t, s=s0 + k * step, e=s0 + (k + 1) * step) for k, t in enumerate(new)]
                break
    return words
TITLE = "shot00_title"
DEFAULTS = {TITLE: 3.0, "shot15_endcard": 3.5, "shot01_establishing": 6, "shot02_ferry_rammed": 7, "shot03_swarm": 7,
            "shot04_flotilla": 7, "shot05_boats_sinking": 7, "shot06_jesse_arrives": 6,
            "shot07_radar_line": 6, "shot08_mech_in_line": 7, "shot09_cave": 6, "shot10_bait": 6,
            "shot11_explosion": 6, "shot12_drilling": 7, "shot13_pump": 6, "shot14_radar_again": 8}


def run(cmd, **kw):
    print("+", " ".join(cmd) if isinstance(cmd, list) else cmd, flush=True)
    subprocess.run(cmd, check=True, **kw)


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


# ---------------------------------------------------------------- 1. transcribe
def transcribe():
    if os.path.exists(TRANSCRIPT) and os.path.getmtime(TRANSCRIPT) > os.path.getmtime(AUDIO):
        with open(TRANSCRIPT) as fh:
            return json.load(fh)
    import whisper
    model = whisper.load_model("medium.en")   # small.en heard "shark" as "shock"
    res = model.transcribe(AUDIO, word_timestamps=True, language="en",
                           initial_prompt="Jaws 5. Great white sharks. Shark 911 on Amity Island. Police Chief Brody, "
                                          "played by Pedro Pascal. Chief oceanographer Jesse, played by Jesse Plemons, "
                                          "wears a Steve Zissou red cap. Mechanical shark submarine. Shark cave under "
                                          "the Flying Horses carousel. Edgartown Harbor.")
    words = [dict(w=w["word"].strip(), s=w["start"], e=w["end"])
             for seg in res["segments"] for w in seg.get("words", [])]
    out = dict(text=res["text"], words=words, duration=words[-1]["e"] if words else 0)
    with open(TRANSCRIPT, "w") as fh:
        json.dump(out, fh, indent=1)
    return out


# ---------------------------------------------------------------- 2. cue timing
def find_cues(words):
    """Align the whole script to the transcript, then look up where each cue
    phrase (found in the script text) was actually spoken. Robust to Whisper
    mishearing a few words and to the narrator ad-libbing."""
    with open(os.path.join(REPO, "scripts", "jaws5.md")) as fh:
        script = [norm(t) for t in fh.read().split()]
    script = [t for t in script if t]
    toks = [norm(w["w"]) for w in words]
    sm = difflib.SequenceMatcher(None, script, toks, autojunk=False)
    s2t = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            s2t[blk.a + k] = blk.b + k
    starts, pos, tpos = {}, 0, 0
    for shot, phrase, nudge in CUES:
        target = [norm(t) for t in phrase.split()]
        n = len(target)
        # 1) directly in the transcript (what was actually said)
        bt, bt_i = 0.0, None
        for i in range(tpos, len(toks) - n + 1):
            r = difflib.SequenceMatcher(None, toks[i:i + n], target).ratio()
            if r > bt:
                bt, bt_i = r, i
        if bt_i is not None and bt >= 0.8:
            starts[shot] = words[bt_i]["s"] + nudge
            tpos = bt_i + 1
            print(f"   {shot:24s} @ {starts[shot]:6.2f}s  '{' '.join(w['w'] for w in words[bt_i:bt_i + n])}'")
            continue
        n = len(target)
        best, best_i = 0.0, None             # where the cue sits in the script
        for i in range(pos, len(script) - n + 1):
            r = difflib.SequenceMatcher(None, script[i:i + n], target).ratio()
            if r > best:
                best, best_i = r, i
        if best_i is None or best < 0.6:
            print(f"!! cue for {shot} not found in scripts/jaws5.md: '{phrase}'")
            continue
        pos = best_i + 1
        # first script word of the cue that was matched in the transcript
        ti = next((s2t[j] for j in range(best_i, min(len(script), best_i + n + 15)) if j in s2t), None)
        if ti is None:
            print(f"!! could not hear cue for {shot}: '{phrase}'")
            continue
        starts[shot] = words[ti]["s"] + nudge
        tpos = ti + 1
        print(f"   {shot:24s} @ {starts[shot]:6.2f}s  '{' '.join(w['w'] for w in words[ti:ti + n])}'")
    return starts


def compute_timing(starts, duration):
    shots = [s for s, _, _ in CUES]
    timing = {}
    first = starts.get(shots[0], DEFAULTS[TITLE])
    timing[TITLE] = round(max(2.0, first), 3)
    for i, s in enumerate(shots):
        if s not in starts:
            timing[s] = DEFAULTS[s]
            continue
        nxt = next((starts[t] for t in shots[i + 1:] if t in starts), duration + 0.8)
        timing[s] = round(max(1.0, nxt - starts[s]), 3)
    for s, t in timing.items():
        if s != TITLE and not 4 <= t <= 8:
            print(f"   note: {s} is {t:.1f}s (outside the 4-8s target, set by the narration)")
    return timing


# ---------------------------------------------------------------- 3. render
def rendered_seconds(shot):
    p = os.path.join(RENDERS, f"{shot}.mp4")
    if not os.path.exists(p):
        return None
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                         capture_output=True, text=True).stdout.strip()
    return float(out) if out else None


def render_changed(timing):
    for shot in [TITLE] + [s for s, _, _ in CUES]:
        have = rendered_seconds(shot)
        want = int(timing.get(shot, DEFAULTS[shot]) * FPS) / FPS
        if have is None or abs(have - want) > 0.1:
            run([os.path.join(REPO, "tools", "render.sh"), os.path.join(REPO, "scenes", f"{shot}.py")])


# ---------------------------------------------------------------- 4. captions + mux
def ass_time(t):
    h, rem = divmod(max(0, t), 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def fix_word(w):
    core = re.sub(r"^[^\w']+|[^\w']+$", "", w)
    rep = FIXES.get(core.lower())
    return w.replace(core, rep) if rep and core else w


def write_captions(words, path, offset=0.0, max_words=4, max_gap=0.6):
    """Reels-style captions: short chunks, big bold caps with a thick outline."""
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,DejaVu Sans,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,7,3,2,60,60,380,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    words = apply_said(words)
    lines, chunk = [], []

    def flush():
        if chunk:
            txt = " ".join(fix_word(w["w"]) for w in chunk)
            for pat, rep in PHRASE_FIXES:
                txt = re.sub(pat, rep, txt)
            txt = txt.upper()
            lines.append(f"Dialogue: 0,{ass_time(chunk[0]['s'] + offset)},{ass_time(chunk[-1]['e'] + offset)},Cap,,0,0,0,,{txt}")
            chunk.clear()

    for w in words:
        if chunk and (len(chunk) >= max_words or w["s"] - chunk[-1]["e"] > max_gap
                      or chunk[-1]["w"].endswith((".", ",", "?", "!"))):
            flush()
        chunk.append(w)
    flush()
    with open(path, "w") as fh:
        fh.write(head + "\n".join(lines) + "\n")


def concat(shots, out):
    inputs, filt = [], []
    for i, s in enumerate(shots):
        inputs += ["-i", os.path.join(RENDERS, f"{s}.mp4")]
        filt.append(f"[{i}:v]")
    run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex",
         "".join(filt) + f"concat=n={len(shots)}:v=1:a=0[v]", "-map", "[v]",
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), out])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", action="store_true", help="re-render shots whose length changed")
    ap.add_argument("--silent", action="store_true", help="no audio: silent draft with default timings")
    ap.add_argument("--audio", help="narration file (default audio/jaws5.m4a)")
    ap.add_argument("--out", help="output file (default final/jaws5.mp4)")
    a = ap.parse_args()
    global AUDIO, TRANSCRIPT
    if a.audio:
        AUDIO = os.path.abspath(a.audio)
        TRANSCRIPT = os.path.splitext(AUDIO)[0] + ".transcript.json"
    os.makedirs(FINAL, exist_ok=True)
    shots = [TITLE] + [s for s, _, _ in CUES]

    if a.silent or not os.path.exists(AUDIO):
        if not a.silent:
            print("!! audio/jaws5.m4a not found, making a silent draft (use --silent to skip this note)")
        if a.render:
            render_changed({})
        out = os.path.join(FINAL, "jaws5_draft_silent.mp4")
        concat(shots, out)
        print("->", out)
        return

    print("1. transcribing narration")
    tr = transcribe()
    print("2. matching shot cues")
    starts = find_cues(tr["words"])
    timing = compute_timing(starts, tr["duration"])
    with open(TIMING, "w") as fh:
        json.dump(timing, fh, indent=1)
    print(f"   total {sum(timing.values()):.1f}s, narration {tr['duration']:.1f}s -> timing.json")
    if a.render:
        print("3. re-rendering shots whose length changed")
        render_changed(timing)
    print("4. assembling")
    body = os.path.join(FINAL, "_video.mp4")
    concat(shots, body)
    ass = os.path.join(FINAL, "captions.ass")
    write_captions(tr["words"], ass)
    out = os.path.abspath(a.out) if a.out else os.path.join(FINAL, "jaws5.mp4")
    # 70s look: film grain goes on once here (cheaper than per shot)
    look_file = os.path.join(RENDERS, "shot01_establishing", "look")
    film = os.path.exists(look_file) and open(look_file).read().strip() == "70s"
    vf = "tpad=stop_mode=clone:stop_duration=3,"           # hold last frame to the end of the audio
    # chunky PS1-res grain that refreshes on twos (12 fps, like the animation):
    # full-res per-frame grain made a 300 MB file; this is ~70 MB
    res_file = os.path.join(RENDERS, "shot01_establishing", "res")
    res = open(res_file).read().strip().replace("x", ":") if os.path.exists(res_file) else "270:480"
    twos = open(os.path.join(RENDERS, "shot01_establishing", "twos")).read().strip() == "1" \
        if os.path.exists(os.path.join(RENDERS, "shot01_establishing", "twos")) else True
    vf += (f"scale={res}:flags=neighbor,{'fps=12,' if twos else ''}noise=alls=5:allf=t,fps=24,"
           "scale=1080:1920:flags=neighbor,") if film else ""
    vf += f"ass={ass}"
    enc = ["-crf", "24", "-preset", "medium"] if film else ["-crf", "20"]
    run(["ffmpeg", "-loglevel", "error", "-y", "-i", body, "-i", AUDIO,
         "-vf", vf, "-map", "0:v", "-map", "1:a", "-shortest",
         "-c:v", "libx264", *enc, "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
         "-movflags", "+faststart", out])
    os.remove(body)
    print("->", out)


if __name__ == "__main__":
    sys.exit(main())
