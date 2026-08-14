#!/usr/bin/env bash
# search.sh — case-insensitive full-text search across the KB docs/ folder.
# Usage: ./scripts/search.sh "some term"
# Requires ripgrep (rg) on PATH.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KB_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DOCS_DIR="$KB_ROOT/docs"

if ! command -v rg >/dev/null 2>&1; then
  echo "Error: 'rg' (ripgrep) is required but not found on PATH." >&2
  exit 1
fi

if [ "$#" -lt 1 ] || [ -z "${1:-}" ]; then
  echo "Usage: ./scripts/search.sh \"<search term>\"" >&2
  echo "Example: ./scripts/search.sh \"Kea HA\"" >&2
  exit 2
fi

term="$1"
echo "Searching docs/ for: $term"
echo "------------------------------------------------------------"
# -i case-insensitive, -n line numbers, --hidden skip, -g restrict to docs
rg --color=auto -i -n "$term" "$DOCS_DIR"
