# Types Directory 📝

This directory contains TypeScript type definitions that provide type safety and clear interfaces for the application. Each type is designed with quantum documentation and follows the Prime Directives for optimal system governance.

## Core Types

### Chat Types
- **Purpose**: Define interfaces for chat functionality
- **Key Types**:
  - `Message`: Chat message structure
  - `Thread`: Chat thread with messages
  - `UserPreferences`: User settings
  - `ChatState`: Global chat state
  - `ChatContextType`: Combined state and actions
- **Usage**:
  ```tsx
  import { Thread, Message, UserPreferences } from '../types/chat';
  
  const thread: Thread = {
    id: '123',
    title: 'New Conversation',
    messages: [],
    createdAt: Date.now(),
    updatedAt: Date.now(),
    userPreferences: {
      modelId: 'default',
      enableVoice: true,
      temperature: 0.7
    }
  };
  ```

### Voice Types
- **Purpose**: Define interfaces for voice functionality
- **Key Types**:
  - `VoiceState`: Voice recording state
  - `VoiceContextActions`: Voice control actions
  - `VoiceContextType`: Combined state and actions
  - `RecordingOptions`: Voice recording settings
- **Usage**:
  ```tsx
  import { VoiceState, VoiceContextActions } from '../types/voice';
  
  const voiceState: VoiceState = {
    isRecording: false,
    isProcessing: false,
    hasPermission: null,
    error: null,
    stream: null,
    audioData: null
  };
  ```

## Type Safety

1. **Interface Design**
   - Clear property definitions
   - Proper type constraints
   - Comprehensive documentation

2. **Type Guards**
   - Runtime type checking
   - Error prevention
   - Safe type assertions

3. **Generic Types**
   - Reusable type definitions
   - Type parameter constraints
   - Flexible implementations

## Best Practices

1. **Documentation**
   - JSDoc comments for all types
   - Usage examples
   - Property descriptions

2. **Organization**
   - Logical grouping
   - Clear naming conventions
   - Proper exports

3. **Maintenance**
   - Regular type reviews
   - Version tracking
   - Breaking change documentation

## Self-Upgrade Protocol

Types automatically update their documentation through the quantum documentation system. Changes are tracked in:
- @memories.md for development history
- @lessons-learned.md for insights
- @scratchpad.md for active development

## Integration

Types are used throughout the application to ensure type safety:
- React components
- Context providers
- Service layers
- API interfaces

## See Also
- [@memories.md](../../.cursor/memories.md)
- [@lessons-learned.md](../../.cursor/lessons-learned.md)
- [@scratchpad.md](../../.cursor/scratchpad.md)
- [Prime Directives](../../docs/PRIME_DIRECTIVES.md) 