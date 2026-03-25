"""
Primal Genesis Engine - CLI Module

This module contains command-line interface tools for the Primal Genesis Engine.

Key components:
- CLI commands
- Command parsers
- Terminal interfaces
- Administrative tools
"""

from .main import main
from .commands import CommandRegistry

__all__ = ["main", "CommandRegistry"]
