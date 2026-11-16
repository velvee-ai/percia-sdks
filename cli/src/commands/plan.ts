import { Command } from "commander";
import { billingOf, describeBilling, type Plan } from "@percia/sdk";
import type { Context, GlobalOptions } from "../context.js";
import { json } from "../output.js";
import { openSession } from "../session.js";

type Deps = { ctx: Context; globals: () => GlobalOptions };

export function registerPlan(program: Command, { ctx, globals }: Deps) {
	program
		.command("plan")
		.alias("billing")
		.description("Show your plan: free minutes left this month, credit minutes, how you are charged, and what to do next.")
		.action(async () => {
			const g = globals();
			const plan = (await (await openSession(ctx, g)).client.account.plan()) as Plan;
			const billing = billingOf(plan);
			if (g.json) return json(ctx, { ...plan, billing });
			ctx.stdout(describeBilling(billing).join("\n") + "\n");
		});
}
