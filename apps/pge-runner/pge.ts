// Primal Genesis Engine core runtime
// Provides a minimalist policy engine to process inputs through watcher actions.
// Each watcher primitive is a stubbed function allowing future expansion or integration.

type WatcherCall = (payload: any, args?: any) => any;

interface Registry {
  [key: string]: WatcherCall;
}

// --- Watcher primitives (stubs you can flesh out) ---
const registry: Registry = {
  "black-sun-core.absorb": (p, a) => ({ ...p, fuel: (p.fuel ?? 0) + (a?.intensity_from ?? 1) }),
  "serpentine.transmute": (p, a) => ({ ...p, state: `${a?.to}`, from: a?.from }),
  "lunar-mirror.scrub": (p, a) => ({ ...p, removed: a?.strip ?? [] }),
  "echo.normalize": (p, a) => ({ ...p, resonance: a?.target_resonance ?? 432 }),
  "solar.assert": (p, a) => ({ ...p, sovereign_assertion: a?.mantra }),
  "crown.route": (p, a) => ({ ...p, routed_to: a?.to }),

  "abyssal.ground": (p, a) => ({ ...p, grounded: true, depth: a?.depth ?? "auto" }),
  "flame.allocate": (p, a) => ({ ...p, allocation: { to: a?.to, percent: a?.percent ?? 33 } }),
  "martial.posture": (p, a) => ({ ...p, posture: a?.mode ?? "calm-dominance" }),

  "shadow.firewall": (p, a) => ({ ...p, dropped: (p.dropped ?? []).concat("falsehood") }),
  "lunar-mirror.reflect": (p, a) => ({ ...p, reflected: a?.only ?? ["verifiable"] }),
  "memory.log": (p, a) => ({ ...p, audit: true }),

  "crown.rewrite": (p, a) => ({ ...p, charter_principle: a?.principle }),
  "oceanic.balance": (p, a) => ({ ...p, cohesion_target: a?.cohesion_target ?? 0.73 }),
  "temporal.schedule": (p, a) => ({ ...p, review: a?.cadence ?? "weekly" })
};

// --- Policy engine ---
type Rule = {
  match: { "input.kind": string[] };
  actions: { use: string; args?: any }[];
  output: string;
};

export function runPGE(input: { kind: string; level?: number; [k: string]: any }, rules: Record<string, Rule>) {
  const applicable = Object.values(rules).filter(r => r.match["input.kind"].includes(input.kind));
  const results = [] as any[];
  for (const rule of applicable) {
    let payload: any = { input };
    for (const step of rule.actions) {
      const fn = registry[step.use];
      if (!fn) throw new Error(`Missing watcher fn: ${step.use}`);
      payload = fn(payload, step.args);
    }
    results.push({ type: rule.output, payload });
  }
  return results;
}

export default runPGE;
