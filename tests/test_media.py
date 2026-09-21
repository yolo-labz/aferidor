#!/usr/bin/env python3
"""Actual negative media test: erase only the final frame's experimental line.

Requires FFmpeg; lives in make check-media, not the stdlib-only CI test suite.
"""
from pathlib import Path
import runpy
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent
CHECK = runpy.run_path(str(ROOT / "scripts/check-media.py"))["check"]
ASSETS = ROOT / "docs/assets/rendered"

with tempfile.TemporaryDirectory(prefix="aferidor-media-negative-") as directory:
    bad = Path(directory) / "missing-experimental.mp4"
    subprocess.run([
        "ffmpeg", "-v", "error", "-i", str(ASSETS / "portrait.mp4"),
        "-vf", "drawbox=x=0:y=172:w=1080:h=108:color=0xCF222E:t=fill:enable='eq(n,959)'",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "20", "-threads", "0",
        "-pix_fmt", "yuv420p", "-an", str(bad)], check=True)
    try:
        CHECK(bad, ASSETS / "portrait.png")
    except ValueError as error:
        if "disclosure missing/altered at frame 959" not in str(error):
            raise AssertionError(f"failed for the wrong reason: {error}") from error
        print(f"ok — rejected final-frame-only disclosure damage: {error}")
    else:
        raise AssertionError("missing experimental disclosure passed")
