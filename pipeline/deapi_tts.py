"""Licensed Kokoro TTS through deAPI's OpenAI-compatible speech endpoint."""
from __future__ import annotations

import os
import re
import subprocess
import time
from pathlib import Path

import httpx

from pipeline.edge_tts_synth import SentenceTiming

DEAPI_SPEECH_URL = "https://api.deapi.ai/api/v2/audio/speech"
DEAPI_JOB_URL = "https://api.deapi.ai/api/v2/jobs"
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
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    with httpx.Client(timeout=180.0) as client:
        response = client.post(
            DEAPI_SPEECH_URL,
            headers=headers,
            data={
                "text": text,
                "model": os.environ.get("DEAPI_TTS_MODEL", DEFAULT_MODEL),
                "lang": "en-us",
                "speed": os.environ.get("DEAPI_TTS_SPEED", "1.0"),
                "format": "mp3",
                "sample_rate": "24000",
                "mode": "custom_voice",
                "voice": voice or os.environ.get("DEAPI_TTS_VOICE", DEFAULT_VOICE),
            },
        )
        response.raise_for_status()
        request_id = response.json().get("data", {}).get("request_id")
        if not request_id:
            raise RuntimeError(f"No request_id in deAPI TTS response: {response.text}")

        result_url = ""
        for _ in range(90):
            time.sleep(2)
            poll = client.get(f"{DEAPI_JOB_URL}/{request_id}", headers=headers)
            poll.raise_for_status()
            payload = poll.json()
            data = payload.get("data", {})
            status = payload.get("status") or data.get("status") or ""
            result_url = data.get("result_url") or data.get("result") or ""
            if result_url:
                break
            if status in {"error", "failed"}:
                raise RuntimeError(f"deAPI TTS job failed: {payload}")
        else:
            raise RuntimeError(f"deAPI TTS timed out for request {request_id}")

        audio = client.get(result_url)
        audio.raise_for_status()
        out_path.write_bytes(audio.content)

    duration = _ffprobe_duration(out_path)
    return duration, _estimated_sentence_timings(text, duration)
