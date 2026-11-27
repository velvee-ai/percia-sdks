import { Command, CommanderError } from "commander";
import { registerAuth } from "./commands/auth.js";
import { registerCameras } from "./commands/cameras.js";
import { registerCompletion } from "./commands/completion.js";
import { registerDestinations } from "./commands/destinations.js";
import { registerDoctor } from "./commands/doctor.js";
import { registerEvents } from "./commands/events.js";
import { registerHooks } from "./commands/hooks.js";
import { registerListen } from "./commands/listen.js";
import { registerMcp } from "./commands/mcp.js";
import { registerPlan } from "./commands/plan.js";
import { registerWatches } from "./commands/watches.js";
import type { Context, GlobalOptions } from "./context.js";
import { describeError, exitCodeFor, EXIT } from "./errors.js";

export const VERSION = "0.3.1";

export function buildProgram(ctx: Context): Command {
	const program = new Command("percia")
		.description("Percia command line: watch cameras, read events, connect alert destinations.")
		.version(VERSION, "-v, --version")
		.option("--json", "machine-readable output (NDJSON for follow/listen); errors as JSON on stderr")
		.option("--base-url <url>", "Percia host (default: PERCIA_BASE_URL, the saved value, or https://playground.percia.ai)")
		.option("-q, --quiet", "less output")
		.showHelpAfterError("(add --help for usage)")
		.exitOverride()
		.configureOutput({ writeOut: (s) => ctx.stdout(s), writeErr: (s) => ctx.stderr(s) });
	const globals = (): GlobalOptions => program.opts();
	const deps = { ctx, globals };
	registerAuth(program, deps);
	registerPlan(program, deps);
	registerWatches(program, deps);
	registerEvents(program, deps);
	registerCameras(program, deps);
	registerDestinations(program, deps);
	registerHooks(program, deps);
	registerListen(program, deps);
	registerMcp(program, deps);
	registerDoctor(program, deps);
	registerCompletion(program, ctx);
	// Subcommands inherit exitOverride/output so help and usage errors reach `run` instead of exiting the process.
	const inherit = (c: Command) => c.commands.forEach((s) => (s.exitOverride().configureOutput({ writeOut: (t) => ctx.stdout(t), writeErr: (t) => ctx.stderr(t) }), inherit(s)));
	inherit(program);
	return program;
}

/** Run the CLI and return the exit code. Never calls process.exit, so tests can drive it. */
export async function run(argv: string[], ctx: Context): Promise<number> {
	const program = buildProgram(ctx);
	try {
		await program.parseAsync(argv, { from: "user" });
		return EXIT.OK;
	} catch (e) {
		if (e instanceof CommanderError) {
			if (e.code === "commander.helpDisplayed" || e.code === "commander.version" || e.code === "commander.help") return EXIT.OK;
			return EXIT.USAGE;
		}
		const wantsJson = argv.includes("--json");
		const { message, hint, details } = describeError(e);
		if (wantsJson) ctx.stderr(JSON.stringify({ error: { message, hint, ...details } }) + "\n");
		else ctx.stderr(`Error: ${message}${details.request_id ? ` (request ${details.request_id})` : ""}\n${hint ? `${hint}\n` : ""}`);
		return exitCodeFor(e);
	}
}
