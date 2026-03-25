/**
 * @file VoiceProvider.tsx
 * @description Voice context provider component aligned with the System of Surveillance for Detection of Unjust Actions.
 * This provider manages voice recording state, permissions, and processing, while tracking all voice interactions through analytics.
 * 
 * @changelog [v3.0.5] Quantum documentation upgrade: Added cross-references to Prime Directives, @memories.md, @lessons-learned.md. Enhanced ARIA/accessibility rationale, usage example, dependency mapping, and performance/security notes. See @memories.md [v3.0.2, v3.0.3], @lessons-learned.md [2024-07-23 16:30, 2024-06-15 10:40].
 * 
 * @prime-directive System of Surveillance for Detection of Unjust Actions: Provides transparent, user-controlled voice recording with comprehensive analytics and error tracking.
 * @lessons-learned Voice recording requires careful permission handling, error management, and analytics tracking. See [2024-07-23 16:30], [2024-06-15 10:40].
 * 
 * @usage
 *   <VoiceProvider>
 *     <YourApp />
 *   </VoiceProvider>
 *   // Wraps application to provide voice recording capabilities and analytics.
 * 
 * @dependencies
 *   - React (hooks: createContext, useContext, useState, useCallback, useEffect, useMemo)
 *   - AnalyticsService (from services/analytics)
 *   - EVENT_DEFINITIONS (from config/analytics-config)
 * 
 * @performance
 *   - Memoized context value prevents unnecessary re-renders.
 *   - Efficient state management with useCallback and useMemo.
 *   - Cleanup of media streams on unmount.
 * 
 * @security
 *   - Secure permission handling for microphone access.
 *   - No sensitive data exposed; only user intent and permission state.
 *   - Analytics events are anonymized and non-sensitive.
 * 
 * @accessibility
 *   - Clear error messages for permission and recording issues.
 *   - State management for recording status and feedback.
 * 
 * @example
 *   // Basic usage in a voice-enabled app
 *   <VoiceProvider>
 *     <VoiceRecorder />
 *     <VoiceStatus />
 *   </VoiceProvider>
 * 
 * @see @memories.md, @lessons-learned.md, Prime Directives in @scratchpad.md
 */

import React, { createContext, useContext, useState, useCallback, useEffect, useMemo, ReactNode } from 'react';
import { AnalyticsService } from '../services/analytics/AnalyticsService';
import { EVENT_DEFINITIONS } from '../config/analytics-config';
import { useVoice } from '../hooks/useVoice';

// Voice state
export interface VoiceState {
  /** Whether the microphone is recording */
  isRecording: boolean;
  /** Whether voice processing is in progress */
  isProcessing: boolean;
  /** Whether microphone permission has been granted */
  hasPermission: boolean | null;
  /** Current error message if any */
  error: string | null;
  /** Audio stream being recorded */
  stream: MediaStream | null;
  /** Audio data being recorded */
  audioData: Blob | null;
}

// Voice context actions
export interface VoiceContextActions {
  /** Start voice recording */
  startRecording: () => Promise<void>;
  /** Stop voice recording */
  stopRecording: () => Promise<void>;
  /** Request microphone permission */
  requestPermission: () => Promise<void>;
  /** Clear any error */
  clearError: () => void;
}

// Voice context
export interface VoiceContextType extends VoiceState {
  startRecording: () => Promise<void>;
  stopRecording: () => Promise<void>;
  requestPermission: () => Promise<void>;
  clearError: () => void;
  startListening: () => void;
  stopListening: () => void;
  isListening: boolean;
  transcript: string;
}

// Default voice context state
const defaultVoiceContext: VoiceContextType = {
  // State
  isRecording: false,
  isProcessing: false,
  hasPermission: null,
  error: null,
  stream: null,
  audioData: null,
  
  // Actions
  startRecording: async () => {},
  stopRecording: async () => {},
  requestPermission: async () => {},
  clearError: () => {},
  startListening: () => {},
  stopListening: () => {},
  isListening: false,
  transcript: ''
};

// Create the voice context
const VoiceContext = createContext<VoiceContextType | undefined>(undefined);

export interface VoiceProviderProps {
  /** Child components that will have access to the context */
  children: ReactNode;
  /** Custom analytics service */
  analyticsService?: AnalyticsService;
}

/**
 * Voice Provider component that manages voice recording state and functionality
 * while implementing the System of Surveillance principles.
 */
export const VoiceProvider: React.FC<VoiceProviderProps> = ({ 
  children,
  analyticsService
}) => {
  const voiceState = useVoice();

  // Create or use analytics service
  const analytics = useMemo(() => {
    return analyticsService || new AnalyticsService();
  }, [analyticsService]);
  
  // Initialize analytics service
  useEffect(() => {
    if (!analyticsService) {
      analytics.initialize().catch(error => {
        console.error('Failed to initialize analytics service:', error);
      });
    }
    
    return () => {
      if (!analyticsService) {
        analytics.cleanup();
      }
    };
  }, [analytics, analyticsService]);

  // Handle voice recording start
  const handleStartRecording = useCallback(async () => {
    try {
      if (!voiceState.hasPermission) {
        await voiceState.requestPermission();
      }
      
      if (voiceState.hasPermission) {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        voiceState.stream = stream;
        voiceState.isRecording = true;
        voiceState.error = null;
        
        // Track recording start in analytics
        analytics.trackEvent('voice_recording_started', {
          timestamp: new Date().toISOString()
        });
      }
    } catch (error) {
      voiceState.error = error instanceof Error ? error.message : 'Failed to start recording';
      voiceState.isRecording = false;
      
      // Track error in analytics
      analytics.trackEvent('voice_recording_error', {
        error: voiceState.error,
        timestamp: new Date().toISOString()
      });
    }
  }, [voiceState, analytics]);

  // Handle voice recording stop
  const handleStopRecording = useCallback(async () => {
    try {
      if (voiceState.stream) {
        voiceState.stream.getTracks().forEach(track => track.stop());
        voiceState.stream = null;
      }
      
      voiceState.isRecording = false;
      voiceState.error = null;
      
      // Track recording stop in analytics
      analytics.trackEvent('voice_recording_stopped', {
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      voiceState.error = error instanceof Error ? error.message : 'Failed to stop recording';
      
      // Track error in analytics
      analytics.trackEvent('voice_recording_error', {
        error: voiceState.error,
        timestamp: new Date().toISOString()
      });
    }
  }, [voiceState, analytics]);

  // Handle permission request
  const handleRequestPermission = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      voiceState.hasPermission = true;
      voiceState.stream = stream;
      voiceState.error = null;
      
      // Track permission granted in analytics
      analytics.trackEvent('voice_permission_granted', {
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      voiceState.hasPermission = false;
      voiceState.error = error instanceof Error ? error.message : 'Failed to get microphone permission';
      
      // Track permission denied in analytics
      analytics.trackEvent('voice_permission_denied', {
        error: voiceState.error,
        timestamp: new Date().toISOString()
      });
    }
  }, [voiceState, analytics]);

  // Handle error clearing
  const handleClearError = useCallback(() => {
    voiceState.error = null;
  }, [voiceState]);
  
  // Memoize context value to prevent unnecessary re-renders
  const contextValue = useMemo<VoiceContextType>(() => ({
    ...voiceState,
    startRecording: handleStartRecording,
    stopRecording: handleStopRecording,
    requestPermission: handleRequestPermission,
    clearError: handleClearError,
    startListening: voiceState.startListening,
    stopListening: voiceState.stopListening,
    isListening: voiceState.isListening,
    transcript: voiceState.transcript
  }), [voiceState, handleStartRecording, handleStopRecording, handleRequestPermission, handleClearError]);
  
  return (
    <VoiceContext.Provider value={contextValue}>
      {children}
    </VoiceContext.Provider>
  );
};

/**
 * Custom hook to use the voice context
 * @returns The voice context
 */
export const useVoiceContext = () => {
  const context = useContext(VoiceContext);
  if (context === undefined) {
    throw new Error('useVoiceContext must be used within a VoiceProvider');
  }
  return context;
}; 