"""
Primal Genesis Engine - Protocols Module

This module contains communication protocols and data exchange formats for the Primal Genesis Engine.

Key components:
- Message protocols
- Data serialization formats
- Communication interfaces
- Protocol adapters
"""

from .base import BaseProtocol
from .messaging import MessageProtocol

__all__ = ["BaseProtocol", "MessageProtocol"]
