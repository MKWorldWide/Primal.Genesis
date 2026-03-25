# Primal Genesis Python Package

Python core package for the Primal Genesis Engine.

## Purpose

Provides the core Python functionality including:
- Configuration management
- API endpoints and services
- Protocol implementations
- Integration boundaries
- Governance systems
- CLI tools

## Package Structure

```
packages/primal_genesis/
├── core/          # Configuration, utilities, base services
├── api/            # REST API, WebSocket handlers, authentication
├── protocols/      # Communication protocols and data formats
├── integrations/   # External service adapters (future Athena boundary)
├── governance/     # Policy management, decision frameworks
└── cli/            # Command-line tools and administration
```

## Current State

**Phase 2: Skeleton Created**

Package structure and placeholder files created. Ready for implementation migration from root-level files.

## Migration Plan

Core components will be migrated from repository root:
- `config.py` → `packages/primal_genesis/core/config.py`
- New API implementation in `packages/primal_genesis/api/`
- Protocol definitions in `packages/primal_genesis/protocols/`
- Integration boundaries in `packages/primal_genesis/integrations/`

## Future Implementation

- FastAPI-based web services
- Configuration and policy management
- Module registry and discovery
- CLI tools for system administration
- Integration boundaries for external services
