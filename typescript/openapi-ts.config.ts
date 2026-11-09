import { defineConfig } from "@hey-api/openapi-ts";

// Generates typed operations from the pinned OpenAPI document (../spec/openapi.json).
// Output is committed (src/generated) so reviews show API changes and the npm build needs no network.
export default defineConfig({
	input: "../spec/openapi.json",
	output: { path: "src/generated", clean: true },
	plugins: ["@hey-api/typescript", { name: "@hey-api/sdk", operations: { strategy: "flat" } }, "@hey-api/client-fetch"],
});
