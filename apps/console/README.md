# Console App

React/Next.js application for Primal Genesis Engine user interface.

## Purpose

Provides a web-based console for:
- System monitoring and control
- Configuration management
- Module and policy visualization
- User interaction and feedback

## Current State

**Phase 8A: Console Wiring and Revamp Completed**

The console has been transformed from disconnected fragments into a real command-center UI that displays live engine state through the Phase 7A/7B API layer.

## Migrated Components

### Frontend Structure
```
apps/console/src/
├── components/
│   ├── chat/Chat.tsx
│   ├── analytics/VoiceAnalyticsDashboard.tsx
│   └── ConsoleDashboard.tsx (NEW)
├── providers/
│   ├── VoiceProvider.tsx
│   ├── ChatProvider.tsx (created)
│   └── README.md
├── hooks/
│   ├── useVoice.ts
│   ├── useSelfUpgrade.ts
│   └── README.md
├── types/
│   ├── chat.ts (created)
│   └── README.md
├── services/
│   └── api.ts (NEW)
├── App.tsx (REVAMPED)
├── App.css (NEW)
└── components/styles/
    └── ConsoleDashboard.css (NEW)
```

## New Features Added

### API Integration
- **API Service Layer**: Created `services/api.ts` with full API client
- **Real Data Connection**: Console now fetches live data from engine API
- **Error Handling**: Proper error states and retry functionality
- **Type Safety**: Full TypeScript interfaces for all API responses

### Command Center Dashboard
- **ConsoleDashboard Component**: Complete command-center UI replacing fragments
- **System Status**: Live system health, version, and uptime display
- **Module Overview**: Real module states with health percentages
- **Recent Activity**: Live activity feed from engine memory
- **Policy Summary**: Current policy counts and configurations
- **Runtime Action Panel**: Safe runtime execution with honest simulation indicators

### UI Improvements
- **Responsive Design**: Mobile-friendly grid layouts
- **Loading States**: Clear loading indicators for all data fetching
- **Error States**: User-friendly error messages and retry options
- **Status Indicators**: Visual status indicators with consistent color coding
- **Execution Feedback**: Detailed execution results with scope and side-effect information

## API Endpoints Consumed

The console now connects to these Phase 7A/7B API endpoints:

- `GET /api/v1/health` - System health and execution mode
- `GET /api/v1/snapshot` - Complete system snapshot
- `GET /api/v1/modules` - Module overview with health metrics
- `GET /api/v1/policies` - Policy configuration summary
- `GET /api/v1/memory/recent` - Recent activity/memory entries
- `POST /api/v1/runtime/execute` - Runtime action execution
- `GET /api/v1/runtime/check/{module}/{action}` - Policy checking

## Runtime Interaction

The runtime action panel provides:
- **Module Name Input**: Text input for target module
- **Action Name Input**: Text input for specific action
- **Payload Input**: JSON textarea for optional parameters
- **Execute Button**: Triggers API execution with loading states
- **Result Display**: Shows execution details including:
  - Execution status (executed/failed)
  - Execution mode (local-simulated)
  - Outcome (success/error/denied)
  - Scope (local-only)
  - Side effect level (read-only)
  - Execution details and messages

## Honest Execution Display

The console clearly indicates that all execution is:
- **Local**: Actions execute within the local engine
- **Simulated**: No real external operations occur
- **Read-only**: No persistent side effects
- **Honest**: All execution metadata is displayed transparently

## Usage

1. Start the Primal Genesis API server (Phase 7A/7B)
2. Run the console application:
   ```bash
   cd apps/console
   npm start
   ```
3. Access the console at `http://localhost:3000`
4. Configure `REACT_APP_API_URL` if API runs on different port

## Future Enhancements

Planned for future phases:
- Athena observation views integration
- Richer module management controls
- Deeper policy inspection interfaces
- Memory exploration and search capabilities
- Real-time updates via WebSocket
- Authentication and authorization
- Multi-user support

## Technical Notes

- Built with React 18 and TypeScript
- Uses modern CSS Grid for responsive layouts
- Implements proper error boundaries and loading states
- Maintains type safety throughout the application
- Follows consistent design patterns and naming conventions
- `src/hooks/` → `apps/console/src/hooks/`
- `src/types/` → `apps/console/src/types/`

## Integration Status

**Ready for Phase 3C**: Tooling migration and backend connection
- Frontend components are in their new home
- Minimal providers and types created for functionality
- Import paths updated for new structure
- No Athena migration (preserved as separate)
