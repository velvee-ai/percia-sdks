// A scriptable SSE server that speaks the dev-feed contract (percia-cf docs/specs/platform/dev-feed.md) over real HTTP,
// so fetch streaming, framing and reconnects are exercised for real. Each connection consumes the next scripted step.
import { createServer, type IncomingMessage, type Server, type ServerResponse } from "node:http";
import type { AddressInfo } from "node:net";

export type Conn = { req: IncomingMessage; res: ServerResponse; url: URL; n: number };
export type Step = (c: Conn) => void | Promise<void>;
export type RecordedConn = { n: number; url: URL; headers: IncomingMessage["headers"] };

export const evt = (cursor: number, over: Record<string, unknown> = {}) => ({
	id: String(cursor),
	body: { id: `dec_${cursor}`, watchId: "w_abc", occurrenceId: `occ_${cursor}`, type: "goal.met", goal: "A person is at the door", reason: "A person stands at the door.", confidence: 0.93, at: "2026-11-14T09:30:00Z", eventId: `evt-${cursor}`, ...over },
});

/** The exact bytes of one message, like the server: `id`, `event`, `data` (one JSON line). */
export const message = (e: ReturnType<typeof evt>) => `id: ${e.id}\nevent: ${(e.body as { type: string }).type}\ndata: ${JSON.stringify(e.body)}\n\n`;

export const open = (c: Conn, status = 200, headers: Record<string, string> = {}) => {
	c.res.writeHead(status, { "content-type": "text/event-stream", "cache-control": "no-cache, no-transform", ...headers });
	c.res.write("retry: 3000\n: connected\n\n");
};

/** Open, send the frames, then close the connection (as the server does after `event: end`). */
export const send = (...frames: string[]): Step => (c) => {
	open(c);
	for (const f of frames) c.res.write(f);
	c.res.end();
};
/** Open, send the frames, then keep the connection open until the client goes away. */
export const hold = (...frames: string[]): Step => (c) => {
	open(c);
	for (const f of frames) c.res.write(f);
};
export const end = (reason = "max_duration") => `event: end\ndata: ${JSON.stringify({ reason })}\n\n`;
export const resync = (from: number) => `event: resync\ndata: ${JSON.stringify({ reason: "cursor_too_old", from })}\n\n`;
export const fail = (status: number, code: string, message: string, headers: Record<string, string> = {}): Step => (c) => {
	c.res.writeHead(status, { "content-type": "application/json", "x-percia-request-id": "req_mock", ...headers });
	c.res.end(JSON.stringify({ error: { code, message, request_id: "req_mock" }, message, request_id: "req_mock" }));
};

export class MockSse {
	connections: RecordedConn[] = [];
	steps: Step[] = [];
	keys = new Set(["pk_live_test"]);
	private server?: Server;
	private sockets = new Set<import("node:net").Socket>();
	then(...s: Step[]) { this.steps.push(...s); return this; }
	async listen(): Promise<{ origin: string; close: () => Promise<void> }> {
		this.server = createServer(async (req, res) => {
			const url = new URL(req.url!, `http://${req.headers.host}`);
			const n = this.connections.length + 1;
			this.connections.push({ n, url, headers: req.headers });
			const bearer = /^Bearer (.+)$/.exec(req.headers.authorization ?? "")?.[1];
			if (url.pathname !== "/api/events/stream") return void res.writeHead(404).end();
			if (!bearer || !this.keys.has(bearer)) return fail(401, "invalid_api_key", "Missing or invalid API key.")({ req, res, url, n });
			const step = this.steps.shift() ?? hold();
			await step({ req, res, url, n });
		});
		this.server.on("connection", (s) => (this.sockets.add(s), s.on("close", () => this.sockets.delete(s))));
		await new Promise<void>((r) => this.server!.listen(0, "127.0.0.1", r));
		const { port } = this.server.address() as AddressInfo;
		return { origin: `http://127.0.0.1:${port}`, close: () => new Promise((r) => (this.sockets.forEach((s) => s.destroy()), this.server!.close(() => r()))) };
	}
}
