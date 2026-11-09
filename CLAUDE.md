# Jaws series — project notes for Claude

A comedy Instagram Reels series ("Jaws 5", "Jaws 6", …). The owner records a
voiceover pitching an absurd sequel; we make an intentionally cheap
1998-PlayStation-style 3D video for it. Everything is built from code in
Blender (primitives only, **no downloaded assets**), rendered headlessly with
EEVEE, and assembled with ffmpeg. Jaws 5 (`episodes/jaws5/`) is the finished
reference episode: copy its patterns.

## Making a new episode (e.g. Jaws 6)

1. **Inputs** go in `episodes/jaws6/`: `script.md` (the text) and
   `audio/narration.m4a`. The owner may send a phone video (`.mp4`, often a
   black screen): extract the audio with
   `ffmpeg -i in.mp4 -vn -c:a copy episodes/jaws6/audio/narration.m4a`.
   If there is no written script, transcribe first and use that.
2. **Transcribe** before planning: the recording is usually ad-libbed and
   tighter than the written script. Shots must follow what was *said*.
   `python3 tools/assemble.py jaws6` transcribes (cached in
   `audio/transcript.json`); or run Whisper directly.
3. **Shot list**: one shot per beat of narration, 4–8 s each (fast
   narration can force shorter), simple camera moves (slow push-ins, pans,
   a little shake for action). Propose it to the owner and get approval
   before building, as was done for Jaws 5.
4. **Scenes**: one script per shot in `episodes/jaws6/scenes/shotNN_name.py`
   (copy a Jaws 5 scene as a template). `shot00_title.py` and an end card
   (`build_title(F, "7", subtitle="COMING SOON")`) come almost free from
   `lib/jaws/title.py`. Each scene reads its length with
   `shot_seconds("shotNN", default)`.
5. **Episode config** `episodes/jaws6/episode.py` (copy Jaws 5's): `CUES`
   (shot → phrase where it starts, + nudge seconds), caption `FIXES` /
   `PHRASE_FIXES` / `SAID` corrections, `DEFAULTS`, `TITLE`, `WHISPER_PROMPT`.
6. **Preview cheaply** while building: `JAWS_FRAMES=1,60,120 tools/render.sh
   episodes/jaws6/scenes/shot03_x.py` renders a few stills in seconds. Look
   at them (Read the PNGs, or tile with ffmpeg) before full renders. A
   low-res pass (`JAWS_JANK=1`, ~10 s/shot) is fine for checking motion.
7. **Final**: `tools/render_all.sh jaws6` (full HD) then
   `python3 tools/assemble.py jaws6 --render` →
   `episodes/jaws6/final/jaws6.mp4` (title + shots + narration + captions).
   Check frames at key lines against the transcript before sending.

## Series so far (for recaps and continuity)

- **Jaws 5**: a shark rams a ferry off Amity, a swarm attacks ("Shark 911").
  Brody (Pedro Pascal) and oceanographer Jesse (Jesse Plemons, red beanie)
  track them on radar to an egg cave under the Flying Horses carousel; Brody's
  mechanical shark sub lures them with a giant ham, they blow the entrance,
  drill through the carousel and pump the cave dry.
- **Jaws 6**: opens with "Previously on Jaws 5" (reused Jaws 5 footage) and a
  99% critics score. Fourth of July in Edgartown Harbor at dusk: a shark rams
  the fireworks barge, it tips, rockets fire flat into the sailboats ("War of
  1812", the anthem won't stop). The radar finds them under the harbor; same
  plan as Jaws 5, cave under the bookstore. Twist: the sharks are
  **radioactive mutants** (glowing green). Ends on the open question "where
  are they coming from?": a green glow on the horizon. Sets up Jaws 7.
- **Jaws 7**: (built in another session) the Russian nuclear sub; Brody steals it.
- **Jaws 8**: Brody takes the stolen sub to Leningrad with American soldiers in
  ushanka disguises (plus one guy who actually speaks Russian), sneaks into the
  Kremlin and hears Soviet leader Brezhnev (played by **Bill Belichick**: cut-off
  hoodie, X's and O's chalkboard) explain the plan: scare Americans out of the
  water so nobody joins the Navy or Coast Guard, then win the Cold War at sea.
  **CIA officer Rob Gronkowski** smuggles Brody and Jesse out in a truck to
  Finland and a plane home. Amity was just the start; the plan is still in
  motion; only Brody can stop it. Sets up Jaws 9. The sub is a placeholder
  (`soviet.make_sub`, `_recap_sub.py`) until the Jaws 7 model/footage is merged.
- Episode patterns that worked: the title card plays under the intro line
  when the narration starts at 0 s; a recap shot from earlier renders
  (`shot01_recap.py`); cast cards on "played by ...".

## House style (current defaults, chosen by the owner)

- **Full HD clean low-poly**: native 1080x1920, 24 fps, AA 8, soft shadows,
  ambient occlusion, gentle bloom (`JANK=0`, `HD=True` in `common.py`).
  The models stay chunky and flat-shaded; the joke is the cheap style, but it
  should look *good for the style*.
- **70s film look** (`JAWS_LOOK=70s`, the default): hazy dusty sky, low warm
  sun, muted olive/teal/amber palette, film grade + halation + vignette in
  `tools/render.sh`, light soft grain added once in `assemble.py`.
- Captions: big bold white caps, black outline, lower third, ≤4 words per
  chunk. Keep important action out of the bottom ~25% of frame.
- Older looks remain available per render: `JAWS_JANK=1` (PS1 jank: low res,
  vertex wobble, dithered palette, 12 fps), `2` (+ ragdolls, CRT), `3`
  (+ deliberate bugs), `JAWS_LOOK=sunny`. See README "Quality knobs".

## Reusable assets (`lib/jaws/`)

- `shark.py`: `make_shark(name, loc, rot_z, scale, variant="real"|"mech")`,
  `open_jaw`, `chomp`, `swim_wag`. Shared meshes: swarms of 20–100 are cheap.
- `people.py`: `make_brody`, `make_jesse` (red beanie + shades), `walk`,
  `point`. Rigs: `p.root/head/torso/arm_l/arm_r/leg_l/leg_r`, face −Y.
- `world.py`: `make_ocean`, `make_island` (Amity: houses, lighthouse,
  harbor; returns `dock_end`, `carousel_spot`), `make_ferry`,
  `make_small_boat`, `make_extra` (tourists/kids), `make_gull`, `splash`,
  `bob`, ragdolls (`make_ragdoll_extra`, `rigid`).
- `props.py`: `make_carousel`/`animate_carousel`, radar (`make_radar`,
  `radar_land`, `dot_line`, `radar_sweep`, `blink`), `underwater`,
  `make_cave_cutaway`, `make_bait`, `explosion`, `make_drill`, `make_pump`,
  `water_spray`.
- `fireworks.py` (Jaws 6): `dusk(s)` night sky (call before `make_island` so
  windows glow), `firework`, `burst`, `rocket_streak` (flat rockets),
  `make_barge`, `fire` (flames + smoke + flicker light), `smoke_pall`,
  `flash_light`. Keep spark emission low (~1.5) or colors clip to white.
- `town.py` (Jaws 6): `make_bookstore`, `make_marquee`/`chase_bulbs`,
  `make_sailboat`, `make_flag` (waving), `bunting`, `make_pa_pole`,
  `music_notes`, `question_mark`, `light_bulb`, `pop_in`, `make_tomato`.
- `soviet.py` (Jaws 8): `make_sub` (placeholder), `make_kremlin`, `make_brezhnev`,
  `make_gronk`, `make_soldier` (ushanka; `disguise=True` adds fake mustache),
  `_hat_ushanka` (any rig), `make_truck`, `make_plane`, `make_border_gate`,
  `make_map_table` + `pin`/`dotted_path`/`follow_path` (war-room map),
  `make_chalkboard`/`chalk_mark`/`chalk_arrow`, `speech_bubble`,
  `make_soviet_flag`, `make_recruit_booth`, `make_tumbleweed`/`roll`,
  `alarm_light`, `sweat`, `spin`. Test still: `tests/scenes/test_soviet.py`.
- Radioactive: `make_shark(..., variant="rad")` (glowing green),
  `props.make_rad_sign`, `make_geiger`/`needle_swing`, `make_beaker`.
- Reusing old footage: `episodes/jaws6/scenes/shot01_recap.py` loads earlier
  renders into Blender's sequencer and sets `LOOK = "clip"` so it isn't
  graded twice.
- `common.py`: scene/camera (`reset_scene`, `add_sun`, `add_camera`,
  `key_camera`, `add_shake`), `mat` (look-aware), `box/cyl/ico/text/decal`,
  `pixel_mat` (ASCII-art textures), `shot_seconds`, `render`.
- Build new recurring assets as functions in `lib/jaws/` so later episodes
  reuse them; give each a test still in `tests/scenes/`.

## Hard-won lessons

- **Whisper**: use `medium.en` with `WHISPER_PROMPT` (names/places).
  `small.en` heard the owner's "shark" as "shock". Never use "shark" in CUE
  phrases. Ask the owner about unclear phrases and fix them with `SAID`.
- **Cue matching** tries the transcript first, then the script. Check the
  printed `@ time 'words'` lines; nudge with the third CUES value.
- **Render time**: full HD is ~3–4 s/frame (CPU, no GPU), ~2–2.5 h per
  episode (Jaws 6: 18 shots in 1 h 45 min; night shots with many lights ~3 s/frame).
  Cloud background jobs are killed at **2 h**: `render_all.sh` resumes
  (skips finished shots); split long shots with `JAWS_RANGE=1-110`,
  `JAWS_RANGE=111-999`, then `JAWS_ENCODE_ONLY=1` (each step < 10 min).
- **Labels**: text must not cast shadows. `text()` sets the material's
  `shadow_method = "NONE"` (EEVEE legacy ignores `visible_shadow`). Don't
  share a text material with non-text objects.
- **Overlapping surfaces flicker** (z-fighting) in HD, e.g. a prop placed
  inside the carousel column; hide or offset one of them.
- **Rigid bodies**: the cache is simulated in `render()` after all edits;
  never put the PS1 vertex-snap modifier on rigid bodies.
- Key event frames proportionally to the shot length (`int(F * 0.4)`), since
  lengths change when retimed to the narration.
- Grain is expensive to compress: keep it light (HD reel ≈ 26 MB).
- The 3D characters stay generic blocky figures, and no real brands (e.g.
  ferry company logos) in the 3D scenes. Exception, chosen by the owner:
  **cast photo cards**. When the narration names the cast ("Police Chief
  Brody, played by Pedro Pascal", "Jesse, played by Jesse Plemons"), the
  owner's photos in `assets/cast/` pop up as tilted cards (original 1975
  Brody on "Police Chief Brody", then the actor on "played by ..."). The
  same cards work for any image on a line (Jaws 6: a War of 1812 painting
  on "friggin' War of 1812"). Set them
  in `CAST` in `episode.py`; `assemble.py` overlays them (no re-render).

## Environment

Cloud environment "Jaws": Blender 4.0 + xvfb (apt), `openai-whisper` (pip;
if `import whisper` fails at session start, `pip install openai-whisper`),
network access to `openaipublic.azureedge.net` for Whisper model weights
(Hugging Face and download.blender.org are blocked). Use `xvfb-run` (faster
than pure background mode). Commit and push finished renders and finals:
the container is temporary.
