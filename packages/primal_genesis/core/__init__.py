"""
Primal Genesis Engine - Core Module

This module contains the core functionality of the Primal Genesis Engine,
including configuration management, basic services, and foundational utilities.

Key components:
- Configuration management
- Module registry and management
- Policy engine and governance
- Memory store and event logging
- Core runtime orchestration
- System visibility layer
- Core utilities and helpers
- Base classes and interfaces
- Service orchestration
"""

from .config import Config
from .registry import ModuleRegistry, ModuleRecord
from .policy import PolicyEngine, PolicyRecord
from .memory import MemoryStore, MemoryRecord
from .runtime import CoreRuntime
from .visibility import VisibilityService
from .console_bridge import ConsoleBridge

# Base classes will be added in future phases
# from .base import BaseService

__all__ = [
    "Config", 
    "ModuleRegistry", "ModuleRecord",
    "PolicyEngine", "PolicyRecord", 
    "MemoryStore", "MemoryRecord",
    "CoreRuntime",
    "VisibilityService",
    "ConsoleBridge"
]
