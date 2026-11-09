import { Command } from "commander";
import type { Event } from "@percia/sdk";
import type { Context, GlobalOptions } from "../context.js";
import { CliError, EXIT, stripControl } from "../errors.js";
import { isoOrDash, json, ndjson, table } from "../output.js";
import { openSession } from "../session.js";

type Deps = { ctx: Context; globals: () => GlobalOptions };

export const eventRow = (e: Event & { watchId?: string }) => ({ at: isoOrDash(e.at), watch: e.watchId, type: e.type, conf: typeof e.confidence === "number" ? e.confidence.toFixed(2) : "", delivery: e.deliveryStatus, reason: e.reason });
const columns = [{ key: "at" }, { key: "watch" }, { key: "type" }, { key: "conf" }, { key: "delivery" }, { key: "reason", max: 70 }];

/** Seen-id window: bounded so a long `--follow` does not grow without limit. */
export class SeenSet {
	private ids = new Set<string>();
	constructor(private max = 2000) {}
	has(id: string) { return this.ids.has(id); }
	add(id: string) {
		this.ids.add(id);
		if (this.ids.size > this.max) this.ids.delete(this.ids.values().next().value as string);
	}
}

/**
 * One poll of the account feed: newest-first events up to the first id already seen, returned oldest first.
 * This is the dedupe rule from the hooks doc for polling triggers. The cap bounds a poll after a long gap.
 */
export async function pollNew(fetchPage: () => Promise<{ events: Event[] }>, seen: SeenSet, capPages = 1): Promise<Event[]> {
	void capPages;
	const page = await fetchPage();
	const fresh: Event[] = [];
	for (const e of page.events) {
		if (seen.has(e.id)) break;
		fresh.push(e);
	}
	for (const e of fresh) seen.add(e.id);
	return fresh.reverse();
}

export function registerEvents(program: Command, { ctx, globals }: Deps) {
	const ev = program.command("events").description("Read events (every time a goal was met).");
	ev.command("list")
		.description("List events across all your watches, newest first. --follow keeps polling for new ones.")
		.option("--watch <id>", "only this watch")
		.option("--type <type>", "only this event type, e.g. goal.met")
		.option("--since <time>", "only events after this time (ISO 8601 or unix seconds)")
		.option("--limit <n>", "how many to show (1 to 100)", (v) => Number(v), 20)
		.option("--all", "page through every matching event (not with --follow)")
		.option("-f, --follow", "keep polling and print new events as they arrive (NDJSON with --json)")
		.option("--interval <seconds>", "poll interval for --follow (minimum 2)", (v) => Number(v), 5)
		.action(async (o: { watch?: string; type?: string; since?: string; limit: number; all?: boolean; follow?: boolean; interval: number }) => {
			const g = globals();
			if (!(o.limit >= 1 && o.limit <= 100)) throw new CliError("--limit must be 1 to 100.", EXIT.USAGE);
			if (o.all && o.follow) throw new CliError("Use --all or --follow, not both.", EXIT.USAGE);
			const { client } = await openSession(ctx, g);
			const filters = { watchId: o.watch, type: o.type, since: o.since && /^\d+$/.test(o.since) ? Number(o.since) : o.since };

			if (o.all) {
				const rows: Event[] = [];
				for await (const e of client.events.iterate({ ...filters, limit: 100 })) rows.push(e);
				if (g.json) return json(ctx, rows);
				return void ctx.stdout(rows.length ? table(rows.map(eventRow), columns) : "No events.\n");
			}

			const first = await client.events.list({ ...filters, limit: o.limit });
			if (!o.follow) {
				if (g.json) return json(ctx, first);
				return void ctx.stdout(first.events.length ? table(first.events.map(eventRow), columns) : "No events.\n");
			}

			// Follow: show the latest `limit` oldest-first, then poll for anything newer than what we have.
			const seen = new SeenSet();
			const initial = [...first.events].reverse();
			for (const e of initial) seen.add(e.id);
			const emit = (e: Event) => (g.json ? ndjson(ctx, e) : ctx.stdout(`${isoOrDash(e.at)}  ${e.watchId ?? ""}  ${e.type}  ${typeof e.confidence === "number" ? e.confidence.toFixed(2) : ""}  ${e.deliveryStatus ?? ""}  ${stripControl(e.reason).replace(/\s+/g, " ").slice(0, 100)}\n`));
			initial.forEach(emit);
			const interval = Math.max(2, o.interval) * 1000;
			while (!ctx.signal.aborted) {
				await ctx.sleep(interval, ctx.signal).catch(() => {});
				if (ctx.signal.aborted) break;
				const fresh = await pollNew(() => client.events.list({ ...filters, limit: 100 }), seen);
				fresh.forEach(emit);
			}
		});
}
