# Jaws series — PS1-style comedy reels

Intentionally janky 1998-PlayStation-style 3D, built entirely from code in
Blender (no downloaded assets), rendered headlessly with EEVEE at
1080×1920 / 24 fps.

## Layout

| Path | What |
|---|---|
| `lib/jaws/` | shared asset library: sharks, Brody/Jesse, island, ferry, boats, carousel, radar, cave, effects, title cards |
| `episodes/<ep>/scenes/shotNN_*.py` | one script per shot |
| `episodes/<ep>/episode.py` | shot cues, caption fixes, Whisper vocabulary |
| `episodes/<ep>/script.md`, `audio/narration.m4a` | the script and the recording |
| `episodes/<ep>/renders/`, `final/<ep>.mp4` | rendered shots and the finished reel |
| `tools/render.sh` | render one scene |
| `tools/render_all.sh <ep>` | render every shot of an episode (resumable) |
| `tools/assemble.py <ep>` | Whisper → shot timing → (re-render) → title + shots + narration + captions |
| `tests/scenes/` | model test stills |
| `CLAUDE.md` | workflow, house style and lessons for new sessions |

## Usage

```bash
tools/render.sh episodes/jaws5/scenes/shot05_boats_sinking.py        # one shot (5-12 min in HD)
JAWS_FRAMES=1,60,120 tools/render.sh episodes/jaws5/scenes/shot05_boats_sinking.py   # quick stills
tools/render_all.sh jaws5                                            # every shot (~2.5 h in HD)
python3 tools/assemble.py jaws5 --render                             # -> episodes/jaws5/final/jaws5.mp4
```

## Jank levels

Default is **0** (clean full HD). Set `JAWS_JANK=N` for a render, or put
`os.environ.setdefault("JAWS_JANK", "2")` at the top of a single scene.

- **0** clean full-HD low-poly (AA, soft shadows, AO, bloom)
- **1** PS1 hardware: animation on twos (12 fps), screen-space vertex snapping
  (wobble), 270×480 internal res, 48-color dithered palette
- **2** + distance fog/pop-in, rigid-body ragdolls with pixel-art faces, googly
  shark eyes, CRT/VHS post (scanlines, color bleed, grain, vignette)
- **3** + deliberate bugs (see `episodes/jaws5/scenes/shot02_ferry_rammed.py`)

## Quality knobs

Jank sets defaults; override any single one per render:

| Env var | Values | Effect |
|---|---|---|
| `JAWS_PIXEL_SCALE` | 1 (default), 2, 3, 4 | internal res 270x480 … native 1080x1920 |
| `JAWS_SNAP` | 1 / 0 | PS1 vertex wobble on/off |
| `JAWS_AA` | 8 (default), 1 … 16 | anti-aliasing samples (1 = jagged edges) |
| `JAWS_COLORS` | 48 / N / 0 | dithered palette size (0 = full color) |
| `JAWS_TWOS` | 1 / 0 | 12 fps animation vs smooth 24 |

See `docs/quality_compare.png` for four presets on the ferry.

## Looks

`JAWS_LOOK=70s` (default) or `JAWS_LOOK=sunny` (the original bright palette). `70s`
gives hazy dusty skies, a low warm sun, a muted olive/teal/amber palette, a
film grade with warm halation and vignette, and chunky grain on twos (added
in `assemble.py`).

## Requirements

Blender 4.0 (`apt-get install blender xvfb`), ffmpeg, `pip install openai-whisper`
(model `medium.en`, downloaded on first use).
