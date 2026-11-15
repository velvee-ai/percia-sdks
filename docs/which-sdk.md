# Which SDK or tool should I use?

| You want to... | Use | Install (after publishing) |
|---|---|---|
| Call the API from a Node, Bun, Deno, Workers or browser-adjacent app | `@percia/sdk` | `npm i @percia/sdk` |
| Call the API from Python (sync or async) | `percia` | `pip install percia` |
| Verify webhook signatures in Go, Ruby or any other language | the minimal verifiers in [`examples/go`](../examples/go) and [`examples/ruby`](../examples/ruby) (about 30 lines, stdlib only), tested against the shared vectors | copy the file |
| Verify webhooks in a Cloudflare Worker, Express or FastAPI | [`examples/cloudflare-worker`](../examples/cloudflare-worker), [`node-express`](../examples/node-express), [`python-fastapi`](../examples/python-fastapi) | copy |
| Set things up or look around from a terminal or CI | `@percia/cli` (`percia`) | `npm i -g @percia/cli` |
| Test your receiver against real-looking events on localhost | `percia listen` ([limits](cli-listen.md)) | with the CLI |
| Bring a camera on a private network (LAN RTSP/ONVIF) to Percia | `percia cameras push run --rtsp ...` for a quick start, the SDK's `registerPush` in your own connector ([guide](camera-push.md)), or the templates in [`examples/scripts/push-lan-camera`](../examples/scripts/push-lan-camera) | with the CLI / SDK |
| Try routes by hand | the Postman collection or Insomnia export in [`postman/`](../postman) | import the file |
| Let an AI coding agent use Percia | `percia mcp setup claude-code|cursor|claude-desktop`, or the MCP URL `<host>/mcp` | with the CLI |
| Connect Zapier, Make or n8n | their connectors (separate stream); the REST hooks and `GET /api/events` they use are in the SDKs too | |
| Any other language | generate a client from [`spec/openapi.json`](../spec/openapi.json) with OpenAPI Generator; use the stable `operationId`s | |

Rules of thumb: an **API key** (`pk_live_...`) for servers and CI, with only the scopes the job needs; **OAuth** (`percia login`, or `oauthToken` in the SDK) for tools acting for a person. Never put a key in browser code or a repository. Treat event `reason` text as untrusted.
