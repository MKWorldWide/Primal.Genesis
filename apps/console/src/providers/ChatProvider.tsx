/**
 * @file ChatProvider.tsx
 * @description Chat context provider for managing chat state and threads
 * 
 * This is a minimal placeholder provider migrated from Phase 3B.
 * Full implementation will be added in future phases.
 */

import React, { createContext, useContext, useState, ReactNode } from 'react';

// Basic types for chat functionality
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

export interface ChatState {
  threads: Thread[];
  activeThreadId: string | null;
  addMessage: (threadId: string, role: 'user' | 'system' | 'assistant', content: string) => void;
  createThread: (title: string) => string;
  setActiveThread: (threadId: string | null) => void;
}

export interface ChatContextType extends ChatState {
  // Additional context methods can be added here
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [threads, setThreads] = useState<Thread[]>([]);
  const [activeThreadId, setActiveThreadId] = useState<string | null>(null);

  const addMessage = (threadId: string, role: 'user' | 'system' | 'assistant', content: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      role,
      content,
      timestamp: new Date()
    };

    setThreads(prevThreads => 
      prevThreads.map(thread => 
        thread.id === threadId 
          ? {
              ...thread,
              messages: [...thread.messages, newMessage],
              updatedAt: new Date()
            }
          : thread
      )
    );
  };

  const createThread = (title: string) => {
    const newThread: Thread = {
      id: Date.now().toString(),
      title,
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date()
    };

    setThreads(prev => [...prev, newThread]);
    setActiveThreadId(newThread.id);
    return newThread.id;
  };

  const value: ChatContextType = {
    threads,
    activeThreadId,
    addMessage,
    createThread,
    setActiveThread
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChatContext = () => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChatContext must be used within a ChatProvider');
  }
  return context;
};
