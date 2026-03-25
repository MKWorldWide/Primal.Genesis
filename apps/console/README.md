# Console App

React/Next.js application for the Primal Genesis Engine user interface.

## Purpose

Provides a web-based console for:
- System monitoring and control
- Configuration management
- Module and policy visualization
- User interaction and feedback

## Current State

**Phase 3B: Frontend Migration Completed**

React components have been migrated from `src/` to `apps/console/src/`:
- ✅ Chat components with provider integration
- ✅ Voice recording hooks and providers
- ✅ Analytics dashboard (with minimal imports)
- ✅ Type definitions for chat functionality
- ✅ README documentation for all modules

## Migrated Components

### Frontend Structure
```
apps/console/src/
├── components/
│   ├── chat/Chat.tsx
│   └── analytics/VoiceAnalyticsDashboard.tsx
├── providers/
│   ├── VoiceProvider.tsx
│   ├── ChatProvider.tsx (created)
│   └── README.md
├── hooks/
│   ├── useVoice.ts
│   ├── useSelfUpgrade.ts
│   └── README.md
└── types/
    ├── chat.ts (created)
    └── README.md
```

### Import Updates
- **ChatProvider.tsx**: Created minimal provider for chat functionality
- **chat.ts**: Created type definitions for Message, Thread, etc.
- **VoiceAnalyticsDashboard**: Commented out missing service imports

## Future Implementation

- Next.js app structure
- Integration with Python API
- Real-time updates via WebSocket
- Responsive design for mobile and desktop

## Migration Plan

Components were migrated from `src/` directory:
- `src/components/` → `apps/console/src/components/`
- `src/providers/` → `apps/console/src/providers/`
- `src/hooks/` → `apps/console/src/hooks/`
- `src/types/` → `apps/console/src/types/`

## Integration Status

**Ready for Phase 3C**: Tooling migration and backend connection
- Frontend components are in their new home
- Minimal providers and types created for functionality
- Import paths updated for new structure
- No Athena migration (preserved as separate)
