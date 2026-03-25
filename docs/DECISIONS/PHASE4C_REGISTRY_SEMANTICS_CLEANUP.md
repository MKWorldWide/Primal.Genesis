# Phase 4C Registry Semantics Cleanup

*Completed: Phase 4C of Primal Genesis Engine rebuild*

## Overview

Successfully cleaned up and standardized the semantics of the module registry without expanding the schema unnecessarily. This semantics-cleanup phase made the registry records and documentation more internally consistent, particularly around the meaning of the `entrypoint` field.

## Semantic Inconsistency Found

### Problem: Mixed Entrypoint Meanings
The current `entrypoint` field was mixing different semantics:

**Before Cleanup**:
- `packages.primal_genesis` - Mixed package-style and import-style
- `packages.athena` - Mixed package-style and import-style  
- `apps/console/src` - Repo-relative path (correct)
- `apps/override-core/index.js` - Repo-relative path (correct)
- `apps/pge-runner/pge.ts` - Repo-relative path (correct)

**Issues**:
- Python packages used internal package paths instead of public import identity
- Inconsistent between Python and JS/TS module types
- Confusing documentation about what `entrypoint` actually means

## Standardization Rule Adopted

### Entrypoint Field Definition
Standardized `entrypoint` with this clear rule:

- **For Python packages**: Use the intended public import identity
  - `primal_genesis` (not `packages.primal_genesis`)
  - `athena` (not `packages.athena`)

- **For JS/TS apps/tools**: Use repo-relative executable or primary runtime path
  - `apps/override-core/index.js`
  - `apps/pge-runner/pge.ts`
  - `apps/console/src`

### Rationale
- **Clear distinction**: Different module types have different entrypoint conventions
- **Public identity**: Python packages use their public import names
- **Executable paths**: JS/TS tools use their actual executable files
- **No schema expansion**: Clarified meaning without adding new fields

## Seeded Module Values Changed

### Updated Python Package Entrypoints
**primal_genesis**:
- Before: `packages.primal_genesis`
- After: `primal_genesis` (public import identity)

**athena**:
- Before: `packages.athena`
- After: `athena` (public import identity)

### Preserved JS/TS Entrypoints
**console**: `apps/console/src` (unchanged - already correct)

**override-core**: `apps/override-core/index.js` (unchanged - already correct)

**pge-runner**: `apps/pge-runner/pge.ts` (unchanged - already correct)

## Files Updated

### Core Registry Module
**`packages/primal_genesis/core/registry.py`**:
- Updated seeded module `entrypoint` values
- Added inline comments explaining semantics
- Preserved all other functionality

### Documentation
**`packages/primal_genesis/README.md`**:
- Added entrypoint example in usage code
- Added clear semantics documentation section
- Updated example to show entrypoint usage

### Persisted Registry Data
**`packages/data/registry.json`**:
- Regenerated with updated semantics
- No duplicate registry files created
- Canonical storage location preserved

## Validation Results

### Registry Functionality
```bash
✅ Registry with updated semantics:
  - primal_genesis: entrypoint="primal_genesis" (core)
  - console: entrypoint="apps/console/src" (frontend)
  - override-core: entrypoint="apps/override-core/index.js" (tooling)
  - pge-runner: entrypoint="apps/pge-runner/pge.ts" (tooling)
  - athena: entrypoint="athena" (intelligence)
```

### Consistency Verification
- ✅ Python packages use public import identity
- ✅ JS/TS apps use repo-relative executable paths
- ✅ No mixed semantics between module types
- ✅ Documentation matches implementation

### Storage Location Preserved
- ✅ Canonical registry file: `packages/data/registry.json`
- ✅ No duplicate registry files created
- ✅ Deterministic storage path maintained

## Intentionally Deferred

### No Schema Expansion
- **No new fields added**: Clarified existing `entrypoint` field
- **No redesign**: Kept simple dataclass structure
- **No complexity increase**: Maintained minimal design

### Future Enhancements
- **Module validation**: Could add entrypoint validation later
- **Type-specific handling**: Could add module type-specific logic
- **Auto-discovery**: Could add automatic entrypoint detection
- **Dependency resolution**: Could add dependency graph support

## Technical Notes

### Semantics Documentation
```python
# Added inline comments for clarity
entrypoint="primal_genesis"  # Public import identity
entrypoint="apps/console/src"  # Repo-relative primary runtime path
entrypoint="apps/override-core/index.js"  # Repo-relative executable
```

### Registry Regeneration
- **Old registry file removed**: `packages/data/registry.json` deleted
- **New registry generated**: With updated semantics on first run
- **Clean transition**: No corruption or data loss

### Documentation Clarity
```markdown
**Entrypoint Semantics**:
- **Python packages**: Use public import identity (`primal_genesis`, `athena`)
- **JS/TS apps**: Use repo-relative executable path (`apps/console/src`, `apps/override-core/index.js`)
```

## Success Criteria Met

- ✅ **Semantic inconsistency resolved**: Clear entrypoint definition established
- ✅ **Standardized rule implemented**: Consistent across all module types
- ✅ **Seeded values updated**: Python packages use public import identity
- ✅ **Registry data updated**: Persisted data matches new semantics
- ✅ **Documentation clarified**: Entry point meaning explained
- ✅ **No schema expansion**: Simple design preserved
- ✅ **No duplicate files**: Clean registry file management

## Conclusion

Phase 4C successfully straightened the labels on the control panel so every switch means what it says. The registry now has consistent, clear semantics for the `entrypoint` field across all module types without expanding the schema or adding unnecessary complexity.

The cleanup provides a solid foundation for future development while maintaining the small, simple, honest design established in previous phases. The registry now teaches and uses consistent patterns for different module types, making it more predictable and easier to understand.
