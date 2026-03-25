"""
Memory System

Provides an append-only memory store for Primal Genesis Engine to remember
what actions and events occurred.

Author: Primal Genesis Engine Team
Version: 0.1.0
"""

import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime


@dataclass
class MemoryRecord:
    """Represents a memory/event entry in the system."""
    module_name: str
    event_type: str
    content: str
    timestamp: str
    metadata: Optional[Dict] = None

    def to_dict(self) -> Dict:
        data = asdict(self)
        # Ensure metadata is never None in serialized form
        if data['metadata'] is None:
            data['metadata'] = {}
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> "MemoryRecord":
        # Basic validation for required fields
        if not isinstance(data, dict):
            raise ValueError("Memory data must be a dictionary")
        if 'module_name' not in data or 'event_type' not in data or 'content' not in data or 'timestamp' not in data:
            raise ValueError("Memory data must contain 'module_name', 'event_type', 'content', and 'timestamp' fields")
        return cls(**data)

    @classmethod
    def create(cls, module_name: str, event_type: str, content: str, metadata: Optional[Dict] = None) -> "MemoryRecord":
        """Create a new memory record with current timestamp."""
        timestamp = datetime.utcnow().isoformat() + 'Z'  # UTC timestamp with Z suffix
        return cls(
            module_name=module_name,
            event_type=event_type,
            content=content,
            timestamp=timestamp,
            metadata=metadata or {}
        )


class MemoryStore:
    """Simple append-only memory store with JSON persistence."""
    
    def __init__(self, storage_path: Optional[str] = None):
        self._memories: List[MemoryRecord] = []
        # Use deterministic default path relative to package location
        if storage_path is None:
            # Default to data directory within package
            package_root = Path(__file__).parent.parent.parent
            self.storage_path = package_root / "data" / "memory.json"
        else:
            self.storage_path = Path(storage_path)
        
        self._load_memories()
    
    def append_memory(self, memory: MemoryRecord) -> None:
        """Append a new memory record."""
        if not memory or not memory.module_name or not memory.event_type:
            raise ValueError("Memory must have valid module_name and event_type")
        
        self._memories.append(memory)
        self._save_memories()
    
    def create_memory(self, module_name: str, event_type: str, content: str, metadata: Optional[Dict] = None) -> None:
        """Create and append a new memory record with current timestamp."""
        memory = MemoryRecord.create(module_name, event_type, content, metadata)
        self.append_memory(memory)
    
    def list_memories(self, limit: Optional[int] = None) -> List[MemoryRecord]:
        """List all memories, optionally limited to recent ones."""
        memories = list(self._memories)
        # Return in reverse chronological order (newest first)
        memories.reverse()
        
        if limit is not None and limit > 0:
            return memories[:limit]
        
        return memories
    
    def list_by_module(self, module_name: str, limit: Optional[int] = None) -> List[MemoryRecord]:
        """List memories for a specific module."""
        if not module_name:
            return []
        
        module_memories = [m for m in self._memories if m.module_name == module_name]
        # Return in reverse chronological order (newest first)
        module_memories.reverse()
        
        if limit is not None and limit > 0:
            return module_memories[:limit]
        
        return module_memories
    
    def list_by_event_type(self, event_type: str, limit: Optional[int] = None) -> List[MemoryRecord]:
        """List memories for a specific event type."""
        if not event_type:
            return []
        
        event_memories = [m for m in self._memories if m.event_type == event_type]
        # Return in reverse chronological order (newest first)
        event_memories.reverse()
        
        if limit is not None and limit > 0:
            return event_memories[:limit]
        
        return event_memories
    
    def get_memory_count(self) -> int:
        """Get total number of memories."""
        return len(self._memories)
    
    def clear_memories(self) -> None:
        """Clear all memories (use with caution)."""
        self._memories.clear()
        self._save_memories()
    
    def _load_memories(self) -> None:
        """Load memories from JSON file."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not isinstance(data, list):
                        raise ValueError("Memory data must be a list")
                    
                    loaded_memories = []
                    for memory_data in data:
                        try:
                            memory = MemoryRecord.from_dict(memory_data)
                            loaded_memories.append(memory)
                        except (ValueError, TypeError) as e:
                            # Skip invalid memories but continue loading others
                            print(f"Warning: Skipping invalid memory record: {e}")
                            continue
                    
                    self._memories = loaded_memories
                    
            except (json.JSONDecodeError, ValueError, KeyError, TypeError) as e:
                # Start fresh if file is corrupted
                print(f"Warning: Memory file corrupted, starting fresh: {e}")
                self._memories = []
        else:
            self._memories = []
    
    def _save_memories(self) -> None:
        """Save memories to JSON file."""
        try:
            # Ensure parent directory exists
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            
            data = [memory.to_dict() for memory in self._memories]
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except (OSError, IOError) as e:
            print(f"Warning: Failed to save memories: {e}")
