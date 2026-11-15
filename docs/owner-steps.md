# Owner steps

Nothing here has been done. The assistant never publishes, never creates accounts and never holds registry credentials. Everything below needs you, logged in. Status of the names on 2026-11-09 (checked read-only): `@percia/sdk` and `@percia/cli` do not exist on npm (a 404 does not prove you own the `@percia` scope: step 2 does), `percia` on PyPI returns 404 (free).

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
5. Release: bump `version` in `python/pyproject.toml` and `python/percia/_version.py`, update `python/CHANGELOG.md`, commit, then `git tag python-v0.2.0 && git push origin python-v0.2.0`. Rehearse first: Actions > "Release (PyPI)" > Run workflow > `testpypi`.

## 3. What only a real account can verify

- **OAuth login** (`percia login`): dynamic client registration with a `http://127.0.0.1:<random>/callback` redirect URI. The issuer advertises registration and PKCE but nothing says it accepts loopback redirect URIs with a changing port, or unauthenticated registration. The flow is tested against a mock authorization server only. If registration refuses it, `percia login --with-key` and `PERCIA_API_KEY` are the fallback and the server needs a loopback redirect allowance (RFC 8252 section 7.3).
- **A real API key against the real host**: every API call is tested against a mock built from the OpenAPI document. Create a key (dashboard > API keys, scopes `watches:read watches:write watches:delete events:read cameras:read cameras:write integrations:read integrations:write hooks:write`), then:
  ```bash
  PERCIA_API_KEY=pk_live_... percia whoami && percia watches list && percia events list --limit 3
  ```
  The pinned spec matched the live host on 2026-11-09 (`/events`, `/hooks`, SMS and WhatsApp present); if you point at another host, `percia doctor` and `pnpm spec:check --url <host>/api/openapi.json` show whether it is behind.
- **Real signed deliveries** verified by the TS and Python verifiers: create a webhook watch pointing at a tunnel (`cloudflared tunnel --url http://localhost:3000`) running `examples/node-express`, run `percia watches test <id>`. The verifiers are proven only against the shared vectors and a locally signed body.
- **`mcp setup`** against installed clients: the file formats follow the documented configs (`.mcp.json`, `~/.cursor/mcp.json`, `claude_desktop_config.json` with `mcp-remote`), unverified against current client versions.
- **Cloudflare Worker example**: `wrangler dev` / deploy needs your Cloudflare login. **Vapi example**: documentation only; the request shape is unverified (check Vapi's docs, use your own Vapi key).
- **Pairing and connect links** (`cameras add`, `destinations connect`) need a person to open them on a phone / signed in to Percia.

## 4. When the server API changes

```bash
pnpm spec:sync        # pins https://playground.percia.ai/api/openapi.json
pnpm generate         # TS, Python, Postman
git diff              # review, then commit
```
The daily "Spec drift" workflow fails (and opens a `spec-drift` issue) whenever the live document differs from the pin. It was green when this was written (live and pin identical, 105 operations, sha256 `ed96ffa14960`, 2026-11-14).

## 4b. Releasing camera push (now part of 0.3.0)

Nothing here has been published or tagged. The versions in the repo are `0.2.0` (SDK, CLI, Python). The camera push server is deployed (percia-cf master `bb95c92`, Worker versions `d7aff9a6` then `5a591ed8`), the spec pin is the live document, `pnpm spec:check` is green and the SDKs use the real `status` and `bulk` routes (with a 404 fallback for older servers). Remaining before publishing:

1. `pnpm spec:sync && pnpm generate && git diff`: expect no change. If the live document moved, review the diff and adjust the SDKs and `spec/camera-push-contract.json`. `pnpm spec:check` must pass.
2. With a **test account** (never create cameras in production by accident): `PERCIA_API_KEY=... percia cameras push register --name smoke --external-id smoke-1`, `percia cameras status <id>` (expect `state: waiting`, then `online` once publishing), rotate, revoke (status shows `revoked`), `cameras remove`; SDK smoke for `cameras.bulk` with two throwaway `externalId`s, then remove them; and with ffmpeg 7.1+ on a LAN machine `percia cameras push run --rtsp ...` against a real camera; check the camera goes online in the dashboard and a watch on `percia-cam://<id>` produces events. This is the only check that proves the live responses match the recorded contract.
3. Update `CHANGELOG.md` and the per-package changelogs from "unreleased" to the release date.
4. Publish as in sections 1 and 2 (npm `@percia/sdk` first, then `@percia/cli`; PyPI tag `python-v0.2.0`). Do not tag before steps 1-2. Run `pnpm install --frozen-lockfile && pnpm generate:check && pnpm test && pnpm build` first.
5. `percia listen` and `events.stream` are in 0.3.0, see section 4c.

## 4c. Releasing `percia listen` (0.3.0)

Nothing here has been published or tagged. The versions in the repo are `0.3.0` (SDK, CLI, Python) and include camera push (4b). The CLI and SDK stream code is tested offline against a mock SSE server that follows percia-cf `docs/specs/platform/dev-feed.md`. Remaining before publishing:

1. **Confirm the server is deployed**: `curl -sS -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $KEY" https://playground.percia.ai/api/events/stream --max-time 3` should print 200 (it streams; the timeout ends it). A 404 means the dev feed is not live yet: do not publish.
2. `pnpm spec:sync && pnpm generate && git diff`: the live document will list `/events/stream` once deployed (it is not in the current pin). Review, then check `typescript/src/stream.ts` still matches the operation (query `watchId`, `concernId`, `type`, `backlog`, `since`).
3. **Live smoke with a test account** (never production data): create a webhook watch with a throwaway target, keep its `whsec_...`, run `PERCIA_API_KEY=... PERCIA_WEBHOOK_SECRET=whsec_... percia listen --forward-to http://localhost:3000/hook --backlog 3` against `examples/node-express` (or any receiver), trigger an event (`percia watches test <id>`), and check the receiver verifies the signature and prints the event. Also: a key without `events:read` gives a clear 403; a third concurrent `listen` shows the 429 message; leave one running past 10 minutes and see `Reconnected` with no duplicate; Ctrl-C exits 0.
4. Update `CHANGELOG.md` and the per-package changelogs from "unreleased" to the release date.
5. Publish as in sections 1 and 2 (npm `@percia/sdk` first, then `@percia/cli`; PyPI tag `python-v0.3.0`). Do not tag before steps 1 to 3. Run `pnpm install --frozen-lockfile && pnpm generate:check && pnpm test && pnpm build` and `cd python && pytest` first.

## 5. Optional

- Docker/Homebrew/winget packaging of the CLI, a `percia` PyPI console script, signing with sigstore beyond npm provenance, and hosted generators (Stainless, Speakeasy, Fern) are not set up.
