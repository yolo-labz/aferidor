#!/usr/bin/env python3
"""Fail-closed portrait gate; requires FFmpeg/ffprobe (no Python packages).

The poster's RGB disclosure region is pinned after visual inspection. Compare
EVERY decoded video frame against it, including the experimental line. This is
an image-integrity check, not OCR or an independent semantic review. A changed
font renderer requires inspecting the new poster before updating its checksum.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs/assets/rendered"
BANNER_SHA256 = "06882686d2816184663b7b57d4d76062f0ded3f950814652d3fd330d4f0b4ced"


def decode(path: Path, crop: str, pix_fmt: str) -> bytes:
    return subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(path), "-vf", crop,
                                    "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", pix_fmt, "-"])


def check(video: Path, poster: Path) -> None:
    if not 0 < video.stat().st_size <= 8 * 1024 * 1024:
        raise ValueError("MP4 must be nonempty and <=8 MiB")
    info = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams",
                                              "-show_format", "-of", "json", str(video)]))
    streams = info["streams"]
    if len(streams) != 1 or streams[0]["codec_type"] != "video":
        raise ValueError("exactly one video stream and no audio expected")
    stream = streams[0]
    if (stream["codec_name"], stream["width"], stream["height"], stream["pix_fmt"]) != (
            "h264", 1080, 1920, "yuv420p"):
        raise ValueError("expected H.264 1080x1920 yuv420p")
    if stream["avg_frame_rate"] != "24/1" or stream.get("sample_aspect_ratio") != "1:1":
        raise ValueError("expected 24 fps, square pixels")
    if abs(float(info["format"]["duration"]) - 40) > 0.05:
        raise ValueError("expected five 8-second scenes")
    png = poster.read_bytes()
    if (png[:8] != b"\x89PNG\r\n\x1a\n" or
            (int.from_bytes(png[16:20], "big"), int.from_bytes(png[20:24], "big")) != (1080, 1920)
            or len(png) > 400 * 1024):
        raise ValueError("expected 1080x1920 PNG poster <=400 KiB")
    full = decode(poster, "crop=1080:280:0:0", "rgb24")
    if hashlib.sha256(full).hexdigest() != BANNER_SHA256:
        raise ValueError("poster disclosure differs from visually inspected reference")
    crop = "crop=1080:280:0:0,scale=540:140"
    reference = decode(poster, crop, "gray")
    # Focus on white glyphs, so a flat red box cannot pass on background area.
    glyphs = [i for i, value in enumerate(reference) if value > 160]
    if len(glyphs) < 3000:
        raise ValueError("reference disclosure lacks visible glyphs")
    count, worst = 0, 0.0
    cmd = ["ffmpeg", "-v", "error", "-i", str(video), "-vf", crop,
           "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as process:
        try:
            while frame := process.stdout.read(len(reference)):
                if len(frame) != len(reference):
                    raise ValueError("truncated decoded frame")
                error = sum(abs(frame[i] - reference[i]) for i in glyphs) / len(glyphs)
                worst = max(worst, error)
                if error > 6:
                    raise ValueError(f"disclosure missing/altered at frame {count}: glyph MAE={error:.2f}")
                count += 1
            if process.wait() != 0:
                raise ValueError("FFmpeg decode failed")
        finally:
            if process.poll() is None:
                process.terminate()
    if count != 960:
        raise ValueError(f"expected 960 decoded frames, got {count}")
    print(f"ok — H.264 1080x1920, 40s, 24fps, silent, {video.stat().st_size} bytes; "
          f"disclosure intact in {count}/960 frames (worst glyph MAE {worst:.3f})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, default=ASSETS / "portrait.mp4")
    parser.add_argument("--poster", type=Path, default=ASSETS / "portrait.png")
    args = parser.parse_args()
    check(args.video, args.poster)
