"""Licensed Kokoro TTS through deAPI's OpenAI-compatible speech endpoint."""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

import httpx

from pipeline.edge_tts_synth import SentenceTiming

DEAPI_SPEECH_URL = "https://oai.deapi.ai/v1/audio/speech"
DEFAULT_MODEL = "Kokoro"
DEFAULT_VOICE = "af_bella"


def _ffprobe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def _estimated_sentence_timings(text: str, duration: float) -> list[SentenceTiming]:
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    if not sentences:
        sentences = [text.strip()]

    weights = [max(len(s.split()), 1) for s in sentences]
    total_weight = sum(weights)
    total_ms = max(int(duration * 1000), 1)
    offset_ms = 0
    timings: list[SentenceTiming] = []

    for index, (sentence, weight) in enumerate(zip(sentences, weights)):
        sentence_ms = (
            total_ms - offset_ms
            if index == len(sentences) - 1
            else max(int(total_ms * weight / total_weight), 1)
        )
        timings.append(
            SentenceTiming(
                text=sentence,
                offset_ms=offset_ms,
                duration_ms=sentence_ms,
            )
        )
        offset_ms += sentence_ms

    return timings


def synthesize_full(
    text: str, out_path: Path, voice: str | None = None,
) -> tuple[float, list[SentenceTiming]]:
    """Generate speech and return duration plus estimated sentence timings."""
    token = os.environ.get("DEAPI_TOKEN", "").strip()
    if not token:
        raise RuntimeError("DEAPI_TOKEN is required for licensed Kokoro TTS")

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    response = httpx.post(
        DEAPI_SPEECH_URL,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "model": os.environ.get("DEAPI_TTS_MODEL", DEFAULT_MODEL),
            "voice": voice or os.environ.get("DEAPI_TTS_VOICE", DEFAULT_VOICE),
            "input": text,
            "response_format": "mp3",
            "speed": float(os.environ.get("DEAPI_TTS_SPEED", "1.0")),
        },
        timeout=180.0,
    )
    response.raise_for_status()
    out_path.write_bytes(response.content)

    duration = _ffprobe_duration(out_path)
    return duration, _estimated_sentence_timings(text, duration)
