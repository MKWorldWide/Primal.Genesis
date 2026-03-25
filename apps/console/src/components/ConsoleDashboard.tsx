/**
 * @file ConsoleDashboard.tsx
 * @description Main console dashboard component for Primal Genesis Engine
 * Provides real command-center UI with API integration
 */

import React, { useState, useEffect } from 'react';
import { apiClient, HealthResponse, SystemSnapshot, ModuleOverview, PolicyOverview, RecentActivity, ExecutionRequest, ExecutionResponse } from '../services/api';

import './styles/ConsoleDashboard.css';

interface ConsoleDashboardProps {
  /** Optional title override */
  title?: string;
}

/**
 * Main console dashboard that displays real engine state
 */
const ConsoleDashboard: React.FC<ConsoleDashboardProps> = ({ title = "Primal Genesis Console" }) => {
  // State management
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [systemSnapshot, setSystemSnapshot] = useState<SystemSnapshot | null>(null);
  const [moduleOverview, setModuleOverview] = useState<ModuleOverview | null>(null);
  const [policyOverview, setPolicyOverview] = useState<PolicyOverview | null>(null);
  const [recentActivity, setRecentActivity] = useState<RecentActivity | null>(null);
  
  // Loading states
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  
  // Runtime execution state
  const [executionRequest, setExecutionRequest] = useState<ExecutionRequest>({
    module_name: '',
    action_name: '',
    payload: {}
  });
  const [executionResult, setExecutionResult] = useState<ExecutionResponse | null>(null);
  const [executing, setExecuting] = useState<boolean>(false);

  // Fetch all data on component mount
  useEffect(() => {
    fetchAllData();
  }, []);

  /**
   * Fetch all dashboard data
   */
  const fetchAllData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Parallel fetch all data
      const [
        healthData,
        snapshotData,
        moduleData,
        policyData,
        activityData
      ] = await Promise.all([
        apiClient.getHealth(),
        apiClient.getSystemSnapshot(),
        apiClient.getModuleOverview(),
        apiClient.getPolicyOverview(),
        apiClient.getRecentActivity(10)
      ]);

      setHealth(healthData);
      setSystemSnapshot(snapshotData);
      setModuleOverview(moduleData);
      setPolicyOverview(policyData);
      setRecentActivity(activityData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch dashboard data');
      console.error('Dashboard data fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handle runtime execution
   */
  const handleExecuteAction = async () => {
    if (!executionRequest.module_name || !executionRequest.action_name) {
      setError('Module name and action name are required');
      return;
    }

    setExecuting(true);
    setExecutionResult(null);
    setError(null);

    try {
      const result = await apiClient.executeModuleAction(executionRequest);
      setExecutionResult(result);
      
      // Refresh data after execution
      fetchAllData();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Execution failed');
      console.error('Runtime execution error:', err);
    } finally {
      setExecuting(false);
    }
  };

  /**
   * Format timestamp for display
   */
  const formatTimestamp = (timestamp: string): string => {
    try {
      return new Date(timestamp).toLocaleString();
    } catch {
      return timestamp;
    }
  };

  /**
   * Get status class for styling
   */
  const getStatusClass = (status: string): string => {
    switch (status.toLowerCase()) {
      case 'healthy':
      case 'operational':
      case 'enabled':
        return 'status-good';
      case 'warning':
      case 'degraded':
        return 'status-warning';
      case 'error':
      case 'failed':
      case 'disabled':
        return 'status-error';
      default:
        return 'status-unknown';
    }
  };

  // Loading state
  if (loading && !health) {
    return (
      <div className="console-dashboard">
        <div className="loading-state">
          <h1>{title}</h1>
          <div className="loading-spinner"></div>
          <p>Loading engine state...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error && !health) {
    return (
      <div className="console-dashboard">
        <div className="error-state">
          <h1>{title}</h1>
          <div className="error-message">
            <h2>Connection Error</h2>
            <p>{error}</p>
            <button onClick={fetchAllData} className="retry-button">
              Retry Connection
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="console-dashboard">
      <header className="dashboard-header">
        <h1>{title}</h1>
        <div className="header-status">
          <span className={`status-indicator ${getStatusClass(health?.status || 'unknown')}`}>
            {health?.status || 'Unknown'}
          </span>
          <span className="execution-mode">
            {health?.execution_mode || 'Unknown'}
          </span>
        </div>
        <button onClick={fetchAllData} className="refresh-button">
          Refresh All
        </button>
      </header>

      {error && (
        <div className="error-banner">
          <span className="error-text">{error}</span>
          <button onClick={() => setError(null)} className="dismiss-error">
            ×
          </button>
        </div>
      )}

      <div className="dashboard-grid">
        {/* System Status Section */}
        <section className="status-section">
          <h2>System Status</h2>
          {systemSnapshot && (
            <div className="status-grid">
              <div className="status-item">
                <label>System Status</label>
                <span className={`status-value ${getStatusClass(systemSnapshot.system_status.status)}`}>
                  {systemSnapshot.system_status.status}
                </span>
              </div>
              <div className="status-item">
                <label>Version</label>
                <span className="status-value">{systemSnapshot.system_status.version}</span>
              </div>
              <div className="status-item">
                <label>Uptime</label>
                <span className="status-value">{systemSnapshot.system_status.uptime}</span>
              </div>
              <div className="status-item">
                <label>Last Updated</label>
                <span className="status-value">
                  {formatTimestamp(systemSnapshot.timestamp)}
                </span>
              </div>
            </div>
          )}
        </section>

        {/* Module Overview Section */}
        <section className="modules-section">
          <h2>Module Overview</h2>
          {moduleOverview && (
            <div className="modules-summary">
              <div className="summary-stats">
                <div className="stat-item">
                  <label>Total Modules</label>
                  <span className="stat-value">{moduleOverview.summary.total_modules}</span>
                </div>
                <div className="stat-item">
                  <label>Enabled</label>
                  <span className="stat-value status-good">{moduleOverview.summary.enabled_modules}</span>
                </div>
                <div className="stat-item">
                  <label>Disabled</label>
                  <span className="stat-value status-error">{moduleOverview.summary.disabled_modules}</span>
                </div>
                <div className="stat-item">
                  <label>Health</label>
                  <span className="stat-value">{moduleOverview.summary.health_percentage}%</span>
                </div>
              </div>
              
              <div className="modules-list">
                <h3>Module Details</h3>
                <div className="module-grid">
                  {moduleOverview.module_details.map((module, index) => (
                    <div key={index} className={`module-card ${module.enabled ? 'enabled' : 'disabled'}`}>
                      <h4>{module.name}</h4>
                      <div className="module-info">
                        <span className="module-type">{module.type}</span>
                        <span className={`module-status ${getStatusClass(module.enabled ? 'enabled' : 'disabled')}`}>
                          {module.enabled ? 'Enabled' : 'Disabled'}
                        </span>
                      </div>
                      <div className="module-details">
                        <p><strong>Location:</strong> {module.location}</p>
                        <p><strong>Entrypoint:</strong> {module.entrypoint}</p>
                        <p><strong>Version:</strong> {module.version}</p>
                        {module.description && (
                          <p><strong>Description:</strong> {module.description}</p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </section>

        {/* Recent Activity Section */}
        <section className="activity-section">
          <h2>Recent Activity</h2>
          {recentActivity && (
            <div className="activity-feed">
              <div className="activity-summary">
                <span className="activity-count">
                  {recentActivity.summary.total_activities} activities
                </span>
                <span className="activity-level">
                  Level: {recentActivity.summary.activity_level}
                </span>
              </div>
              
              {recentActivity.activities.length > 0 ? (
                <div className="activity-list">
                  {recentActivity.activities.map((activity, index) => (
                    <div key={activity.id} className="activity-item">
                      <div className="activity-header">
                        <span className="activity-module">{activity.module}</span>
                        <span className="activity-type">{activity.event_type}</span>
                        <span className="activity-timestamp">
                          {formatTimestamp(activity.timestamp)}
                        </span>
                      </div>
                      <div className="activity-content">
                        <p>{activity.content}</p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="no-activity">
                  <p>No recent activity to display</p>
                </div>
              )}
            </div>
          )}
        </section>

        {/* Policy Summary Section */}
        <section className="policy-section">
          <h2>Policy Summary</h2>
          {policyOverview && (
            <div className="policy-summary">
              <div className="policy-stats">
                <div className="stat-item">
                  <label>Total Policies</label>
                  <span className="stat-value">{policyOverview.total_policies}</span>
                </div>
                <div className="stat-item">
                  <label>Enabled</label>
                  <span className="stat-value status-good">{policyOverview.enabled_policies}</span>
                </div>
                <div className="stat-item">
                  <label>Disabled</label>
                  <span className="stat-value status-error">{policyOverview.disabled_policies}</span>
                </div>
                <div className="stat-item">
                  <label>Default Behavior</label>
                  <span className="stat-value">{policyOverview.default_behavior}</span>
                </div>
              </div>
            </div>
          )}
        </section>

        {/* Runtime Action Panel */}
        <section className="runtime-section">
          <h2>Runtime Action Panel</h2>
          <div className="runtime-panel">
            <div className="runtime-warning">
              <p><strong>⚠️ Local Simulated Execution Only</strong></p>
              <p>Actions are executed locally in simulation mode, not as real external operations.</p>
            </div>
            
            <div className="execution-form">
              <div className="form-group">
                <label htmlFor="module-name">Module Name:</label>
                <input
                  id="module-name"
                  type="text"
                  value={executionRequest.module_name}
                  onChange={(e) => setExecutionRequest({
                    ...executionRequest,
                    module_name: e.target.value
                  })}
                  placeholder="Enter module name"
                  className="form-input"
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="action-name">Action Name:</label>
                <input
                  id="action-name"
                  type="text"
                  value={executionRequest.action_name}
                  onChange={(e) => setExecutionRequest({
                    ...executionRequest,
                    action_name: e.target.value
                  })}
                  placeholder="Enter action name"
                  className="form-input"
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="payload">Payload (JSON):</label>
                <textarea
                  id="payload"
                  value={JSON.stringify(executionRequest.payload || {}, null, 2)}
                  onChange={(e) => {
                    try {
                      const payload = JSON.parse(e.target.value);
                      setExecutionRequest({
                        ...executionRequest,
                        payload
                      });
                    } catch {
                      // Invalid JSON, keep current payload
                    }
                  }}
                  placeholder='{"key": "value"}'
                  className="form-textarea"
                  rows={4}
                />
              </div>
              
              <button
                onClick={handleExecuteAction}
                disabled={executing || !executionRequest.module_name || !executionRequest.action_name}
                className="execute-button"
              >
                {executing ? 'Executing...' : 'Execute Action'}
              </button>
            </div>
            
            {executionResult && (
              <div className="execution-result">
                <h3>Execution Result</h3>
                <div className="result-details">
                  <div className="result-item">
                    <label>Executed:</label>
                    <span className={`result-value ${executionResult.executed ? 'success' : 'error'}`}>
                      {executionResult.executed ? 'Yes' : 'No'}
                    </span>
                  </div>
                  <div className="result-item">
                    <label>Outcome:</label>
                    <span className="result-value">{executionResult.outcome}</span>
                  </div>
                  <div className="result-item">
                    <label>Execution Mode:</label>
                    <span className="result-value">{executionResult.execution_mode}</span>
                  </div>
                  <div className="result-item">
                    <label>Scope:</label>
                    <span className="result-value">{executionResult.execution_details.execution_scope}</span>
                  </div>
                  <div className="result-item">
                    <label>Side Effects:</label>
                    <span className="result-value">{executionResult.execution_details.side_effect_level}</span>
                  </div>
                  {executionResult.message && (
                    <div className="result-message">
                      <label>Message:</label>
                      <span className="result-value">{executionResult.message}</span>
                    </div>
                  )}
                  {executionResult.error && (
                    <div className="result-error">
                      <label>Error:</label>
                      <span className="result-value">{executionResult.error}</span>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </section>
      </div>
    </div>
  );
};

export default ConsoleDashboard;
