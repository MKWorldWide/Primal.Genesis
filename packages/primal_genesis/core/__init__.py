"""
Primal Genesis Engine - Core Module

This module contains the core functionality of the Primal Genesis Engine,
including configuration management, basic services, and foundational utilities.

Key components:
- Configuration management
- Module registry and management
- Core utilities and helpers
- Base classes and interfaces
- Service orchestration
"""

from .config import Config
from .registry import ModuleRegistry, ModuleRecord

# Base classes will be added in future phases
# from .base import BaseService

__all__ = ["Config", "ModuleRegistry", "ModuleRecord"]
