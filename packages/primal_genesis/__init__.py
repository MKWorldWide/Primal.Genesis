"""
Primal Genesis Engine - Python Core Package

This package provides the core Python functionality for the Primal Genesis Engine,
including configuration management, API endpoints, protocols, integrations,
governance systems, and CLI tools.

Author: Primal Genesis Engine Team
Version: 0.1.0
"""

__version__ = "0.1.0"
__author__ = "Primal Genesis Engine Team"

# Export core functionality
from .core import (
    Config, 
    ModuleRegistry, ModuleRecord,
    PolicyEngine, PolicyRecord,
    MemoryStore, MemoryRecord,
    CoreRuntime,
    VisibilityService
)

# Future exports will be added as modules are implemented
# from .api import create_app, router
# from .protocols import BaseProtocol, MessageProtocol
# from .integrations import BaseIntegration, IntegrationRegistry
# from .cli import main, CommandRegistry

__all__ = [
    "Config", 
    "ModuleRegistry", "ModuleRecord",
    "PolicyEngine", "PolicyRecord",
    "MemoryStore", "MemoryRecord", 
    "CoreRuntime",
    "VisibilityService"
]
