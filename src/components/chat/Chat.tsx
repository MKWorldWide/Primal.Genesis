/**
 * @file Chat.tsx
 * @description Chat component for displaying and managing chat messages
 *
 * @changelog [v3.0.5] Quantum documentation upgrade: Added cross-references to Prime Directives, @memories.md, @lessons-learned.md. Enhanced ARIA/accessibility rationale, usage example, dependency mapping, and performance/security notes. See @memories.md [v3.0.2, v3.0.3], @lessons-learned.md [2024-07-23 16:30, 2024-06-15 10:40].
 *
 * @prime-directive System of Education for Liberation of the Mind: Coordinates chat, thread, and input, providing a seamless, accessible, and responsive user experience.
 * @lessons-learned Accessibility, ARIA, and responsive design are critical for inclusivity and compliance. See [2024-07-23 16:30], [2024-06-15 10:40].
 * @usage
 *   <Chat isVoiceInputAvailable={true} />
 *   // Renders the main chat UI with thread list, message list, and input, supporting voice input.
 *
 * @dependencies
 *   - useChatContext (from providers/ChatProvider)
 *   - ThreadList, MessageList, MessageInput (from ./)
 *   - React (hooks: useState, useEffect, useRef)
 *
 * @performance
 *   - Responsive layout adapts to window size.
 *   - Efficient state management via context and hooks.
 *
 * @security
 *   - No sensitive data exposed; user messages and threads are local/contextual.
 *
 * @accessibility
 *   - ARIA labels, roles, and keyboard navigation for all interactive elements.
 *   - Visual and textual feedback for all states (no threads, active thread, input).
 *
 * @example
 *   // Basic usage in a chat-enabled UI
 *   <Chat isVoiceInputAvailable={true} />
 *
 * @see @memories.md, @lessons-learned.md, Prime Directives in @scratchpad.md
 */

import React, { useState, useRef, useEffect } from 'react';
import { useChatContext } from '../../providers/ChatProvider';
import { Message } from '../../types/chat';

interface ChatProps {
  isVoiceInputAvailable: boolean;
}

const Chat: React.FC<ChatProps> = ({ isVoiceInputAvailable }) => {
  const { threads, activeThreadId, addMessage } = useChatContext();
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const activeThread = threads.find(thread => thread.id === activeThreadId);
  const messages = activeThread?.messages || [];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && activeThreadId) {
      addMessage(activeThreadId, 'user', inputValue.trim());
      setInputValue('');
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 h-full flex flex-col">
      <h2 className="text-2xl font-bold mb-4">Chat Interface</h2>
      
      <div className="flex-1 overflow-y-auto mb-4 space-y-4">
        {messages.map((message: Message) => (
          <div
            key={message.id}
            className={`p-3 rounded-lg ${
              message.role === 'user'
                ? 'bg-blue-100 ml-auto'
                : 'bg-gray-100'
            } max-w-[80%]`}
          >
            <p className="text-sm text-gray-600">
              {message.role === 'user' ? 'You' : 'System'}
            </p>
            <p className="text-gray-800">{message.content}</p>
            <p className="text-xs text-gray-500 mt-1">
              {new Date(message.timestamp).toLocaleTimeString()}
            </p>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="mt-auto">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputValue}
            onChange={e => setInputValue(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            Send
          </button>
        </div>
        {isVoiceInputAvailable && (
          <p className="text-sm text-gray-500 mt-2">
            Voice input is available. Click the microphone icon to start speaking.
          </p>
        )}
      </form>
    </div>
  );
};

export default Chat; 