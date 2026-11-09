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
CUES = [
    ("shot01_establishing", "we start jaws five on amity island"),
    ("shot02_ferry_rammed", "ferry that gets rammed by a shark"),
    ("shot03_swarm", "a whole swarm of great white sharks"),
    ("shot04_flotilla", "marshalls up all of the boats in amity island harbor"),
    ("shot05_boats_sinking", "a bunch of them get rammed by sharks"),
    ("shot06_jesse_arrives", "chief oceanographer jesse"),
    ("shot07_radar_line", "use their advanced radar detection"),
    ("shot08_mech_in_line", "mechanical shark submarine"),
    ("shot09_cave", "all the sharks are going to a shark cave"),
    ("shot10_bait", "putting some bait in there"),
    ("shot11_explosion", "put explosives on the cave entrance"),
    ("shot12_drilling", "kick all the kids off the ride"),
    ("shot13_pump", "put in a pump and pump out all the water"),
    ("shot14_radar_again", "their advanced radar goes silent"),
]
TITLE = "shot00_title"
DEFAULTS = {TITLE: 3.0, "shot01_establishing": 6, "shot02_ferry_rammed": 7, "shot03_swarm": 7,
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
    model = whisper.load_model("small.en")
    res = model.transcribe(AUDIO, word_timestamps=True, language="en",
                           initial_prompt="Jaws, Amity Island, Chief Brody, Jesse Plemons, Pedro Pascal, "
                                          "Steve Zissou, Flying Horses carousel, Edgartown Harbor.")
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
    starts, pos = {}, 0
    for shot, phrase in CUES:
        target = [norm(t) for t in phrase.split()]
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
        starts[shot] = words[ti]["s"]
        print(f"   {shot:24s} @ {starts[shot]:6.2f}s  '{' '.join(w['w'] for w in words[ti:ti + n])}'")
    return starts


def compute_timing(starts, duration):
    shots = [s for s, _ in CUES]
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
    for shot in [TITLE] + [s for s, _ in CUES]:
        have = rendered_seconds(shot)
        want = int(timing.get(shot, DEFAULTS[shot]) * FPS) / FPS
        if have is None or abs(have - want) > 0.1:
            run([os.path.join(REPO, "tools", "render.sh"), os.path.join(REPO, "scenes", f"{shot}.py")])


# ---------------------------------------------------------------- 4. captions + mux
def ass_time(t):
    h, rem = divmod(max(0, t), 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


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
    lines, chunk = [], []

    def flush():
        if chunk:
            txt = " ".join(w["w"] for w in chunk).upper()
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
    shots = [TITLE] + [s for s, _ in CUES]

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
    run(["ffmpeg", "-loglevel", "error", "-y", "-i", body, "-i", AUDIO,
         "-vf", f"ass={ass}", "-map", "0:v", "-map", "1:a",
         "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
         "-movflags", "+faststart", out])
    os.remove(body)
    print("->", out)


if __name__ == "__main__":
    sys.exit(main())
