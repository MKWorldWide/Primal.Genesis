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

## Quick Start

### Configuration Management

```python
# Import the configuration system
from packages.primal_genesis import Config
# Or alternatively:
from packages.primal_genesis.core import Config

# Create a configuration instance
config = Config()

# Get configuration values
debug_mode = config.get("debug", False)
api_port = config.get("api_port", 8000)

# Set configuration values
config.set("debug", True)
config.save()
```

### Advanced Configuration

```python
# Custom config file location
config = Config("my_custom_config.json")

# Environment variable support
# The system will automatically check for PRIMAL_GENESIS_* env vars
# For example: PRIMAL_GENESIS_API_PORT=8080

# Default configuration structure
default_config = {
    "debug": False,
    "api_port": 8000,
    "log_level": "INFO",
    "data_directory": "./data"
}
```

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

**Phase 3A: Config System Migrated**

- ✅ Configuration management system migrated and functional
- 🚧 API endpoints (placeholder)
- 🚧 Protocol implementations (placeholder)
- 🚧 Integration boundaries (placeholder)
- 🚧 Governance systems (placeholder)
- 🚧 CLI tools (placeholder)

## Migration Status

### Completed (Phase 3A)
- `config.py` → `packages/primal_genesis/core/config.py`
- Package exports configured
- Usage examples documented

### Upcoming (Future Phases)
- API implementation in `packages/primal_genesis/api/`
- Protocol definitions in `packages/primal_genesis/protocols/`
- Integration boundaries in `packages/primal_genesis/integrations/`
- Governance systems in `packages/primal_genesis/governance/`
- CLI tools in `packages/primal_genesis/cli/`

## Development Notes

- The package is designed to be importable from the repository root
- Configuration system supports both JSON files and environment variables
- All modules follow consistent import patterns
- Future modules will be added incrementally

## Future Implementation

- FastAPI-based web services
- Configuration and policy management
- Module registry and discovery
- CLI tools for system administration
- Integration boundaries for external services
