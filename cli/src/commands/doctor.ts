import { Command } from "commander";
import { PerciaApiError, PerciaError } from "@percia/sdk";
import { stat } from "node:fs/promises";
import { configPath, loadConfig } from "../config.js";
import type { Context, GlobalOptions } from "../context.js";
import { CliError, EXIT } from "../errors.js";
import { discover } from "../oauth.js";
import { json } from "../output.js";
import { openSession, resolveBaseUrl } from "../session.js";
import { probeScopes } from "./auth.js";

type Deps = { ctx: Context; globals: () => GlobalOptions };
type Check = { name: string; status: "ok" | "warn" | "fail"; detail: string };

export function registerDoctor(program: Command, { ctx, globals }: Deps) {
	program
		.command("doctor")
		.description("Check the setup: Node version, config permissions, connectivity, clock, sign-in and permissions. Exits 1 when something fails.")
		.action(async () => {
			const g = globals();
			const checks: Check[] = [];
			const add = (name: string, status: Check["status"], detail: string) => checks.push({ name, status, detail });

			const major = Number(process.versions.node.split(".")[0]);
			add("node", major >= 20 ? "ok" : "fail", `Node ${process.versions.node} ${major >= 20 ? "" : "(need 20 or newer)"}`.trim());

			const cfg = await loadConfig(ctx).catch((e) => {
				add("config", "fail", (e as Error).message);
				return undefined;
			});
			const file = configPath(ctx);
			if (cfg) {
				try {
					const st = await stat(file);
					const mode = st.mode & 0o777;
					const open = ctx.platform !== "win32" && (mode & 0o077) !== 0;
					add("config file", open ? "warn" : "ok", open ? `${file} is readable by others (mode ${mode.toString(8)}); run: chmod 600 "${file}"` : `${file} (mode ${mode.toString(8)})`);
				} catch {
					add("config file", "ok", `none yet (${file})`);
				}
			}

			const baseUrl = resolveBaseUrl(ctx, g, cfg ?? { version: 1 });
			add("base url", /^https:\/\//.test(baseUrl) || /^http:\/\/(localhost|127\.0\.0\.1)/.test(baseUrl) ? "ok" : "warn", baseUrl);

			let reachable = false;
			try {
				const t0 = ctx.now();
				const res = await ctx.fetch(`${baseUrl}/api/health`, { signal: AbortSignal.timeout(10_000) });
				reachable = res.ok;
				add("api reachable", res.ok ? "ok" : "fail", `GET /api/health -> ${res.status} in ${ctx.now() - t0} ms`);
				const date = res.headers.get("date");
				if (date) {
					const skew = Math.abs(Date.parse(date) - ctx.now()) / 1000;
					add("clock", skew > 300 ? "fail" : skew > 60 ? "warn" : "ok", `${skew.toFixed(0)} s from the server clock${skew > 300 ? " (webhook signatures use a 300 s window; fix your system time)" : ""}`);
				}
				const conf: any = await (await ctx.fetch(`${baseUrl}/api/config`, { signal: AbortSignal.timeout(10_000) })).json().catch(() => undefined);
				if (conf) add("features", "ok", `phone cameras ${conf.phoneCameraEnabled ? "on" : "off"}, integrations ${conf.integrationsEnabled ? "on" : "off"}`);
			} catch (e) {
				add("api reachable", "fail", `${(e as Error).message}`);
			}

			if (reachable) {
				try {
					const meta = await discover(ctx, baseUrl);
					add("oauth", "ok", `issuer metadata found (${new URL(meta.token_endpoint).origin})`);
				} catch (e) {
					add("oauth", "warn", (e as Error).message);
				}
			}

			if (!cfg?.credentials && !ctx.env.PERCIA_API_KEY) add("credentials", "fail", "none. Run `percia login` or set PERCIA_API_KEY");
			else {
				add("credentials", "ok", ctx.env.PERCIA_API_KEY ? "PERCIA_API_KEY" : cfg!.credentials!.type === "api_key" ? "stored API key" : "stored OAuth session");
				if (cfg?.credentials?.type === "oauth" && !ctx.env.PERCIA_API_KEY && cfg.credentials.expiresAt && cfg.credentials.expiresAt < ctx.now()) add("token", cfg.credentials.refreshToken ? "warn" : "fail", cfg.credentials.refreshToken ? "access token expired; it refreshes on next use" : "access token expired and no refresh token: run `percia login`");
				if (reachable) {
					try {
						const s = await openSession(ctx, g);
						const probes = await probeScopes(s.client);
						add("sign-in works", "ok", "the API accepted the credential");
						const missing = probes.filter((p) => p.granted === false).map((p) => p.scope);
						add("permissions", missing.length ? "warn" : "ok", missing.length ? `no access to: ${missing.join(", ")}` : "all read checks pass");
					} catch (e) {
						add("sign-in works", "fail", e instanceof PerciaApiError ? `${e.status} ${e.code ?? ""} ${e.requestId ? `(request ${e.requestId})` : ""}`.trim() : e instanceof PerciaError || e instanceof CliError ? e.message : String(e));
					}
				}
			}

			const failed = checks.some((c) => c.status === "fail");
			if (g.json) {
				json(ctx, { ok: !failed, checks });
			} else {
				for (const c of checks) ctx.stdout(`${c.status === "ok" ? "ok  " : c.status === "warn" ? "warn" : "FAIL"}  ${c.name.padEnd(15)} ${c.detail}\n`);
				ctx.stdout(failed ? "\nSome checks failed.\n" : "\nAll good.\n");
			}
			if (failed) throw new CliError("doctor found problems", EXIT.FAILURE);
		});
}
