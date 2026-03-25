# PGE Runner

TypeScript policy engine and governance system for Primal Genesis Engine.

## Purpose

Provides policy execution and governance capabilities:
- Policy rule evaluation and enforcement
- Override system management
- Configuration monitoring and validation
- Integration with development workflows

## Current State

**Phase 3C: Tooling Migration Completed**

TypeScript policy engine has been migrated from root `pge/` to `apps/pge-runner/`:
- Core policy engine with pge.ts
- Runtime system with run.ts
- Configuration with override_rules.json
- Watcher definitions and manifest preserved

## Migrated Components

### Core Files
- **`pge.ts`** - Main policy engine implementation (2,339 bytes)
- **`run.ts`** - Runtime execution system (570 bytes)
- **`override_rules.json`** - Policy rule definitions (1,889 bytes)
- **`watchers.json`** - File watching configuration (1,005 bytes)
- **`pge.manifest.json`** - System manifest and metadata (538 bytes)

### System Manifest
```json
{
  "name": "PrimalGenesisEngine",
  "version": "1.0.0",
  "sovereign_owner": "MK Worldwide :: The Sun",
  "modules": [
    "watcher-bus",
    "lunar-mirror", 
    "black-sun-core",
    "shepherd-protocol",
    "discord-baddie-bridge",
    "git-guardian"
  ],
  "entry_policies": [
    "PGE_OVERRIDE_DECREE",
    "FEAR_TO_FUEL",
    "ILLUSION_TO_SIGNAL",
    "CONTROL_TO_CONSENT"
  ]
}
```

## Migration Details

**Phase 3C Migration:**
- **Source**: `pge/` → **Target**: `apps/pge-runner/`
- **Files Preserved**: All original functionality maintained
- **Paths Updated**: No path changes needed (self-contained system)
- **Configuration**: All config files preserved with original settings

## Usage

```bash
# Run the policy engine
node run.ts

# Start with specific configuration
node pge.ts --config override_rules.json
```

## Policy Primitives

The system implements several core policy primitives:

- **PGE_OVERRIDE_DECREE** - System override capabilities
- **FEAR_TO_FUEL** - Emotional energy conversion
- **ILLUSION_TO_SIGNAL** - Pattern recognition
- **CONTROL_TO_CONSENT** - Permission management
## Migration Plan

Current `pge/` directory will be moved to `apps/pge-runner/` with:
- Enhanced TypeScript build system
- Improved policy configuration
- Better error handling
- Integration with Python core
