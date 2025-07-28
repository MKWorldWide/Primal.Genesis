"""
Tests for the quantum synchronization module.
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from athenamist_integration.core.quantum_sync import (
    QuantumNetworkSynchronizer,
    SyncStatus,
    SyncOperation,
    SyncConflict
)

class TestSyncOperation:
    """Tests for the SyncOperation class."""
    
    def test_initialization(self):
        """Test that a sync operation is initialized correctly."""
        op = SyncOperation(
            operation_id="test_op_123",
            source_network="local",
            target_networks=["divina_l3", "novasanctum"],
            memory_pattern=MagicMock()
        )
        
        assert op.operation_id == "test_op_123"
        assert op.source_network == "local"
        assert "divina_l3" in op.target_networks
        assert op.status == SyncStatus.PENDING
    
    def test_update_status(self):
        """Test updating the status of a sync operation."""
        op = SyncOperation("test_op_123", "local", [], MagicMock())
        
        op.update_status(SyncStatus.IN_PROGRESS, {"progress": 50})
        
        assert op.status == SyncStatus.IN_PROGRESS
        assert "progress" in op.metadata
        assert op.metadata["progress"] == 50

class TestQuantumNetworkSynchronizer:
    """Tests for the QuantumNetworkSynchronizer class."""
    
    @pytest.fixture
    async def synchronizer(self, mock_network_manager):
        """Create a QuantumNetworkSynchronizer instance for testing."""
        return QuantumNetworkSynchronizer(mock_network_manager)
    
    @pytest.mark.asyncio
    async def test_sync_memory_success(self, synchronizer):
        """Test successful memory synchronization."""
        # Mock the network manager
        mock_memory = {"id": "mem1", "content": "Test memory"}
        
        with patch.object(synchronizer.network_manager, 'broadcast_memory') as mock_broadcast:
            # Setup mock
            mock_broadcast.return_value = {
                'status': 'success',
                'network_results': {
                    'divina_l3': {'status': 'success', 'message_id': 'msg123'},
                    'novasanctum': {'status': 'success', 'message_id': 'msg456'}
                }
            }
            
            # Test sync
            result = await synchronizer.sync_memory(
                memory=mock_memory,
                target_networks=['divina_l3', 'novasanctum'],
                source_network='local',
                sync_strategy='push'
            )
            
            # Verify results
            assert result['status'] == 'success'
            assert 'operation_id' in result
            assert 'results' in result
            assert 'divina_l3' in result['results']
    
    @pytest.mark.asyncio
    async def test_sync_memory_conflict(self, synchronizer):
        """Test memory synchronization with conflict resolution."""
        # Mock the network manager to raise a conflict
        mock_memory = {"id": "mem1", "content": "Test memory"}
        
        with patch.object(synchronizer.network_manager, 'broadcast_memory') as mock_broadcast:
            # Setup mock to raise a conflict
            mock_broadcast.side_effect = SyncConflict(
                "Version conflict detected",
                conflicts=[
                    {
                        'version_id': 'v1',
                        'source_network': 'divina_l3',
                        'timestamp': '2025-07-27T00:00:00Z',
                        'quantum_entropy': 0.9
                    },
                    {
                        'version_id': 'v2',
                        'source_network': 'local',
                        'timestamp': '2025-07-27T01:00:00Z',
                        'quantum_entropy': 0.8
                    }
                ]
            )
            
            # Test sync with conflict resolution
            result = await synchronizer.sync_memory(
                memory=mock_memory,
                target_networks=['divina_l3'],
                source_network='local',
                sync_strategy='push',
                conflict_resolution='timestamp'  # Resolve by timestamp
            )
            
            # Verify conflict was resolved
            assert result['status'] == 'resolved'
            assert result['resolution_strategy'] == 'timestamp'
    
    @pytest.mark.asyncio
    async def test_resolve_conflict_by_timestamp(self, synchronizer):
        """Test conflict resolution by timestamp."""
        conflicts = [
            {'version_id': 'v1', 'timestamp': '2025-07-27T00:00:00Z'},
            {'version_id': 'v2', 'timestamp': '2025-07-28T00:00:00Z'}
        ]
        
        op = SyncOperation("test_op", "local", [], MagicMock())
        result = await synchronizer._resolve_by_timestamp(op, conflicts)
        
        assert result['resolution'] == 'latest_version'
        assert result['selected_version'] == 'v2'
    
    @pytest.mark.asyncio
    async def test_resolve_conflict_by_entropy(self, synchronizer):
        """Test conflict resolution by quantum entropy."""
        conflicts = [
            {'version_id': 'v1', 'quantum_entropy': 0.7},
            {'version_id': 'v2', 'quantum_entropy': 0.9}
        ]
        
        op = SyncOperation("test_op", "local", [], MagicMock())
        result = await synchronizer._resolve_by_entropy(op, conflicts)
        
        assert result['resolution'] == 'highest_entropy'
        assert result['selected_version'] == 'v2'
    
    @pytest.mark.asyncio
    async def test_resolve_conflict_by_source_priority(self, synchronizer):
        """Test conflict resolution by source network priority."""
        conflicts = [
            {'version_id': 'v1', 'source_network': 'divina_l3'},
            {'version_id': 'v2', 'source_network': 'local'}
        ]
        
        op = SyncOperation("test_op", "local", [], MagicMock())
        result = await synchronizer._resolve_by_source_priority(op, conflicts)
        
        assert result['resolution'] == 'source_priority'
        assert result['selected_version'] == 'v1'  # divina_l3 has higher priority
    
    @pytest.mark.asyncio
    async def test_resolve_conflict_by_merge(self, synchronizer):
        """Test conflict resolution by merging changes."""
        conflicts = [
            {
                'version_id': 'v1',
                'source_network': 'divina_l3',
                'data': {'field1': 'value1', 'field2': 'value2'}
            },
            {
                'version_id': 'v2',
                'source_network': 'local',
                'data': {'field1': 'updated', 'field3': 'value3'}
            }
        ]
        
        op = SyncOperation("test_op", "local", [], MagicMock())
        result = await synchronizer._resolve_by_merge(op, conflicts)
        
        assert result['resolution'] == 'merged'
        assert 'divina_l3' in result['sources']
        assert 'local' in result['sources']
        assert len(result['merged_fields']) == 3  # field1, field2, field3
