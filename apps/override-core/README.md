# Override Core Tool

Node.js development tooling and override system for Primal Genesis Engine.

## Purpose

Provides development-time tooling and configuration override capabilities:
- File watching and hot reload
- Development server management
- Configuration overrides for local development
- Build and deployment automation

## Current State

**Phase 3C: Tooling Migration Completed**

Node.js tooling has been migrated from root `override_core/` to `apps/override-core/`:
- Core override system with index.js
- File watching with log_watcher.js
- Package configuration preserved
- Dependencies and scripts maintained

## Migrated Components

### Core Files
- **`index.js`** - Main override system entry point (3,314 bytes)
- **`log_watcher.js`** - File watching and logging system (388 bytes)
- **`package.json`** - Node.js package configuration
- **`package-lock.json`** - Dependency lock file

### Package Scripts
```json
{
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "start": "node index.js",
    "watch": "node log_watcher.js"
  }
}
```

### Dependencies
- **chokidar** - File watching
- **express** - Web server framework
- **node-fetch** - HTTP requests
- **nodemon** - Development monitoring

## Migration Details

**Phase 3C Migration:**
- **Source**: `override_core/` → **Target**: `apps/override-core/`
- **Files Preserved**: All original functionality maintained
- **Paths Updated**: No path changes needed (relative paths used)
- **Configuration**: Package.json preserved with original settings

## Usage

```bash
# Start the override core system
npm start

# Watch for file changes
npm run watch
```

## Integration Status

**Ready for Integration:**
- Tooling is in proper application boundary
- No path dependencies on root structure
- Ready to connect with other apps and packages
- Development environment configuration maintained

## Future Development

- Enhanced file watching capabilities
- Integration with console app
- Configuration management improvements
- Build pipeline automation with:
- Updated package.json dependencies
- Improved TypeScript support
- Enhanced configuration management
- Better error handling and logging
