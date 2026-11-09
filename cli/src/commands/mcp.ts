import { Command } from "commander";
import { chmod, copyFile, mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { loadConfig } from "../config.js";
import type { Context, GlobalOptions } from "../context.js";
import { CliError, EXIT } from "../errors.js";
import { json } from "../output.js";
import { resolveBaseUrl } from "../session.js";

type Deps = { ctx: Context; globals: () => GlobalOptions };
export type Target = "claude-code" | "cursor" | "claude-desktop";
export const TARGETS: Target[] = ["claude-code", "cursor", "claude-desktop"];

/**
 * The MCP server entry for a target. By default it carries no secret: Claude Code, Cursor and mcp-remote sign in with OAuth.
 * `withKey` references $PERCIA_API_KEY where the client expands environment variables; Claude Desktop cannot, so `embedKey` writes the key itself.
 */
export function buildEntry(target: Target, url: string, o: { withKey?: boolean; embedKey?: string }): Record<string, unknown> {
	if (target === "claude-code") return { type: "http", url, ...(o.withKey ? { headers: { Authorization: "Bearer ${PERCIA_API_KEY}" } } : {}) };
	if (target === "cursor") return { url, ...(o.withKey ? { headers: { Authorization: "Bearer ${env:PERCIA_API_KEY}" } } : {}) };
	// Claude Desktop only launches local stdio servers: mcp-remote bridges to the remote one.
	const args = ["-y", "mcp-remote", url, ...(o.embedKey ? ["--header", "Authorization:${PERCIA_AUTH}"] : [])];
	return { command: "npx", args, ...(o.embedKey ? { env: { PERCIA_AUTH: `Bearer ${o.embedKey}` } } : {}) };
}

export function configFile(ctx: Context, target: Target, scope: "project" | "user"): string {
	if (target === "claude-code") return join(ctx.cwd, ".mcp.json");
	if (target === "cursor") return scope === "project" ? join(ctx.cwd, ".cursor", "mcp.json") : join(ctx.homedir, ".cursor", "mcp.json");
	if (ctx.platform === "darwin") return join(ctx.homedir, "Library", "Application Support", "Claude", "claude_desktop_config.json");
	if (ctx.platform === "win32") return join(ctx.env.APPDATA ?? join(ctx.homedir, "AppData", "Roaming"), "Claude", "claude_desktop_config.json");
	return join(ctx.env.XDG_CONFIG_HOME ?? join(ctx.homedir, ".config"), "Claude", "claude_desktop_config.json");
}

/** Merge one server into a JSON config without touching anything else. Returns the new text. Throws CliError on unparseable JSON (we never overwrite a file we cannot read). */
export function mergeServer(existing: string | undefined, name: string, entry: Record<string, unknown>, force: boolean): { text: string; changed: boolean; replaced: boolean } {
	let doc: Record<string, any> = {};
	if (existing && existing.trim()) {
		try {
			doc = JSON.parse(existing);
		} catch {
			throw new CliError("The existing config file is not valid JSON; refusing to overwrite it.", EXIT.FAILURE, "Fix it or move it aside, then run again.");
		}
		if (!doc || typeof doc !== "object" || Array.isArray(doc)) throw new CliError("The existing config file is not a JSON object.", EXIT.FAILURE);
	}
	const servers = (doc.mcpServers ??= {});
	const prev = servers[name];
	const same = prev && JSON.stringify(prev) === JSON.stringify(entry);
	if (prev && !same && !force) throw new CliError(`An MCP server named "${name}" already exists with a different setup.`, EXIT.FAILURE, "Pass --force to replace it.");
	servers[name] = entry;
	return { text: JSON.stringify(doc, null, 2) + "\n", changed: !same, replaced: Boolean(prev && !same) };
}

export function registerMcp(program: Command, { ctx, globals }: Deps) {
	const mcp = program.command("mcp").description("Connect AI tools to Percia's MCP server.");
	mcp
		.command("setup <target>")
		.description(`Write the MCP config for ${TARGETS.join(", ")}. No secret is written unless you ask: these clients sign in with OAuth.`)
		.option("--scope <scope>", "project or user (cursor); claude-code writes ./.mcp.json", "project")
		.option("--name <name>", "server name", "percia")
		.option("--url <url>", "MCP endpoint (default: <base>/mcp)")
		.option("--with-key", "authenticate with an API key instead of OAuth: references $PERCIA_API_KEY (Claude Desktop: embeds the stored key in the file)")
		.option("--force", "replace an existing entry with the same name")
		.option("--dry-run", "print what would be written and change nothing")
		.action(async (target: string, o: { scope: string; name: string; url?: string; withKey?: boolean; force?: boolean; dryRun?: boolean }) => {
			const g = globals();
			if (!TARGETS.includes(target as Target)) throw new CliError(`Unknown target "${target}".`, EXIT.USAGE, `Use one of: ${TARGETS.join(", ")}`);
			if (o.scope !== "project" && o.scope !== "user") throw new CliError("--scope must be project or user.", EXIT.USAGE);
			const t = target as Target;
			const cfg = await loadConfig(ctx);
			const url = o.url ?? `${resolveBaseUrl(ctx, g, cfg)}/mcp`;
			let embedKey: string | undefined;
			if (o.withKey && t === "claude-desktop") {
				embedKey = ctx.env.PERCIA_API_KEY ?? (cfg.credentials?.type === "api_key" ? cfg.credentials.apiKey : undefined);
				if (!embedKey) throw new CliError("--with-key for Claude Desktop needs an API key (PERCIA_API_KEY or `percia login --with-key`).", EXIT.USAGE);
			}
			const entry = buildEntry(t, url, { withKey: o.withKey, embedKey });
			const file = configFile(ctx, t, o.scope as "project" | "user");

			let existing: string | undefined;
			try {
				existing = await readFile(file, "utf8");
			} catch (e) {
				if ((e as NodeJS.ErrnoException).code !== "ENOENT") throw e;
			}
			const merged = mergeServer(existing, o.name, entry, Boolean(o.force));
			// The preview never shows a key.
			const preview = embedKey ? merged.text.split(embedKey).join("<your key>") : merged.text;
			if (o.dryRun) return g.json ? json(ctx, { file, dryRun: true, entry: JSON.parse(preview).mcpServers[o.name] }) : void ctx.stdout(`Would write ${file}:\n${preview}`);

			if (merged.changed) {
				await mkdir(dirname(file), { recursive: true });
				if (existing !== undefined) await copyFile(file, `${file}.percia-bak`).catch(() => {});
				const tmp = `${file}.${process.pid}.tmp`;
				await writeFile(tmp, merged.text, { mode: embedKey ? 0o600 : 0o644 });
				if (embedKey) await chmod(tmp, 0o600).catch(() => {});
				await rename(tmp, file);
			}
			const notes: string[] = [];
			if (!o.withKey) notes.push(t === "claude-code" ? "Start Claude Code, run /mcp and choose Authenticate for percia." : t === "cursor" ? "Open Cursor's MCP settings and sign in to percia." : "The first start opens a browser to sign in (mcp-remote). Restart Claude Desktop.");
			else if (embedKey) notes.push("The API key is stored in that file (owner-only). Prefer OAuth if you can.");
			else notes.push("Export PERCIA_API_KEY in the environment your client starts from.");
			if (t === "claude-desktop") notes.push("Claude.ai users can skip this: Settings > Connectors > Add custom connector, URL " + url);
			if (g.json) return json(ctx, { file, changed: merged.changed, replaced: merged.replaced, url, notes });
			ctx.stdout(`${merged.changed ? "Wrote" : "Already configured:"} ${file}\n  server "${o.name}" -> ${url}\n${notes.map((n) => `  ${n}\n`).join("")}`);
		});
}
