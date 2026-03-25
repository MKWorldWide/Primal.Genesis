"""
Module Registry System

Provides a simple module registry for Primal Genesis Engine to track
and manage available modules in the repository.

Author: Primal Genesis Engine Team
Version: 0.1.0
"""

import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from pathlib import Path


@dataclass
class ModuleRecord:
    """Represents a module in Primal Genesis Engine."""
    name: str
    module_type: str
    description: str
    version: str
    enabled: bool = True
    location: str = ""
    entrypoint: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "ModuleRecord":
        return cls(**data)


class ModuleRegistry:
    """Simple module registry with JSON persistence."""
    
    def __init__(self, storage_path: Optional[str] = None):
        self._modules: Dict[str, ModuleRecord] = {}
        # Use deterministic default path relative to package location
        if storage_path is None:
            # Default to data directory within package
            package_root = Path(__file__).parent.parent.parent
            self.storage_path = package_root / "data" / "registry.json"
        else:
            self.storage_path = Path(storage_path)
        
        self._load_registry()
    
    def register_module(self, module: ModuleRecord) -> None:
        """Register a new module."""
        self._modules[module.name] = module
        self._save_registry()
    
    def get_module(self, name: str) -> Optional[ModuleRecord]:
        """Get a module by name."""
        return self._modules.get(name)
    
    def list_modules(self) -> List[ModuleRecord]:
        """List all registered modules."""
        return list(self._modules.values())
    
    def list_enabled_modules(self) -> List[ModuleRecord]:
        """List only enabled modules."""
        return [m for m in self._modules.values() if m.enabled]
    
    def enable_module(self, name: str) -> bool:
        """Enable a module."""
        if name in self._modules:
            self._modules[name].enabled = True
            self._save_registry()
            return True
        return False
    
    def disable_module(self, name: str) -> bool:
        """Disable a module."""
        if name in self._modules:
            self._modules[name].enabled = False
            self._save_registry()
            return True
        return False
    
    def _load_registry(self) -> None:
        """Load registry from JSON file."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    for name, module_data in data.items():
                        self._modules[name] = ModuleRecord.from_dict(module_data)
            except (json.JSONDecodeError, KeyError, TypeError):
                # Start fresh if file is corrupted
                self._seed_default_modules()
        else:
            self._seed_default_modules()
    
    def _save_registry(self) -> None:
        """Save registry to JSON file."""
        # Ensure parent directory exists
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {name: module.to_dict() for name, module in self._modules.items()}
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _seed_default_modules(self) -> None:
        """Seed registry with default modules."""
        default_modules = [
            ModuleRecord(
                name="primal_genesis",
                module_type="core",
                description="Python core package for Primal Genesis Engine",
                version="0.1.0",
                location="packages/primal_genesis",
                entrypoint="packages.primal_genesis"
            ),
            ModuleRecord(
                name="console",
                module_type="frontend",
                description="React/TypeScript console UI application",
                version="0.1.0",
                location="apps/console",
                entrypoint="apps/console/src"
            ),
            ModuleRecord(
                name="override-core",
                module_type="tooling",
                description="Node.js development tooling and override system",
                version="0.1.0",
                location="apps/override-core",
                entrypoint="apps/override-core/index.js"
            ),
            ModuleRecord(
                name="pge-runner",
                module_type="tooling",
                description="TypeScript policy engine and governance system",
                version="0.1.0",
                location="apps/pge-runner",
                entrypoint="apps/pge-runner/pge.ts"
            ),
            ModuleRecord(
                name="athena",
                module_type="intelligence",
                description="Cross-project intelligence system",
                version="0.1.0",
                location="packages/athena",
                entrypoint="packages/athena"
            )
        ]
        
        for module in default_modules:
            self._modules[module.name] = module
        
        self._save_registry()
