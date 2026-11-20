// The World — 20 November 2026.
// Writes the entry image (entry.png, next to this file) to
// $MAKEFUN_OUTPUT_DIR/entry.png (default /output). Node 22, stdlib only.
// The image is validated first (PNG signature, size, IHDR dimensions)
// and written atomically (temp file + rename), so a failed run never
// leaves a truncated entry.png behind. Running twice writes identical bytes.
import { mkdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const MAX_BYTES = 1048576; // 1 MiB
const MAX_DIMENSION = 1024;

const src = join(import.meta.dirname, "entry.png");
const bytes = readFileSync(src);

if (bytes.length < 33 || !bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error("entry.png is not a PNG file");
}
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
// IHDR is the first chunk: 4-byte length, "IHDR", then width/height (BE u32).
if (bytes.toString("latin1", 12, 16) !== "IHDR") {
  throw new Error("entry.png has no IHDR chunk");
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width === 0 || height === 0 || width > MAX_DIMENSION || height > MAX_DIMENSION) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, "entry.png");
const tmpPath = join(outDir, `.entry.png.tmp-${process.pid}`);
writeFileSync(tmpPath, bytes);
renameSync(tmpPath, outPath);
