"""Generate a no-voice sound-effects bed for visual unboxing Shorts."""
from __future__ import annotations

import math
import random
import shutil
import struct
import subprocess
import wave
from pathlib import Path


SAMPLE_RATE = 44_100
DEFAULT_DURATION = 36.0


def _add_tone(
    samples: list[float],
    start: float,
    duration: float,
    freq_start: float,
    freq_end: float,
    volume: float,
) -> None:
    start_i = max(0, int(start * SAMPLE_RATE))
    count = max(1, int(duration * SAMPLE_RATE))
    end_i = min(len(samples), start_i + count)
    phase = 0.0
    for i in range(start_i, end_i):
        pos = (i - start_i) / count
        freq = freq_start + (freq_end - freq_start) * pos
        phase += 2 * math.pi * freq / SAMPLE_RATE
        env = math.sin(math.pi * pos)
        samples[i] += math.sin(phase) * env * volume


def _add_hit(samples: list[float], start: float, volume: float) -> None:
    start_i = max(0, int(start * SAMPLE_RATE))
    count = int(0.45 * SAMPLE_RATE)
    rnd = random.Random(int(start * 1000))
    for j in range(count):
        i = start_i + j
        if i >= len(samples):
            break
        pos = j / count
        decay = math.exp(-9 * pos)
        low = math.sin(2 * math.pi * 72 * j / SAMPLE_RATE) * decay
        noise = (rnd.random() * 2 - 1) * decay * 0.55
        samples[i] += (low + noise) * volume


def _write_wav(path: Path, samples: list[float]) -> None:
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        frames = bytearray()
        for sample in samples:
            sample = max(-0.98, min(0.98, sample))
            frames.extend(struct.pack("<h", int(sample * 32767)))
        wav.writeframes(bytes(frames))


def synthesize_full(narration: str, out_path: Path, voice: str | None = None) -> tuple[float, list]:
    """Write an MP3 containing cinematic whooshes, clicks, risers, and hits."""
    del narration, voice

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    duration = DEFAULT_DURATION
    total = int(duration * SAMPLE_RATE)
    samples = [0.0] * total

    rnd = random.Random(42)
    for i in range(total):
        t = i / SAMPLE_RATE
        bed = math.sin(2 * math.pi * 44 * t) * 0.018
        shimmer = math.sin(2 * math.pi * 880 * t) * 0.004
        samples[i] += bed + shimmer + (rnd.random() * 2 - 1) * 0.006

    for start in [0.6, 5.8, 11.2, 17.1, 23.4, 29.0]:
        _add_tone(samples, start, 1.15, 180, 980, 0.13)
        _add_hit(samples, start + 1.05, 0.34)

    for start in [3.2, 8.7, 14.5, 20.2, 26.5, 32.0]:
        _add_tone(samples, start, 0.22, 1500, 900, 0.10)

    wav_path = out_path.with_suffix(".wav")
    _write_wav(wav_path, samples)

    if shutil.which("ffmpeg"):
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "warning",
                "-i", str(wav_path),
                "-c:a", "libmp3lame", "-b:a", "192k",
                str(out_path),
            ],
            check=True,
        )
        wav_path.unlink(missing_ok=True)
    else:
        wav_path.replace(out_path)

    return duration, []
