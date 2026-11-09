import QRCode from "qrcode";
import type { Context } from "./context.js";
import { stripControl } from "./errors.js";

export const json = (ctx: Context, value: unknown) => ctx.stdout(JSON.stringify(value, null, 2) + "\n");
export const ndjson = (ctx: Context, value: unknown) => ctx.stdout(JSON.stringify(value) + "\n");

/** Left-aligned table. Cell text is stripped of control characters (cells often hold model or user text). */
export function table(rows: Record<string, unknown>[], columns: { key: string; title?: string; max?: number }[]): string {
	if (rows.length === 0) return "";
	const cell = (v: unknown, max = 60) => {
		const s = stripControl(v === null || v === undefined ? "" : typeof v === "object" ? JSON.stringify(v) : String(v)).replace(/\s+/g, " ");
		return s.length > max ? s.slice(0, max - 1) + "…" : s;
	};
	const data = rows.map((r) => columns.map((c) => cell(r[c.key], c.max)));
	const heads = columns.map((c) => (c.title ?? c.key).toUpperCase());
	const widths = heads.map((h, i) => Math.max(h.length, ...data.map((d) => d[i].length)));
	const line = (cells: string[]) => cells.map((c, i) => c.padEnd(widths[i])).join("  ").trimEnd();
	return [line(heads), ...data.map(line)].join("\n") + "\n";
}

/** A QR code for a URL, drawn with block characters, or "" when it cannot be drawn. */
export async function qr(url: string): Promise<string> {
	try {
		return await QRCode.toString(url, { type: "terminal", small: true });
	} catch {
		return "";
	}
}

export const isoOrDash = (v: unknown) => (typeof v === "string" && v ? v.replace(/\.\d+Z$/, "Z") : "-");
