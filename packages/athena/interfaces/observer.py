"""
Athena Observer Bridge

Provides a read-only observation interface for Athena to safely observe
the Primal Genesis Engine core spine without mutation capabilities.

Author: Primal Genesis Engine Team
Version: 0.1.0
"""

from typing import Dict, List, Optional, Any
from datetime import datetime


class CoreObserver:
    """
    Read-only observer interface for Athena to observe the Primal Genesis Engine.
    
    This interface provides safe, read-only access to system state, activity,
    and configuration without allowing any mutations or side effects.
    """
    
    def __init__(self, visibility_service):
        """
        Initialize the observer with a visibility service.
        
        Args:
            visibility_service: The visibility service to observe
        """
        self.visibility = visibility_service
        self._observer_id = f"athena_observer_{datetime.utcnow().isoformat()}"
    
    def observe_system_snapshot(self) -> Dict:
        """
        Observe a complete system snapshot.
        
        Returns:
            Dict with read-only system state
        """
        snapshot = self.visibility.get_system_snapshot()
        
        # Add observer metadata for tracking
        return {
            'observer_metadata': {
                'observer_id': self._observer_id,
                'observation_time': datetime.utcnow().isoformat() + 'Z',
                'access_level': 'read_only',
                'data_source': 'primal_genesis_core'
            },
            'system_snapshot': snapshot
        }
    
    def observe_recent_activity(self, limit: int = 10) -> Dict:
        """
        Observe recent system activity.
        
        Args:
            limit: Maximum number of activities to observe
            
        Returns:
            Dict with read-only recent activity
        """
        activity = self.visibility.get_recent_activity(limit=limit)
        
        return {
            'observer_metadata': {
                'observer_id': self._observer_id,
                'observation_time': datetime.utcnow().isoformat() + 'Z',
                'access_level': 'read_only',
                'data_source': 'primal_genesis_memory'
            },
            'recent_activity': activity
        }
    
    def observe_module_state(self) -> Dict:
        """
        Observe module state and health.
        
        Returns:
            Dict with read-only module information
        """
        module_health = self.visibility.get_module_health()
        
        return {
            'observer_metadata': {
                'observer_id': self._observer_id,
                'observation_time': datetime.utcnow().isoformat() + 'Z',
                'access_level': 'read_only',
                'data_source': 'primal_genesis_registry'
            },
            'module_state': module_health
        }
    
    def observe_policy_overview(self) -> Dict:
        """
        Observe policy system overview.
        
        Returns:
            Dict with read-only policy information
        """
        policy_overview = self.visibility.get_policy_overview()
        
        return {
            'observer_metadata': {
                'observer_id': self._observer_id,
                'observation_time': datetime.utcnow().isoformat() + 'Z',
                'access_level': 'read_only',
                'data_source': 'primal_genesis_policy'
            },
            'policy_overview': policy_overview
        }
    
    def observe_memory_statistics(self) -> Dict:
        """
        Observe memory system statistics.
        
        Returns:
            Dict with read-only memory information
        """
        memory_stats = self.visibility.get_memory_statistics()
        
        return {
            'observer_metadata': {
                'observer_id': self._observer_id,
                'observation_time': datetime.utcnow().isoformat() + 'Z',
                'access_level': 'read_only',
                'data_source': 'primal_genesis_memory'
            },
            'memory_statistics': memory_stats
        }
    
    def observe_execution_patterns(self) -> Dict:
        """
        Observe execution patterns and trends.
        
        Returns:
            Dict with execution pattern analysis
        """
        recent_activity = self.visibility.get_recent_activity(limit=50)
        activities = recent_activity.get('activities', [])
        
        # Analyze execution patterns
        execution_patterns = {
            'total_actions': len(activities),
            'successful_actions': len([a for a in activities if a['event_type'] == 'action_executed']),
            'denied_actions': len([a for a in activities if a['event_type'] == 'action_denied']),
            'failed_actions': len([a for a in activities if a['event_type'] == 'action_failed']),
            'validation_failures': len([a for a in activities if a['event_type'] == 'validation_failure']),
            'active_modules': list(set(a['module'] for a in activities)),
            'action_distribution': self._analyze_action_distribution(activities),
            'module_activity': self._analyze_module_activity(activities),
            'time_patterns': self._analyze_time_patterns(activities),
            'success_rate': self._calculate_success_rate(activities)
        }
        
        return {
            'observer_metadata': {
                'observer_id': self._observer_id,
                'observation_time': datetime.utcnow().isoformat() + 'Z',
                'access_level': 'read_only',
                'data_source': 'primal_genesis_runtime_analysis'
            },
            'execution_patterns': execution_patterns
        }
    
    def observe_system_trends(self) -> Dict:
        """
        Observe system trends and deeper insights.
        
        Returns:
            Dict with trend analysis and insights
        """
        recent_activity = self.visibility.get_recent_activity(limit=100)
        activities = recent_activity.get('activities', [])
        
        # Analyze trends
        trends = {
            'activity_trend': self._analyze_activity_trend(activities),
            'module_usage_trend': self._analyze_module_usage_trend(activities),
            'policy_effectiveness': self._analyze_policy_effectiveness(activities),
            'system_stability': self._analyze_system_stability(activities),
            'performance_indicators': self._calculate_performance_indicators(activities)
        }
        
        return {
            'observer_metadata': {
                'observer_id': self._observer_id,
                'observation_time': datetime.utcnow().isoformat() + 'Z',
                'access_level': 'read_only',
                'data_source': 'primal_genesis_trends'
            },
            'system_trends': trends
        }
    
    def observe_detailed_module_state(self) -> Dict:
        """
        Observe detailed module state with richer information.
        
        Returns:
            Dict with detailed module analysis
        """
        module_health = self.visibility.get_module_health()
        recent_activity = self.visibility.get_recent_activity(limit=50)
        
        # Analyze module-specific activity
        detailed_state = {}
        for module in module_health['module_details']:
            module_name = module['name']
            module_activities = [a for a in recent_activity.get('activities', []) 
                             if a['module'] == module_name]
            
            detailed_state[module_name] = {
                'basic_info': {
                    'type': module['type'],
                    'enabled': module['enabled'],
                    'location': module['location'],
                    'entrypoint': module['entrypoint'],
                    'description': module['description'],
                    'version': module['version']
                },
                'recent_activity': {
                    'total_actions': len(module_activities),
                    'last_action': module_activities[0]['event_type'] if module_activities else None,
                    'last_action_time': module_activities[0]['timestamp'] if module_activities else None,
                    'action_types': list(set(a['event_type'] for a in module_activities))
                },
                'health_indicators': {
                    'recent_success_rate': self._calculate_module_success_rate(module_activities),
                    'activity_level': 'active' if len(module_activities) > 0 else 'inactive'
                }
            }
        
        return {
            'observer_metadata': {
                'observer_id': self._observer_id,
                'observation_time': datetime.utcnow().isoformat() + 'Z',
                'access_level': 'read_only',
                'data_source': 'primal_genesis_detailed_state'
            },
            'detailed_module_state': detailed_state
        }
    
    # Helper methods for deeper analysis
    def _analyze_action_distribution(self, activities: List[Dict]) -> Dict:
        """Analyze distribution of action types."""
        distribution = {}
        for activity in activities:
            event_type = activity['event_type']
            if event_type not in distribution:
                distribution[event_type] = 0
            distribution[event_type] += 1
        return distribution
    
    def _analyze_module_activity(self, activities: List[Dict]) -> Dict:
        """Analyze activity by module."""
        module_activity = {}
        for activity in activities:
            module = activity['module']
            if module not in module_activity:
                module_activity[module] = []
            module_activity[module].append(activity['event_type'])
        return module_activity
    
    def _analyze_time_patterns(self, activities: List[Dict]) -> Dict:
        """Analyze time-based patterns in activities."""
        if not activities:
            return {'pattern': 'no_data'}
        
        # Simple time pattern analysis
        hourly_distribution = {}
        for activity in activities:
            try:
                hour = int(activity['timestamp'][11:13])  # Extract hour from ISO timestamp
                if hour not in hourly_distribution:
                    hourly_distribution[hour] = 0
                hourly_distribution[hour] += 1
            except:
                continue
        
        return {
            'total_activities': len(activities),
            'hourly_distribution': hourly_distribution,
            'peak_hour': max(hourly_distribution.items(), key=lambda x: x[1])[0] if hourly_distribution else None
        }
    
    def _calculate_success_rate(self, activities: List[Dict]) -> float:
        """Calculate success rate of actions."""
        if not activities:
            return 0.0
        
        successful = len([a for a in activities if a['event_type'] == 'action_executed'])
        total = len([a for a in activities if a['event_type'] in ['action_executed', 'action_denied', 'action_failed']])
        
        return (successful / total * 100) if total > 0 else 0.0
    
    def _analyze_activity_trend(self, activities: List[Dict]) -> Dict:
        """Analyze activity trend over time."""
        if len(activities) < 2:
            return {'trend': 'insufficient_data'}
        
        # Simple trend analysis based on recent vs older activities
        mid_point = len(activities) // 2
        recent_half = activities[:mid_point]
        older_half = activities[mid_point:]
        
        recent_count = len([a for a in recent_half if a['event_type'] == 'action_executed'])
        older_count = len([a for a in older_half if a['event_type'] == 'action_executed'])
        
        if recent_count > older_count:
            trend = 'increasing'
        elif recent_count < older_count:
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'recent_success_rate': (recent_count / len(recent_half) * 100) if len(recent_half) > 0 else 0.0,
            'older_success_rate': (older_count / len(older_half) * 100) if len(older_half) > 0 else 0.0
        }
    
    def _analyze_module_usage_trend(self, activities: List[Dict]) -> Dict:
        """Analyze module usage trends."""
        module_usage = {}
        for activity in activities:
            module = activity['module']
            if module not in module_usage:
                module_usage[module] = 0
            module_usage[module] += 1
        
        # Sort by usage
        sorted_modules = sorted(module_usage.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'total_modules': len(module_usage),
            'active_modules': len([m for m in module_usage.values() if m > 0]),
            'top_modules': sorted_modules[:5],
            'usage_distribution': module_usage
        }
    
    def _analyze_policy_effectiveness(self, activities: List[Dict]) -> Dict:
        """Analyze policy effectiveness."""
        policy_actions = [a for a in activities if a['event_type'] in ['action_denied', 'action_executed']]
        
        if not policy_actions:
            return {'effectiveness': 'no_data'}
        
        denied = len([a for a in policy_actions if a['event_type'] == 'action_denied'])
        total = len(policy_actions)
        
        effectiveness = ((total - denied) / total * 100) if total > 0 else 100.0
        
        return {
            'total_policy_evaluations': total,
            'denied_actions': denied,
            'allowed_actions': total - denied,
            'effectiveness_rate': effectiveness,
            'effectiveness_level': 'high' if effectiveness >= 80 else 'medium' if effectiveness >= 60 else 'low'
        }
    
    def _analyze_system_stability(self, activities: List[Dict]) -> Dict:
        """Analyze system stability indicators."""
        if not activities:
            return {'stability': 'no_data'}
        
        # Calculate stability metrics
        error_activities = [a for a in activities if a['event_type'] in ['action_failed', 'validation_failure']]
        total_activities = len(activities)
        
        error_rate = (len(error_activities) / total_activities * 100) if total_activities > 0 else 0.0
        
        return {
            'stability_level': 'stable' if error_rate < 5 else 'unstable' if error_rate < 15 else 'critical',
            'error_rate': error_rate,
            'total_errors': len(error_activities),
            'error_types': list(set(a['event_type'] for a in error_activities))
        }
    
    def _calculate_performance_indicators(self, activities: List[Dict]) -> Dict:
        """Calculate performance indicators."""
        if not activities:
            return {'performance': 'no_data'}
        
        successful_actions = [a for a in activities if a['event_type'] == 'action_executed']
        total_actions = len([a for a in activities if a['event_type'] in ['action_executed', 'action_denied', 'action_failed']])
        
        return {
            'throughput': len(successful_actions),
            'success_rate': (len(successful_actions) / total_actions * 100) if total_actions > 0 else 0.0,
            'activity_level': 'high' if len(successful_actions) > 10 else 'medium' if len(successful_actions) > 5 else 'low'
        }
    
    def _calculate_module_success_rate(self, module_activities: List[Dict]) -> float:
        """Calculate success rate for specific module."""
        if not module_activities:
            return 0.0
        
        successful = len([a for a in module_activities if a['event_type'] == 'action_executed'])
        total = len([a for a in module_activities if a['event_type'] in ['action_executed', 'action_denied', 'action_failed']])
        
        return (successful / total * 100) if total > 0 else 0.0
    
    def observe_system_health(self) -> Dict:
        """
        Observe overall system health and status.
        
        Returns:
            Dict with system health assessment
        """
        module_state = self.visibility.get_module_health()
        policy_overview = self.visibility.get_policy_overview()
        memory_stats = self.visibility.get_memory_statistics()
        
        # Calculate health indicators
        health_indicators = {
            'module_health_score': self._calculate_module_health_score(module_state),
            'policy_health_score': self._calculate_policy_health_score(policy_overview),
            'memory_health_score': self._calculate_memory_health_score(memory_stats),
            'overall_health_score': 0.0,  # Will be calculated below
            'health_status': 'unknown',
            'recommendations': []
        }
        
        # Calculate overall health
        overall_score = (
            health_indicators['module_health_score'] * 0.4 +
            health_indicators['policy_health_score'] * 0.3 +
            health_indicators['memory_health_score'] * 0.3
        )
        health_indicators['overall_health_score'] = overall_score
        
        # Determine health status
        if overall_score >= 0.9:
            health_indicators['health_status'] = 'excellent'
        elif overall_score >= 0.7:
            health_indicators['health_status'] = 'good'
        elif overall_score >= 0.5:
            health_indicators['health_status'] = 'fair'
        else:
            health_indicators['health_status'] = 'poor'
            health_indicators['recommendations'].append('System health is below optimal levels')
        
        return {
            'observer_metadata': {
                'observer_id': self._observer_id,
                'observation_time': datetime.utcnow().isoformat() + 'Z',
                'access_level': 'read_only',
                'data_source': 'primal_genesis_health_analysis'
            },
            'system_health': health_indicators
        }
    
    def _analyze_action_distribution(self, activities: List[Dict]) -> Dict:
        """Analyze distribution of action types."""
        distribution = {}
        for activity in activities:
            event_type = activity['event_type']
            if event_type not in distribution:
                distribution[event_type] = 0
            distribution[event_type] += 1
        return distribution
    
    def _analyze_time_distribution(self, activities: List[Dict]) -> Dict:
        """Analyze time-based distribution of activities."""
        if not activities:
            return {'pattern': 'no_activity'}
        
        # Simple time-based analysis
        timestamps = [activity['timestamp'] for activity in activities]
        return {
            'pattern': 'active',
            'first_activity': timestamps[-1] if timestamps else None,
            'last_activity': timestamps[0] if timestamps else None,
            'activity_span': len(timestamps)
        }
    
    def _calculate_module_health_score(self, module_state: Dict) -> float:
        """Calculate module health score (0.0 to 1.0)."""
        total_modules = module_state.get('total_modules', 0)
        enabled_modules = module_state.get('enabled_modules', 0)
        
        if total_modules == 0:
            return 0.0
        
        # Health based on enabled module ratio
        return enabled_modules / total_modules
    
    def _calculate_policy_health_score(self, policy_overview: Dict) -> float:
        """Calculate policy health score (0.0 to 1.0)."""
        total_policies = policy_overview.get('total_policies', 0)
        enabled_policies = policy_overview.get('enabled_policies', 0)
        
        if total_policies == 0:
            return 0.0
        
        # Health based on enabled policy ratio
        return enabled_policies / total_policies
    
    def _calculate_memory_health_score(self, memory_stats: Dict) -> float:
        """Calculate memory health score (0.0 to 1.0)."""
        total_memories = memory_stats.get('total_memories', 0)
        
        if total_memories == 0:
            return 0.5  # Neutral score for empty memory
        
        # Health based on recent activity (simple heuristic)
        recent_activity = memory_stats.get('recent_activity', 0)
        activity_ratio = min(recent_activity / max(total_memories, 1), 1.0)
        
        return 0.5 + (activity_ratio * 0.5)  # Scale from 0.5 to 1.0
    
    def get_observer_info(self) -> Dict:
        """
        Get information about this observer instance.
        
        Returns:
            Dict with observer metadata
        """
        return {
            'observer_id': self._observer_id,
            'access_level': 'read_only',
            'capabilities': [
                'observe_system_snapshot',
                'observe_recent_activity',
                'observe_module_state',
                'observe_policy_overview',
                'observe_memory_statistics',
                'observe_execution_patterns',
                'observe_system_health'
            ],
            'restrictions': [
                'no_mutation_capabilities',
                'no_execution_capabilities',
                'no_policy_modification',
                'no_memory_modification',
                'no_module_enable_disable'
            ],
            'created_at': self._observer_id.split('_')[-1],
            'data_sources': [
                'primal_genesis_core',
                'primal_genesis_registry',
                'primal_genesis_policy',
                'primal_genesis_memory',
                'primal_genesis_runtime_analysis',
                'primal_genesis_health_analysis'
            ]
        }
