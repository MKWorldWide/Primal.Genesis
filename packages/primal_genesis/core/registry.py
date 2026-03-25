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
        # Basic validation for required fields
        if not isinstance(data, dict):
            raise ValueError("Module data must be a dictionary")
        if 'name' not in data or 'module_type' not in data:
            raise ValueError("Module data must contain 'name' and 'module_type' fields")
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
        """Register a new module. Overwrites existing module with same name."""
        if not module or not module.name:
            raise ValueError("Module must have a valid name")
        self._modules[module.name] = module
        self._save_registry()
    
    def get_module(self, name: str) -> Optional[ModuleRecord]:
        """Get a module by name."""
        if not name or not isinstance(name, str):
            return None
        return self._modules.get(name)
    
    def list_modules(self) -> List[ModuleRecord]:
        """List all registered modules."""
        return list(self._modules.values())
    
    def list_enabled_modules(self) -> List[ModuleRecord]:
        """List only enabled modules."""
        return [m for m in self._modules.values() if m.enabled]
    
    def enable_module(self, name: str) -> bool:
        """Enable a module."""
        if not name or not isinstance(name, str):
            return False
        if name in self._modules:
            self._modules[name].enabled = True
            self._save_registry()
            return True
        return False
    
    def disable_module(self, name: str) -> bool:
        """Disable a module."""
        if not name or not isinstance(name, str):
            return False
        if name in self._modules:
            self._modules[name].enabled = False
            self._save_registry()
            return True
        return False
    
    def _load_registry(self) -> None:
        """Load registry from JSON file."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not isinstance(data, dict):
                        raise ValueError("Registry data must be a dictionary")
                    
                    loaded_modules = {}
                    for name, module_data in data.items():
                        try:
                            module = ModuleRecord.from_dict(module_data)
                            # Ensure name consistency
                            if module.name != name:
                                module.name = name
                            loaded_modules[name] = module
                        except (ValueError, TypeError) as e:
                            # Skip invalid modules but continue loading others
                            print(f"Warning: Skipping invalid module '{name}': {e}")
                            continue
                    
                    self._modules = loaded_modules
                    
            except (json.JSONDecodeError, ValueError, KeyError, TypeError) as e:
                # Start fresh if file is corrupted
                print(f"Warning: Registry file corrupted, starting fresh: {e}")
                self._seed_default_modules()
        else:
            self._seed_default_modules()
    
    def _save_registry(self) -> None:
        """Save registry to JSON file."""
        try:
            # Ensure parent directory exists
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            
            data = {name: module.to_dict() for name, module in self._modules.items()}
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except (OSError, IOError) as e:
            print(f"Warning: Failed to save registry: {e}")
    
    def _seed_default_modules(self) -> None:
        """Seed registry with default modules."""
        default_modules = [
            ModuleRecord(
                name="primal_genesis",
                module_type="core",
                description="Python core package for Primal Genesis Engine",
                version="0.1.0",
                location="packages/primal_genesis",
                entrypoint="primal_genesis"  # Public import identity
            ),
            ModuleRecord(
                name="console",
                module_type="frontend",
                description="React/TypeScript console UI application",
                version="0.1.0",
                location="apps/console",
                entrypoint="apps/console/src"  # Repo-relative primary runtime path
            ),
            ModuleRecord(
                name="override-core",
                module_type="tooling",
                description="Node.js development tooling and override system",
                version="0.1.0",
                location="apps/override-core",
                entrypoint="apps/override-core/index.js"  # Repo-relative executable
            ),
            ModuleRecord(
                name="pge-runner",
                module_type="tooling",
                description="TypeScript policy engine and governance system",
                version="0.1.0",
                location="apps/pge-runner",
                entrypoint="apps/pge-runner/pge.ts"  # Repo-relative executable
            ),
            ModuleRecord(
                name="athena",
                module_type="intelligence",
                description="Cross-project intelligence system",
                version="0.1.0",
                location="packages/athena",
                entrypoint="athena"  # Public import identity
            )
        ]
        
        for module in default_modules:
            self._modules[module.name] = module
        
        self._save_registry()
