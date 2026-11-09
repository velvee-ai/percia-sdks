# Owner steps

Nothing here has been done. The assistant never publishes, never creates accounts and never holds registry credentials. Everything below needs you, logged in. Status of the names on 2026-11-09 (checked read-only): `@percia/sdk` and `@percia/cli` do not exist on npm (a 404 does not prove you own the `@percia` scope: step 1 does), `percia` on PyPI returns 404 (free).

## 0. Put the repo on GitHub

1. Create the repository (the workflows assume `percia-ai/percia-sdks`; if the owner/name differs, change it in `.github/workflows/release.yml` (the `if:` guard), in `typescript/package.json` and `cli/package.json` (`repository`, `homepage`) and in the PyPI/npm trusted-publisher forms below).
2. Push `main` (this branch is `divi-vijayakumar/sdks-cli`, merge it first). Turn on Actions.
3. Settings > Actions > General: "Allow GitHub Actions to create and approve pull requests" (changesets opens the release PR).
4. Pin third-party actions to commit SHAs before the first release if your policy requires it (they are on major tags now).

## 1. npm: org, 2FA, names

1. Sign in at npmjs.com. Account > Two-Factor Authentication > **Authorization and publishing**. Save the recovery codes.
2. Create the organization **`percia`** (npmjs.com > Add Organization, the free plan is enough for public packages). That reserves the `@percia` scope. If the name is taken, pick another scope and rename `@percia/sdk` and `@percia/cli` (package names, imports in `cli/`, docs, README).
3. Check: `npm view @percia/sdk` must answer 404.
4. **First publish by hand** (a package must exist before trusted publishing can be attached to it):
   ```bash
   pnpm install --frozen-lockfile && pnpm test && pnpm build
   cd typescript && npm publish --access public      # prompts for your one-time code; do the SDK first
   cd ../cli && pnpm publish --access public --no-git-checks   # pnpm rewrites workspace:* to the real version
   ```
   (`publishConfig.provenance` is on, which only works from CI; for this first manual publish add `--provenance=false`.) Or run the first release through changesets with a temporary granular token in the repo secret `NPM_TOKEN`, then delete the token.
5. Trusted publishing, once per package: npmjs.com > the package > Settings > **Trusted Publisher** > GitHub Actions: organization/user `percia-ai`, repository `percia-sdks`, workflow filename `release.yml`, environment blank. Do it for `@percia/sdk` and `@percia/cli`. Then in each package's Settings > Publishing access choose "Require two-factor authentication and disallow tokens".
6. From now on: add a changeset in PRs (`pnpm changeset`), merge; the workflow opens "Version packages"; merging that PR publishes with provenance and no stored token.

## 2. PyPI: project name, 2FA, trusted publishing

1. Sign in at pypi.org, enable 2FA (an authenticator app or a security key) and save recovery codes. Do the same on test.pypi.org if you want the dry run.
2. Check `https://pypi.org/project/percia/` is still 404.
3. Add a **pending trusted publisher** (this reserves the name on first successful publish, no token): pypi.org > Your account > Publishing > "Add a new pending publisher": project name `percia`, owner `percia-ai`, repository `percia-sdks`, workflow `release-python.yml`, environment `pypi`. Repeat on test.pypi.org with environment `testpypi` for a rehearsal.
4. GitHub > Settings > Environments: create `pypi` (add yourself as a required reviewer so a tag does not publish unattended) and `testpypi`.
5. Release: bump `version` in `python/pyproject.toml` and `python/percia/__init__.py`/`_config.py` if it is repeated there (`grep -rn "0.1.0" python/percia/*.py`), update `python/CHANGELOG.md`, commit, then `git tag python-v0.1.0 && git push origin python-v0.1.0`. Rehearse first: Actions > "Release (PyPI)" > Run workflow > `testpypi`.

## 3. What only a real account can verify

- **OAuth login** (`percia login`): dynamic client registration with a `http://127.0.0.1:<random>/callback` redirect URI. The issuer advertises registration and PKCE but nothing says it accepts loopback redirect URIs with a changing port, or unauthenticated registration. The flow is tested against a mock authorization server only. If registration refuses it, `percia login --with-key` and `PERCIA_API_KEY` are the fallback and the server needs a loopback redirect allowance (RFC 8252 section 7.3).
- **A real API key against the real host**: every API call is tested against a mock built from the OpenAPI document. Create a key (dashboard > API keys, scopes `watches:read watches:write watches:delete events:read cameras:read cameras:write integrations:read integrations:write hooks:write`), then:
  ```bash
  PERCIA_API_KEY=pk_live_... percia whoami && percia watches list && percia events list --limit 3
  ```
  Expect `/events` and `/hooks` to 404 until percia-cf master is deployed (the live host is behind master).
- **Real signed deliveries** verified by the TS and Python verifiers: create a webhook watch pointing at a tunnel (`cloudflared tunnel --url http://localhost:3000`) running `examples/node-express`, run `percia watches test <id>`. The verifiers are proven only against the shared vectors and a locally signed body.
- **`mcp setup`** against installed clients: the file formats follow the documented configs (`.mcp.json`, `~/.cursor/mcp.json`, `claude_desktop_config.json` with `mcp-remote`), unverified against current client versions.
- **Cloudflare Worker example**: `wrangler dev` / deploy needs your Cloudflare login. **Vapi example**: documentation only; the request shape is unverified (check Vapi's docs, use your own Vapi key).
- **Pairing and connect links** (`cameras add`, `destinations connect`) need a person to open them on a phone / signed in to Percia.

## 4. After the live host catches up with master

```bash
pnpm spec:sync        # pins https://playground.percia.ai/api/openapi.json
pnpm generate         # TS, Python, Postman
git diff              # review, then commit
```
The daily "Spec drift" workflow fails (and opens a `spec-drift` issue) whenever the live document differs from the pin. It is red from day one because of the deploy gap above.

## 5. Optional

- Docker/Homebrew/winget packaging of the CLI, a `percia` PyPI console script, signing with sigstore beyond npm provenance, and hosted generators (Stainless, Speakeasy, Fern) are not set up.
