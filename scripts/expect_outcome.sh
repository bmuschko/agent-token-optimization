#!/usr/bin/env bash
# Run a make target and check its pytest summary line contains the expected outcome.
#
# Usage: scripts/expect_outcome.sh "3 failed, 1 passed" task T=t1
set -u
want="$1"
shift
summary="$(make "$@" 2>&1 | grep -E '^=+ .*(passed|failed).* =+$' | tail -1)"
echo "make $*: ${summary:-no pytest summary}"
if ! grep -q "$want" <<<"$summary"; then
  echo "::error::expected '$want' from 'make $*'"
  exit 1
fi
