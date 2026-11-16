import type { GetPlanResponses } from "./generated/types.gen.js";

/** The answer of `GET /api/plan` (`client.account.plan()`). Every billing field is additive: older servers omit some, so read them as optional. */
export type Plan = GetPlanResponses[200] & { cardRequired?: boolean; billingUrl?: string };

/**
 * The `billing` block that MCP `whoami` returns, built from a plan so REST callers read the same words and numbers.
 * Fields a server does not send are `null` (booleans default to the safe value), never invented.
 */
export interface Billing {
	/** "Free" or "Pay as you go". */
	planLabel: string | null;
	/** This month's free camera-minutes left (plus any unused card bonus). */
	freeMinutesRemaining: number | null;
	/** Redeemed or granted camera-minutes left (used before the free minutes). */
	creditMinutes: number | null;
	minutesUsedThisMonth: number | null;
	/** False when billing or a failed payment blocks a new watch now: check this before `watches.create`. */
	canStartWatches: boolean;
	/** One plain sentence on how the account is charged. */
	howCharged: string | null;
	/** What to tell the person when watches cannot start or minutes are gone; null when nothing is needed. */
	nextStep: string | null;
	billingUrl: string | null;
	paymentState: "active" | "grace" | "blocked" | null;
	/** A card subscription is on file. */
	paid: boolean;
	blockReason: "needs_billing" | "spend_cap" | null;
	limitsNote: string | null;
	/** True while adding a card would still grant the one-time bonus. */
	bonusAvailable: boolean;
	bonusMinutes: number | null;
	hasCard: boolean;
	/** When the monthly free minutes come back (ISO 8601). */
	freeMinutesResetsAt: string | null;
}

const num = (v: unknown) => (typeof v === "number" ? v : null);
const str = (v: unknown) => (typeof v === "string" ? v : null);

/** Read the billing facts out of a `GET /api/plan` answer. Pure; accepts older answers that lack the newer fields. */
export function billingOf(plan: Plan): Billing {
	const p = plan as Record<string, unknown>;
	const payment = (p.payment ?? {}) as { state?: unknown; billingUrl?: unknown };
	const state = payment.state === "active" || payment.state === "grace" || payment.state === "blocked" ? payment.state : null;
	const reason = p.blockReason === "needs_billing" || p.blockReason === "spend_cap" ? p.blockReason : null;
	return {
		planLabel: str(p.label),
		freeMinutesRemaining: num(p.freeMinutesLeft),
		creditMinutes: num(p.creditMinutes),
		minutesUsedThisMonth: num(p.minutesUsedThisMonth),
		canStartWatches: p.canStartWatches !== false && state !== "blocked",
		howCharged: str(p.howCharged),
		nextStep: str(p.nextStep),
		billingUrl: str(p.billingUrl) ?? str(payment.billingUrl),
		paymentState: state,
		paid: p.paid === true,
		blockReason: reason,
		limitsNote: str(p.limitsNote),
		bonusAvailable: p.bonusAvailable === true,
		bonusMinutes: num(p.bonusMinutes),
		hasCard: p.hasCard === true || p.paid === true,
		freeMinutesResetsAt: str(p.freeMinutesResetsAt),
	};
}

/** Plain lines for a person: plan, minutes, how charged, next step. The CLI prints these; reuse them in your own tool. */
export function describeBilling(b: Billing): string[] {
	const lines: string[] = [];
	if (b.planLabel) lines.push(`Plan:          ${b.planLabel}${b.hasCard ? " (card on file)" : ""}`);
	if (b.freeMinutesRemaining !== null) lines.push(`Free minutes:  ${b.freeMinutesRemaining} left this month${b.freeMinutesResetsAt ? ` (more on ${b.freeMinutesResetsAt.slice(0, 10)})` : ""}`);
	if (b.creditMinutes !== null) lines.push(`Credit:        ${b.creditMinutes} minutes`);
	if (b.minutesUsedThisMonth !== null) lines.push(`Used:          ${b.minutesUsedThisMonth} minutes this month`);
	lines.push(`New watches:   ${b.canStartWatches ? "can start" : `blocked${b.blockReason ? ` (${b.blockReason})` : b.paymentState === "blocked" ? " (payment failed)" : ""}`}`);
	if (b.howCharged) lines.push(`How charged:   ${b.howCharged}`);
	if (b.bonusAvailable && b.bonusMinutes) lines.push(`Card bonus:    ${b.bonusMinutes} more free minutes once when you add a card`);
	if (b.nextStep) lines.push(`Next step:     ${b.nextStep}`);
	if (b.billingUrl) lines.push(`Billing:       ${b.billingUrl}`);
	return lines;
}

/** One condition of a watch's goal. `kind: "event"` fires when it starts (a car pulls in); `"state"` while it stays true. */
export interface Concern {
	id?: string;
	text: string;
	kind: "state" | "event";
	/** Harmless look-alikes this condition must not fire on. */
	ignore?: string[];
}

/** What Percia understood of a goal (`watch.interpretation`, `watches.interpret`). Null on watches made before goal understanding or with `interpret: false`. Read `gaps`/`untestable` and ask the person. */
export interface Interpretation {
	concerns?: Concern[];
	gaps?: string[];
	untestable?: string[];
	needsLook?: boolean;
	/** Why the understanding is partial: `review_skipped` or another reason; absent when complete. */
	degraded?: string;
	[k: string]: unknown;
}
