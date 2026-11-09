export type Page<T> = { events?: T[]; nextCursor?: string | null };

/**
 * Follow `nextCursor` until it is null. Lazy: a page is fetched only when the loop needs the next item,
 * so `for await (...) { break }` costs one request. `maxPages` is a safety bound for runaway loops (default: none).
 */
export async function* paginate<T>(fetchPage: (cursor: string | undefined) => Promise<Page<T>>, options: { maxPages?: number } = {}): AsyncGenerator<T, void, void> {
	let cursor: string | undefined;
	for (let pages = 0; !options.maxPages || pages < options.maxPages; pages++) {
		const page = await fetchPage(cursor);
		for (const item of page.events ?? []) yield item;
		if (!page.nextCursor || page.nextCursor === cursor) return;
		cursor = page.nextCursor;
	}
}

/** Collect an async iterator into an array (bounded by `limit` items when given). */
export async function toArray<T>(it: AsyncIterable<T>, limit = Infinity): Promise<T[]> {
	const out: T[] = [];
	if (limit <= 0) return out;
	for await (const x of it) {
		out.push(x);
		if (out.length >= limit) break;
	}
	return out;
}
