# Asset generation. Everything here is reproducible from versioned source —
# nothing in docs/assets/rendered/ is hand-edited.
#
#   make assets        regenerate every rendered asset
#   make demo          re-record the terminal demo (slow; changes dates)
#   make check         run the whole verification suite
#
# Needs: python3 (stdlib only). For `assets`: inkscape, imagemagick, agg,
# ffmpeg + DejaVu fonts. `portrait` needs no phone or new capture.
# For `demo`: asciinema + agg — available on nix without installing anything:
#   nix-shell -p asciinema asciinema-agg --run 'make demo'

SOURCE   := docs/assets/source
RENDERED := docs/assets/rendered

.PHONY: all assets demo demo-fone portrait check check-assets check-media test clean help

help:
	@echo 'make assets   regenerate rendered images from source'
	@echo 'make demo     re-record the CLI terminal cast and GIF'
	@echo 'make demo-fone  re-record the phone-loop cast (needs a real phone)'
	@echo 'make portrait  render the portrait textual replay (no phone)'
	@echo 'make check    tests + stdlib asset checks'
	@echo 'make check-media  FFmpeg gate: portrait format + every-frame disclosure'

all: assets

# Every terminal asset ships light AND dark. GitHub renders README images on a
# near-black canvas for half its users, and a single light-theme GIF is a white
# slab there — the README picks between them with <picture media=…>, which is
# the platform's own mechanism rather than a second copy of the markdown.
assets: portrait $(RENDERED)/social-preview.png \
        $(RENDERED)/demo.gif $(RENDERED)/demo-dark.gif $(RENDERED)/demo.png \
        $(RENDERED)/demo-fone.gif $(RENDERED)/demo-fone-dark.gif $(RENDERED)/demo-fone.png

# Text is flattened to paths (-T) so the card renders identically on a machine
# that has none of the fonts named in the SVG.
$(RENDERED)/social-preview.png: $(SOURCE)/social-preview.svg
	@mkdir -p $(RENDERED)
	inkscape $< --export-type=png --export-filename=$@ -w 1280 -h 640 -T
	@echo "  $@ -> $$(identify -format '%wx%h %b' $@)"

# The GIF is rendered from the cast, and the cast is only re-recorded by
# `make demo` — so `make assets` is fast and does not churn the recording.
$(RENDERED)/demo.gif: $(SOURCE)/demo.cast
	@mkdir -p $(RENDERED)
	agg --font-size 15 --line-height 1.35 --theme github-light --speed 1.4 \
	    --idle-time-limit 0.7 --last-frame-duration 4 $< $@
	@echo "  $@ -> $$(identify -format '%wx%h %n frames %b' $@ | head -1)"

$(RENDERED)/demo-dark.gif: $(SOURCE)/demo.cast
	@mkdir -p $(RENDERED)
	agg --font-size 15 --line-height 1.35 --theme github-dark --speed 1.4 \
	    --idle-time-limit 0.7 --last-frame-duration 4 $< $@
	@echo "  $@ -> $$(identify -format '%wx%h %n frames %b' $@ | head -1)"

# The phone demo carries its disclosure BURNED INTO EVERY FRAME, not beside the
# image. A GIF gets screenshotted, embedded and reshared with the prose stripped
# off, and this one shows a real handset being driven through a purchase — the
# single most misreadable thing in the repository. The caption is the only part
# of the disclosure that travels with it.
BANNER_FONT := $(shell fc-match 'DejaVu Sans:bold' -f '%{file}')

$(RENDERED)/demo-fone.gif: $(SOURCE)/demo-fone.cast
	@mkdir -p $(RENDERED)
	agg --font-size 15 --line-height 1.35 --theme github-light --speed 1.4 \
	    --idle-time-limit 0.7 --last-frame-duration 4 $< $@.tmp.gif
	magick $@.tmp.gif -coalesce -gravity south -background '#CF222E' -splice 0x56 \
	    -font '$(BANNER_FONT)' -fill white \
	    -pointsize 19 -annotate +0+30 'VITRINE LOCAL DE DEMONSTRAÇÃO — NÃO É IFOOD NEM APP DE ENTREGA' \
	    -pointsize 15 -annotate +0+8  'gravação real num Android físico · aferidor-fone é experimental' \
	    -layers optimize $@
	@rm -f $@.tmp.gif
	@echo "  $@ -> $$(identify -format '%wx%h %n frames %b' $@ | head -1)"

$(RENDERED)/demo-fone-dark.gif: $(SOURCE)/demo-fone.cast
	@mkdir -p $(RENDERED)
	agg --font-size 15 --line-height 1.35 --theme github-dark --speed 1.4 \
	    --idle-time-limit 0.7 --last-frame-duration 4 $< $@.tmp.gif
	magick $@.tmp.gif -coalesce -gravity south -background '#CF222E' -splice 0x56 \
	    -font '$(BANNER_FONT)' -fill white \
	    -pointsize 19 -annotate +0+30 'VITRINE LOCAL DE DEMONSTRAÇÃO — NÃO É IFOOD NEM APP DE ENTREGA' \
	    -pointsize 15 -annotate +0+8  'gravação real num Android físico · aferidor-fone é experimental' \
	    -layers optimize $@
	@rm -f $@.tmp.gif
	@echo "  $@ -> $$(identify -format '%wx%h %n frames %b' $@ | head -1)"

# Static fallback: the final frame, for anyone who cannot see the animation.
$(RENDERED)/demo.png: $(RENDERED)/demo.gif
	magick $< -coalesce -delete 0--2 $@

$(RENDERED)/demo-fone.png: $(RENDERED)/demo-fone.gif
	magick $< -coalesce -delete 0--2 $@

# 100 columns because the widest line aferidor prints is 96; at 80 it wraps and the
# table becomes unreadable. asciinema 3 needs --window-size, not --cols.
demo:
	AFERIDOR="$$PWD/bin/aferidor" asciinema rec --window-size 100x30 --overwrite \
	  -c "sh $(SOURCE)/demo.sh" $(SOURCE)/demo.cast
	$(MAKE) $(RENDERED)/demo.gif $(RENDERED)/demo.png

# Needs a real phone attached and the fixture storefront open on it:
#   python3 -m http.server 8099 --directory $(SOURCE)   # then open the page
# See docs/assets/source/demo-fone.sh for the full preconditions.
demo-fone:
	AFERIDOR="$$PWD/bin/aferidor" FONE="$$PWD/bin/aferidor-fone" \
	  asciinema rec --window-size 100x30 --overwrite \
	  -c "sh $(SOURCE)/demo-fone.sh" $(SOURCE)/demo-fone.cast
	$(MAKE) $(RENDERED)/demo-fone.gif $(RENDERED)/demo-fone.png

# Explicit encoder choice: portable default; this draft used working VAAPI.
MEDIA_ENCODER ?= libx264
portrait:
	python3 $(SOURCE)/portrait.py --encoder $(MEDIA_ENCODER)

check-media:
	python3 tests/test_portrait.py
	python3 scripts/check-media.py
	python3 tests/test_media.py

check: test check-assets

test:
	sh tests/run.sh

check-assets:
	python3 scripts/check-assets.py

clean:
	rm -f $(RENDERED)/*.png $(RENDERED)/*.gif $(RENDERED)/portrait.mp4
