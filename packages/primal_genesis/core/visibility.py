"""
Visibility System

Provides a small visibility layer for Primal Genesis Engine to summarize
system state for future console/UI integration.

Author: Primal Genesis Engine Team
Version: 0.1.0
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from .registry import ModuleRegistry
from .policy import PolicyEngine
from .memory import MemoryStore
from .runtime import CoreRuntime


class VisibilityService:
    """Small visibility service for system snapshots and activity summaries."""
    
    def __init__(self, runtime: CoreRuntime):
        self.runtime = runtime
        self.registry = runtime.registry
        self.policy_engine = runtime.policy_engine
        self.memory_store = runtime.memory_store
    
    def get_system_snapshot(self) -> Dict:
        """
        Get a comprehensive system snapshot.
        
        Returns:
            Dict with complete system state overview
        """
        return {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'system': {
                'status': 'operational',
                'uptime': 'simulated',  # Could be calculated in future phases
                'version': '0.1.0'
            },
            'modules': self._get_module_snapshot(),
            'policies': self._get_policy_snapshot(),
            'memory': self._get_memory_snapshot(),
            'activity': self._get_activity_summary()
        }
    
    def get_recent_activity(self, limit: int = 10) -> Dict:
        """
        Get recent system activity summary.
        
        Args:
            limit: Maximum number of recent activities to return
            
        Returns:
            Dict with recent activity information
        """
        recent_memories = self.memory_store.list_memories(limit=limit)
        
        return {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'total_activities': len(recent_memories),
            'activities': [
                {
                    'module': memory.module_name,
                    'event_type': memory.event_type,
                    'content': memory.content,
                    'timestamp': memory.timestamp,
                    'metadata': memory.metadata or {}
                }
                for memory in recent_memories
            ],
            'activity_breakdown': self._analyze_activity_breakdown(recent_memories)
        }
    
    def get_module_health(self) -> Dict:
        """
        Get module health and status overview.
        
        Returns:
            Dict with module health information
        """
        all_modules = self.registry.list_modules()
        enabled_modules = self.registry.list_enabled_modules()
        
        return {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'total_modules': len(all_modules),
            'enabled_modules': len(enabled_modules),
            'disabled_modules': len(all_modules) - len(enabled_modules),
            'modules_by_type': self._group_modules_by_type(all_modules),
            'module_details': [
                {
                    'name': module.name,
                    'type': module.module_type,
                    'enabled': module.enabled,
                    'location': module.location,
                    'entrypoint': module.entrypoint,
                    'description': module.description,
                    'version': module.version
                }
                for module in all_modules
            ]
        }
    
    def get_policy_overview(self) -> Dict:
        """
        Get policy system overview.
        
        Returns:
            Dict with policy system information
        """
        all_policies = self.policy_engine.list_policies()
        enabled_policies = self.policy_engine.list_enabled_policies()
        
        return {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'total_policies': len(all_policies),
            'enabled_policies': len(enabled_policies),
            'disabled_policies': len(all_policies) - len(enabled_policies),
            'policies_by_effect': self._group_policies_by_effect(all_policies),
            'policy_details': [
                {
                    'module': policy.module_name,
                    'action': policy.action_name,
                    'effect': policy.effect,
                    'enabled': policy.enabled,
                    'description': policy.description
                }
                for policy in all_policies
            ]
        }
    
    def get_memory_statistics(self) -> Dict:
        """
        Get memory system statistics.
        
        Returns:
            Dict with memory statistics
        """
        all_memories = self.memory_store.list_memories()
        
        return {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'total_memories': len(all_memories),
            'memory_types': self._analyze_memory_types(all_memories),
            'memory_by_module': self._analyze_memory_by_module(all_memories),
            'recent_activity': len([m for m in all_memories 
                                  if self._is_recent_memory(m.timestamp)]),
            'oldest_memory': all_memories[-1].timestamp if all_memories else None,
            'newest_memory': all_memories[0].timestamp if all_memories else None
        }
    
    def _get_module_snapshot(self) -> Dict:
        """Get module information for snapshot."""
        all_modules = self.registry.list_modules()
        enabled_modules = self.registry.list_enabled_modules()
        
        return {
            'total': len(all_modules),
            'enabled': len(enabled_modules),
            'disabled': len(all_modules) - len(enabled_modules),
            'types': list(set(module.module_type for module in all_modules)),
            'enabled_modules': [module.name for module in enabled_modules]
        }
    
    def _get_policy_snapshot(self) -> Dict:
        """Get policy information for snapshot."""
        all_policies = self.policy_engine.list_policies()
        enabled_policies = self.policy_engine.list_enabled_policies()
        
        return {
            'total': len(all_policies),
            'enabled': len(enabled_policies),
            'disabled': len(all_policies) - len(enabled_policies),
            'effects': list(set(policy.effect for policy in all_policies)),
            'default_behavior': 'deny'  # Conservative default
        }
    
    def _get_memory_snapshot(self) -> Dict:
        """Get memory information for snapshot."""
        all_memories = self.memory_store.list_memories()
        
        return {
            'total': len(all_memories),
            'event_types': list(set(memory.event_type for memory in all_memories)),
            'recent_count': len([m for m in all_memories 
                               if self._is_recent_memory(m.timestamp)])
        }
    
    def _get_activity_summary(self) -> Dict:
        """Get activity summary for snapshot."""
        recent_memories = self.memory_store.list_memories(limit=5)
        
        return {
            'recent_count': len(recent_memories),
            'activity_level': 'normal' if len(recent_memories) > 0 else 'quiet',
            'last_activity': recent_memories[0].timestamp if recent_memories else None
        }
    
    def _group_modules_by_type(self, modules: List) -> Dict:
        """Group modules by type."""
        grouped = {}
        for module in modules:
            module_type = module.module_type
            if module_type not in grouped:
                grouped[module_type] = []
            grouped[module_type].append(module.name)
        return grouped
    
    def _group_policies_by_effect(self, policies: List) -> Dict:
        """Group policies by effect."""
        grouped = {'allow': [], 'deny': []}
        for policy in policies:
            grouped[policy.effect].append(f"{policy.module_name}:{policy.action_name}")
        return grouped
    
    def _analyze_activity_breakdown(self, memories: List) -> Dict:
        """Analyze activity breakdown by event type."""
        breakdown = {}
        for memory in memories:
            event_type = memory.event_type
            if event_type not in breakdown:
                breakdown[event_type] = 0
            breakdown[event_type] += 1
        return breakdown
    
    def _analyze_memory_types(self, memories: List) -> Dict:
        """Analyze memory types distribution."""
        types = {}
        for memory in memories:
            event_type = memory.event_type
            if event_type not in types:
                types[event_type] = 0
            types[event_type] += 1
        return types
    
    def _analyze_memory_by_module(self, memories: List) -> Dict:
        """Analyze memory distribution by module."""
        by_module = {}
        for memory in memories:
            module = memory.module_name
            if module not in by_module:
                by_module[module] = 0
            by_module[module] += 1
        return by_module
    
    def _is_recent_memory(self, timestamp: str) -> bool:
        """Check if memory is recent (within last hour)."""
        try:
            memory_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            one_hour_ago = datetime.utcnow().replace(tzinfo=memory_time.tzinfo) - timedelta(hours=1)
            return memory_time > one_hour_ago
        except:
            return False
