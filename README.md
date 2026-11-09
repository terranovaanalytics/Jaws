# Jaws 5 — PS1-style comedy reel

Intentionally janky 1998-PlayStation-style 3D, built entirely from code in
Blender (no downloaded assets), rendered headlessly with EEVEE at
1080×1920 / 24 fps.

## Layout

| Path | What |
|---|---|
| `lib/jaws/common.py` | scene/camera/render helpers, PS1 materials, **jank levels**, text, timing |
| `lib/jaws/shark.py` | great white + mech shark sub (shared meshes, hinged jaw, tail wag) |
| `lib/jaws/people.py` | Brody, Jesse (blocky rigs, walk/point helpers) |
| `lib/jaws/world.py` | ocean, Amity Island, ferry, small boats, extras, gulls, splashes, ragdolls |
| `lib/jaws/props.py` | carousel, radar screen, shark cave cutaway, bait, explosion, drill, pump, spray |
| `scenes/shotNN_*.py` | one script per shot (`shot00_title` … `shot14_radar_again`) |
| `tools/render.sh` | render one scene → `renders/<scene>.mp4` |
| `tools/assemble.py` | Whisper → shot timing → re-render → title + shots + narration + captions |
| `scripts/jaws5.md` | the narration script |
| `audio/jaws5.m4a` | the narration (add it!) |

## Usage

```bash
tools/render.sh scenes/shot05_boats_sinking.py           # re-render one shot (~10-20 s)
JAWS_FRAMES=1,60,120 tools/render.sh scenes/shot05_boats_sinking.py   # quick stills
python3 tools/assemble.py --render                        # full reel -> final/jaws5.mp4
python3 tools/assemble.py --silent                        # no audio yet: silent draft
```

`assemble.py` transcribes `audio/jaws5.m4a` with Whisper (`small.en`), finds
where each shot's cue line is spoken (`CUES` in the script — edit to move a
cut), writes `timing.json` (every scene reads its length from it), re-renders
shots whose length changed, and burns in captions.

## Jank levels

Default is **1**. Set `JAWS_JANK=N` for a render, or put
`os.environ.setdefault("JAWS_JANK", "2")` at the top of a single scene.

- **0** clean low-poly
- **1** PS1 hardware: animation on twos (12 fps), screen-space vertex snapping
  (wobble), 270×480 internal res, 48-color dithered palette
- **2** + distance fog/pop-in, rigid-body ragdolls with pixel-art faces, googly
  shark eyes, CRT/VHS post (scanlines, color bleed, grain, vignette)
- **3** + deliberate bugs (see `scenes/shot02_ferry_rammed.py`)

## Requirements

Blender 4.0 (`apt-get install blender xvfb`), ffmpeg, `pip install openai-whisper`.
