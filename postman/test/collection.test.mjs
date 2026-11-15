import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";
import { buildModel } from "../scripts/generate.mjs";
import { createMock } from "./mock.mjs";
import { runFolder } from "./runner.mjs";

const pkg = join(dirname(fileURLToPath(import.meta.url)), "..");
const spec = JSON.parse(readFileSync(join(pkg, "..", "spec", "openapi.json"), "utf8"));
const read = (f) => readFileSync(join(pkg, f), "utf8");
const collection = JSON.parse(read("percia.postman_collection.json"));
const env = JSON.parse(read("percia.postman_environment.json"));
const insomnia = JSON.parse(read("percia.insomnia.json"));
const model = buildModel(spec);

const opLine = (item) => /^(?:.*\n)*?operationId: (\w+)/m.exec(item.request.description)?.[1];
const flat = (folders) => folders.flatMap((f) => f.item.map((i) => ({ folder: f.name, item: i })));

test("collection is Postman v2.1 with collection-level bearer auth", () => {
	assert.equal(collection.info.schema, "https://schema.getpostman.com/json/collection/v2.1.0/collection.json");
	assert.deepEqual(collection.auth, { type: "bearer", bearer: [{ key: "token", value: "{{apiKey}}", type: "string" }] });
	assert.equal(collection.item[0].name, "Quickstart");
});

test("every api-key-capable operation appears exactly once outside Quickstart, and nothing else does", () => {
	const expected = [];
	for (const [path, item] of Object.entries(spec.paths))
		for (const [method, op] of Object.entries(item))
			if (op["x-percia-stream"]) continue; // endless response: not a request (see postman/README.md)
			else if ((op.security ?? []).some((s) => "bearerAuth" in s) || ["getHealth", "getConfig", "getStatus"].includes(op.operationId)) expected.push(op.operationId);
	const got = flat(collection.item.slice(1)).map(({ item }) => opLine(item));
	assert.deepEqual([...new Set(got)].sort(), [...expected].sort());
	// Variants (a second useful shape of one operation, e.g. a push camera) repeat an operationId on purpose.
	assert.equal(new Set(got).size, got.length - model.variants);
	assert.equal(model.requests.length - model.variants + model.skipped, model.total);
	assert.ok(collection.item.some((f) => f.item.some((i) => /push camera/i.test(i.name))));
});

test("Quickstart is the five-step flow in order", () => {
	const ids = collection.item[0].item.map(opLine);
	assert.deepEqual(ids, ["createWatch", "testWatchDelivery", "getWatch", "listWatchEvents", "deleteWatch"]);
});

test("each request URL resolves to a spec path and method", () => {
	const templates = Object.entries(spec.paths).map(([p, ops]) => ({ re: new RegExp("^/api" + p.replace(/\{[^}]+\}/g, "\\{\\{\\w+\\}\\}") + "$"), ops }));
	for (const { item } of flat(collection.item)) {
		const r = item.request;
		assert.ok(r.url.raw.startsWith("{{baseUrl}}/api/"), r.url.raw);
		const path = "/" + r.url.path.join("/");
		const t = templates.find((x) => x.re.test(path));
		assert.ok(t, `no spec path for ${path}`);
		assert.ok(t.ops[r.method.toLowerCase()], `${r.method} ${path} not in spec`);
		assert.ok(item.event.some((e) => e.listen === "test" && e.script.exec.length > 0), `${item.name} has no test script`);
		if (r.body) JSON.parse(r.body.raw);
	}
});

test("environment has the documented variables and no secret values", () => {
	const byKey = Object.fromEntries(env.values.map((v) => [v.key, v]));
	for (const k of ["baseUrl", "apiKey", "webhookUrl", "watchId", "cameraId", "hookId", "eventId"]) assert.ok(byKey[k], k);
	assert.equal(byKey.baseUrl.value, "https://playground.percia.ai");
	assert.equal(byKey.apiKey.type, "secret");
	for (const v of env.values.filter((x) => x.type === "secret")) assert.equal(v.value, "");
	assert.doesNotMatch(read("percia.postman_environment.json") + read("percia.postman_collection.json") + read("percia.insomnia.json"), /pk_live_[0-9a-f]|whsec_[0-9a-f]{8}/);
});

test("scripts never log secrets", () => {
	const all = JSON.stringify(collection);
	assert.doesNotMatch(all, /console\./);
});

test("insomnia export is v4 with the same folders, requests and environment", () => {
	assert.equal(insomnia._type, "export");
	assert.equal(insomnia.__export_format, 4);
	const groups = insomnia.resources.filter((r) => r._type === "request_group").map((r) => r.name);
	assert.deepEqual(groups, collection.item.map((f) => f.name));
	assert.equal(insomnia.resources.filter((r) => r._type === "request").length, flat(collection.item).length);
	const ids = insomnia.resources.map((r) => r._id);
	assert.equal(new Set(ids).size, ids.length);
	const base = insomnia.resources.find((r) => r._type === "environment");
	assert.equal(base.data.baseUrl, "https://playground.percia.ai");
	assert.equal(base.data.apiKey, "");
	for (const r of insomnia.resources.filter((x) => x._type === "request" && x.authentication.type)) assert.equal(r.authentication.token, "{{ _.apiKey }}");
});

test("generator is deterministic and the committed files are up to date", () => {
	const run = () => JSON.parse(execFileSync("node", [join(pkg, "scripts", "generate.mjs"), "--stdout"], { maxBuffer: 1 << 27 }).toString());
	const a = run();
	assert.deepEqual(a, run());
	assert.equal(a["percia.postman_collection.json"], read("percia.postman_collection.json"), "run: node postman/scripts/generate.mjs");
	assert.equal(a["percia.postman_environment.json"], read("percia.postman_environment.json"));
	assert.equal(a["percia.insomnia.json"], read("percia.insomnia.json"));
});

test("dry run: Quickstart folder against a mock server built from the spec", async () => {
	const mock = createMock(spec);
	const base = await mock.listen();
	try {
		const vars = { baseUrl: base, apiKey: "pk_live_test_placeholder", webhookUrl: "https://example.com/hooks/percia" };
		const results = await runFolder(collection, "Quickstart", vars);
		const failed = results.flatMap((r) => r.tests.filter((t) => !t.ok).map((t) => `${r.name}: ${t.name}: ${t.error}`));
		assert.deepEqual(failed, []);
		assert.equal(results.length, 5);
		assert.deepEqual(results.map((r) => r.status), [201, 200, 200, 200, 200]);
		assert.ok(vars.watchId, "watchId saved");
		assert.ok(vars.webhookSecret, "webhookSecret saved");
		assert.ok(mock.seen.every((s) => s.authorization === "Bearer pk_live_test_placeholder"));
		assert.deepEqual(mock.seen.map((s) => s.method), ["POST", "POST", "GET", "GET", "DELETE"]);
		const events = await runFolder(collection, "Events feed", vars);
		assert.deepEqual(events.flatMap((r) => r.tests.filter((t) => !t.ok)), []);
		const hooks = await runFolder(collection, "REST hooks", vars);
		assert.deepEqual(hooks.flatMap((r) => r.tests.filter((t) => !t.ok)), []);
	} finally { await mock.close(); }
});
