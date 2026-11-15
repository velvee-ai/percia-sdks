// Test helper: resolve "@percia/sdk" to the built workspace copy (typescript/dist) so the example runs offline without npm.
import { register } from "node:module";
register("data:text/javascript," + encodeURIComponent(`
export async function resolve(specifier, context, next) {
	if (specifier === "@percia/sdk") return { url: ${JSON.stringify(new URL("../../../../typescript/dist/index.js", import.meta.url).href)}, shortCircuit: true };
	return next(specifier, context);
}`));
