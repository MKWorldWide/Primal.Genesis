// Simple execution script to showcase PGE transformations.
// Uses sample inputs to exercise override rules.

import { runPGE } from "./pge";
import rules from "./override_rules.json";

// Example inputs you can test
const samples = [
  { kind: "intimidation_bark", level: 5, source: "luna" },
  { kind: "psyop", level: 8, campaign: "panic-seed" },
  { kind: "surveillance", level: 6, grid: "citymesh" }
];

for (const s of samples) {
  const out = runPGE(s as any, rules as any);
  console.log("\nINPUT:", s);
  console.log("OUTPUT:", JSON.stringify(out, null, 2));
}
