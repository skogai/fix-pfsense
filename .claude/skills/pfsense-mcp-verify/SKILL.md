---
name: pfsense-mcp-verify
description: Run the pfsense-mcp-server pre-PR verification gate (tests, coverage, lint, and optionally the MCP protocol E2E smoke test). Use before opening a PR or when asked to verify changes to pfsense-mcp-server.
---

Run this from the `pfsense-mcp-server/` directory (a separate git repo nested in this workspace — its own `CLAUDE.md` has full conventions).

1. Run the full test suite:
   ```bash
   pytest -v
   ```
2. Run with coverage — CI gate is `>=40%`:
   ```bash
   pytest --cov=src --cov-report=term-missing
   ```
3. Lint — must be clean:
   ```bash
   ruff check src/ tests/
   ```
4. If the change touches transports, auth, startup, or tool registration, also run the protocol-level E2E suite (needs `node`/`npx` and `jq` on PATH, no live pfSense required):
   ```bash
   make test-e2e
   ```

Report pass/fail for each step. If `ruff check` fails, do not blind-fix with `ruff check --fix` without reviewing the diff. If a new or changed tool sends a payload to the pfSense API, confirm there's a matching contract test under `tests/contract/` (see `CONTRIBUTING.md` — mirror API field names verbatim, use `assert_payload_valid()`), and confirm every new non-read tool carries `@guarded` or `@rate_limited`.
