/**
 * @file chat.ts
 * @description TypeScript type definitions for chat functionality
 * 
 * Basic chat types migrated from Phase 3B.
 * Will be expanded as chat functionality grows.
 */

export interface Message {
  id: string;
  role: 'user' | 'system' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface Thread {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}

export interface UserPreferences {
  theme: 'light' | 'dark';
  fontSize: 'small' | 'medium' | 'large';
  autoSave: boolean;
}

export interface ChatState {
  threads: Thread[];
  activeThreadId: string | null;
  isLoading: boolean;
  error: string | null;
}

export interface ChatContextType extends ChatState {
  addMessage: (threadId: string, role: 'user' | 'system' | 'assistant', content: string) => void;
  createThread: (title: string) => string;
  setActiveThread: (threadId: string | null) => void;
  updatePreferences: (preferences: Partial<UserPreferences>) => void;
}
