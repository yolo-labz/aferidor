#!/bin/sh
# Every runnable check in the project. No network, no phone, no browser.
#
#   sh tests/run.sh
#
# If this passes, the arithmetic that every decision downstream depends on is
# intact: package normalisation, the migration rule, the page collector's
# parsing, and the payment gate.

set -eu

cd "$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"

fail=0
run() {
  printf '\n== %s\n' "$1"
  shift
  if "$@"; then :; else fail=1; fi
}

run "portrait — fixture reflow and disclosure layout" python3 tests/test_portrait.py
run "aferidor — units, numbers, migration rule" python3 bin/aferidor selftest
run "aferidor-fone — payment gate, element matching" python3 tests/test_fone.py
run "aferidor-mcp — protocol, failures, and no payment capability" python3 tests/test_mcp.py
run "aferidor — receipts import once, history, and low stock" python3 tests/test_historico.py

if command -v node >/dev/null 2>&1; then
  run "extension — page collector parsing" node tests/coletor.test.mjs
else
  printf '\n== extension — page collector parsing\nSKIPPED (node not installed)\n'
fi

# The shipped template must be valid on its own terms, or a first-time user's
# very first command fails.
# Invoked indirectly via `run` below, which shellcheck cannot see. Older
# versions report that as SC2317, newer ones as SC2329 — disable both so the
# lint result does not depend on which distro the runner ships.
# shellcheck disable=SC2329,SC2317
check_template() {
  # Absolute path captured BEFORE any cd — inside the subshells below, $PWD is
  # the temporary household directory, not this repository.
  bin="$(pwd)/bin/aferidor"
  tmp=$(mktemp -d)
  # shellcheck disable=SC2064  # expand $tmp now, not at trap time
  trap "rm -rf '$tmp'" EXIT
  python3 "$bin" init "$tmp" >/dev/null || return 1
  for cmd in check advise falta historico zap; do
    ( cd "$tmp" && python3 "$bin" "$cmd" >/dev/null ) || {
      printf 'aferidor %s failed on a fresh repository\n' "$cmd"; return 1; }
  done
  ( cd "$tmp" && python3 "$bin" compare oleo-de-soja >/dev/null ) || {
    printf 'aferidor compare failed on a fresh repository\n'; return 1; }
  printf 'ok — init, check, advise and compare all succeed on a fresh repository\n'
}
run "template — a fresh household repository validates" check_template

# The upgrade path, which nothing else exercises: an install from before the
# 20/09/2026 rename is a complete copy under the old name, so it keeps working
# forever and quietly goes stale. This asserts the installer actually removes it
# before installing anything — and does so without being pointed at a PREFIX,
# which would prove nothing about what real users have on disk.
#
# shellcheck disable=SC2329,SC2317
check_upgrade() {
  tmp=$(mktemp -d)
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" EXIT
  mkdir -p "$tmp/data/feira/bin" "$tmp/data/feira/docs" \
           "$tmp/bin" "$tmp/skills/feira-precos"
  for tool in aferidor aferidor-fone aferidor-mcp; do
    echo 'old copy' > "$tmp/data/feira/bin/$tool"
  done
  echo 'old skill' > "$tmp/skills/feira-precos/SKILL.md"
  # The old binaries were named `feira`, not `aferidor`: the old *installation*
  # lives under an `aferidor` path (it is today's layout), while the commands it
  # put on PATH carry the old name.
  for tool in feira feira-fone feira-mcp; do
    ln -s "$tmp/data/feira/bin/aferidor" "$tmp/bin/$tool"
  done

  AFERIDOR_PREFIX="$tmp/data/aferidor" \
  AFERIDOR_BINDIR="$tmp/bin" \
  AFERIDOR_SKILLDIR="$tmp/skills" \
  HOME="$tmp" sh install.sh --no-skills --dry-run > "$tmp/out" 2>&1 || return 1

  # Deriving the legacy paths from the configured ones is the whole point: a
  # hardcoded ~/.local/share/feira would pass a test written with real defaults
  # and do nothing at all for anyone who moved their prefix.
  grep -q "rm -rf $tmp/data/feira" "$tmp/out" || {
    printf 'the old install was not removed: %s\n' "$tmp/data/feira"; return 1; }
  grep -q "rm -f $tmp/bin/feira$" "$tmp/out" || {
    printf 'the old command was not removed: %s\n' "$tmp/bin/feira"; return 1; }
  grep -q "rm -rf $tmp/skills/feira-precos" "$tmp/out" || {
    printf 'the old skill was not removed: %s\n' "$tmp/skills/feira-precos"; return 1; }

  # The real install, on empty directories, so the assertion below is about what
  # the installer *did*, not what it said it would do.
  AFERIDOR_PREFIX="$tmp/data/aferidor" \
  AFERIDOR_BINDIR="$tmp/bin" \
  AFERIDOR_SKILLDIR="$tmp/skills" \
  HOME="$tmp" sh install.sh > "$tmp/real" 2>&1 || return 1
  [ -d "$tmp/data/feira" ] && { printf 'the old install survived a real run\n'; return 1; }
  [ -L "$tmp/bin/feira" ] && { printf 'the old command survived a real run\n'; return 1; }
  [ -x "$tmp/bin/aferidor" ] || { printf 'the new command was not installed\n'; return 1; }
  # An old skill surviving next to the new one is the duplicate that actually
  # confuses an agent: two files describing the same procedure, one of them stale.
  [ -e "$tmp/skills/feira-precos" ] && { printf 'the old skill survived a real run\n'; return 1; }
  [ -d "$tmp/skills/aferidor-precos" ] || { printf 'the new skills were not installed\n'; return 1; }

  printf 'ok — a pre-rename install is removed, not left to shadow the new one\n'
}
run "installer — upgrade from the old name" check_upgrade

printf '\n'
if [ "$fail" -eq 0 ]; then
  printf 'ALL CHECKS PASSED\n'
else
  printf 'SOME CHECKS FAILED\n'
fi
exit "$fail"
