"""
API Module

FastAPI-based API layer for Primal Genesis Engine.
Provides modular router structure for exposing core functionality.

Author: Primal Genesis Engine Team
Version: 0.1.0
"""

from .app import create_app, app

__all__ = ["create_app", "app"]
