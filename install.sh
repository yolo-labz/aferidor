#!/bin/sh
# aferidor installer — https://github.com/yolo-labz/aferidor
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/yolo-labz/aferidor/main/install.sh | sh
#   ./install.sh --dry-run          # show what would happen, change nothing
#   ./install.sh --casa ~/minha-casa
#   ./install.sh --version v0.1.0   # pin an exact release
#
# Everything this script does lives under your home directory. It never uses
# sudo, never writes outside the prefix, and refuses to run as root.
#
# Reviewing before running is encouraged and supported:
#   curl -fsSL <url> -o install.sh && less install.sh && sh install.sh
#
# The entire body is wrapped in a brace group. The shell must parse the whole
# thing before executing any of it, so a download that is cut off halfway fails
# as a syntax error instead of silently running the first half.

{ # ===========================================================================

set -eu

REPO="yolo-labz/aferidor"
VERSION="${AFERIDOR_VERSION:-main}"
PREFIX="${AFERIDOR_PREFIX:-${XDG_DATA_HOME:-$HOME/.local/share}/aferidor}"
BINDIR="${AFERIDOR_BINDIR:-$HOME/.local/bin}"
SKILLDIR="${AFERIDOR_SKILLDIR:-$HOME/.claude/skills}"

# The project was called `feira` before 20/09/2026. An install from that era is
# a *complete working copy* under the old name, not a dangling link, so it keeps
# answering to old commands forever and quietly becomes the stale one. This
# installer removes it — the binaries, the copy, and the skill directories that
# would otherwise sit next to the new ones describing the same procedure twice.
#
# Household data is never here: it lives in whatever directory you passed to
# `aferidor init`, which this does not touch.
LEGACY="${AFERIDOR_LEGACY_PREFIX:-$(dirname "$PREFIX")/feira}"
CASA=""
DRY_RUN=0
NO_SKILLS=0
TMP=""

# --- output ----------------------------------------------------------------

if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  B=$(printf '\033[1m'); D=$(printf '\033[2m'); R=$(printf '\033[0m')
else
  B=""; D=""; R=""
fi

say()  { printf '%s\n' "$*"; }
step() { printf '%s==>%s %s\n' "$B" "$R" "$*"; }
note() { printf '%s    %s%s\n' "$D" "$*" "$R"; }
die()  { printf '%s\n' "aferidor: $*" >&2; exit "${2:-1}"; }
run()  { if [ "$DRY_RUN" -eq 1 ]; then note "would: $*"; else "$@"; fi; }

# Invoked by the trap below, which shellcheck cannot see. Older versions report
# that as SC2317, newer ones as SC2329 — disable both so the lint result does
# not depend on which shellcheck the runner ships.
# shellcheck disable=SC2329,SC2317
cleanup() {
  if [ -n "$TMP" ] && [ -d "$TMP" ]; then rm -rf "$TMP"; fi
  return 0   # never let cleanup rewrite the script's exit status
}
trap cleanup EXIT INT TERM

# --- arguments -------------------------------------------------------------

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run)    DRY_RUN=1 ;;
    --no-skills)  NO_SKILLS=1 ;;
    --casa)       CASA="${2:?--casa needs a directory}"; shift ;;
    --casa=*)     CASA="${1#*=}" ;;
    --version)    VERSION="${2:?--version needs a tag}"; shift ;;
    --version=*)  VERSION="${1#*=}" ;;
    --prefix)     PREFIX="${2:?--prefix needs a directory}"; shift ;;
    --prefix=*)   PREFIX="${1#*=}" ;;
    -h|--help)
      sed -n '2,20p' "$0" 2>/dev/null || say "See https://github.com/$REPO"
      exit 0 ;;
    *) die "unknown option: $1  (try --help)" 2 ;;
  esac
  shift
done

[ "$DRY_RUN" -eq 1 ] && say "${D}dry run — nothing will be written${R}" && say ""

# --- refuse to run as root -------------------------------------------------
#
# There is no reason for this to be root, and `curl | sudo sh` is the failure
# mode that makes the whole pattern deservedly unpopular.

if [ "$(id -u)" = "0" ] && [ -z "${AFERIDOR_ALLOW_ROOT:-}" ]; then
  die "refusing to install as root. Run this as your normal user — everything
     goes under \$HOME and sudo is never needed." 3
fi

# --- prerequisites ---------------------------------------------------------

step "Checking prerequisites"

PY=""
for candidate in python3 python3.13 python3.12 python3.11 python; do
  if command -v "$candidate" >/dev/null 2>&1; then
    if "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' 2>/dev/null; then
      PY="$candidate"; break
    fi
  fi
done

if [ -z "$PY" ]; then
  die "needs Python 3.9 or newer, and none was found on PATH.

     Debian/Ubuntu   sudo apt install python3
     Fedora          sudo dnf install python3
     macOS           brew install python3   (or install Xcode command line tools)
     Windows         install WSL, then follow the Linux steps

     Nothing else is required — aferidor uses only the standard library." 2
fi
note "python: $PY ($("$PY" -c 'import platform;print(platform.python_version())'))"

DOWNLOADER=""
command -v curl >/dev/null 2>&1 && DOWNLOADER="curl"
[ -z "$DOWNLOADER" ] && command -v wget >/dev/null 2>&1 && DOWNLOADER="wget"

# --- locate the source -----------------------------------------------------
#
# Two modes. Running from a checkout installs what is on disk, which is what
# you want when reviewing or developing. Piped from the network, it fetches a
# pinned tarball.

SELF_DIR=""
case "$0" in
  */*) SELF_DIR=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd) ;;
  # `sh install.sh` from inside the checkout: $0 carries no directory at all.
  # Piped from curl, $0 is the shell's own name and ./$0 will not exist.
  *)   [ -f "./$0" ] && SELF_DIR=$(pwd) ;;
esac

if [ -n "$SELF_DIR" ] && [ -f "$SELF_DIR/bin/aferidor" ] && [ -d "$SELF_DIR/template" ]; then
  SRC="$SELF_DIR"
  step "Installing from this checkout"
  note "$SRC"
else
  [ -z "$DOWNLOADER" ] && die "needs curl or wget to download the release" 2
  TMP=$(mktemp -d 2>/dev/null || mktemp -d -t aferidor)
  TARBALL="https://codeload.github.com/$REPO/tar.gz/$VERSION"

  step "Downloading aferidor ($VERSION)"
  if [ "$DOWNLOADER" = "curl" ]; then
    curl -fsSL --proto '=https' --tlsv1.2 "$TARBALL" -o "$TMP/aferidor.tar.gz" \
      || die "download failed. Check your connection, or that '$VERSION' is a real tag." 1
  else
    wget -qO "$TMP/aferidor.tar.gz" "$TARBALL" \
      || die "download failed. Check your connection, or that '$VERSION' is a real tag." 1
  fi

  # Publish this digest in the release notes so a suspicious reader can check
  # that the bytes they got are the bytes everyone else got.
  if command -v sha256sum >/dev/null 2>&1; then
    note "sha256: $(sha256sum "$TMP/aferidor.tar.gz" | cut -d' ' -f1)"
  elif command -v shasum >/dev/null 2>&1; then
    note "sha256: $(shasum -a 256 "$TMP/aferidor.tar.gz" | cut -d' ' -f1)"
  fi

  if [ -n "${AFERIDOR_SHA256:-}" ]; then
    got=$(sha256sum "$TMP/aferidor.tar.gz" 2>/dev/null | cut -d' ' -f1 \
          || shasum -a 256 "$TMP/aferidor.tar.gz" | cut -d' ' -f1)
    [ "$got" = "$AFERIDOR_SHA256" ] || die "checksum mismatch.
     expected $AFERIDOR_SHA256
     got      $got
     Do not proceed. Report this at https://github.com/$REPO/issues" 1
    note "checksum verified"
  fi

  tar -xzf "$TMP/aferidor.tar.gz" -C "$TMP" || die "could not unpack the archive" 1
  SRC=$(find "$TMP" -maxdepth 1 -type d -name 'aferidor-*' | head -n1)
  [ -d "$SRC" ] || die "unexpected archive layout" 1
fi

[ -f "$SRC/bin/aferidor" ] || die "the source at $SRC has no bin/aferidor — wrong directory?" 1

# --- install ---------------------------------------------------------------

step "Installing to $PREFIX"

if [ -f "$PREFIX/bin/aferidor" ]; then
  note "an existing install is here; it will be replaced (your household data is untouched)"
fi

# --- upgrade from the old name --------------------------------------------
#
# Done before anything is written, so a `--dry-run` shows it too, and so the
# removal cannot be skipped by a later failure that exits early.
if [ -d "$LEGACY" ]; then
  step "Removing the old '$LEGACY' install"
  note "copied from the previous name; the new copy below replaces it"
  run rm -rf "$LEGACY"
fi
for old in feira-lista feira-nota-fiscal feira-pedido feira-precos; do
  if [ -e "$SKILLDIR/$old" ]; then
    step "Removing the old skill '$old'"
    run rm -rf "$SKILLDIR/$old"
  fi
done
for old in feira feira-fone feira-mcp; do
  if [ -L "$BINDIR/$old" ]; then
    step "Removing the old command '$old'"
    run rm -f "$BINDIR/$old"
  fi
done

run mkdir -p "$PREFIX" "$BINDIR"
for part in bin template skills docs extensao; do
  [ -e "$SRC/$part" ] || continue
  run rm -rf "$PREFIX/$part"
  run cp -R "$SRC/$part" "$PREFIX/$part"
done
run chmod +x "$PREFIX/bin/aferidor" "$PREFIX/bin/aferidor-fone" "$PREFIX/bin/aferidor-mcp"

# Symlinks rather than copies, so the next install upgrades them automatically.
for tool in aferidor aferidor-fone aferidor-mcp; do
  if [ "$DRY_RUN" -eq 0 ]; then
    ln -sf "$PREFIX/bin/$tool" "$BINDIR/$tool"
  else
    note "would: ln -sf $PREFIX/bin/$tool $BINDIR/$tool"
  fi
  note "$tool -> $BINDIR/$tool"
done

# --- verify ----------------------------------------------------------------

step "Verifying"
if [ "$DRY_RUN" -eq 0 ]; then
  "$PY" "$PREFIX/bin/aferidor" selftest || die "the self-test failed — this install is not trustworthy, please report it" 1
else
  note "would: aferidor selftest"
fi

# --- agent skills ----------------------------------------------------------

if [ "$NO_SKILLS" -eq 0 ] && [ -d "$SRC/skills" ]; then
  step "Installing agent skills"
  if [ -d "$(dirname "$SKILLDIR")" ] || [ -d "$SKILLDIR" ]; then
    run mkdir -p "$SKILLDIR"
    for skill in "$SRC"/skills/*/; do
      [ -d "$skill" ] || continue
      name=$(basename "$skill")
      run rm -rf "$SKILLDIR/$name"
      run cp -R "$skill" "$SKILLDIR/$name"
      note "$name"
    done
  else
    note "no ~/.claude directory found — skipping."
    note "If you use Claude Code, copy $PREFIX/skills/* into ~/.claude/skills/ later."
  fi
fi

# --- household repository --------------------------------------------------

if [ -n "$CASA" ]; then
  step "Creating your household repository"
  if [ "$DRY_RUN" -eq 0 ]; then
    "$PY" "$PREFIX/bin/aferidor" init "$CASA"
  else
    note "would: aferidor init $CASA"
  fi
fi

# --- PATH ------------------------------------------------------------------
#
# Deliberately does not edit shell rc files. Silent edits to a dotfile are how
# installers earn their reputation, and a wrong guess about which shell you use
# breaks your terminal, not ours.

case ":${PATH}:" in
  *":$BINDIR:"*) PATH_OK=1 ;;
  *)             PATH_OK=0 ;;
esac

say ""
step "Done"
say ""

if [ "$PATH_OK" -eq 0 ]; then
  say "  ${B}One manual step:${R} $BINDIR is not on your PATH."
  say "  Add this line to your ~/.bashrc, ~/.zshrc or ~/.config/fish/config.fish:"
  say ""
  say "      export PATH=\"\$PATH:$BINDIR\""
  say ""
  say "  Then open a new terminal. Until then, use the full path:"
  say "      $PREFIX/bin/aferidor --help"
  say ""
fi

if [ -z "$CASA" ]; then
  say "  Next: create a household repository."
  say ""
  say "      aferidor init ~/minha-casa"
  say "      cd ~/minha-casa"
  say "      aferidor advise"
  say ""
  say "  Then open AGENTS.md and write your household's rules in your own words."
else
  say "  Next:"
  say ""
  say "      cd $CASA"
  say "      aferidor advise          # what the example data recommends"
  say "      \$EDITOR AGENTS.md     # your household's rules"
  say ""
fi

say "  Guide (Portuguese):  $PREFIX/docs/02-o-metodo.md"
say "  Talk to it (MCP):    $PREFIX/docs/explicacao/como-conversar.md"
say "  Browser extension:   $PREFIX/extensao/  (load unpacked — see its README)"
say "  Uninstall:           rm -rf $PREFIX $BINDIR/aferidor $BINDIR/aferidor-fone $BINDIR/aferidor-mcp"
say "  Your data is yours and lives only in the household directory."
say ""

exit 0

} # ===========================================================================
