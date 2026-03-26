"""
Integration Contract Registry

Provides a minimal, focused registry for integration contracts
that works alongside the existing registry system.
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path

try:
    from .contracts import IntegrationContract
except ImportError:
    from contracts import IntegrationContract


class IntegrationContractRegistry:
    """
    Minimal registry for integration contracts.
    
    Provides basic contract registration, listing, and retrieval
    without duplicating the main registry system.
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize the contract registry.
        
        Args:
            storage_path: Path to store contract data (defaults to packages/data/)
        """
        if storage_path is None:
            # Use deterministic local storage under packages/data/
            # Calculate path from this file location to packages/data/
            current_dir = Path(__file__).parent
            storage_path = current_dir.parent.parent / 'data' / 'integration_contracts.json'
        
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._contracts: Dict[str, IntegrationContract] = {}
        self._load_contracts()
    
    def register(self, contract: IntegrationContract) -> None:
        """
        Register an integration contract.
        
        Args:
            contract: The integration contract to register
        """
        contract.update_timestamp()
        self._contracts[contract.name] = contract
        self._save_contracts()
    
    def get_contract(self, name: str) -> Optional[IntegrationContract]:
        """
        Get a contract by name.
        
        Args:
            name: The contract name
            
        Returns:
            IntegrationContract if found, None otherwise
        """
        return self._contracts.get(name)
    
    def list_contracts(self) -> List[IntegrationContract]:
        """
        List all registered contracts.
        
        Returns:
            List of all integration contracts
        """
        return list(self._contracts.values())
    
    def list_contracts_by_type(self, integration_type: str) -> List[IntegrationContract]:
        """
        List contracts by integration type.
        
        Args:
            integration_type: The type to filter by
            
        Returns:
            List of contracts of the specified type
        """
        return [
            contract for contract in self._contracts.values()
            if contract.integration_type == integration_type
        ]
    
    def list_enabled_contracts(self) -> List[IntegrationContract]:
        """
        List only enabled contracts.
        
        Returns:
            List of enabled integration contracts
        """
        return [
            contract for contract in self._contracts.values()
            if contract.enabled
        ]
    
    def update_contract(self, name: str, updates: Dict) -> bool:
        """
        Update an existing contract.
        
        Args:
            name: The contract name to update
            updates: Dictionary of fields to update
            
        Returns:
            True if updated, False if not found
        """
        if name not in self._contracts:
            return False
        
        contract = self._contracts[name]
        for key, value in updates.items():
            if hasattr(contract, key):
                setattr(contract, key, value)
        
        contract.update_timestamp()
        self._save_contracts()
        return True
    
    def remove_contract(self, name: str) -> bool:
        """
        Remove a contract from the registry.
        
        Args:
            name: The contract name to remove
            
        Returns:
            True if removed, False if not found
        """
        if name not in self._contracts:
            return False
        
        del self._contracts[name]
        self._save_contracts()
        return True
    
    def get_contracts_summary(self) -> Dict:
        """
        Get a summary of all contracts.
        
        Returns:
            Dictionary with contract statistics and summaries
        """
        contracts = list(self._contracts.values())
        enabled = [c for c in contracts if c.enabled]
        active = [c for c in contracts if c.is_active()]
        
        return {
            'total_contracts': len(contracts),
            'enabled_contracts': len(enabled),
            'active_contracts': len(active),
            'integration_types': list(set(c.integration_type for c in contracts)),
            'contracts': [c.get_summary() for c in contracts]
        }
    
    def _load_contracts(self) -> None:
        """Load contracts from persistent storage."""
        if not self.storage_path.exists():
            return
        
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for contract_data in data.get('contracts', []):
                contract = IntegrationContract.from_dict(contract_data)
                self._contracts[contract.name] = contract
                
        except (json.JSONDecodeError, KeyError, IOError) as e:
            # Start with empty registry if file is corrupted
            self._contracts = {}
    
    def _save_contracts(self) -> None:
        """Save contracts to persistent storage."""
        data = {
            'contracts': [contract.to_dict() for contract in self._contracts.values()],
            'last_saved': IntegrationContract().registered_at
        }
        
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            # Log error but continue - registry will work in memory
            pass


# Global instance for easy access
_integration_contract_registry = None


def get_integration_contract_registry() -> IntegrationContractRegistry:
    """
    Get the global integration contract registry instance.
    
    Returns:
        Global IntegrationContractRegistry instance
    """
    global _integration_contract_registry
    if _integration_contract_registry is None:
        _integration_contract_registry = IntegrationContractRegistry()
    return _integration_contract_registry
