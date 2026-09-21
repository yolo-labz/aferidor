# 014 — Portrait replay from the existing fixture recording

## Spec

Produce an unpublished 1080×1920 H.264 MP4 and PNG poster from the existing
`docs/assets/source/demo-fone.cast`, not from a live account or new phone run.
Keep local-storefront, not-iFood/not-delivery-app and experimental disclosures
legible in every frame. Retain the README light/dark GIFs, alt text, contrast
and budgets. No savings promise. Apache-2.0 source and explicit provenance.

## Plan

The 100-column terminal table cannot simply shrink to portrait. Parse the five
recorded command/output blocks, wrap prose, remove accessibility coordinates
and stack comparison table cells vertically. Render five eight-second cards:
a **textual replay**, explicitly labeled reformatted with edited timing, not a
fresh execution or pixel-perfect terminal recording. Preserve the recorded
payment refusal. Reuse Python stdlib, Inkscape and FFmpeg; use the working VAAPI
encoder on this host, retain libx264 for portable regeneration. No new framework.

Add a stdlib asset budget check plus a separate fail-closed FFmpeg media gate
(format, duration, size, silent audio, all-frame banner comparison). Keep the
existing stdlib-only CI asset checker usable without installing video tools;
`make check-media` is the additional local/coordinator gate, not a CI claim.
Check parsing/layout with one runnable unittest file; inspect all five cards.

## Tasks

- [x] Inspect prior research, fixture capture, Makefile, manifest and PR #13.
- [x] Run baseline `make check` (all existing checks pass).
- [x] Implement cast-derived renderer and small regression/media checks.
- [x] Generate MP4/poster; inspect representative frames; run all checks.
- [x] Commit evidence and open ordinary code/docs PR #14; canonical report in
  `docs/swarm-2026-09-21.md` accompanies the report-only follow-up commit.
- [ ] Coordinator: full GLM exact-head independent review after queue recovery.
- [ ] Coordinator: decide merge; no worker merge/deployment/public posting.

Generator: OpenAI / GPT-6 Astra (GLM precursor was read-only).
