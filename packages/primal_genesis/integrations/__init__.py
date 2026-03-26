"""
Primal Genesis Engine - Integrations Module

This module contains external system integrations and adapters for the Primal Genesis Engine.

Key components:
- External service adapters
- Integration interfaces
- Third-party connectors
- Integration contract model and registry
- Future Athena integration boundary
"""

from .contracts import IntegrationContract
from .contract_registry import IntegrationContractRegistry, get_integration_contract_registry
from .seed_contracts import seed_integration_contracts

# Future Athena integration will be added here
# from .athena import AthenaIntegration

# Base integration will be added when needed
# from .base import BaseIntegration
# from .registry import IntegrationRegistry

__all__ = [
    "IntegrationContract",
    "IntegrationContractRegistry", 
    "get_integration_contract_registry",
    "seed_integration_contracts"
]
