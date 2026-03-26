"""
Integration Contract Model

Defines the standardized IntegrationContract dataclass and supporting
serialization helpers for Primal Genesis Engine modules and integrations.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import json
from datetime import datetime


@dataclass
class IntegrationContract:
    """
    Standardized contract for Primal Genesis Engine integrations and modules.
    
    Provides a clean, explicit declaration of what an integration is,
    what it can do, and how it should be represented across engine layers.
    """
    name: str
    integration_type: str
    description: str
    version: str
    enabled: bool = True
    entrypoint: str = ""
    capabilities: List[str] = field(default_factory=list)
    status: str = "unknown"
    read_only: bool = True
    ui_surface: Optional[str] = None
    
    # Metadata fields
    registered_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')
    last_updated: str = field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert contract to dictionary for serialization."""
        return {
            'name': self.name,
            'integration_type': self.integration_type,
            'description': self.description,
            'version': self.version,
            'enabled': self.enabled,
            'entrypoint': self.entrypoint,
            'capabilities': self.capabilities,
            'status': self.status,
            'read_only': self.read_only,
            'ui_surface': self.ui_surface,
            'registered_at': self.registered_at,
            'last_updated': self.last_updated
        }
    
    def to_json(self) -> str:
        """Convert contract to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IntegrationContract':
        """Create contract from dictionary."""
        return cls(
            name=data['name'],
            integration_type=data['integration_type'],
            description=data['description'],
            version=data['version'],
            enabled=data.get('enabled', True),
            entrypoint=data.get('entrypoint', ''),
            capabilities=data.get('capabilities', []),
            status=data.get('status', 'unknown'),
            read_only=data.get('read_only', True),
            ui_surface=data.get('ui_surface'),
            registered_at=data.get('registered_at', datetime.utcnow().isoformat() + 'Z'),
            last_updated=data.get('last_updated', datetime.utcnow().isoformat() + 'Z')
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'IntegrationContract':
        """Create contract from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def update_timestamp(self) -> None:
        """Update the last_updated timestamp."""
        self.last_updated = datetime.utcnow().isoformat() + 'Z'
    
    def has_capability(self, capability: str) -> bool:
        """Check if contract has a specific capability."""
        return capability in self.capabilities
    
    def is_active(self) -> bool:
        """Check if contract is active and enabled."""
        return self.enabled and self.status.lower() in ['active', 'running', 'enabled']
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a concise summary of the contract."""
        return {
            'name': self.name,
            'type': self.integration_type,
            'status': self.status,
            'enabled': self.enabled,
            'capabilities_count': len(self.capabilities),
            'read_only': self.read_only,
            'version': self.version
        }
