# Contributing

Thanks for helping. Bug reports and small, focused pull requests are welcome.

- **Issues:** describe what you did, what you expected and what happened, with the SDK or CLI version. Leave out API keys and webhook secrets.
- **Security problems:** do not use issues; see [SECURITY.md](SECURITY.md).
- **Spec and generated code:** `spec/openapi.json` comes from the Percia API and the generated code (`typescript/src/generated`, `python/percia/_generated`, `postman/*.json`) is produced from it. Do not edit those by hand; change the hand-written layer instead, or open an issue about the API.

## Develop

```bash
pnpm install
pnpm test                # TypeScript SDK and CLI, offline
pnpm typecheck && pnpm lint
cd python && python3 -m venv .venv && . .venv/bin/activate && pip install -e ".[dev]" && pytest -q
```

All tests run offline against mock servers built from the spec; no real credentials are needed. Add a test with each change, and a changeset (`pnpm changeset`) when you change `@percia/sdk` or `@percia/cli`.

By contributing you agree your work is licensed under the [MIT License](LICENSE).
