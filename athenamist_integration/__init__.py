"""
AthenaMist-Blended Integration Package
=====================================

This package provides comprehensive integration modules for:
- AI Integration (Multiple AI providers)
- LilithOSi Integration (iOS firmware development)
- Phantom Integration (Security scanning and reconnaissance)
- Primal Sovereign Core Integration (Voice processing and AWS optimization)
- Shadow Nexus Integration (Forex trading, data retrieval, and command network)

Author: AthenaMist-Blended Team
Version: 2.0
License: MIT
"""

from .ai_integration import AIIntegrationManager
from .lilithos_integration import LilithOSiManager
from .phantom_integration import PhantomManager
from .primal_sovereign_integration import PrimalSovereignManager, VoiceCommandType, ProcessingStatus
from .shadow_nexus_integration import ShadowNexusManager, TradingSignalType, OperationStatus, CommandPlatform
from .xai_integration import XAIIntegrationManager, XAIRequest, XAIResponse, XAIModelType, QuantumState
from .the_nine_integration import TheNineIntegrationManager, Layer9Request, Layer9Response, Layer9State, Ellipsis9Pattern

__all__ = [
    'AIIntegrationManager',
    'LilithOSiManager', 
    'PhantomManager',
    'PrimalSovereignManager',
    'VoiceCommandType',
    'ProcessingStatus',
    'ShadowNexusManager',
    'TradingSignalType',
    'OperationStatus',
    'CommandPlatform',
    'XAIIntegrationManager',
    'XAIRequest',
    'XAIResponse',
    'XAIModelType',
    'QuantumState',
    'TheNineIntegrationManager',
    'Layer9Request',
    'Layer9Response',
    'Layer9State',
    'Ellipsis9Pattern'
]

__version__ = "2.0"
__author__ = "AthenaMist-Blended Team" 