import { defineConfig } from "tsup";

export default defineConfig({
	entry: { bin: "src/bin.ts", index: "src/index.ts" },
	format: ["esm"],
	dts: { entry: { index: "src/index.ts" } },
	target: "node20",
	platform: "node",
	clean: true,
	sourcemap: false,
	external: ["@percia/sdk", "commander", "qrcode"],
});
