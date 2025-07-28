# API Reference

This document provides detailed documentation for the Primal Genesis Engine API. The API is built using FastAPI and provides RESTful endpoints for interacting with the system's quantum and AI capabilities.

## Base URL

```
https://api.primalgenesis.engine/v1
```

## Authentication

All API endpoints require authentication. Include your API key in the `X-API-Key` header:

```
X-API-Key: your_api_key_here
```

## Rate Limiting

- **Free Tier**: 100 requests per hour
- **Pro Tier**: 10,000 requests per hour
- **Enterprise**: Custom limits available

## Error Handling

All error responses follow this format:

```json
{
  "detail": "Error message describing the issue",
  "status": 400,
  "code": "error_code"
}
```

## Endpoints

### Quantum Operations

#### Create Quantum State

```
POST /quantum/states
```

Create a new quantum state.

**Request Body:**

```json
{
  "qubits": 2,
  "entanglement": true,
  "parameters": {
    "theta": 0.5,
    "phi": 1.0
  }
}
```

**Response:**

```json
{
  "state_id": "qs_1234567890abcdef",
  "qubits": 2,
  "entangled": true,
  "created_at": "2023-07-20T12:00:00Z"
}
```

#### Get Quantum State

```
GET /quantum/states/{state_id}
```

Retrieve a quantum state by ID.

**Path Parameters:**
- `state_id` (string, required): The ID of the quantum state to retrieve

**Response:**

```json
{
  "state_id": "qs_1234567890abcdef",
  "qubits": 2,
  "entangled": true,
  "state_vector": [0.7071, 0, 0, 0.7071],
  "created_at": "2023-07-20T12:00:00Z"
}
```

### AI Model Operations

#### Generate Text

```
POST /ai/generate
```

Generate text using the specified AI model.

**Request Body:**

```json
{
  "model": "mistral-large-latest",
  "prompt": "Explain quantum entanglement in simple terms.",
  "max_tokens": 500,
  "temperature": 0.7,
  "top_p": 0.9
}
```

**Response:**

```json
{
  "generated_text": "Quantum entanglement is a phenomenon where two or more particles become connected in such a way that the state of one particle is directly related to the state of the other, no matter how far apart they are...",
  "model": "mistral-large-latest",
  "tokens_used": 145,
  "finish_reason": "stop"
}
```

#### List Available Models

```
GET /ai/models
```

List all available AI models.

**Response:**

```json
{
  "models": [
    {
      "id": "mistral-large-latest",
      "name": "Mistral Large",
      "provider": "Mistral AI",
      "capabilities": ["text", "completion"],
      "max_tokens": 32000
    },
    {
      "id": "gpt-4o",
      "name": "GPT-4o",
      "provider": "OpenAI",
      "capabilities": ["text", "completion", "vision"],
      "max_tokens": 128000
    }
  ]
}
```

### Memory Operations

#### Store Memory

```
POST /memory/store
```

Store a new memory in the system.

**Request Body:**

```json
{
  "content": "The user prefers dark mode interface.",
  "tags": ["preferences", "ui"],
  "metadata": {
    "source": "user_preferences",
    "importance": 0.8
  }
}
```

**Response:**

```json
{
  "memory_id": "mem_1234567890abcdef",
  "content": "The user prefers dark mode interface.",
  "tags": ["preferences", "ui"],
  "created_at": "2023-07-20T12:00:00Z",
  "embedding": [0.1, 0.2, 0.3, ...]
}
```

#### Search Memories

```
GET /memory/search
```

Search for memories using semantic search.

**Query Parameters:**
- `query` (string, required): The search query
- `limit` (integer, optional): Maximum number of results to return (default: 10)
- `min_score` (float, optional): Minimum similarity score (0.0 to 1.0)

**Response:**

```json
{
  "results": [
    {
      "memory_id": "mem_1234567890abcdef",
      "content": "The user prefers dark mode interface.",
      "tags": ["preferences", "ui"],
      "score": 0.95,
      "created_at": "2023-07-20T12:00:00Z"
    }
  ],
  "total_results": 1
}
```

### Network Operations

#### Get Network Status

```
GET /network/status
```

Get the current status of the SovereignMesh network.

**Response:**

```json
{
  "status": "online",
  "nodes_online": 42,
  "last_sync": "2023-07-20T11:59:30Z",
  "throughput": {
    "inbound": "1.2 MB/s",
    "outbound": "0.8 MB/s"
  },
  "block_height": 123456
}
```

#### Broadcast Message

```
POST /network/broadcast
```

Broadcast a message to the SovereignMesh network.

**Request Body:**

```json
{
  "message": "Quantum state update available",
  "channel": "state_updates",
  "priority": "high",
  "ttl": 3600
}
```

**Response:**

```json
{
  "message_id": "msg_1234567890abcdef",
  "timestamp": "2023-07-20T12:00:00Z",
  "nodes_reached": 42
}
```

## WebSocket API

### Connect to WebSocket

```
wss://api.primalgenesis.engine/v1/ws
```

### Authentication

Send an authentication message immediately after connecting:

```json
{
  "type": "auth",
  "api_key": "your_api_key_here"
}
```

### Subscribe to Events

```json
{
  "type": "subscribe",
  "channels": ["state_updates", "network_events"]
}
```

### Event Format

```json
{
  "type": "event",
  "channel": "state_updates",
  "data": {
    "state_id": "qs_1234567890abcdef",
    "event": "state_updated",
    "timestamp": "2023-07-20T12:00:00Z"
  }
}
```

## SDKs

### Python SDK

```python
from primalgenesis import PrimalGenesisClient

# Initialize client
client = PrimalGenesisClient(api_key="your_api_key_here")

# Generate text
response = client.ai.generate(
    model="mistral-large-latest",
    prompt="Explain quantum computing in simple terms.",
    max_tokens=500
)
print(response.generated_text)

# Create quantum state
state = client.quantum.create_state(qubits=2, entanglement=True)
print(f"Created quantum state: {state.state_id}")
```

### JavaScript/TypeScript SDK

```typescript
import { PrimalGenesisClient } from '@primalgenesis/sdk';

// Initialize client
const client = new PrimalGenesisClient({
  apiKey: 'your_api_key_here',
});

// Generate text
const response = await client.ai.generate({
  model: 'mistral-large-latest',
  prompt: 'Explain quantum computing in simple terms.',
  maxTokens: 500,
});

console.log(response.generatedText);

// Create quantum state
const state = await client.quantum.createState({
  qubits: 2,
  entanglement: true,
});

console.log(`Created quantum state: ${state.stateId}`);
```

## Rate Limits

| Endpoint | Rate Limit |
|----------|------------|
| `/quantum/*` | 1000 requests/hour |
| `/ai/*` | 500 requests/hour |
| `/memory/*` | 2000 requests/hour |
| `/network/*` | 100 requests/minute |

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid request parameters |
| 401 | Unauthorized - Invalid or missing API key |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Something went wrong |
| 503 | Service Unavailable - Service temporarily unavailable |

## Changelog

### v1.0.0 (2023-07-20)
- Initial release of the Primal Genesis Engine API
- Support for quantum state operations
- Integration with multiple AI providers
- Memory storage and retrieval
- SovereignMesh network integration
