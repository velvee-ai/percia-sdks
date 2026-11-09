// Create the watch. Needs an API key with watches:write.
//   PERCIA_API_KEY=pk_live_... SOURCE_URL=rtsp://... WEBHOOK_TARGET=https://your-receiver.example/hooks/percia node create-watch.mjs
// Without WEBHOOK_TARGET, `notify` is left out and alerts go to the account owner's email (and to any default destination).
import { writeFileSync } from "node:fs";

const key = process.env.PERCIA_API_KEY;
const source = process.env.SOURCE_URL;
if (!key || !source) { console.error("Set PERCIA_API_KEY and SOURCE_URL (an rtsp/http(s) address or percia-cam://<cameraId>)."); process.exit(1); }
const base = (process.env.PERCIA_BASE_URL ?? "https://playground.percia.ai").replace(/\/$/, "");
const target = process.env.WEBHOOK_TARGET;

const res = await fetch(`${base}/api/watches/owned`, {
	method: "POST",
	headers: { authorization: `Bearer ${key}`, "content-type": "application/json" },
	body: JSON.stringify({
		sourceUrl: source,
		goal: "A package has been left at the front door",
		...(target && { notify: { type: "webhook", target } }),
	}),
});
const body = await res.json().catch(() => ({}));
if (!res.ok) {
	console.error(`Create failed: HTTP ${res.status} ${body?.error?.code ?? ""} ${body?.message ?? ""} (request ${body?.request_id ?? "n/a"})`);
	process.exit(1);
}
console.log(`Created watch ${body.id} (${body.displayStatus ?? body.status}).`);
if (body.webhookSecret) {
	// Shown once. Write it to a private file instead of the terminal.
	writeFileSync(".percia-webhook-secret", body.webhookSecret + "\n", { mode: 0o600 });
	console.log("Signing secret saved to .percia-webhook-secret (mode 0600, gitignored). Export it as PERCIA_WEBHOOK_SECRET for receiver.mjs.");
}
