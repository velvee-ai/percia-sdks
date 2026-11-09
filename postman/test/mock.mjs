// A tiny mock server built from spec/openapi.json: answers each documented operation with its example or a sample
// generated from the response schema. Offline, no dependencies. Used by the collection dry run.
import { createServer } from "node:http";

export function createMock(spec) {
	const deref = (node, seen = []) => {
		if (node && node.$ref) {
			if (seen.includes(node.$ref)) return {};
			const t = node.$ref.replace(/^#\//, "").split("/").reduce((o, k) => o?.[k], spec);
			return deref(t, [...seen, node.$ref]);
		}
		return node;
	};
	const full = (schema, depth = 0) => {
		const s = deref(schema) ?? {};
		if (s.example !== undefined) return s.example;
		if (s.const !== undefined) return s.const;
		if (s.enum) return s.enum[0];
		for (const k of ["oneOf", "anyOf"]) if (s[k]) return full(s[k][0], depth + 1);
		const type = Array.isArray(s.type) ? (s.type.find((t) => t !== "null") ?? "null") : s.type;
		if (type === "object" || s.properties) return depth > 5 ? {} : Object.fromEntries(Object.entries(s.properties ?? {}).map(([k, v]) => [k, full(v, depth + 1)]));
		if (type === "array") return depth > 5 || !s.items ? [] : [full(s.items, depth + 1)];
		if (type === "integer" || type === "number") return 1;
		if (type === "boolean") return false;
		if (type === "null") return null;
		return s.format === "date-time" ? "2026-11-01T09:30:00Z" : "text";
	};
	const routes = [];
	for (const [path, item] of Object.entries(spec.paths)) {
		const re = new RegExp("^/api" + path.replace(/\{[^}]+\}/g, "[^/]+") + "$");
		for (const [method, op] of Object.entries(item)) routes.push({ method: method.toUpperCase(), re, op, path });
	}
	const seen = [];
	const server = createServer((req, res) => {
		const url = new URL(req.url, "http://x");
		seen.push({ method: req.method, path: url.pathname, authorization: req.headers.authorization });
		const route = routes.find((r) => r.method === req.method && r.re.test(url.pathname));
		const reply = (code, body, headers = {}) => { res.writeHead(code, { "content-type": "application/json", "x-percia-request-id": "req_mock", ...headers }); res.end(body === undefined ? "" : JSON.stringify(body)); };
		if (!route) return reply(404, { error: { code: "not_found", message: "no such route" }, message: "no such route" });
		const code = Object.keys(route.op.responses).filter((c) => /^2\d\d$/.test(c)).sort()[0] ?? "200";
		const media = route.op.responses[code]?.content?.["application/json"];
		if (code === "204" || !media) return reply(Number(code));
		return reply(Number(code), media.example ?? full(media.schema));
	});
	return { server, seen, listen: () => new Promise((ok) => server.listen(0, "127.0.0.1", () => ok(`http://127.0.0.1:${server.address().port}`))), close: () => new Promise((ok) => server.close(ok)) };
}
