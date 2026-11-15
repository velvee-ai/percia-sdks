// Follow the developer event feed (GET /api/events/stream) and POST each event to a local server, signed like a real webhook.
// The same thing `percia listen --forward-to` does, in 40 lines you can adapt. A development tool, not a delivery path.
import { createClient, signWebhook } from "@percia/sdk";

/** Forward every event of the stream to `target` until `signal` aborts. Resolves with the number of events forwarded. */
export async function forwardStream({ client, target, secret, signal, filters = {}, log = () => {} }) {
	let n = 0;
	for await (const item of client.events.stream({ ...filters, signal })) {
		if (item.kind === "reconnect") log(`reconnecting in ${Math.ceil(item.delayMs / 1000)}s (${item.reason})`);
		if (item.kind === "resync") log("the server could not resume from the last event; backfill with GET /api/events if you need the gap");
		if (item.kind !== "event") continue;
		// Sign and send the exact string the server sent: a re-serialised body would not verify.
		const res = await fetch(target, {
			method: "POST",
			headers: { "content-type": "application/json", "percia-signature": await signWebhook(item.data, secret) },
			body: item.data,
			redirect: "manual",
			signal: AbortSignal.timeout(10_000),
		}).catch((e) => ({ status: `failed (${e.cause?.code ?? e.message})` }));
		n++;
		log(`${item.event.type} ${item.event.eventId.slice(0, 8)} -> ${res.status}`);
	}
	return n;
}

if (import.meta.url === `file://${process.argv[1]}`) {
	const { PERCIA_API_KEY, PERCIA_WEBHOOK_SECRET, FORWARD_TO = "http://localhost:3000/hook", PERCIA_BASE_URL } = process.env;
	if (!PERCIA_API_KEY || !PERCIA_WEBHOOK_SECRET) {
		console.error("Set PERCIA_API_KEY (events:read) and PERCIA_WEBHOOK_SECRET (the watch's whsec_...).");
		process.exit(2);
	}
	const ctl = new AbortController();
	process.on("SIGINT", () => ctl.abort());
	const client = createClient({ apiKey: PERCIA_API_KEY, baseUrl: PERCIA_BASE_URL });
	const n = await forwardStream({ client, target: FORWARD_TO, secret: PERCIA_WEBHOOK_SECRET, signal: ctl.signal, log: (l) => console.log(l) });
	console.log(`stopped after ${n} events`);
}
