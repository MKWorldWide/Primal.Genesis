"""
Primal Genesis Engine - Core Module

This module contains the core functionality of the Primal Genesis Engine,
including configuration management, basic services, and foundational utilities.

Key components:
- Configuration management
- Core utilities and helpers
- Base classes and interfaces
- Service orchestration
"""

from .config import Config
from .base import BaseService

__all__ = ["Config", "BaseService"]
