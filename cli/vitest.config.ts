import { fileURLToPath } from "node:url";
import { defineConfig } from "vitest/config";

export default defineConfig({
	resolve: { alias: { "@percia/sdk": fileURLToPath(new URL("../typescript/src/index.ts", import.meta.url)) } },
	test: { include: ["test/**/*.test.ts"], environment: "node", testTimeout: 15000 },
});
