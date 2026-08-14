#!/usr/bin/env bash
# Search the pfSense DNS KB with ripgrep.
# Usage: ./scripts/search.sh "query" [extra rg args...]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$HERE"
if ! command -v rg >/dev/null 2>&1; then
  echo "ripgrep (rg) not found; falling back to grep -r" >&2
  grep -rIn -- "$@" docs/ notes/ || true
  exit 0
fi
rg --heading --line-number --color=auto "$@" docs/ notes/
