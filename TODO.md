# TODO

| Variable                                                                        | Where it actually comes from                                                                                  |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `PFSENSE_URL`                                                                   | Your pfSense box's own hostname/IP — not documented anywhere, it's your deployment                            |
| `PFSENSE_VERSION`                                                               | pfSense UI: **Dashboard** (shows version) — already enumerated in the file from `PFSENSE_API_INSTALLATION.md` |
| `AUTH_METHOD`                                                                   | Your choice (api_key / basic / jwt) — tradeoffs explained in `PFSENSE_API_INSTALLATION.md`                    |
| `PFSENSE_API_KEY`                                                               | pfSense UI: **System > REST API > Keys** (generate, after installing the REST API package)                    |
| `PFSENSE_USERNAME` / `PFSENSE_PASSWORD`                                         | Your local pfSense admin account — **System > User Manager**                                                  |
| `VERIFY_SSL`                                                                    | Policy decision — leave `true`                                                                                |
| `PFSENSE_CA_FILE`                                                               | pfSense UI: **System > Cert. Manager > CAs** — export the CA, save as PEM locally                             |
| `MCP_HOST` / `MCP_PORT`                                                         | Your deployment choice — defaults are fine                                                                    |
| `MCP_API_KEY`                                                                   | Generate locally: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`                             |
| `MCP_ALLOWED_ORIGINS`                                                           | Depends on what client/app connects over HTTP transport                                                       |
| `ENABLE_HATEOAS`, `LOG_LEVEL`, `API_TIMEOUT`                                    | Tuning knobs — defaults are fine                                                                              |
| `MCP_READ_ONLY`                                                                 | Policy decision                                                                                               |
| `MCP_AUDIT_LOG`, `MCP_RATE_LIMIT_*`, `MCP_ALLOWED_TOOLS`, `MCP_ROLLBACK_BUFFER` | Policy/ops decisions — defaults reasonable as commented                                                       |
