"""
Console Bridge

Provides a small, explicit bridge between the Python visibility layer and future console.
This creates a console-facing visibility contract that future UI can consume.

Author: Primal Genesis Engine Team
Version: 0.1.0
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from .visibility import VisibilityService
from ..integrations.contract_registry import get_integration_contract_registry


class ConsoleBridge:
    """Small console-facing bridge for system visibility."""
    
    def __init__(self, visibility_service: VisibilityService):
        """
        Initialize console bridge with visibility service.
        
        Args:
            visibility_service: The visibility service to bridge to console
        """
        self.visibility = visibility_service
    
    def get_console_summary(self) -> Dict:
        """
        Get a console-oriented summary of system state.
        
        Returns:
            Dict with console-friendly system summary
        """
        system_snapshot = self.visibility.get_system_snapshot()
        
        return {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'console_version': '0.1.0',
            'system_status': {
                'status': system_snapshot['system']['status'],
                'version': system_snapshot['system']['version'],
                'uptime': system_snapshot['system']['uptime']
            },
            'modules': {
                'total_count': system_snapshot['modules']['total'],
                'enabled_count': system_snapshot['modules']['enabled'],
                'disabled_count': system_snapshot['modules']['disabled'],
                'enabled_modules': system_snapshot['modules']['enabled_modules'],
                'available_types': system_snapshot['modules']['types']
            },
            'policies': {
                'total_count': system_snapshot['policies']['total'],
                'enabled_count': system_snapshot['policies']['enabled'],
                'disabled_count': system_snapshot['policies']['disabled'],
                'default_behavior': system_snapshot['policies']['default_behavior'],
                'available_effects': system_snapshot['policies']['effects']
            },
            'memory': {
                'total_count': system_snapshot['memory']['total'],
                'event_types': system_snapshot['memory']['event_types'],
                'recent_count': system_snapshot['memory']['recent_count']
            },
            'activity': {
                'recent_count': system_snapshot['activity']['recent_count'],
                'activity_level': system_snapshot['activity']['activity_level'],
                'last_activity': system_snapshot['activity']['last_activity']
            }
        }
    
    def get_module_overview(self) -> Dict:
        """
        Get a console-friendly module overview.
        
        Returns:
            Dict with module information for console display
        """
        module_health = self.visibility.get_module_health()
        
        return {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'summary': {
                'total_modules': module_health['total_modules'],
                'enabled_modules': module_health['enabled_modules'],
                'disabled_modules': module_health['disabled_modules'],
                'health_percentage': round((module_health['enabled_modules'] / max(module_health['total_modules'], 1)) * 100, 1)
            },
            'modules_by_type': module_health['modules_by_type'],
            'module_details': module_health['module_details']
        }
    
    def get_recent_activity(self, limit: int = 10) -> Dict:
        """
        Get recent activity formatted for console display.
        
        Args:
            limit: Maximum number of activities to return
            
        Returns:
            Dict with console-friendly activity data
        """
        recent_activity = self.visibility.get_recent_activity(limit=limit)
        
        return {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'summary': {
                'total_activities': recent_activity['total_activities'],
                'showing_limit': limit,
                'activity_types': list(set(activity['event_type'] for activity in recent_activity['activities']))
            },
            'activities': [
                {
                    'id': idx + 1,
                    'module': activity['module'],
                    'event_type': activity['event_type'],
                    'content': activity['content'],
                    'timestamp': activity['timestamp'],
                    'metadata': activity['metadata'],
                    'display_type': self._get_display_type(activity['event_type'])
                }
                for idx, activity in enumerate(recent_activity['activities'])
            ]
        }
    
    def get_athena_observations(self) -> Dict:
        """
        Get Athena's observations of the system for console display.
        
        Returns:
            Dict with Athena's observational insights
        """
        from athena.interfaces.observer import CoreObserver
        
        # Create Athena observer
        observer = CoreObserver(self.visibility)
        
        # Gather observations
        observations = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'system_health': observer.observe_system_health(),
            'system_trends': observer.observe_system_trends(),
            'module_state': observer.observe_module_state(),
            'execution_patterns': observer.observe_execution_patterns(),
            'memory_statistics': observer.observe_memory_statistics()
        }
        
        return observations
    
    def get_integrations_overview(self) -> Dict:
        """
        Get integrations/modules overview for future expansion.
        
        Returns:
            Dict with integration surface information
        """
        module_health = self.visibility.get_module_health()
        
        return {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'integration_surface': {
                'total_modules': module_health['total_modules'],
                'enabled_modules': module_health['enabled_modules'],
                'disabled_modules': module_health['disabled_modules'],
                'available_types': list(set(module['type'] for module in module_health['module_details'])),
                'modules_by_type': module_health['modules_by_type'],
            },
            'module_details': module_health['module_details'],
            'integration_readiness': {
                'has_enabled_modules': module_health['enabled_modules'] > 0,
                'has_multiple_types': len(set(module['type'] for module in module_health['module_details'])) > 1,
                'health_percentage': round((module_health['enabled_modules'] / max(module_health['total_modules'], 1)) * 100, 1)
            }
        }
    
    def get_system_health(self) -> Dict:
        """
        Get system health metrics for console display.
        
        Returns:
            Dict with health indicators for console
        """
        module_health = self.visibility.get_module_health()
        policy_overview = self.visibility.get_policy_overview()
        memory_stats = self.visibility.get_memory_statistics()
        
        # Calculate overall health score
        module_health_score = (module_health['enabled_modules'] / max(module_health['total_modules'], 1)) * 100
        policy_health_score = (policy_overview['enabled_policies'] / max(policy_overview['total_policies'], 1)) * 100
        
        overall_health = (module_health_score * 0.4 + policy_health_score * 0.3 + 50) / 100  # Memory contributes less
        
        return {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'overall_health': {
                'score': round(overall_health, 1),
                'status': self._get_health_status(overall_health),
                'recommendation': self._get_health_recommendation(overall_health)
            },
            'component_health': {
                'modules': {
                    'score': round(module_health_score, 1),
                    'status': self._get_health_status(module_health_score)
                },
                'policies': {
                    'score': round(policy_health_score, 1),
                    'status': self._get_health_status(policy_health_score)
                }
            },
            'metrics': {
                'total_modules': module_health['total_modules'],
                'enabled_modules': module_health['enabled_modules'],
                'total_policies': policy_overview['total_policies'],
                'enabled_policies': policy_overview['enabled_policies'],
                'total_memories': memory_stats['total_memories'],
                'recent_activity': memory_stats['recent_activity']
            }
        }
    
    def _get_display_type(self, event_type: str) -> str:
        """Get display type for console based on event type."""
        display_types = {
            'action_executed': 'success',
            'action_denied': 'warning',
            'action_failed': 'error',
            'validation_failure': 'error',
            'module_registered': 'info',
            'policy_created': 'info'
        }
        return display_types.get(event_type, 'info')
    
    def _get_health_status(self, score: float) -> str:
        """Get health status based on score."""
        if score >= 90:
            return 'excellent'
        elif score >= 75:
            return 'good'
        elif score >= 60:
            return 'fair'
        else:
            return 'poor'
    
    def get_integration_contracts(self) -> Dict:
        """
        Get integration contracts for console display.
        
        Returns:
            Dict with integration contract information
        """
        registry = get_integration_contract_registry()
        contracts = registry.list_contracts()
        
        # Convert to console-friendly format
        contract_data = []
        for contract in contracts:
            contract_data.append({
                'name': contract.name,
                'type': contract.integration_type,
                'description': contract.description,
                'version': contract.version,
                'enabled': contract.enabled,
                'status': contract.status,
                'read_only': contract.read_only,
                'capabilities': contract.capabilities,
                'ui_surface': contract.ui_surface,
                'entrypoint': contract.entrypoint
            })
        
        return {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'contracts': contract_data,
            'summary': registry.get_contracts_summary()
        }
    
    def _get_health_recommendation(self, score: float) -> str:
        """Get health recommendation based on score."""
        if score >= 90:
            return 'System is operating optimally'
        elif score >= 75:
            return 'System is operating well'
        elif score >= 60:
            return 'System needs attention'
        else:
            return 'System requires immediate attention'
