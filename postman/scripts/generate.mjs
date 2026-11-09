#!/usr/bin/env node
// Generate the Postman collection (v2.1), the Postman environment and the Insomnia v4 export from spec/openapi.json.
// Deterministic: same spec in, same bytes out (no dates, no random ids). Zero dependencies.
//
//   node postman/scripts/generate.mjs            write the three files next to this package
//   node postman/scripts/generate.mjs --stdout   print a JSON object with the three documents (used by the tests)
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const pkgDir = join(here, "..");
const specPath = join(pkgDir, "..", "spec", "openapi.json");

// ---------- helpers ----------
const sha = (s) => createHash("sha1").update(s).digest("hex");
const uuid = (s) => { const h = sha(s); return `${h.slice(0, 8)}-${h.slice(8, 12)}-4${h.slice(13, 16)}-a${h.slice(17, 20)}-${h.slice(20, 32)}`; };
const json = (v) => JSON.stringify(v, null, 2);

/** Resolve a local $ref. */
const makeDeref = (spec) => {
	const resolve = (node, seen = []) => {
		if (node && typeof node === "object" && node.$ref) {
			if (seen.includes(node.$ref)) return {};
			const target = node.$ref.replace(/^#\//, "").split("/").reduce((o, k) => o?.[k.replace(/~1/g, "/").replace(/~0/g, "~")], spec);
			return resolve(target, [...seen, node.$ref]);
		}
		return node;
	};
	return resolve;
};

/** A small deterministic sample for a JSON schema: required properties only, first choice of any union. */
export function sample(schema, resolve, depth = 0) {
	const s = resolve(schema) ?? {};
	if (s.example !== undefined) return s.example;
	if (s.const !== undefined) return s.const;
	if (s.default !== undefined) return s.default;
	if (s.enum) return s.enum[0];
	for (const key of ["oneOf", "anyOf"]) if (s[key]) return sample(s[key][0], resolve, depth + 1);
	if (s.allOf) return Object.assign({}, ...s.allOf.map((p) => sample(p, resolve, depth + 1)));
	const type = Array.isArray(s.type) ? (s.type.find((t) => t !== "null") ?? "null") : s.type;
	if (type === "object" || s.properties) {
		if (depth > 4) return {};
		const props = s.properties ?? {};
		const names = (s.required ?? []).filter((n) => n in props);
		return Object.fromEntries(names.map((n) => [n, sample(props[n], resolve, depth + 1)]));
	}
	if (type === "array") return depth > 4 || !s.items ? [] : [sample(s.items, resolve, depth + 1)];
	if (type === "integer" || type === "number") return s.minimum ?? 1;
	if (type === "boolean") return false;
	if (type === "null") return null;
	if (s.format === "email") return "you@example.com";
	if (s.format === "date-time") return "2026-11-01T09:30:00Z";
	if (s.format === "uri") return "https://example.com";
	const min = s.minLength ?? 1;
	return "x".repeat(Math.max(1, Math.min(min, 8)));
}

const singular = (w) => w.replace(/ies$/, "y").replace(/(ch|sh|x|ss)es$/, "$1").replace(/([^s])s$/, "$1");
/** {id} after "watches" is watchId; other params keep their name. */
const varFor = (path, name) => {
	if (name === "token" && path.startsWith("/devices")) return "deviceToken";
	if (name !== "id") return name;
	const before = path.split("/").filter(Boolean);
	const idx = before.indexOf("{id}");
	return `${singular(before[idx - 1].replace(/-/g, ""))}Id`;
};

// ---------- selection ----------
const PLATFORM_PUBLIC = new Set(["getHealth", "getConfig", "getStatus"]);
const TAG_ORDER = ["watches", "events", "hooks", "cameras", "integrations", "agents", "sites", "evidence", "devices", "billing", "platform"];
const TAG_TITLE = { watches: "Watches", events: "Events feed", hooks: "REST hooks", cameras: "Phone cameras", integrations: "Integrations", agents: "Agents", sites: "Sites", evidence: "Evidence and tests", devices: "Push devices", billing: "Plan and usage", platform: "Platform" };

const BODY_OVERRIDES = {
	updateWatch: { status: "paused" },
	createCamera: { name: "Hall phone" },
	createConnectLink: { service: "slack" },
	setWatchIntegrations: { rules: [{ connectionId: "{{connectionId}}", on: "*" }] },
	createAgent: { name: "Loading bay", config: { concerns: [{ id: "van", text: "A delivery van is parked in the loading bay", kind: "state" }] } },
	updateAgent: { config: { concerns: [{ id: "van", text: "A delivery van is parked in the loading bay", kind: "state" }] } },
	createHook: { url: "{{webhookUrl}}", events: ["goal.met"], label: "Postman hook" },
	createWatch: { sourceUrl: "rtsp://cam.example.com/stream", goal: "A person is standing at the front door", notify: { type: "webhook", target: "{{webhookUrl}}" } },
	checkCameraPairing: { pairing: "{{pairUrl}}" },
	publishAgent: { note: "Postman" },
	createSite: { name: "Front yard", notes: "Gate on the left." },
	askSite: { question: "Was anyone at the gate today?" },
	registerDevice: { token: "{{deviceToken}}", platform: "ios", appVersion: "1.0.0" },
};
const QUERY_DEFAULTS = { limit: "50", since: "2026-11-01T00:00:00Z" };

// ---------- test scripts (plain JS, no pm.expect, so the offline runner needs only pm.test) ----------
const SAVE_FN = [
	"function save(name, value) {",
	"  if (value === undefined || value === null) return;",
	"  pm.collectionVariables.set(name, value);",
	"  if (pm.environment && pm.environment.name) pm.environment.set(name, value);",
	"}",
];
const bodyJson = ["var body = null;", "try { body = pm.response.json(); } catch (e) { body = null; }"];

function testScript(op, saves = []) {
	const success = Object.keys(op.responses).filter((c) => /^[23]\d\d$/.test(c)).map(Number);
	const wantsJson = success.some((c) => c !== 204 && op.responses[String(c)].content?.["application/json"]);
	const exec = [`var okCodes = ${JSON.stringify(success.length ? success : [200])};`, ...(saves.length ? SAVE_FN : [])];
	exec.push(
		`pm.test("status is a documented success code (" + okCodes.join("/") + ")", function () {`,
		`  if (okCodes.indexOf(pm.response.code) === -1) throw new Error("got " + pm.response.code);`,
		`});`,
	);
	if (wantsJson) {
		exec.push(...bodyJson, `pm.test("body is JSON", function () {`, `  if (body === null) throw new Error("response body is not JSON");`, `});`);
	} else exec.push("var body = null;");
	exec.push(
		`pm.test("errors use the shared envelope", function () {`,
		`  if (pm.response.code < 400) return;`,
		`  var e = null; try { e = pm.response.json(); } catch (x) { e = null; }`,
		`  if (!e || typeof e.message !== "string") throw new Error("missing message");`,
		`  if (e.error && typeof e.error.code !== "string") throw new Error("missing error.code");`,
		`});`,
	);
	if (saves.length) {
		exec.push(`if (body && pm.response.code < 400) {`, ...saves.map((l) => `  ${l}`), `}`);
	}
	return exec;
}

const SAVES = {
	createWatch: ['save("watchId", body.id);', 'save("webhookSecret", body.webhookSecret);'],
	listWatchEvents: ['if (body.events && body.events.length) save("eventId", body.events[0].id);'],
	listAccountEvents: ['save("cursor", body.nextCursor);', 'if (body.events && body.events.length) save("eventId", body.events[0].id);'],
	getSampleEvent: ['if (body.events && body.events.length) save("eventId", body.events[0].id);'],
	createHook: ['save("hookId", body.id);', 'save("hookSecret", body.secret);'],
	createCamera: ['if (body.camera) save("cameraId", body.camera.id);', 'save("pairUrl", body.pairUrl);'],
	createConnectLink: ['save("connectUrl", body.connectUrl);'],
	listIntegrations: ['if (Array.isArray(body) && body.length) save("connectionId", body[0].id);'],
	createAgent: ['save("agentId", body.id);'],
	createSite: ['save("siteId", body.id);'],
};

// ---------- model ----------
export function buildModel(spec) {
	const resolve = makeDeref(spec);
	const ops = [];
	let skipped = 0;
	for (const [path, item] of Object.entries(spec.paths)) {
		for (const [method, op] of Object.entries(item)) {
			const apiKeyCapable = (op.security ?? []).some((s) => "bearerAuth" in s);
			const open = PLATFORM_PUBLIC.has(op.operationId);
			if (!apiKeyCapable && !open) { skipped++; continue; }
			ops.push({ method: method.toUpperCase(), path, op, open });
		}
	}
	const tagRank = (t) => (TAG_ORDER.includes(t) ? TAG_ORDER.indexOf(t) : TAG_ORDER.length);
	ops.sort((a, b) => tagRank(a.op.tags[0]) - tagRank(b.op.tags[0]) || a.path.localeCompare(b.path) || a.method.localeCompare(b.method));

	const requests = ops.map(({ method, path, op, open }) => {
		const params = (op.parameters ?? []).map((p) => resolve(p));
		const urlPath = path.replace(/\{(\w+)\}/g, (_, n) => `{{${varFor(path, n)}}}`);
		const query = params.filter((p) => p.in === "query").map((p) => ({ key: p.name, value: QUERY_DEFAULTS[p.name] ?? "", disabled: p.name !== "limit", description: p.description ?? "" }));
		let bodyText = null;
		const content = op.requestBody?.content?.["application/json"];
		if (content) {
			const value = BODY_OVERRIDES[op.operationId] ?? content.example ?? sample(content.schema, resolve);
			bodyText = json(value);
		}
		const scopes = op["x-percia-scopes"] ?? [];
		const description = [
			`operationId: ${op.operationId}`,
			"",
			op.summary,
			...(op.description ? ["", op.description] : []),
			"",
			open ? "Auth: none." : `Scopes: ${scopes.length ? scopes.join(", ") : "(none listed)"}.`,
			...(op["x-percia-destructive"] ? ["", "Destructive: also needs watches:delete (unless noted in the API description)."] : []),
		].join("\n");
		return {
			operationId: op.operationId, tag: op.tags[0], method, path, urlPath, query, bodyText, open,
			name: `${op.summary}`, description,
			test: testScript(op, SAVES[op.operationId] ?? []),
		};
	});

	// The five-step flow of docs/integrators/quickstart.md, in order.
	const byId = Object.fromEntries(requests.map((r) => [r.operationId, r]));
	const quick = [
		["1. Create a webhook watch (save webhookSecret)", "createWatch", "The response is the only time you see `webhookSecret`. The test saves it as the `webhookSecret` variable (never logged). Set `webhookUrl` first: a public https address of your receiver."],
		["2. Send a signed test event to your receiver", "testWatchDelivery", "No camera needed. Needs a receiver at `webhookUrl`; see examples/ for ready-made ones."],
		["3. Read the watch back", "getWatch", "The secret is never returned again; you get `secretHint`."],
		["4. Read the decisions it produced", "listWatchEvents", "Newest first. Page with `cursor`."],
		["5. Delete the watch", "deleteWatch", "Cleans up the quickstart watch."],
	].map(([name, id, note]) => ({ ...byId[id], folder: "Quickstart", name, description: `${note}\n\n${byId[id].description}` }));

	const folders = [{ name: "Quickstart", requests: quick }];
	for (const tag of [...new Set(requests.map((r) => r.tag))]) folders.push({ name: TAG_TITLE[tag] ?? tag, requests: requests.filter((r) => r.tag === tag).map((r) => ({ ...r, folder: TAG_TITLE[tag] ?? tag })) });

	const vars = new Set(["baseUrl", "apiKey", "webhookUrl"]);
	for (const r of requests) for (const m of `${r.urlPath} ${r.bodyText ?? ""}`.matchAll(/\{\{(\w+)\}\}/g)) vars.add(m[1]);
	for (const r of requests) for (const l of r.test) for (const m of l.matchAll(/save\("(\w+)"/g)) vars.add(m[1]);
	const envVars = ["baseUrl", "apiKey", "webhookUrl", ...[...vars].filter((v) => !["baseUrl", "apiKey", "webhookUrl"].includes(v)).sort()];
	return { folders, requests, skipped, total: Object.values(spec.paths).reduce((n, p) => n + Object.keys(p).length, 0), envVars, spec };
}

const ENV_DEFAULTS = { baseUrl: "https://playground.percia.ai", webhookUrl: "https://example.com/hooks/percia" };
const SECRETS = new Set(["apiKey", "webhookSecret", "hookSecret", "pairUrl", "connectUrl", "deviceToken"]);

// ---------- Postman ----------
const pmItem = (r) => ({
	name: r.name,
	event: [{ listen: "test", script: { type: "text/javascript", exec: r.test } }],
	request: {
		method: r.method,
		header: [{ key: "Accept", value: "application/json" }, ...(r.bodyText ? [{ key: "Content-Type", value: "application/json" }] : [])],
		...(r.bodyText && { body: { mode: "raw", raw: r.bodyText, options: { raw: { language: "json" } } } }),
		...(r.open && { auth: { type: "noauth" } }),
		url: {
			raw: `{{baseUrl}}/api${r.urlPath}${r.query.length ? "?" + r.query.map((q) => `${q.key}=${q.value}`).join("&") : ""}`,
			host: ["{{baseUrl}}"],
			path: ["api", ...r.urlPath.split("/").filter(Boolean)],
			...(r.query.length && { query: r.query.map((q) => ({ key: q.key, value: q.value, ...(q.disabled && { disabled: true }), description: q.description })) }),
		},
		description: r.description,
	},
	response: [],
});

export function buildPostman(model) {
	const { spec } = model;
	return {
		info: {
			_postman_id: uuid("percia-collection"),
			name: "Percia API",
			description: `${spec.info.description}\n\nGenerated from spec/openapi.json (version ${spec.info.version}). Set the \`apiKey\` environment variable to a key created in the dashboard. Start with the Quickstart folder. Regenerate with \`node postman/scripts/generate.mjs\`.`,
			schema: "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
		},
		auth: { type: "bearer", bearer: [{ key: "token", value: "{{apiKey}}", type: "string" }] },
		variable: model.envVars.filter((v) => !SECRETS.has(v)).map((key) => ({ key, value: ENV_DEFAULTS[key] ?? "", type: "string" })),
		item: model.folders.map((f) => ({ name: f.name, item: f.requests.map(pmItem) })),
	};
}

export function buildPostmanEnv(model) {
	return {
		id: uuid("percia-environment"),
		name: "Percia",
		values: model.envVars.map((key) => ({ key, value: ENV_DEFAULTS[key] ?? "", type: SECRETS.has(key) ? "secret" : "default", enabled: true })),
		_postman_variable_scope: "environment",
	};
}

// ---------- Insomnia v4 ----------
export function buildInsomnia(model) {
	const ws = "wrk_" + sha("percia-workspace").slice(0, 16);
	const env = (name) => name.replace(/^{{(\w+)}}$/, "{{ _.$1 }}");
	const tpl = (s) => s.replace(/\{\{(\w+)\}\}/g, "{{ _.$1 }}");
	const resources = [
		{ _id: ws, _type: "workspace", parentId: null, name: "Percia API", description: "Generated from spec/openapi.json. Select the Percia environment and set apiKey.", scope: "collection" },
		{
			_id: "env_" + sha("percia-base").slice(0, 16), _type: "environment", parentId: ws, name: "Base Environment", isPrivate: false, metaSortKey: 1,
			data: Object.fromEntries(model.envVars.map((k) => [k, ENV_DEFAULTS[k] ?? ""])),
		},
	];
	let n = 0;
	for (const f of model.folders) {
		const gid = "fld_" + sha("folder:" + f.name).slice(0, 16);
		resources.push({ _id: gid, _type: "request_group", parentId: ws, name: f.name, description: "", environment: {}, metaSortKey: -(1000 - ++n) });
		for (const r of f.requests) {
			resources.push({
				_id: "req_" + sha(`req:${f.name}:${r.name}`).slice(0, 16), _type: "request", parentId: gid, name: r.name, description: r.description, method: r.method,
				url: tpl(`{{baseUrl}}/api${r.urlPath}`),
				parameters: r.query.map((q) => ({ name: q.key, value: q.value, disabled: q.disabled })),
				headers: [{ name: "Accept", value: "application/json" }, ...(r.bodyText ? [{ name: "Content-Type", value: "application/json" }] : [])],
				...(r.bodyText && { body: { mimeType: "application/json", text: tpl(r.bodyText) } }),
				authentication: r.open ? {} : { type: "bearer", token: "{{ _.apiKey }}" },
				metaSortKey: -(1000 - ++n),
			});
		}
	}
	return { _type: "export", __export_format: 4, __export_date: "2026-11-09T00:00:00.000Z", __export_source: "percia-sdks/postman/scripts/generate.mjs", resources };
}

export function generateAll(spec = JSON.parse(readFileSync(specPath, "utf8"))) {
	const model = buildModel(spec);
	return {
		model,
		files: {
			"percia.postman_collection.json": json(buildPostman(model)) + "\n",
			"percia.postman_environment.json": json(buildPostmanEnv(model)) + "\n",
			"percia.insomnia.json": json(buildInsomnia(model)) + "\n",
		},
	};
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
	const { model, files } = generateAll();
	if (process.argv.includes("--stdout")) process.stdout.write(JSON.stringify(files));
	else {
		mkdirSync(pkgDir, { recursive: true });
		for (const [name, text] of Object.entries(files)) writeFileSync(join(pkgDir, name), text);
		console.log(`postman: ${model.requests.length} requests in ${model.folders.length} folders (+5 quickstart), skipped ${model.skipped} of ${model.total} operations (session-only or internal)`);
	}
}
