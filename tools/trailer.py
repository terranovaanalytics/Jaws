#!/usr/bin/env python3
"""Assemble a no-narration, trailer-style episode: shots + trailer text cards +
a synthesized score + sound effects.

    python3 tools/trailer.py kids/cronchisk            # timing.json + final video
    python3 tools/trailer.py kids/cronchisk --audio-only  # just rebuild audio/score.wav

Reads <ep>/episode.py:
  SHOTS  [(shot, seconds)]                 -> timing.json (the scenes read it)
  CARDS  [(shot, offset, duration, text)]  -> burned-in trailer text
  SFX    [(shot, offset, kind)]            -> sound effects (kinds below)
  MUSIC  [(shot, section)]                 -> score sections from that shot on:
         intro | hit | drive | break | tension | climax | end
Everything is generated with numpy (no samples, no downloads).
Output: <ep>/final/<name>.mp4
"""
import argparse
import importlib.util
import json
import os
import subprocess
import wave

import numpy as np

SR = 44100
FPS = 24
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
rng = np.random.default_rng(7)


# ---------------------------------------------------------------- synth basics
def t_(dur):
    return np.arange(int(dur * SR)) / SR


def env(n, a=0.005, d=0.1, s=0.0, r=0.05, hold=None):
    """ADSR-ish envelope over n samples (times in seconds)."""
    e = np.zeros(n)
    A, D, R = int(a * SR), int(d * SR), int(r * SR)
    H = n - A - D - R if hold is None else int(hold * SR)
    H = max(0, H)
    i = 0
    seg = np.linspace(0, 1, max(1, A))
    e[i:i + len(seg)] = seg[:n - i]
    i += A
    if i < n:
        seg = np.linspace(1, s, max(1, D))
        e[i:i + len(seg)] = seg[:n - i]
        i += D
    if i < n:
        e[i:i + H] = s
        i += H
    if i < n:
        seg = np.linspace(s, 0, max(1, R))
        e[i:i + len(seg)] = seg[:n - i]
    return e


def hz(note):
    """'E2' / 'F#3' / 'Bb1' -> frequency."""
    names = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
    n = names[note[0]]
    rest = note[1:]
    if rest.startswith("#"):
        n += 1
        rest = rest[1:]
    elif rest.startswith("b"):
        n -= 1
        rest = rest[1:]
    midi = 12 * (int(rest) + 1) + n
    return 440.0 * 2 ** ((midi - 69) / 12)


def saw(f, t):
    return 2 * ((f * t) % 1.0) - 1


def square(f, t, duty=0.5):
    return np.where((f * t) % 1.0 < duty, 1.0, -1.0)


def lowpass(x, cutoff):
    """One-pole low-pass (cutoff Hz, scalar or array)."""
    a = np.exp(-2 * np.pi * np.asarray(cutoff, float) / SR)
    a = np.broadcast_to(a, x.shape)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc
        y[i] = acc
    return y


def lp_fast(x, cutoff):
    """Cheap fixed low-pass via FFT (for long noise beds)."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


def bp_fast(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= (1 / (1 + (lo / np.maximum(f, 1)) ** 4)) * (1 / (1 + (f / hi) ** 4))
    return np.fft.irfft(X, len(x))


def noise(dur):
    return rng.uniform(-1, 1, int(dur * SR))


def add(buf, x, at, gain=1.0):
    i = int(at * SR)
    if i >= len(buf) or i + len(x) <= 0:
        return
    if i < 0:
        x, i = x[-i:], 0
    n = min(len(x), len(buf) - i)
    buf[i:i + n] += x[:n] * gain


# ---------------------------------------------------------------- instruments
def bass(note, dur):
    t = t_(dur)
    f = hz(note)
    x = 0.6 * saw(f, t) + 0.5 * np.sin(2 * np.pi * f * t)
    x = lp_fast(x, 700)
    return x * env(len(t), 0.004, dur * 0.6, 0.35, 0.04)


def twang(note, dur, vib=True):
    """Surf/spy guitar: bright plucked saw, a bit of vibrato and echo."""
    t = t_(dur)
    f = hz(note) * (1 + (0.006 * np.sin(2 * np.pi * 5.5 * t) * np.clip(t * 3, 0, 1) if vib else 0))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = 0.55 * np.sign(np.sin(ph)) * 0.5 + 0.5 * np.sin(ph) + 0.25 * np.sin(2 * ph)
    x = lp_fast(x, 2600)
    x *= env(len(t), 0.003, dur * 0.8, 0.25, 0.08)
    out = x.copy()
    for k, g in ((0.18, 0.35), (0.36, 0.15)):              # slap echo
        d = int(k * SR)
        out[d:] += x[:-d] * g if d < len(x) else 0
    return out


def brass(notes, dur, bright=1.0):
    """Big brass stab/chord: detuned saws through a swelling low-pass."""
    t = t_(dur)
    x = np.zeros(len(t))
    for n in notes:
        f = hz(n)
        for det in (-0.004, 0.0, 0.005):
            x += saw(f * (1 + det), t)
    x /= len(notes) * 3
    cut = 600 + 3000 * bright * np.clip(t / 0.06, 0, 1) * np.exp(-t * 2.0)
    x = lowpass(x, cut)
    return x * env(len(t), 0.02, 0.25, 0.6, 0.15)


def pad(notes, dur, bright=900):
    t = t_(dur)
    x = np.zeros(len(t))
    for n in notes:
        f = hz(n)
        for det in (-0.003, 0.003):
            x += saw(f * (1 + det), t)
    x = lp_fast(x / (len(notes) * 2), bright)
    return x * env(len(t), min(1.0, dur * 0.3), 0.1, 1.0, min(1.0, dur * 0.3))


def kick():
    t = t_(0.3)
    f = 50 + 120 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def snare():
    t = t_(0.2)
    return (bp_fast(noise(0.2), 800, 7000) * 0.8 + 0.3 * np.sin(2 * np.pi * 190 * t)) * np.exp(-t * 18)


def hat(open_=False):
    d = 0.18 if open_ else 0.05
    t = t_(d)
    return bp_fast(noise(d), 7000, 15000) * np.exp(-t * (14 if open_ else 70))


def cymbal(dur=2.5):
    t = t_(dur)
    return bp_fast(noise(dur), 3000, 16000) * np.exp(-t * 1.6)


def timp(note, dur=0.8):
    t = t_(dur)
    f = hz(note)
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 1.5 * t)) * np.exp(-t * 4)


def strings_trem(notes, dur, rate=12):
    t = t_(dur)
    x = np.zeros(len(t))
    for n in notes:
        x += saw(hz(n), t)
    x = lp_fast(x / len(notes), 2200)
    trem = 0.6 + 0.4 * np.sign(np.sin(2 * np.pi * rate * t))
    return x * trem * env(len(t), 0.2, 0.1, 1.0, 0.2)


# ---------------------------------------------------------------- the score
BPM = 120
BEAT = 60 / BPM
BAR = 4 * BEAT
RIFF = [("E2", 0, 1), ("E2", 1.5, 0.5), ("G2", 2, 1), ("E2", 3, 0.5), ("D2", 3.5, 0.5),   # bar A
        ("A2", 4, 1), ("A2", 5.5, 0.5), ("C3", 6, 1), ("B2", 7, 1)]                      # bar B
RIFF2 = [("E2", 0, 1), ("E2", 1.5, 0.5), ("G2", 2, 1), ("A2", 3, 1),
         ("B2", 4, 1), ("B2", 5.5, 0.5), ("D3", 6, 0.5), ("C3", 6.5, 0.5), ("B2", 7, 1)]
TUNE = [("B4", 0, 1.5), ("E5", 1.5, 0.5), ("D5", 2, 1), ("B4", 3, 1),                    # 4-bar spy melody
        ("A4", 4, 0.5), ("B4", 4.5, 0.5), ("G4", 5, 1), ("E4", 6, 2),
        ("B4", 8, 1.5), ("E5", 9.5, 0.5), ("G5", 10, 1), ("F#5", 11, 1),
        ("E5", 12, 0.5), ("D5", 12.5, 0.5), ("B4", 13, 1), ("E5", 14, 2)]
STAB = ["E3", "B3", "D4", "G4"]          # Em7 stab
STAB_DARK = ["E3", "Bb3", "D4", "F4"]    # tension stab


def drums(buf, t0, bars, fill=True, busy=1.0, gain=0.5):
    for b in range(bars):
        base = t0 + b * BAR
        for k in range(4):
            if k in (0, 2) or (busy > 1 and k == 3):
                add(buf, kick(), base + k * BEAT, 0.9 * gain)
            if k in (1, 3):
                add(buf, snare(), base + k * BEAT, 0.5 * gain)
        for e in range(8 if busy <= 1 else 16):
            step = BEAT / 2 if busy <= 1 else BEAT / 4
            add(buf, hat(open_=(e % 4 == 3 and busy <= 1)), base + e * step, 0.25 * gain)
        if fill and b % 4 == 3:
            for k in range(4):
                add(buf, snare(), base + 3 * BEAT + k * BEAT / 4, 0.35 * gain * (k + 1) / 4)


def riff(buf, t0, bars, which=RIFF, gain=0.5, octave_up=False):
    for b in range(0, bars, 2):
        for n, at, d in which:
            if b + at / 4 >= bars:
                continue
            note = n if not octave_up else n[:-1] + str(int(n[-1]) + 1)
            add(buf, bass(note, d * BEAT * 0.95), t0 + b * BAR + at * BEAT, gain)


def score(total, sections):
    """sections: [(start_time, name)] sorted. Returns a mono float buffer."""
    buf = np.zeros(int((total + 3) * SR))
    sec = sections + [(total, "_stop")]
    for (s0, name), (s1, _) in zip(sec, sec[1:]):
        bars = max(1, int(np.ceil((s1 - s0) / BAR)))
        dur = s1 - s0
        if name == "intro":
            add(buf, pad(["E1", "E2", "B2"], dur + 0.5, 400), s0, 0.35)
            for b in range(int(dur / BEAT)):
                if b % 2 == 0:
                    add(buf, bass("E2", BEAT * 0.8), s0 + b * BEAT, 0.35)
                add(buf, hat(), s0 + b * BEAT + BEAT / 2, 0.12)
                if b % 8 == 6:
                    add(buf, twang("B3", BEAT * 1.6), s0 + b * BEAT, 0.18)
                    add(buf, twang("C4", BEAT * 1.2), s0 + b * BEAT + BEAT * 1.5, 0.14)
        elif name == "hit":
            add(buf, brass(STAB, 1.6), s0 + 1.9, 0.5)
            add(buf, cymbal(3), s0 + 1.9, 0.35)
            add(buf, timp("E2", 1.2), s0 + 1.9, 0.6)
            add(buf, strings_trem(["E3", "B3", "E4"], 1.8), s0, 0.12)
            riff(buf, s0 + 1.9 + BEAT, max(1, int((dur - 2.4) / BAR) + 1), gain=0.45)
            drums(buf, s0 + 1.9 + BEAT, max(1, int((dur - 2.4) / BAR) + 1), fill=False, gain=0.45)
        elif name in ("drive", "climax"):
            big = name == "climax"
            drums(buf, s0, bars, busy=1.6 if big else 1.0, gain=0.55 if big else 0.45)
            riff(buf, s0, bars, which=RIFF2 if big else RIFF, gain=0.5)
            for b in range(bars):
                if b % 2 == 0:
                    add(buf, brass(STAB, BEAT * 0.9), s0 + b * BAR, 0.32 if big else 0.22)
            mel_start = s0 + (0 if big else 2 * BAR)
            reps = int((s1 - mel_start) / (4 * BAR)) + 1
            for r in range(reps):
                for n, at, d in TUNE:
                    tt = mel_start + r * 4 * BAR + at * BEAT
                    if tt < s1 - 0.1:
                        add(buf, twang(n, d * BEAT * 1.1), tt, 0.24 if big else 0.2)
            if big:
                add(buf, strings_trem(["E4", "G4", "B4"], dur), s0, 0.07)
        elif name == "break":
            add(buf, pad(["E2", "G2", "B2"], dur + 0.3, 700), s0, 0.3)
            for b in range(int(dur / BEAT)):
                add(buf, bass("E2", BEAT * 0.4), s0 + b * BEAT, 0.4)
                add(buf, kick(), s0 + b * BEAT, 0.35)
        elif name == "tension":
            steps = int(dur / (BEAT / 2))
            for k in range(steps):
                n = ["E2", "F2", "E2", "F#2"][(k // 2) % 4]
                add(buf, bass(n, BEAT * 0.45), s0 + k * BEAT / 2, 0.42)
                add(buf, hat(), s0 + k * BEAT / 2, 0.14)
            for k in range(int(dur / BEAT)):
                add(buf, timp("E2" if k % 2 == 0 else "B1", 0.6), s0 + k * BEAT, 0.3)
            add(buf, strings_trem(["E4", "F4", "Bb4"], dur, rate=16), s0, 0.1)
        elif name == "end":
            add(buf, brass(["E2", "B2", "E3", "G3", "B3", "F#4", "E4"], 4.5, bright=1.2), s0 + 0.0, 0.5)
            add(buf, twang("E5", 1.0), s0 + 0.05, 0.2)
            add(buf, twang("B4", 3.0), s0 + 0.55, 0.2)
            add(buf, cymbal(4), s0, 0.35)
            add(buf, timp("E2", 1.5), s0, 0.7)
            add(buf, pad(["E2", "B2", "G3", "D4"], dur + 1, 1200), s0 + 0.2, 0.25)
            add(buf, twang("E4", 2.5), s0 + 3.2, 0.18)           # the little final guitar twang
            add(buf, twang("B4", 2.0), s0 + 3.45, 0.14)
            add(buf, twang("E5", 2.5), s0 + 3.7, 0.16)
    return buf


# ---------------------------------------------------------------- sound effects
def sfx(kind):
    if kind == "rain":
        x = bp_fast(noise(7.0), 1500, 9000) * 0.35
        return x * env(len(x), 0.6, 0.1, 1.0, 1.5)
    if kind == "waves":
        d = 6.5
        t = t_(d)
        x = lp_fast(noise(d), 900) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 3.2) ** 2)
        return x * env(len(t), 0.5, 0.1, 1.0, 1.5) * 1.2
    if kind == "latch":
        x = np.zeros(int(0.25 * SR))
        for at in (0.0, 0.12):
            c = bp_fast(noise(0.03), 2000, 8000) * np.exp(-t_(0.03) * 150)
            add(x, c, at, 1.0)
        return x
    if kind == "glass":
        d = 1.2
        t = t_(d)
        x = bp_fast(noise(d), 3000, 15000) * np.exp(-t * 5)
        for k in range(12):
            f = rng.uniform(2500, 7000)
            at = rng.uniform(0, 0.8)
            p = np.sin(2 * np.pi * f * t_(0.25)) * np.exp(-t_(0.25) * 25)
            add(x, p, at, 0.3)
        return x * 0.8
    if kind == "thud":
        t = t_(0.5)
        return (np.sin(2 * np.pi * np.cumsum(45 + 60 * np.exp(-t * 20)) / SR) * np.exp(-t * 7)
                + lp_fast(noise(0.5), 300) * np.exp(-t * 15)) * 0.9
    if kind == "slurp":
        d = 1.2
        t = t_(d)
        f = 300 + 900 * np.sin(np.pi * t / d) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t))
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.05, 0.1, 0.8, 0.3) * 0.4
    if kind == "whoosh":
        d = 1.0
        t = t_(d)
        x = noise(d)
        out = np.zeros_like(x)
        for k in range(8):                                  # moving band
            lo = 300 + 3000 * (k / 8)
            seg = slice(int(k / 8 * len(x)), int((k + 1) / 8 * len(x)))
            out[seg] = bp_fast(x, lo, lo * 2.5)[seg]
        return out * np.sin(np.pi * t / d) ** 2 * 0.8
    if kind == "boom":
        d = 2.5
        t = t_(d)
        x = lp_fast(noise(d), 400) * np.exp(-t * 2.2) * 1.4
        x += np.sin(2 * np.pi * np.cumsum(35 + 50 * np.exp(-t * 6)) / SR) * np.exp(-t * 3) * 0.9
        return x
    if kind == "hum":
        d = 4.0
        t = t_(d)
        return lp_fast(saw(55, t) + saw(55.7, t), 300) * env(len(t), 0.3, 0.1, 1.0, 1.5) * 0.25
    if kind == "chomp":
        t = t_(0.25)
        x = lp_fast(noise(0.25), 2500) * np.exp(-t * 25)
        x += np.sin(2 * np.pi * 120 * t) * np.exp(-t * 20) * 0.6
        return x
    if kind == "clang":
        d = 1.5
        t = t_(d)
        x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * dk) for f, dk in
                ((420, 3), (1130, 4), (1980, 5), (2770, 7), (3500, 9)))
        return x / 4
    if kind == "alarm":
        d = 3.6
        t = t_(d)
        f = np.where((t % 0.5) < 0.25, 880, 660)
        x = square(1, np.cumsum(f) / SR) * 0.5
        return lp_fast(x, 3000) * env(len(t), 0.01, 0.1, 1.0, 0.3) * 0.25
    if kind == "jet":
        d = 4.5
        t = t_(d)
        x = bp_fast(noise(d), 200, 3000) * np.clip(t / 1.5, 0, 1)
        x += saw(80 + 40 * t / d, t) * 0.15
        return x * env(len(t), 0.5, 0.1, 1.0, 1.2) * 0.7
    if kind == "zap":
        t = t_(0.5)
        f = 1800 * np.exp(-t * 6) + 200
        return square(1, np.cumsum(f) / SR) * np.exp(-t * 6) * 0.35
    if kind == "pop":
        t = t_(0.12)
        return np.sin(2 * np.pi * np.cumsum(400 + 900 * t / 0.12) / SR) * np.exp(-t * 30) * 0.7
    if kind == "gulp":
        d = 0.6
        t = t_(d)
        f = 500 - 350 * np.sin(np.pi * t / d)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.02, 0.1, 0.9, 0.15) * 0.9
    if kind == "bubbles":
        x = np.zeros(int(3.5 * SR))
        for k in range(22):
            at = rng.uniform(0, 3.2)
            dd = 0.06
            tt = t_(dd)
            b = np.sin(2 * np.pi * np.cumsum(rng.uniform(500, 1200) * (1 + 3 * tt / dd)) / SR) * np.exp(-tt * 40)
            add(x, b, at, 0.3)
        return x
    if kind == "radio":
        d = 1.2
        t = t_(d)
        x = bp_fast(noise(d), 1200, 3500) * 0.3 * env(len(t), 0.01, 0.1, 1.0, 0.1)
        add(x, np.sin(2 * np.pi * 1400 * t_(0.12)) * 0.4, 0.0)
        add(x, np.sin(2 * np.pi * 1800 * t_(0.08)) * 0.4, d - 0.1)
        return x
    if kind == "creak":
        d = 1.0
        t = t_(d)
        f = 300 + 200 * np.sin(2 * np.pi * 3 * t) + 100 * np.sin(2 * np.pi * 37 * t)
        return lp_fast(saw(1, np.cumsum(f) / SR), 2000) * env(len(t), 0.05, 0.2, 0.6, 0.2) * 0.25
    if kind == "sting":
        return brass(["E3", "F3", "Bb3", "Eb4"], 2.0, bright=1.4) * 1.1
    if kind == "power":
        d = 1.5
        t = t_(d)
        f = 60 + 500 * (t / d) ** 2
        return lp_fast(saw(1, np.cumsum(f) / SR), 2500) * env(len(t), 0.05, 0.1, 1.0, 0.2) * 0.35
    if kind == "beeps":
        x = np.zeros(int(3.0 * SR))
        for k in range(6):
            add(x, np.sin(2 * np.pi * 1500 * t_(0.09)) * 0.35, k * 14 / FPS)
        return x
    if kind == "powerdown":
        d = 1.4
        t = t_(d)
        f = 500 * np.exp(-t * 2.5) + 30
        return lp_fast(saw(1, np.cumsum(f) / SR), 2000) * env(len(t), 0.01, 0.1, 1.0, 0.4) * 0.4
    if kind == "clink":
        d = 1.2
        t = t_(d)
        x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 6) for f in (2093, 3136, 4186, 5274))
        x2 = np.zeros_like(x)
        add(x2, x, 0.0, 0.18)
        add(x2, x * 0.8, 0.07, 0.15)
        return x2
    raise ValueError(f"unknown sfx kind {kind!r}")


# ---------------------------------------------------------------- assembly
def load(ep):
    spec = importlib.util.spec_from_file_location("episode", os.path.join(ep, "episode.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def starts(shots):
    out, t = {}, 0.0
    for s, d in shots:
        n = round(d * FPS) / FPS
        out[s] = (t, n)
        t += n
    return out, t


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    st = (x * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.column_stack([st, st]).tobytes())


def build_audio(m, ep):
    st, total = starts(m.SHOTS)
    sections = sorted((st[s][0], name) for s, name in m.MUSIC)
    music = score(total, sections)
    fx = np.zeros_like(music)
    for s, off, kind in m.SFX:
        add(fx, sfx(kind), st[s][0] + off, 1.0)
    mix = music / max(1e-6, np.abs(music).max()) * 0.55 + fx / max(1e-6, np.abs(fx).max()) * 0.6
    n = int((total + 1.5) * SR)
    mix = mix[:n]
    fade = int(1.2 * SR)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix = np.tanh(mix * 1.3) / np.tanh(1.3)                  # gentle glue / limiter
    mix /= max(1e-6, np.abs(mix).max()) / 0.92
    os.makedirs(os.path.join(ep, "audio"), exist_ok=True)
    path = os.path.join(ep, "audio", "score.wav")
    write_wav(path, mix)
    return path, total


def ass_time(t):
    h, rem = divmod(max(0, t), 3600)
    mm, s = divmod(rem, 60)
    return f"{int(h)}:{int(mm):02d}:{s:05.2f}"


def write_cards(m, path):
    st, _ = starts(m.SHOTS)
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Card,DejaVu Sans,66,&H00FFFFFF,&H00FFFFFF,&H00101010,&H96000000,-1,0,0,0,100,100,8,0,1,4,4,2,70,70,470,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for s, off, dur, txt in m.CARDS:
        t0 = st[s][0] + off
        body = txt.replace("\n", "\\N")
        lines.append(f"Dialogue: 0,{ass_time(t0)},{ass_time(t0 + dur)},Card,,0,0,0,,{{\\fad(250,300)}}{body}")
    with open(path, "w") as fh:
        fh.write(head + "\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode", help="episode folder, e.g. kids/cronchisk")
    ap.add_argument("--audio-only", action="store_true")
    a = ap.parse_args()
    ep = os.path.abspath(a.episode)
    name = os.path.basename(ep)
    m = load(ep)
    with open(os.path.join(ep, "timing.json"), "w") as fh:
        json.dump(dict(m.SHOTS), fh, indent=1)
    print("1. score + sound effects")
    wav, total = build_audio(m, ep)
    print(f"   {total:.1f}s -> {wav}")
    if a.audio_only:
        return
    final = os.path.join(ep, "final")
    os.makedirs(final, exist_ok=True)
    print("2. text cards")
    ass = os.path.join(final, "cards.ass")
    write_cards(m, ass)
    print("3. assembling")
    inputs, pre, cat = [], "", ""
    for i, (s, d) in enumerate(m.SHOTS):
        inputs += ["-i", os.path.join(ep, "renders", f"{s}.mp4")]
        want = round(d * FPS) / FPS
        pre += f"[{i}:v]tpad=stop_mode=clone:stop_duration=1,trim=duration={want:.4f},setpts=PTS-STARTPTS[s{i}];"
        cat += f"[s{i}]"
    n = len(m.SHOTS)
    graph = pre + cat + f"concat=n={n}:v=1:a=0[c];[c]tpad=stop_mode=clone:stop_duration=1.5,ass={ass}[v]"
    out = os.path.join(final, f"{name}.mp4")
    cmd = ["ffmpeg", "-loglevel", "error", "-y", *inputs, "-i", wav, "-filter_complex", graph,
           "-map", "[v]", "-map", f"{n}:a", "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-shortest", "-c:v", "libx264", "-crf", "21", "-preset", "medium",
           "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print("->", out)


if __name__ == "__main__":
    main()
