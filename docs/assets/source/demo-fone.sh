#!/bin/sh
# Source for the README's headline demo: the phone loop.
#
#   make demo-fone     # re-record and re-render (needs a real phone attached)
#
# This records a REAL run. `aferidor-fone` talks to a real, Play-certified handset
# over adb and reads the real accessibility tree — nothing here is mocked, and
# the payment refusal at the end is the program refusing, not a printf.
#
# What IS a stand-in is the shop: docs/assets/source/vitrine-fixture.html, a
# fake storefront serving the same example items as template/. Recording against
# a real delivery app would mean opening somebody's account, with their address
# and their order history, on camera — and driving a third party's app to make a
# promotional asset. The fixture keeps the demo honest about the tool while
# keeping a real household out of it.
#
# Prerequisites, all checked below so the recording fails loudly instead of
# silently producing a broken GIF:
#   - one phone attached, in `device` state
#   - the fixture served and open in the phone's browser
#   - ANDROID_SERIAL pinned
#
# As with demo.sh, each command is printed rather than run from a real prompt,
# so the cast carries no hostname, username or $PWD. The serial is masked for
# the same reason: this phone is reached over a private network, and its address
# is infrastructure, not something a README needs to publish.

set -eu

AFERIDOR="${AFERIDOR:-aferidor}"
FONE="${FONE:-aferidor-fone}"
CASA=$(mktemp -d)
trap 'rm -rf "$CASA"' EXIT

$AFERIDOR init "$CASA" >/dev/null
cd "$CASA"

type_out() {
  printf '\033[32m$\033[0m '
  printf '%s' "$1" | fold -w1 | while read -r c || [ -n "$c" ]; do
    printf '%s' "${c:- }"
    sleep 0.028
  done
  printf '\n'
  sleep 0.45
}

clear
sleep 0.6

# 1. A real phone, not an emulator. Delivery apps that hold a card check Play
#    Integrity, and this is the line where that stops being a claim.
type_out "aferidor-fone dispositivos"
$FONE dispositivos | sed -E 's/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:[0-9]+/R58N90XXXXX/'
sleep 2.2

# 2. Read the shop's own screen. These prices are being read out of the app,
#    not fetched from anybody's catalogue.
printf '\n'
type_out "aferidor-fone tela"
$FONE tela | head -12
sleep 3.4

# 3. The decision. The 900 ml bottle is cheaper on the shelf and dearer per
#    litre — which is the entire argument of the project, and the reason the
#    agent is about to pick the bottle that *looks* more expensive.
printf '\n'
type_out "aferidor compare oleo-de-soja"
$AFERIDOR compare oleo-de-soja
sleep 3.6

# 4. Build the cart. A real tap, on a real handset, verified by re-reading the
#    screen afterwards.
printf '\n'
type_out "aferidor-fone tocar 'Adicionar Soya'"
$FONE tocar "Adicionar Soya"
sleep 2.6

# 5. And then it stops. This is the product.
printf '\n'
type_out "aferidor-fone tocar 'Pagar'"
if $FONE tocar "Pagar"; then
  printf '\n  DEMO FAILED: the payment button was not refused.\n'
  exit 1
fi
sleep 4.0
