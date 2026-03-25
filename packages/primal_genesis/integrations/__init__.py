"""
Primal Genesis Engine - Integrations Module

This module contains external system integrations and adapters for the Primal Genesis Engine.

Key components:
- External service adapters
- Integration interfaces
- Third-party connectors
- Future Athena integration boundary
"""

from .base import BaseIntegration
from .registry import IntegrationRegistry

# Future Athena integration will be added here
# from .athena import AthenaIntegration

__all__ = ["BaseIntegration", "IntegrationRegistry"]
