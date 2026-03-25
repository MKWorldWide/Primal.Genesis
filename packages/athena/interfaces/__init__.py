"""
Athena Interfaces Module

Defines the core interfaces and protocols for Athena's intelligence capabilities.

This module provides the foundational contracts that all Athena components
will implement, ensuring consistency and interoperability across the system.

Components:
- CoreObserver: Read-only observation interface for Primal Genesis Engine
- BaseInterface: Core interface definition (future)
- IntelligenceInterface: General intelligence contract (future)
- CommunicationInterface: Inter-system communication protocols (future)

Status: Core observer implemented, others reserved for future phases
"""

from .observer import CoreObserver

__all__ = ["CoreObserver"]
