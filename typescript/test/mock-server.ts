// A mock Percia API built from the pinned OpenAPI document (../spec/openapi.json): routes, auth + scopes, example responses.
// Offline; no Prism needed. Tests can script failures per operationId and inspect the recorded requests.
import { readFileSync } from "node:fs";
import { createServer, type Server } from "node:http";
import type { AddressInfo } from "node:net";

const spec = JSON.parse(readFileSync(new URL("../../spec/openapi.json", import.meta.url), "utf8"));

type Json = any;
type Operation = { operationId: string; method: string; path: string; regex: RegExp; params: string[]; op: Json };

const operations: Operation[] = [];
for (const [path, item] of Object.entries<Json>(spec.paths)) {
	for (const [method, op] of Object.entries<Json>(item)) {
		const params: string[] = [];
		const regex = new RegExp("^/api" + path.replace(/\{(\w+)\}/g, (_, n) => (params.push(n), "([^/]+)")) + "$");
		operations.push({ operationId: op.operationId, method: method.toUpperCase(), path, regex, params, op });
	}
}

const resolve = (node: Json): Json => {
	if (node && node.$ref) return resolve(node.$ref.replace(/^#\//, "").split("/").reduce((a: Json, k: string) => a[k], spec));
	return node;
};

/** A minimal instance of a JSON schema (examples win; objects fill required + all properties one level). */
export function instance(schemaIn: Json, depth = 0): Json {
	const s = resolve(schemaIn);
	if (!s || depth > 6) return null;
	if (s.example !== undefined) return s.example;
	if (s.const !== undefined) return s.const;
	if (s.enum) return s.enum[0];
	if (s.oneOf || s.anyOf) return instance((s.oneOf ?? s.anyOf)[0], depth + 1);
	const type = Array.isArray(s.type) ? s.type.find((t: string) => t !== "null") : s.type;
	switch (type) {
		case "object":
			return Object.fromEntries(Object.entries<Json>(s.properties ?? {}).map(([k, v]) => [k, instance(v, depth + 1)]));
		case "array":
			return s.items ? [instance(s.items, depth + 1)] : [];
		case "integer":
		case "number":
			return s.minimum ?? 1;
		case "boolean":
			return true;
		case "string":
			return s.format === "date-time" ? "2026-11-01T09:30:00.000Z" : "x";
		default:
			return null;
	}
}

export type Recorded = { operationId: string; method: string; url: URL; headers: Headers; body: unknown };
export type Scripted = { status: number; body?: unknown; headers?: Record<string, string> };

export class MockPercia {
	/** key -> granted scopes. Default has one all-powerful key `pk_live_test`. */
	keys = new Map<string, string[]>([["pk_live_test", ["watches:read", "watches:write", "watches:delete", "events:read", "cameras:read", "cameras:write", "integrations:read", "integrations:write", "devices:write", "hooks:write"]]]);
	requests: Recorded[] = [];
	private scripts = new Map<string, Scripted[]>();
	/** Override the response for an operation: consumed in order, then the spec example is served again. */
	script(operationId: string, ...responses: Scripted[]) { this.scripts.set(operationId, [...(this.scripts.get(operationId) ?? []), ...responses]); }
	/** Fixed bodies for an operation (not consumed), e.g. a paginated feed. */
	handlers = new Map<string, (rec: Recorded) => Scripted | undefined>();
	reset() { this.requests = []; this.scripts.clear(); this.handlers.clear(); }
	operationIds() { return operations.map((o) => o.operationId); }

	private error(status: number, code: string, message: string, extra: Record<string, string> = {}): Response {
		const request_id = "req_mock_" + this.requests.length;
		return Response.json({ error: { code, message, request_id }, message, request_id }, { status, headers: { "x-percia-request-id": request_id, ...extra } });
	}

	handle = async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
		const req = new Request(input as RequestInfo, init);
		const url = new URL(req.url);
		const match = operations.map((o) => ({ o, m: o.method === req.method ? o.regex.exec(url.pathname) : null })).find((x) => x.m);
		if (!match) return this.error(404, "not_found", `No route ${req.method} ${url.pathname}`);
		const { o, m } = match;
		const text = await req.text();
		const body = text ? (() => { try { return JSON.parse(text); } catch { return text; } })() : undefined;
		const rec: Recorded = { operationId: o.operationId, method: req.method, url, headers: req.headers, body };
		this.requests.push(rec);

		// Auth: operations with security [] are public; others need a Bearer key holding every scope in x-percia-scopes.
		const needs: string[] | undefined = o.op["x-percia-scopes"];
		if (needs) {
			const bearer = /^Bearer (.+)$/.exec(req.headers.get("authorization") ?? "")?.[1];
			if (!bearer || !this.keys.has(bearer)) return this.error(401, "invalid_api_key", "Missing or invalid API key.");
			const have = this.keys.get(bearer)!;
			const missing = needs.find((s) => !have.includes(s));
			if (missing) return this.error(403, "insufficient_scope", `This key needs the ${missing} scope.`);
		}

		const forced = this.scripts.get(o.operationId)?.shift() ?? this.handlers.get(o.operationId)?.(rec);
		if (forced) return Response.json(forced.body ?? {}, { status: forced.status, headers: { "x-percia-request-id": "req_scripted", ...forced.headers } });

		const codes = Object.keys(o.op.responses).filter((c) => /^2\d\d$/.test(c));
		const code = codes[0] ?? "200";
		const content = resolve(o.op.responses[code])?.content?.["application/json"];
		if (!content) return new Response(null, { status: Number(code) === 200 ? 204 : Number(code), headers: { "x-percia-request-id": "req_mock" } });
		const payload = content.example !== undefined ? content.example : instance(content.schema);
		return Response.json(payload, { status: Number(code), headers: { "x-percia-request-id": "req_mock" } });
	};

	/** Serve over real HTTP on a random port (exercises the real fetch + Request clone path). */
	async listen(): Promise<{ origin: string; close: () => Promise<void> }> {
		const server: Server = createServer(async (nreq, nres) => {
			const chunks: Buffer[] = [];
			for await (const c of nreq) chunks.push(c as Buffer);
			const origin = `http://${nreq.headers.host}`;
			const res = await this.handle(new Request(origin + nreq.url, { method: nreq.method, headers: nreq.headers as Record<string, string>, body: ["GET", "HEAD"].includes(nreq.method!) ? undefined : Buffer.concat(chunks) }));
			nres.writeHead(res.status, Object.fromEntries(res.headers));
			nres.end(Buffer.from(await res.arrayBuffer()));
		});
		await new Promise<void>((r) => server.listen(0, "127.0.0.1", r));
		const { port } = server.address() as AddressInfo;
		return { origin: `http://127.0.0.1:${port}`, close: () => new Promise((r) => server.close(() => r())) };
	}
}
