#!/bin/sh
# Source for the README terminal demo. Recorded with asciinema, rendered with agg.
#
#   make demo        # re-record and re-render
#
# Everything shown is the fixture data that ships in template/ — no household
# data, ever. The demo runs against a throwaway directory so it is repeatable
# and leaves nothing behind.
#
# The script prints each command before running it rather than using a real
# shell prompt, so the recording has no hostname, no username and no $PWD from
# the machine that recorded it.

set -eu

AFERIDOR="${AFERIDOR:-aferidor}"
CASA=$(mktemp -d)
trap 'rm -rf "$CASA"' EXIT

# Typing effect. Fast enough not to bore, slow enough to follow.
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

type_out "aferidor init minha-casa"
$AFERIDOR init "$CASA" | sed "s|$CASA|minha-casa|g" | head -3
sleep 1.4

printf '\n'
type_out "cd minha-casa"
cd "$CASA"
sleep 0.3

# The reveal: the 900 ml bottle has the smaller sticker price and the larger
# price per litre. This is the whole argument of the project in one screen.
printf '\n'
type_out "aferidor compare oleo-de-soja"
$AFERIDOR compare oleo-de-soja
sleep 3.2

# And then the part people do not expect: it says stay put.
printf '\n'
type_out "aferidor advise"
$AFERIDOR advise
sleep 3.0
