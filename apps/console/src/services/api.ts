/**
 * @file api.ts
 * @description API service layer for Primal Genesis Engine console
 * Provides simple, explicit calls to Phase 7A/7B API endpoints
 */

// API base URL - configurable for development
const API_BASE_URL = (process as any).env.REACT_APP_API_URL || 'http://localhost:8000';

// API response types
export interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
  service: string;
  execution_mode: string;
}

export interface SystemSnapshot {
  timestamp: string;
  console_version: string;
  system_status: {
    status: string;
    version: string;
    uptime: string;
  };
  modules: {
    total_count: number;
    enabled_count: number;
    disabled_count: number;
    enabled_modules: string[];
    available_types: string[];
  };
  policies: {
    total_count: number;
    enabled_count: number;
    disabled_count: number;
    default_behavior: string;
    available_effects: string[];
  };
  memory: {
    total_count: number;
    event_types: string[];
    recent_count: number;
  };
  activity: {
    level: string;
    last_activity: string;
    last_updated: string;
  };
}

export interface ModuleOverview {
  timestamp: string;
  summary: {
    total_modules: number;
    enabled_modules: number;
    disabled_modules: number;
    health_percentage: number;
  };
  modules_by_type: Record<string, string[]>;
  module_details: Array<{
    name: string;
    type: string;
    enabled: boolean;
    location: string;
    entrypoint: string;
    description: string;
    version: string;
  }>;
}

export interface PolicyOverview {
  timestamp: string;
  total_policies: number;
  enabled_policies: number;
  disabled_policies: number;
  default_behavior: string;
  available_effects: string[];
  policies_by_effect: Record<string, any[]>;
}

export interface RecentActivity {
  timestamp: string;
  summary: {
    total_activities: number;
    limit: number;
    activity_level: string;
  };
  activities: Array<{
    id: string;
    module: string;
    event_type: string;
    timestamp: string;
    content: string;
    display_type: string;
  }>;
}

export interface ExecutionRequest {
  module_name: string;
  action_name: string;
  payload?: Record<string, any>;
}

export interface ExecutionResponse {
  executed: boolean;
  execution_mode: string;
  outcome: string;
  payload: Record<string, any>;
  execution_details: {
    module_type: string;
    module_location: string;
    module_entrypoint: string;
    action: string;
    simulated: boolean;
    execution_time: string;
    execution_scope: string;
    side_effect_level: string;
  };
  message?: string;
  error?: string;
}

export interface PolicyCheckResponse {
  allowed: boolean;
  policy: any;
  reason: string;
}

/**
 * API error class for consistent error handling
 */
export class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public response?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

/**
 * Simple API client for Primal Genesis Engine
 */
class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Make HTTP request with error handling
   */
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({} as any));
        throw new ApiError(
          errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
          response.status,
          errorData
        );
      }

      return await response.json();
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new ApiError(`Network error: ${error.message}`);
    }
  }

  /**
   * Get API health status
   */
  async getHealth(): Promise<HealthResponse> {
    return this.request<HealthResponse>('/api/v1/health');
  }

  /**
   * Get complete system snapshot
   */
  async getSystemSnapshot(): Promise<SystemSnapshot> {
    return this.request<SystemSnapshot>('/api/v1/snapshot');
  }

  /**
   * Get module overview
   */
  async getModuleOverview(): Promise<ModuleOverview> {
    return this.request<ModuleOverview>('/api/v1/modules');
  }

  /**
   * Get policies overview
   */
  async getPolicyOverview(): Promise<PolicyOverview> {
    return this.request<PolicyOverview>('/api/v1/policies');
  }

  /**
   * Get recent activity
   */
  async getRecentActivity(limit: number = 10): Promise<RecentActivity> {
    return this.request<RecentActivity>(`/api/v1/memory/recent?limit=${limit}`);
  }

  /**
   * Execute module action
   */
  async executeModuleAction(request: ExecutionRequest): Promise<ExecutionResponse> {
    return this.request<ExecutionResponse>('/api/v1/runtime/execute', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Check module action policy
   */
  async checkModuleAction(moduleName: string, actionName: string): Promise<PolicyCheckResponse> {
    return this.request<PolicyCheckResponse>(`/api/v1/runtime/check/${moduleName}/${actionName}`);
  }
}

// Export singleton instance
export const apiClient = new ApiClient();

// Export types for use in components
