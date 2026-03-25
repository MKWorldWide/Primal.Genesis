# Phase 2 Migration Map

This document maps current survivors to their future homes in the new repository structure.

## Python Core Migration

### Root Level → packages/primal_genesis/core/

| Current Location | Target Location | Notes |
|------------------|-----------------|-------|
| `config.py` | `packages/primal_genesis/core/config.py` | Core configuration management |
| `setup.py` | Root (update for new package structure) | Update package references |
| `pyproject.toml` | Root (update for new package structure) | Update package name and structure |
| `requirements.txt` | Root (update for new package structure) | May need package-specific requirements |

### New Python Modules (to be implemented)

| Target Location | Purpose | Implementation Status |
|-----------------|---------|---------------------|
| `packages/primal_genesis/core/base.py` | Base classes and interfaces | Placeholder created |
| `packages/primal_genesis/api/app.py` | FastAPI application | Placeholder created |
| `packages/primal_genesis/api/routes.py` | API routes | Placeholder created |
| `packages/primal_genesis/protocols/base.py` | Protocol base classes | Placeholder created |
| `packages/primal_genesis/protocols/messaging.py` | Message protocols | Placeholder created |
| `packages/primal_genesis/integrations/base.py` | Integration base classes | Placeholder created |
| `packages/primal_genesis/integrations/registry.py` | Integration registry | Placeholder created |
| `packages/primal_genesis/governance/policy.py` | Policy management | Placeholder created |
| `packages/primal_genesis/governance/registry.py` | Module registry | Placeholder created |
| `packages/primal_genesis/cli/main.py` | CLI entry point | Placeholder created |
| `packages/primal_genesis/cli/commands.py` | CLI commands | Placeholder created |

## Frontend Migration

### src/ → apps/console/src/

| Current Location | Target Location | Notes |
|------------------|-----------------|-------|
| `src/components/chat/` | `apps/console/src/components/chat/` | Chat interface |
| `src/components/analytics/` | `apps/console/src/components/analytics/` | Analytics dashboard |
| `src/providers/VoiceProvider.tsx` | `apps/console/src/providers/VoiceProvider.tsx` | Voice context provider |
| `src/providers/README.md` | `apps/console/src/providers/README.md` | Provider documentation |
| `src/hooks/useVoice.ts` | `apps/console/src/hooks/useVoice.ts` | Voice recording hooks |
| `src/hooks/useSelfUpgrade.ts` | `apps/console/src/hooks/useSelfUpgrade.ts` | Self-upgrade hooks |
| `src/hooks/README.md` | `apps/console/src/hooks/README.md` | Hooks documentation |
| `src/types/README.md` | `apps/console/src/types/README.md` | Type documentation |

### New Console Structure (to be implemented)

| Target Location | Purpose | Implementation Status |
|-----------------|---------|---------------------|
| `apps/console/next.config.js` | Next.js configuration | To be created |
| `apps/console/package.json` | Console app dependencies | To be created |
| `apps/console/tsconfig.json` | TypeScript configuration | To be created |
| `apps/console/pages/` | Next.js pages | To be created |
| `apps/console/styles/` | CSS/styling | To be created |

## Tooling Migration

### Existing Tools → apps/

| Current Location | Target Location | Notes |
|------------------|-----------------|-------|
| `override_core/` | `apps/override-core/` | Development override system |
| `pge/` | `apps/pge-runner/` | Policy engine runner |

### Tooling Updates Needed

| Current File | Target Location | Updates Required |
|--------------|-----------------|-----------------|
| `override_core/package.json` | `apps/override-core/package.json` | Update dependencies, build scripts |
| `pge/package.json` | `apps/pge-runner/package.json` | Add TypeScript build, update dependencies |
| `pge/tsconfig.json` | `apps/pge-runner/tsconfig.json` | Update for new structure |

## Scaffold Preservation

### Future Integration Boundaries

| Current Location | Target Location | Purpose |
|------------------|-----------------|---------|
| `src/athena/` | `packages/primal_genesis/integrations/athena/` | Future Athena intelligence layer |
| `src/agents/PGES.ts` | `apps/console/src/agents/PGES.ts` | Agent system foundation |

### Scaffold Implementation Plan

| Component | Current State | Future Implementation |
|----------|---------------|---------------------|
| Athena Integration | Minimal `signal.js` placeholder | Full intelligence layer integration |
| Agent System | Single `PGES.ts` file | Multi-agent system with console integration |

## Documentation Migration

### Current Documentation

| Current Location | Target Location | Action |
|------------------|-----------------|--------|
| `docs/CURRENT_STATE.md` | `docs/CURRENT_STATE.md` | Keep (newly created) |
| `docs/VISION.md` | `docs/VISION.md` | Keep (newly created) |
| `docs/ROADMAP.md` | `docs/ROADMAP.md` | Keep (newly created) |
| `docs/API.md` | `docs/API.md` | Update during Phase 3 |
| `docs/DEVELOPER_GUIDE.md` | `docs/DEVELOPER_GUIDE.md` | Update during Phase 3 |
| `docs/ARCHITECTURE.md` | `docs/ARCHITECTURE.md` | Update during Phase 3 |

### New Documentation Structure

| Target Location | Purpose | Status |
|-----------------|---------|--------|
| `docs/DECISIONS/` | Architecture decisions and migration maps | Created |
| `docs/DECISIONS/PHASE2_MIGRATION_MAP.md` | This migration map | Created |

## Configuration Updates

### Package Configuration

| File | Updates Required |
|------|------------------|
| `pyproject.toml` | Update package structure, dependencies |
| `Makefile` | Update package references to `primal_genesis` |
| `pytest.ini` | Update test paths for new structure |
| `requirements-test.txt` | Update for new package structure |

### Import Updates

| Component | Current Imports | Future Imports |
|-----------|-----------------|----------------|
| React components | Relative imports from `src/` | Relative imports from `apps/console/src/` |
| Python modules | Root-level imports | Package imports from `primal_genesis.*` |
| Tooling | Local references | Cross-app references |

## Migration Priority

### High Priority (Phase 3.1)
1. Python core (`config.py` → `packages/primal_genesis/core/`)
2. Package structure setup
3. Basic imports and configuration

### Medium Priority (Phase 3.2)
1. Frontend migration (`src/` → `apps/console/`)
2. Tooling migration (`override_core/`, `pge/` → `apps/`)
3. Documentation updates

### Low Priority (Phase 3.3)
1. Scaffold enhancement (Athena, agents)
2. Advanced configuration
3. Integration testing

## Validation Checklist

### Post-Migration Validation
- [ ] All Python imports work with new package structure
- [ ] React components can be imported in console app
- [ ] Node.js applications start correctly
- [ ] TypeScript compilation works
- [ ] Tests can find and run against new structure
- [ ] Documentation references are accurate
- [ ] Git history is preserved

### Integration Testing
- [ ] Console app can communicate with Python API
- [ ] Policy engine can interface with core systems
- [ ] Override system works with new structure
- [ ] End-to-end workflows function

This migration map provides a clear path for moving all surviving components into their new homes while preserving functionality and preparing for future integration.
