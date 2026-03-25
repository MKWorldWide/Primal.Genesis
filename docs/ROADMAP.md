# Primal Genesis Engine Roadmap

## Phase Overview

### Phase 0: Classification ✅ COMPLETED
- Repository intelligence audit completed
- All components classified as IMPLEMENTED, PARTIALLY IMPLEMENTED, SCAFFOLDED, BROKEN, DEPRECATED, VISION-ONLY, or UNCLEAR
- Evidence-based classification with confidence levels and recommendations
- Survivors and removal candidates identified

### Phase 1: Pruning ✅ COMPLETED
- Broken components removed (quantum_cli.py, AWS scripts, contaminated tests)
- Ceremonial components archived (ignition_protocol.py, genesis.meta, quantum docs)
- Misleading documentation marked as UNDER_REWRITE
- Working components preserved and validated
- Archive structure created and populated

### Phase 2: Skeleton Creation ✅ IN PROGRESS
- New repository structure created (apps/, packages/, docs/)
- Python package skeleton established (packages/primal_genesis/)
- Architecture spine documents created (CURRENT_STATE.md, VISION.md, ROADMAP.md)
- Placeholder files and README stubs created
- Migration map prepared

### Phase 3: Migration (NEXT)
- Move survivors into new structure
- Update imports and references
- Reconnect disconnected components
- Validate new structure works

### Phase 4: Test Rebuild
- Rebuild test suite from scratch
- Test Python package structure
- Test React components integration
- Test Node.js tooling

### Phase 5: First Real Module
- Implement Config/Registry/Module Manifest Core
- Establish module management system
- Create first working end-to-end flow

## Detailed Phase Plans

### Phase 3: Migration Details

#### Python Core Migration
- `config.py` → `packages/primal_genesis/core/config.py`
- `setup.py` integration with new package structure
- Update `pyproject.toml` for new package layout
- Create base classes and utilities

#### Frontend Migration
- `src/components/*` → `apps/console/src/components/*`
- `src/providers/*` → `apps/console/src/providers/*`
- `src/hooks/*` → `apps/console/src/hooks/*`
- `src/types/*` → `apps/console/src/types/*`
- Create React/Next.js app structure

#### Tooling Migration
- `override_core/` → `apps/override-core/`
- `pge/` → `apps/pge-runner/`
- Update package.json and dependencies
- Create proper TypeScript builds

#### Scaffold Preservation
- `src/athena/` → `packages/primal_genesis/integrations/athena/` (future)
- `src/agents/PGES.ts` → `apps/console/src/agents/PGES.ts` (future)

### Phase 4: Test Rebuild Details

#### Python Tests
- Create `tests/test_core.py` for configuration management
- Create `tests/test_api.py` for future API endpoints
- Create `tests/test_integrations.py` for integration boundaries
- Update pytest configuration for new package structure

#### Frontend Tests
- Create React component tests
- Create integration tests for providers and hooks
- Set up Jest/React Testing Library

#### Tooling Tests
- Create Node.js application tests
- Create PGE runner tests
- Test override-core functionality

### Phase 5: First Module Details

#### Config/Registry Core
- Module discovery and registration
- Configuration validation and management
- Policy enforcement framework
- Module lifecycle management

#### API Foundation
- Basic FastAPI application
- Configuration endpoints
- Module management endpoints
- Health check and monitoring

#### Console Integration
- Connect React app to Python API
- Module management interface
- Configuration management UI
- System monitoring dashboard

## Success Criteria

### Phase 3 Success
- All survivors moved to new structure
- No broken imports or references
- Applications can start and run
- Git history preserved

### Phase 4 Success
- All tests pass
- Coverage meets quality standards
- CI/CD pipeline works
- Documentation is accurate

### Phase 5 Success
- End-to-end functionality works
- Module system operates
- Configuration management complete
- Ready for first external module

## Timeline Estimates

- **Phase 3**: 2-3 days (migration and reconnection)
- **Phase 4**: 2-3 days (test rebuild and validation)
- **Phase 5**: 3-5 days (first real module implementation)
- **Total to MVP**: 7-11 days

## Risk Mitigation

### Technical Risks
- **Import Breakage**: Careful migration with validation at each step
- **Dependency Conflicts**: Resolve during migration, test thoroughly
- **Build Failures**: Set up CI/CD early to catch issues

### Architectural Risks
- **Over-Engineering**: Keep initial implementation simple
- **Wrong Abstractions**: Focus on concrete problems first
- **Performance Issues**: Profile and optimize after functionality works

### Project Risks
- **Scope Creep**: Stick to defined phases
- **Perfectionism**: Good enough is better than perfect
- **Burnout**: Regular commits, small incremental changes

## Next Steps

1. **Complete Phase 2**: Finish skeleton creation and documentation
2. **Begin Phase 3**: Start with Python core migration
3. **Validate Early**: Test each migration step immediately
4. **Iterate Quickly**: Small, frequent commits with clear messages
5. **Maintain Vision**: Keep humanity-first principles in all decisions

This roadmap provides a clear path from the current cleaned repository to a functional, modular system that embodies the Primal Genesis Engine vision.
