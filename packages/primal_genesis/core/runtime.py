"""
Core Runtime System

Provides a small coordinating layer that connects registry, policy, and memory
to create the first internal nervous system of Primal Genesis Engine.

Author: Primal Genesis Engine Team
Version: 0.1.0
"""

from typing import Dict, Optional, Any
from .registry import ModuleRegistry
from .policy import PolicyEngine, PolicyRecord
from .memory import MemoryStore, MemoryRecord


class CoreRuntime:
    """Small coordinating layer for registry, policy, and memory."""
    
    def __init__(self, 
                 registry_path: Optional[str] = None,
                 policy_path: Optional[str] = None,
                 memory_path: Optional[str] = None):
        self.registry = ModuleRegistry(registry_path)
        self.policy_engine = PolicyEngine(policy_path)
        self.memory_store = MemoryStore(memory_path)
    
    def execute_module_action(self, 
                             module_name: str, 
                             action_name: str, 
                             payload: Optional[Dict] = None) -> Dict:
        """
        Execute a module action with policy evaluation and memory recording.
        
        Args:
            module_name: Name of the module performing the action
            action_name: Name of the action being performed
            payload: Optional payload data for the action
            
        Returns:
            Dict with execution result including:
            - success: bool - whether action was allowed and executed
            - allowed: bool - whether action was allowed by policy
            - policy: PolicyRecord or None - the policy that was evaluated
            - reason: str - explanation of the result
            - memory_record: MemoryRecord or None - recorded memory
        """
        # Validate inputs
        if not module_name or not action_name:
            result = self._create_result(False, False, None, 'Invalid module_name or action_name', None)
            self._record_validation_failure('execute_module_action', 'Invalid inputs', result)
            return result
        
        # Check if module exists in registry
        module = self.registry.get_module(module_name)
        if module is None:
            result = self._create_result(False, False, None, f'Module {module_name} not found in registry', None)
            self._record_validation_failure(module_name, 'Module not found', result)
            return result
        
        # Check if module is enabled
        if not module.enabled:
            result = self._create_result(False, False, None, f'Module {module_name} is disabled', None)
            self._record_validation_failure(module_name, 'Module disabled', result)
            return result
        
        # Evaluate policy
        policy_result = self.policy_engine.evaluate_action(module_name, action_name)
        
        if not policy_result['allowed']:
            # Action denied by policy - record the denial
            memory_record = self._record_action_denied(module_name, action_name, policy_result)
            
            result = self._create_result(False, False, policy_result['policy'], policy_result['reason'], memory_record)
            return result
        
        # Action allowed - execute and record
        try:
            # For now, we don't actually execute anything - just record the action
            # In future phases, this could dispatch to actual module code
            execution_result = self._execute_action(module_name, action_name, payload)
            
            # Record the successful action
            memory_record = self._record_action_executed(module_name, action_name, execution_result)
            
            result = self._create_result(True, True, policy_result['policy'], policy_result['reason'], memory_record)
            return result
            
        except Exception as e:
            # Record the execution failure
            self._record_action_failed(module_name, action_name, str(e))
            
            result = self._create_result(False, True, policy_result['policy'], f'Execution failed: {str(e)}', None)
            return result
    
    def check_module_action(self, module_name: str, action_name: str) -> Dict:
        """
        Check if a module action is allowed without executing it.
        
        Returns:
            Dict with policy evaluation result
        """
        if not module_name or not action_name:
            return {
                'allowed': False,
                'policy': None,
                'reason': 'Invalid module_name or action_name'
            }
        
        # Check if module exists in registry
        module = self.registry.get_module(module_name)
        if module is None:
            return {
                'allowed': False,
                'policy': None,
                'reason': f'Module {module_name} not found in registry'
            }
        
        # Check if module is enabled
        if not module.enabled:
            return {
                'allowed': False,
                'policy': None,
                'reason': f'Module {module_name} is disabled'
            }
        
        # Evaluate policy
        return self.policy_engine.evaluate_action(module_name, action_name)
    
    def get_system_status(self) -> Dict:
        """Get overall system status."""
        return {
            'modules': {
                'total': len(self.registry.list_modules()),
                'enabled': len(self.registry.list_enabled_modules())
            },
            'policies': {
                'total': len(self.policy_engine.list_policies()),
                'enabled': len(self.policy_engine.list_enabled_policies())
            },
            'memories': {
                'total': self.memory_store.get_memory_count()
            }
        }
    
    def _execute_action(self, module_name: str, action_name: str, payload: Optional[Dict]) -> Dict:
        """
        Execute the actual action with improved realism and structured results.
        
        For now, this simulates execution with realistic outcomes.
        In future phases, this could dispatch to actual module code.
        """
        # Get module info for more realistic execution
        module = self.registry.get_module(module_name)
        if not module:
            return {
                'executed': False,
                'execution_mode': 'simulated',
                'outcome': 'error',
                'error': 'Module not found during execution',
                'payload': payload or {},
                'execution_details': {
                    'module_type': 'unknown',
                    'action': action_name,
                    'simulated': True
                }
            }
        
        # Simulate different execution outcomes based on module type and action
        execution_mode = 'local-simulated'  # More explicit about being local and simulated
        outcome = 'success'
        execution_details = {
            'module_type': module.module_type,
            'module_location': module.location,
            'module_entrypoint': module.entrypoint,
            'action': action_name,
            'simulated': True,
            'execution_time': '0.001s',  # Simulated execution time
            'execution_scope': 'local-only',  # Explicit about local scope
            'side_effect_level': 'read-only'  # Clear about side effect level
        }
        
        # Add some realistic variation based on module type
        if module.module_type == 'core':
            execution_details.update({
                'execution_context': 'core_system',
                'privilege_level': 'system',
                'side_effects': 'configuration_read'
            })
        elif module.module_type == 'frontend':
            execution_details.update({
                'execution_context': 'ui_interaction',
                'privilege_level': 'user',
                'side_effects': 'display_update'
            })
        elif module.module_type == 'tooling':
            execution_details.update({
                'execution_context': 'development_tool',
                'privilege_level': 'developer',
                'side_effects': 'file_system_access'
            })
        elif module.module_type == 'intelligence':
            execution_details.update({
                'execution_context': 'ai_processing',
                'privilege_level': 'analyst',
                'side_effects': 'data_analysis'
            })
        
        return {
            'executed': True,
            'execution_mode': execution_mode,
            'outcome': outcome,
            'payload': payload or {},
            'execution_details': execution_details,
            'message': f'Action {action_name} executed for module {module_name} ({execution_mode} mode)'
        }
    
    def _record_action_executed(self, module_name: str, action_name: str, execution_result: Dict) -> MemoryRecord:
        """Record a successful action execution."""
        content = f"Action '{action_name}' executed successfully for module '{module_name}'"
        metadata = {
            'action': action_name,
            'execution_result': execution_result
        }
        
        self.memory_store.create_memory(module_name, 'action_executed', content, metadata)
        
        # Return the created memory record
        memories = self.memory_store.list_by_module(module_name, limit=1)
        return memories[0] if memories else None
    
    def _record_action_denied(self, module_name: str, action_name: str, policy_result: Dict) -> MemoryRecord:
        """Record a denied action and return the memory record."""
        content = f"Action '{action_name}' denied for module '{module_name}'"
        metadata = {
            'action': action_name,
            'policy_effect': 'deny',
            'policy_reason': policy_result.get('reason', 'Unknown')
        }
        
        self.memory_store.create_memory(module_name, 'action_denied', content, metadata)
        
        # Return the created memory record
        memories = self.memory_store.list_by_module(module_name, limit=1)
        return memories[0] if memories else None
    
    def _record_action_failed(self, module_name: str, action_name: str, error_message: str) -> None:
        """Record a failed action execution."""
        content = f"Action '{action_name}' failed for module '{module_name}': {error_message}"
        metadata = {
            'action': action_name,
            'error': error_message
        }
        
        self.memory_store.create_memory(module_name, 'action_failed', content, metadata)
    
    def _record_validation_failure(self, module_name: str, failure_type: str, result: Dict) -> None:
        """Record a validation failure."""
        content = f"Validation failed for module '{module_name}': {failure_type}"
        metadata = {
            'failure_type': failure_type,
            'result': result
        }
        
        self.memory_store.create_memory('runtime', 'validation_failure', content, metadata)
    
    def _create_result(self, success: bool, allowed: bool, policy: Optional[PolicyRecord], reason: str, memory_record: Optional[MemoryRecord]) -> Dict:
        """Create a consistent result structure."""
        return {
            'success': success,
            'allowed': allowed,
            'policy': policy,
            'reason': reason,
            'memory_record': memory_record
        }
