// Turn a Percia delivery into a Slack Block Kit message. Pure functions, no network, easy to test.

/** Slack mrkdwn only treats & < > specially; escaping them also defuses <!channel>, <!here> and <https://...|label> injection. */
export const escapeSlack = (text) => String(text ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

const clip = (text, max) => (text.length > max ? `${text.slice(0, max - 1)}…` : text);

/**
 * @param {{ id: string, watchId?: string, goal?: string, reason?: string|null, confidence?: number|null, at?: string, type?: string, imageUrl?: string }} event
 * @param {{ includeImage?: boolean, dashboardUrl?: string }} [options]
 */
export function formatSlackMessage(event, { includeImage = false, dashboardUrl } = {}) {
	const goal = escapeSlack(clip(event.goal ?? "Goal met", 200));
	// `reason` was written by a vision model about camera content: show it as quoted data, escaped and clipped.
	const reason = escapeSlack(clip(String(event.reason ?? "").replace(/\s+/g, " ").trim(), 300));
	const when = event.at && !Number.isNaN(Date.parse(event.at)) ? Math.floor(Date.parse(event.at) / 1000) : null;
	const confidence = typeof event.confidence === "number" ? `${Math.round(event.confidence * 100)}%` : null;
	const test = event.type === "goal.test";

	const blocks = [
		{ type: "header", text: { type: "plain_text", text: test ? "Percia test alert" : "Package alert", emoji: true } },
		{ type: "section", text: { type: "mrkdwn", text: `*${goal}*${reason ? `\n>${reason}` : ""}` } },
		{
			type: "context",
			elements: [
				...(when ? [{ type: "mrkdwn", text: `<!date^${when}^{date_short_pretty} {time}|${escapeSlack(event.at)}>` }] : []),
				...(confidence ? [{ type: "mrkdwn", text: `confidence ${confidence}` }] : []),
				{ type: "mrkdwn", text: `watch \`${escapeSlack(event.watchId ?? "?")}\`` },
			],
		},
	];
	// The keyframe link is a private, non-expiring link: anyone in the channel who sees it can open the image. Opt-in only.
	if (includeImage && typeof event.imageUrl === "string" && event.imageUrl.startsWith("https://")) {
		blocks.push({ type: "image", image_url: event.imageUrl, alt_text: "Keyframe from the camera" });
	}
	if (dashboardUrl) blocks.push({ type: "actions", elements: [{ type: "button", text: { type: "plain_text", text: "Open Percia" }, url: dashboardUrl }] });
	return { text: `${test ? "Test: " : ""}${event.goal ?? "Goal met"}`, blocks };
}
