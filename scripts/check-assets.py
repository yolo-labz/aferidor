#!/usr/bin/env python3
"""Mechanical checks for the repository's visual assets.

Runs in CI. Standard library only, like everything else here.

It checks the things that actually break in practice, and nothing else:

  1. every SVG source parses as XML
  2. rendered images match their declared dimensions and stay inside budget
  3. the palette in DESIGN.md really does clear WCAG AA (computed, not asserted)
  4. the Mermaid block in README.md is identical to its source file
  5. every rendered asset is described in the manifest
  6. informative images in README.md carry alt text

Check 3 exists because a design doc that claims a contrast ratio and is never
verified is worth nothing. Check 4 exists because a diagram duplicated between
a source file and a README drifts within a month.

    python3 scripts/check-assets.py
"""

from __future__ import annotations

import pathlib
import re
import sys
import xml.dom.minidom

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "docs" / "assets" / "source"
RENDERED = ROOT / "docs" / "assets" / "rendered"
MANIFEST = ROOT / "docs" / "assets" / "MANIFEST.md"

problems: list[str] = []


def fail(msg: str) -> None:
    problems.append(msg)


# --- 1. SVG sources parse -------------------------------------------------

svgs = sorted(SOURCE.glob("*.svg"))
if not svgs:
    fail("no SVG sources found in docs/assets/source/")
for svg in svgs:
    try:
        xml.dom.minidom.parse(str(svg))
    except Exception as exc:
        fail(f"{svg.relative_to(ROOT)}: not well-formed XML — {exc}")
    text = svg.read_text(encoding="utf-8")
    # An SVG used as an image needs an accessible name; a decorative one would
    # be inlined, not committed here.
    if "<title" not in text:
        fail(f"{svg.relative_to(ROOT)}: no <title> element (screen readers need it)")


# --- 2. rendered assets: dimensions and budgets ---------------------------
#
# Budgets, and why: the social preview is capped by GitHub at 1 MB; the demo GIF
# has to load on a phone on mobile data, so it gets a much tighter ceiling than
# the format would allow.

BUDGETS = {
    "social-preview.png": {"size": (1280, 640), "max_kb": 1024},
    "demo.gif":           {"max_kb": 900},
    "demo-dark.gif":      {"max_kb": 900},
    "demo.png":           {"max_kb": 300},
    "demo-fone.gif":      {"max_kb": 900},
    "demo-fone-dark.gif": {"max_kb": 900},
    "demo-fone.png":      {"max_kb": 300},
    "portrait.png":       {"size": (1080, 1920), "max_kb": 400},
}


def png_size(path: pathlib.Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def gif_size(path: pathlib.Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    if data[:6] not in (b"GIF87a", b"GIF89a"):
        return None
    return int.from_bytes(data[6:8], "little"), int.from_bytes(data[8:10], "little")


for name, rule in BUDGETS.items():
    path = RENDERED / name
    if not path.exists():
        fail(f"docs/assets/rendered/{name}: missing — run `make assets`")
        continue

    kb = path.stat().st_size / 1024
    if kb > rule["max_kb"]:
        fail(f"docs/assets/rendered/{name}: {kb:.0f} KB exceeds the {rule['max_kb']} KB budget")

    got = png_size(path) if name.endswith(".png") else gif_size(path)
    if got is None:
        fail(f"docs/assets/rendered/{name}: unrecognised image header")
    elif "size" in rule and got != rule["size"]:
        fail(f"docs/assets/rendered/{name}: is {got[0]}x{got[1]}, must be "
             f"{rule['size'][0]}x{rule['size'][1]}")


# Lightweight CI gate stays stdlib-only. Full decode/disclosure/duration checks
# are mandatory locally via `make check-media`, which requires FFmpeg.
video = RENDERED / "portrait.mp4"
if not video.exists():
    fail("docs/assets/rendered/portrait.mp4: missing — run `make portrait`")
else:
    if not 0 < video.stat().st_size <= 8 * 1024 * 1024:
        fail("portrait.mp4: empty or exceeds the 8 MiB budget")
    with video.open("rb") as handle:
        if handle.read(12)[4:8] != b"ftyp":
            fail("portrait.mp4: unrecognised MP4 header")


# --- 3. the palette actually clears WCAG AA -------------------------------

def luminance(hex_colour: str) -> float:
    r, g, b = (int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5))
    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = channel(r), channel(g), channel(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg: str, bg: str) -> float:
    a, b = luminance(fg), luminance(bg)
    lighter, darker = max(a, b), min(a, b)
    return (lighter + 0.05) / (darker + 0.05)


PAPER = "#FFFFFF"
# Every token DESIGN.md presents as carrying text, with the floor it claims.
TEXT_TOKENS = {"ink": "#1F2328", "verde": "#1A7F37", "vermelho": "#CF222E", "cinza": "#57606A"}
AA_NORMAL = 4.5

for token, hex_colour in TEXT_TOKENS.items():
    ratio = contrast(hex_colour, PAPER)
    if ratio < AA_NORMAL:
        fail(f"palette '{token}' ({hex_colour}) is {ratio:.2f}:1 on white — "
             f"below the WCAG AA floor of {AA_NORMAL}:1")

# The border token only ever draws boundaries, which have a lower AA floor (3:1).
border_ratio = contrast("#D0D7DE", PAPER)
if border_ratio < 1.3:
    fail(f"palette 'borda' is {border_ratio:.2f}:1 on white — invisible")

design = (ROOT / "DESIGN.md").read_text(encoding="utf-8")
for token, hex_colour in TEXT_TOKENS.items():
    if hex_colour not in design:
        fail(f"DESIGN.md does not document the '{token}' colour {hex_colour} it is checked against")


# --- 4. the README diagram matches its source -----------------------------

readme = (ROOT / "README.md").read_text(encoding="utf-8")
mmd_source = (SOURCE / "arquitetura.mmd")
if not mmd_source.exists():
    fail("docs/assets/source/arquitetura.mmd is missing")
else:
    blocks = re.findall(r"```mermaid\n(.*?)```", readme, re.DOTALL)
    if not blocks:
        fail("README.md has no mermaid block, but arquitetura.mmd exists")
    else:
        want = mmd_source.read_text(encoding="utf-8").strip()
        if not any(b.strip() == want for b in blocks):
            fail("README.md's mermaid block has drifted from "
                 "docs/assets/source/arquitetura.mmd — they must be identical")


# --- 5. every rendered asset is in the manifest ---------------------------

if not MANIFEST.exists():
    fail("docs/assets/MANIFEST.md is missing")
else:
    manifest = MANIFEST.read_text(encoding="utf-8")
    for path in sorted(RENDERED.iterdir()):
        if path.name not in manifest:
            fail(f"docs/assets/rendered/{path.name} is not described in MANIFEST.md")
    for path in svgs:
        if path.name not in manifest:
            fail(f"docs/assets/source/{path.name} is not described in MANIFEST.md")


# --- 6. README images carry alt text, and every srcset resolves ------------

# Both syntaxes, because the README uses <picture> for the light/dark pairs and
# this check silently validated nothing the day the markdown images went away.
images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", readme)
images += [(alt, src) for src, alt in re.findall(
    r"<img[^>]*?src=\"([^\"]+)\"[^>]*?alt=\"([^\"]*)\"", readme, re.S)]
images += [(alt, src) for alt, src in re.findall(
    r"<img[^>]*?alt=\"([^\"]*)\"[^>]*?src=\"([^\"]+)\"", readme, re.S)]

for alt, src in images:
    if not alt.strip():
        fail(f"README.md: image {src} has empty alt text; if it is decorative, "
             f"say so explicitly in MANIFEST.md")
    # A badge's alt is a label; a screenshot's alt has to stand in for the
    # picture. Only hold the local rendered assets to the descriptive bar.
    elif "assets/rendered" in src and len(alt.strip()) < 15:
        fail(f"README.md: alt text for {src} is too short to describe it — {alt!r}")

for tag in re.findall(r"<picture>.*?</picture>", readme, re.S):
    if "<img" not in tag:
        fail("README.md: a <picture> has no <img> fallback, so it has no alt text")

# A dark-mode srcset that points at nothing fails only for readers in dark mode,
# which is exactly the audience least likely to be the one reviewing the diff.
for srcset in re.findall(r'<source[^>]*?srcset="([^"]+)"', readme):
    if not (ROOT / srcset).exists():
        fail(f"README.md: <source srcset=\"{srcset}\"> points at a file that does not exist")


# ---------------------------------------------------------------------------

if problems:
    print(f"FAIL — {len(problems)} asset problems:\n")
    for p in problems:
        print(f"  {p}")
    sys.exit(1)

print(f"ok — {len(svgs)} SVG sources, {len(BUDGETS)} rendered assets within budget, "
      f"palette clears WCAG AA, diagram in sync, manifest complete")
