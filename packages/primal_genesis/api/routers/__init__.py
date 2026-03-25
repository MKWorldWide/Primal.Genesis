"""
API Routers Module

Modular router structure for Primal Genesis Engine API.
Each router handles a specific domain of functionality.

Author: Primal Genesis Engine Team
Version: 0.1.0
"""

from . import health, system, runtime

__all__ = ["health", "system", "runtime"]
