#!/usr/bin/env python3
"""Reflow the existing fixture cast, never execute its recorded commands.

Apache-2.0. Requires Python stdlib, DejaVu fonts, Inkscape and FFmpeg.
Run from any directory: python3 docs/assets/source/portrait.py
"""
from __future__ import annotations

import argparse
from html import escape
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import textwrap

SOURCE = Path(__file__).resolve().parent
RENDERED = SOURCE.parent / "rendered"
SECONDS = 8
FPS = 24
TITLES = ["01 / O aparelho", "02 / A vitrine local", "03 / Preço por litro",
          "04 / O toque registrado", "05 / O limite: pagar"]
DISCLOSURE = ["VITRINE LOCAL DE DEMONSTRAÇÃO", "NÃO É IFOOD NEM APP DE ENTREGA",
              "aferidor-fone é experimental"]


def recorded_blocks(path: Path = SOURCE / "demo-fone.cast") -> list[list[str]]:
    events = [json.loads(line) for line in path.read_text().splitlines()]
    if events[0].get("version") != 3:
        raise ValueError("expected the versioned asciicast v3 fixture")
    output = "".join(e[2] for e in events[1:] if e[1] == "o")
    output = re.sub(r"\x1b\[[0-9;]*[mHJ]", "", output).replace("\r", "")
    if "\x1b" in output:
        raise ValueError("unhandled terminal control sequence")
    blocks = [b.strip().splitlines() for b in re.split(r"(?m)^\$ ", output)[1:]]
    expected = ["aferidor-fone dispositivos", "aferidor-fone tela",
                "aferidor compare oleo-de-soja", "aferidor-fone tocar 'Adicionar Soya'",
                "aferidor-fone tocar 'Pagar'"]
    if [b[0] for b in blocks] != expected:
        raise ValueError("fixture commands changed; review portrait composition")
    return blocks


def reflow(block: list[str]) -> list[str]:
    """Preserve recorded words/numbers; only rearrange the wide table cells."""
    result = []
    for line in block:
        line = line.strip()
        # Coordinates are UI geometry, not prices; discard only trailing pairs.
        line = re.sub(r"\s+\(\d+,\d+\)$", "", line)
        if line.startswith("mercado ") or re.fullmatch(r"[- ]+", line):
            continue  # original column labels become per-row labels below
        if line.startswith(("atacarejo-online ", "mercado-do-bairro ")):
            fields = re.split(r"\s{2,}", line, maxsplit=5)
            if len(fields) != 6:
                raise ValueError("comparison table shape changed")
            name, median, low, high, count, date = fields
            lines = [name, f"mediana {median} / L", f"mín {low} · máx {high}",
                     f"n {count} · última {date}"]
        else:
            lines = [line]
        for item in lines:
            result.extend(textwrap.wrap(item, width=41, break_long_words=False,
                                        break_on_hyphens=False) or [""])
    # Empty spacing from a 30-row terminal wastes the portrait's reading area.
    result = [line for line in result if line]
    if len(result) > 21 or any(len(line) > 41 for line in result):
        raise ValueError("fixture no longer fits the portrait; recompose, do not shrink")
    return result


def scene_svg(index: int, lines: list[str]) -> str:
    def text(value: str, y: int, size: int, family="DejaVu Sans", colour="#1F2328", bold=False):
        return (f'<text x="64" y="{y}" font-family="{family}" font-size="{size}" '
                f'font-weight="{"bold" if bold else "normal"}" fill="{colour}">'
                f'{escape(value)}</text>')
    elements = ['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" '
                'viewBox="0 0 1080 1920">', '<title>Aferidor: replay textual da fixture local</title>',
                '<rect width="1080" height="1920" fill="white"/>',
                '<rect width="1080" height="280" fill="#CF222E"/>']
    for value, y in zip(DISCLOSURE, [82, 150, 224]):
        elements.append(text(value, y, 36, colour="white", bold=True))
    elements += [text("aferidor", 380, 70, bold=True),
                 text(TITLES[index], 478, 46, bold=True),
                 text("Saída do cast existente, reformatada", 544, 30, colour="#57606A")]
    for n, line in enumerate(lines):
        elements.append(text(line, 628 + n * 50, 38, family="DejaVu Sans Mono"))
    elements += ['<rect x="0" y="1690" width="1080" height="230" fill="#F6F8FA"/>',
                 text("REPLAY TEXTUAL · DADOS DE EXEMPLO", 1758, 32, bold=True),
                 text("Tempo editado · sem áudio · rascunho", 1812, 30),
                 text("Não é uma nova execução no celular.", 1866, 30), '</svg>']
    return "\n".join(elements)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--encoder", choices=["libx264", "h264_vaapi"], default="libx264")
    args = parser.parse_args()
    RENDERED.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="aferidor-portrait-") as directory:
        tmp = Path(directory)
        scenes = [scene_svg(i, reflow(b)) for i, b in enumerate(recorded_blocks())]
        sources = []
        for i, svg in enumerate(scenes):
            source = tmp / f"scene{i:02}.svg"
            source.write_text(svg)
            sources.append(str(source))
        # ponytail: five tiny cards in one batch avoid concurrent D-Bus app
        # registration; encoding below still uses VAAPI or all available CPUs.
        subprocess.run(["inkscape", f"--app-id-tag=portrait{os.getpid()}",
                        "--export-type=png", "-T", *sources], check=True)
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "warning", "-y"]
        if args.encoder == "h264_vaapi":
            cmd += ["-vaapi_device", "/dev/dri/renderD128"]
        cmd += ["-framerate", f"1/{SECONDS}", "-i", str(tmp / "scene%02d.png"),
                "-t", str(len(scenes) * SECONDS), "-r", str(FPS), "-an"]
        if args.encoder == "h264_vaapi":
            cmd += ["-vf", "format=nv12,hwupload", "-c:v", "h264_vaapi", "-qp", "22"]
        else:
            cmd += ["-c:v", "libx264", "-preset", "fast", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-threads", "0"]
        cmd += ["-movflags", "+faststart", str(tmp / "portrait.mp4")]
        subprocess.run(cmd, check=True)
        # Only replace deliverables after all rendering/encoding succeeds.
        shutil.copyfile(tmp / "portrait.mp4", RENDERED / "portrait.mp4")
        shutil.copyfile(tmp / "scene04.png", RENDERED / "portrait.png")
    print(f"portrait: {len(scenes)} cards, {len(scenes) * SECONDS}s, 1080x1920, silent")


if __name__ == "__main__":
    main()
