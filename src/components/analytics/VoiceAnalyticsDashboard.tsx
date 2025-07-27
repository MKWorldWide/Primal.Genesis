/**
 * @file VoiceAnalyticsDashboard.tsx
 * @description Dashboard component for visualizing voice system analytics data.
 * Implements the System of Surveillance for Detection principles through transparent
 * data visualization and tracking.
 */

import React, { useState, useEffect, useMemo } from 'react';
import { AnalyticsService } from '../../services/analytics/AnalyticsService';
import { EVENT_DEFINITIONS } from '../../config/analytics-config';
import './styles/VoiceAnalyticsDashboard.css';

// Mock data types
interface MetricData {
  /** Metric name */
  name: string;
  /** Metric value */
  value: number;
  /** Previous value for comparison */
  previousValue?: number;
  /** Unit of measurement */
  unit?: string;
  /** Whether the metric is trending up */
  trendUp?: boolean;
  /** Change percentage */
  changePercent?: number;
}

interface ChartData {
  /** Labels for the chart */
  labels: string[];
  /** Data series */
  series: number[][];
  /** Series names */
  seriesNames: string[];
}

interface AnalyticsMetrics {
  /** Summary metrics */
  summaryMetrics: MetricData[];
  /** Voice recording metrics */
  voiceRecordingMetrics: ChartData;
  /** Command success rate data */
  commandSuccessRate: ChartData;
  /** Recent voice activities */
  recentActivities: Activity[];
}

interface Activity {
  /** Activity ID */
  id: string;
  /** Activity timestamp */
  timestamp: number;
  /** Activity type */
  type: string;
  /** Activity duration */
  durationMs?: number;
  /** Success status */
  success: boolean;
  /** Associated command */
  command?: string;
  /** Error message if applicable */
  error?: string;
}

interface VoiceAnalyticsDashboardProps {
  /** Analytics service instance */
  analyticsService?: AnalyticsService;
  /** Refresh interval in milliseconds */
  refreshInterval?: number;
  /** Whether to use real data or mock data */
  useRealData?: boolean;
}

/**
 * VoiceAnalyticsDashboard component that displays analytics for the voice system.
 * Provides transparency into system usage aligned with the System of Surveillance principles.
 */
const VoiceAnalyticsDashboard: React.FC<VoiceAnalyticsDashboardProps> = ({
  analyticsService,
  refreshInterval = 30000,
  useRealData = false
}) => {
  // State for analytics data
  const [analyticsData, setAnalyticsData] = useState<AnalyticsMetrics | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState<string>('day');
  
  // Create analytics service if not provided
  const service = useMemo(() => {
    return analyticsService || new AnalyticsService();
  }, [analyticsService]);
  
  // Fetch analytics data
  const fetchAnalyticsData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      if (useRealData) {
        // In a real implementation, this would fetch data from a real analytics API
        // For now, we'll use mock data
        console.log('Fetching real analytics data would happen here');
      }
      
      // For this example, we're using mock data
      const mockData = generateMockData(timeRange);
      
      setAnalyticsData(mockData);
    } catch (err) {
      setError('Failed to load analytics data');
      console.error('Analytics data fetch error:', err);
    } finally {
      setLoading(false);
    }
  };
  
  // Generate mock data for the dashboard
  const generateMockData = (range: string): AnalyticsMetrics => {
    const now = new Date();
    const dayLabels = Array(24).fill(0).map((_, i) => `${i}:00`);
    const weekLabels = Array(7).fill(0).map((_, i) => {
      const date = new Date();
      date.setDate(date.getDate() - i);
      return date.toLocaleDateString('en-US', { weekday: 'short' });
    }).reverse();
    const monthLabels = Array(30).fill(0).map((_, i) => {
      const date = new Date();
      date.setDate(date.getDate() - i);
      return date.getDate().toString();
    }).reverse();
    
    const labels = range === 'day' ? dayLabels : range === 'week' ? weekLabels : monthLabels;
    
    // Generate random data for voice recordings
    const voiceRecordingData = Array(labels.length).fill(0).map(() => Math.floor(Math.random() * 100));
    const successfulCommandData = Array(labels.length).fill(0).map(() => Math.floor(Math.random() * 80));
    
    // Activities with timestamps spread over the selected time range
    const activities: Activity[] = [];
    const activityTypes = [
      EVENT_DEFINITIONS.VOICE_SYSTEM.RECORDING_STARTED,
      EVENT_DEFINITIONS.VOICE_SYSTEM.RECORDING_STOPPED,
      EVENT_DEFINITIONS.VOICE_SYSTEM.RECORDING_PROCESSED,
      EVENT_DEFINITIONS.VOICE_SYSTEM.COMMAND_RECOGNIZED,
      EVENT_DEFINITIONS.VOICE_SYSTEM.COMMAND_EXECUTED
    ];
    
    const mockCommands = [
      'Create new task',
      'Send message to Alex',
      'Set reminder for meeting',
      'Check weather',
      'Play music',
      'Search for restaurants',
      'Navigate to home'
    ];
    
    // Create mock activities
    for (let i = 0; i < 20; i++) {
      const timestamp = now.getTime() - Math.floor(Math.random() * 86400000); // Within past 24 hours
      const typeIndex = Math.floor(Math.random() * activityTypes.length);
      const type = activityTypes[typeIndex];
      const success = Math.random() > 0.2; // 80% success rate
      
      activities.push({
        id: `activity-${i}`,
        timestamp,
        type,
        durationMs: Math.floor(Math.random() * 10000), // 0-10 seconds
        success,
        command: type === EVENT_DEFINITIONS.VOICE_SYSTEM.COMMAND_RECOGNIZED ? mockCommands[Math.floor(Math.random() * mockCommands.length)] : undefined,
        error: !success ? 'Command not recognized' : undefined
      });
    }
    
    // Sort activities by timestamp (most recent first)
    activities.sort((a, b) => b.timestamp - a.timestamp);
    
    // Calculate total recordings
    const totalRecordings = voiceRecordingData.reduce((sum, value) => sum + value, 0);
    const totalCommands = successfulCommandData.reduce((sum, value) => sum + value, 0);
    const avgDurationMs = activities
      .filter(a => a.durationMs !== undefined)
      .reduce((sum, a) => sum + (a.durationMs || 0), 0) / activities.length;
    const successRate = Math.round((activities.filter(a => a.success).length / activities.length) * 100);
    
    return {
      summaryMetrics: [
        {
          name: 'Total Recordings',
          value: totalRecordings,
          previousValue: totalRecordings * 0.9,
          changePercent: 10,
          trendUp: true
        },
        {
          name: 'Total Commands',
          value: totalCommands,
          previousValue: totalCommands * 0.85,
          changePercent: 15,
          trendUp: true
        },
        {
          name: 'Avg. Duration',
          value: Math.round(avgDurationMs),
          unit: 'ms',
          previousValue: avgDurationMs * 1.05,
          changePercent: -5,
          trendUp: false
        },
        {
          name: 'Success Rate',
          value: successRate,
          unit: '%',
          previousValue: successRate - 2,
          changePercent: 2,
          trendUp: true
        },
      ],
      voiceRecordingMetrics: {
        labels,
        series: [voiceRecordingData],
        seriesNames: ['Voice Recordings']
      },
      commandSuccessRate: {
        labels,
        series: [successfulCommandData, voiceRecordingData.map(v => v - Math.floor(Math.random() * v * 0.3))],
        seriesNames: ['Successful Commands', 'Total Commands']
      },
      recentActivities: activities.slice(0, 10)
    };
  };
  
  // Format timestamp to human-readable format
  const formatTimestamp = (timestamp: number): string => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };
  
  // Format duration to human-readable format
  const formatDuration = (durationMs?: number): string => {
    if (durationMs === undefined) return 'N/A';
    
    if (durationMs < 1000) {
      return `${durationMs}ms`;
    } else {
      return `${(durationMs / 1000).toFixed(1)}s`;
    }
  };
  
  // Get event type display name
  const getEventTypeDisplay = (type: string): string => {
    switch (type) {
      case EVENT_DEFINITIONS.VOICE_SYSTEM.RECORDING_STARTED:
        return 'Recording Started';
      case EVENT_DEFINITIONS.VOICE_SYSTEM.RECORDING_STOPPED:
        return 'Recording Stopped';
      case EVENT_DEFINITIONS.VOICE_SYSTEM.RECORDING_PROCESSED:
        return 'Recording Processed';
      case EVENT_DEFINITIONS.VOICE_SYSTEM.COMMAND_RECOGNIZED:
        return 'Command Recognized';
      case EVENT_DEFINITIONS.VOICE_SYSTEM.COMMAND_EXECUTED:
        return 'Command Executed';
      default:
        return type;
    }
  };
  
  // Fetch data on component mount and when time range changes
  useEffect(() => {
    fetchAnalyticsData();
    
    // Set up refresh interval
    const intervalId = setInterval(fetchAnalyticsData, refreshInterval);
    
    // Clean up interval on unmount
    return () => clearInterval(intervalId);
  }, [timeRange, refreshInterval]);
  
  if (error) {
    return (
      <div className="analytics-error">
        <h2>Analytics Error</h2>
        <p>{error}</p>
        <button onClick={fetchAnalyticsData}>Retry</button>
      </div>
    );
  }
  
  if (loading && !analyticsData) {
    return (
      <div className="analytics-loading">
        <h2>Loading Analytics Data...</h2>
        <div className="loading-spinner"></div>
      </div>
    );
  }
  
  if (!analyticsData) {
    return (
      <div className="analytics-empty">
        <h2>No Analytics Data Available</h2>
        <p>There is no data to display for the selected time range.</p>
      </div>
    );
  }
  
  return (
    <div className="analytics-dashboard">
      <header className="dashboard-header">
        <h1>Voice System Analytics Dashboard</h1>
        <div className="time-range-selector">
          <button 
            className={timeRange === 'day' ? 'active' : ''} 
            onClick={() => setTimeRange('day')}
          >
            Day
          </button>
          <button 
            className={timeRange === 'week' ? 'active' : ''} 
            onClick={() => setTimeRange('week')}
          >
            Week
          </button>
          <button 
            className={timeRange === 'month' ? 'active' : ''} 
            onClick={() => setTimeRange('month')}
          >
            Month
          </button>
        </div>
      </header>
      
      <section className="metrics-summary">
        <h2>Key Metrics</h2>
        <div className="metrics-grid">
          {analyticsData.summaryMetrics.map((metric, index) => (
            <div key={index} className="metric-card">
              <h3>{metric.name}</h3>
              <div className="metric-value">
                {metric.value}{metric.unit}
                {metric.changePercent !== undefined && (
                  <span className={`trend ${metric.trendUp ? 'up' : 'down'}`}>
                    {metric.trendUp ? '↑' : '↓'} {Math.abs(metric.changePercent)}%
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </section>
      
      <section className="chart-section">
        <div className="chart-container">
          <h2>Voice Recordings</h2>
          <div className="chart-placeholder">
            {/* In a real implementation, this would be a chart component */}
            <div className="chart-bars">
              {analyticsData.voiceRecordingMetrics.series[0].map((value, index) => (
                <div 
                  key={index} 
                  className="chart-bar" 
                  style={{ height: `${(value / Math.max(...analyticsData.voiceRecordingMetrics.series[0])) * 100}%` }}
                  title={`${analyticsData.voiceRecordingMetrics.labels[index]}: ${value} recordings`}
                />
              ))}
            </div>
            <div className="chart-labels">
              {analyticsData.voiceRecordingMetrics.labels.map((label, index) => (
                <span key={index} className="chart-label">
                  {index % 3 === 0 ? label : ''}
                </span>
              ))}
            </div>
          </div>
        </div>
        
        <div className="chart-container">
          <h2>Command Success Rate</h2>
          <div className="chart-placeholder">
            {/* In a real implementation, this would be a chart component */}
            <div className="chart-bars stacked">
              {analyticsData.commandSuccessRate.series[0].map((value, index) => (
                <div 
                  key={index} 
                  className="chart-bar-container"
                  title={`${analyticsData.commandSuccessRate.labels[index]}`}
                >
                  <div 
                    className="chart-bar success" 
                    style={{ 
                      height: `${(value / analyticsData.commandSuccessRate.series[1][index]) * 100}%` 
                    }}
                  />
                  <div 
                    className="chart-bar total" 
                    style={{ 
                      height: `${100 - ((value / analyticsData.commandSuccessRate.series[1][index]) * 100)}%` 
                    }}
                  />
                </div>
              ))}
            </div>
            <div className="chart-labels">
              {analyticsData.commandSuccessRate.labels.map((label, index) => (
                <span key={index} className="chart-label">
                  {index % 3 === 0 ? label : ''}
                </span>
              ))}
            </div>
          </div>
          <div className="chart-legend">
            <div className="legend-item">
              <span className="legend-color success"></span>
              <span>Successful</span>
            </div>
            <div className="legend-item">
              <span className="legend-color total"></span>
              <span>Failed</span>
            </div>
          </div>
        </div>
      </section>
      
      <section className="recent-activities">
        <h2>Recent Voice Activities</h2>
        <table className="activities-table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Activity</th>
              <th>Duration</th>
              <th>Status</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            {analyticsData.recentActivities.map((activity) => (
              <tr key={activity.id} className={activity.success ? 'success' : 'error'}>
                <td>{formatTimestamp(activity.timestamp)}</td>
                <td>{getEventTypeDisplay(activity.type)}</td>
                <td>{formatDuration(activity.durationMs)}</td>
                <td>
                  <span className={`status-indicator ${activity.success ? 'success' : 'error'}`}>
                    {activity.success ? 'Success' : 'Failed'}
                  </span>
                </td>
                <td>
                  {activity.command && <span className="command-text">{activity.command}</span>}
                  {activity.error && <span className="error-text">{activity.error}</span>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
      
      <footer className="dashboard-footer">
        <p>
          Data updates every {refreshInterval / 1000} seconds. 
          Last updated: {new Date().toLocaleString()}
        </p>
        <button className="refresh-button" onClick={fetchAnalyticsData}>
          Refresh Now
        </button>
      </footer>
    </div>
  );
};

export default VoiceAnalyticsDashboard; 