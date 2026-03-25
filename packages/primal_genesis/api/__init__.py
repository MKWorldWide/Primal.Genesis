"""
Primal Genesis Engine - API Module

This module contains the REST API and web service endpoints for the Primal Genesis Engine.

Key components:
- FastAPI application setup
- REST endpoints
- WebSocket handlers
- API middleware and authentication
"""

from .app import create_app
from .routes import router

__all__ = ["create_app", "router"]
