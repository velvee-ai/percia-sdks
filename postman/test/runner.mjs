// A minimal Postman-compatible runner for the generated collection: variable substitution, bearer auth, `pm.test`,
// `pm.response`, `pm.collectionVariables`, `pm.environment`. Enough to run the generated test scripts offline
// (Newman is not installed here and not needed in CI).
import vm from "node:vm";

export async function runFolder(collection, folderName, vars) {
	const folder = collection.item.find((f) => f.name === folderName);
	const sub = (s) => s.replace(/\{\{(\w+)\}\}/g, (_, k) => vars[k] ?? `{{${k}}}`);
	const results = [];
	for (const item of folder.item) {
		const r = item.request;
		const url = sub(r.url.raw);
		const headers = Object.fromEntries(r.header.map((h) => [h.key, sub(h.value)]));
		const bearer = r.auth?.type === "noauth" ? null : collection.auth.bearer[0].value;
		if (bearer) headers.Authorization = `Bearer ${sub(bearer)}`;
		const res = await fetch(url, { method: r.method, headers, body: r.body ? sub(r.body.raw) : undefined });
		const text = await res.text();
		const tests = [];
		const pm = {
			test: (name, fn) => { try { fn(); tests.push({ name, ok: true }); } catch (e) { tests.push({ name, ok: false, error: String(e.message) }); } },
			response: { code: res.status, text: () => text, json: () => JSON.parse(text) },
			collectionVariables: { set: (k, v) => { vars[k] = v; }, get: (k) => vars[k] },
			environment: { name: null },
		};
		const script = item.event.find((e) => e.listen === "test").script.exec.join("\n");
		vm.runInNewContext(script, { pm });
		results.push({ name: item.name, status: res.status, tests });
	}
	return results;
}
