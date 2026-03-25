"""
Policy System

Provides a minimal policy engine for Primal Genesis Engine to control
what actions modules are allowed to perform.

Author: Primal Genesis Engine Team
Version: 0.1.0
"""

import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime


@dataclass
class PolicyRecord:
    """Represents a policy rule for module actions."""
    module_name: str
    action_name: str
    effect: str  # "allow" or "deny"
    description: str = ""
    enabled: bool = True

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "PolicyRecord":
        # Basic validation for required fields
        if not isinstance(data, dict):
            raise ValueError("Policy data must be a dictionary")
        if 'module_name' not in data or 'action_name' not in data or 'effect' not in data:
            raise ValueError("Policy data must contain 'module_name', 'action_name', and 'effect' fields")
        if data['effect'] not in ['allow', 'deny']:
            raise ValueError("Policy effect must be 'allow' or 'deny'")
        return cls(**data)


class PolicyEngine:
    """Simple policy engine with JSON persistence."""
    
    def __init__(self, storage_path: Optional[str] = None):
        self._policies: Dict[str, PolicyRecord] = {}
        # Use deterministic default path relative to package location
        if storage_path is None:
            # Default to data directory within package
            package_root = Path(__file__).parent.parent.parent
            self.storage_path = package_root / "data" / "policies.json"
        else:
            self.storage_path = Path(storage_path)
        
        self._load_policies()
    
    def add_policy(self, policy: PolicyRecord) -> None:
        """Add a new policy. Overwrites existing policy with same module/action."""
        if not policy or not policy.module_name or not policy.action_name:
            raise ValueError("Policy must have valid module_name and action_name")
        if policy.effect not in ['allow', 'deny']:
            raise ValueError("Policy effect must be 'allow' or 'deny'")
        
        policy_key = f"{policy.module_name}:{policy.action_name}"
        self._policies[policy_key] = policy
        self._save_policies()
    
    def get_policy(self, module_name: str, action_name: str) -> Optional[PolicyRecord]:
        """Get a policy for a specific module/action."""
        if not module_name or not action_name:
            return None
        
        policy_key = f"{module_name}:{action_name}"
        return self._policies.get(policy_key)
    
    def list_policies(self) -> List[PolicyRecord]:
        """List all policies."""
        return list(self._policies.values())
    
    def list_enabled_policies(self) -> List[PolicyRecord]:
        """List only enabled policies."""
        return [p for p in self._policies.values() if p.enabled]
    
    def evaluate_action(self, module_name: str, action_name: str) -> Dict:
        """
        Evaluate whether a module action is allowed.
        
        Returns:
            Dict with 'allowed' (bool) and 'policy' (PolicyRecord or None)
        """
        if not module_name or not action_name:
            return {
                'allowed': False,
                'policy': None,
                'reason': 'Invalid module_name or action_name'
            }
        
        policy = self.get_policy(module_name, action_name)
        
        # Default deny: if no matching policy exists, deny the action
        if policy is None:
            return {
                'allowed': False,
                'policy': None,
                'reason': f'No policy found for {module_name}:{action_name} (default deny)'
            }
        
        # Check if policy is enabled
        if not policy.enabled:
            return {
                'allowed': False,
                'policy': policy,
                'reason': f'Policy disabled for {module_name}:{action_name}'
            }
        
        # Return policy effect
        return {
            'allowed': policy.effect == 'allow',
            'policy': policy,
            'reason': f'Policy {"allows" if policy.effect == "allow" else "denies"} {module_name}:{action_name}'
        }
    
    def _load_policies(self) -> None:
        """Load policies from JSON file."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not isinstance(data, dict):
                        raise ValueError("Policy data must be a dictionary")
                    
                    loaded_policies = {}
                    for key, policy_data in data.items():
                        try:
                            policy = PolicyRecord.from_dict(policy_data)
                            # Ensure key consistency
                            expected_key = f"{policy.module_name}:{policy.action_name}"
                            if expected_key != key:
                                policy_key = expected_key
                            else:
                                policy_key = key
                            loaded_policies[policy_key] = policy
                        except (ValueError, TypeError) as e:
                            # Skip invalid policies but continue loading others
                            print(f"Warning: Skipping invalid policy '{key}': {e}")
                            continue
                    
                    self._policies = loaded_policies
                    
            except (json.JSONDecodeError, ValueError, KeyError, TypeError) as e:
                # Start fresh if file is corrupted
                print(f"Warning: Policy file corrupted, starting fresh: {e}")
                self._seed_default_policies()
        else:
            self._seed_default_policies()
    
    def _save_policies(self) -> None:
        """Save policies to JSON file."""
        try:
            # Ensure parent directory exists
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            
            data = {key: policy.to_dict() for key, policy in self._policies.items()}
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except (OSError, IOError) as e:
            print(f"Warning: Failed to save policies: {e}")
    
    def _seed_default_policies(self) -> None:
        """Seed registry with minimal default policies."""
        default_policies = [
            PolicyRecord(
                module_name="primal_genesis",
                action_name="read_config",
                effect="allow",
                description="Allow core package to read configuration"
            ),
            PolicyRecord(
                module_name="primal_genesis",
                action_name="write_config",
                effect="allow",
                description="Allow core package to write configuration"
            ),
            PolicyRecord(
                module_name="console",
                action_name="display_ui",
                effect="allow",
                description="Allow console to display user interface"
            ),
            PolicyRecord(
                module_name="override-core",
                action_name="execute_override",
                effect="allow",
                description="Allow override-core to execute override commands"
            ),
            PolicyRecord(
                module_name="pge-runner",
                action_name="evaluate_policy",
                effect="allow",
                description="Allow PGE runner to evaluate policies"
            ),
            PolicyRecord(
                module_name="athena",
                action_name="process_query",
                effect="allow",
                description="Allow Athena to process queries"
            )
        ]
        
        for policy in default_policies:
            policy_key = f"{policy.module_name}:{policy.action_name}"
            self._policies[policy_key] = policy
        
        self._save_policies()
