"""
Tests for the quantum network module.
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from athenamist_integration.core.quantum_network import QuantumNetworkManager

class TestQuantumNetworkManager:
    """Tests for the QuantumNetworkManager class."""
    
    @pytest.fixture
    async def network_manager(self, mock_config):
        """Create a QuantumNetworkManager instance for testing."""
        # Patch the aiohttp ClientSession to avoid actual network calls
        with patch('aiohttp.ClientSession') as mock_session:
            mock_session.return_value.__aenter__.return_value = AsyncMock()
            manager = QuantumNetworkManager(mock_config)
            yield manager
            await manager.close()
    
    @pytest.mark.asyncio
    async def test_initialization(self, network_manager):
        """Test that the network manager initializes correctly."""
        assert network_manager is not None
        assert hasattr(network_manager, 'networks')
        assert 'divina_l3' in network_manager.networks
        assert 'novasanctum' in network_manager.networks
        assert 'whispurrnet' in network_manager.networks
    
    @pytest.mark.asyncio
    async def test_connect_to_network(self, network_manager):
        """Test connecting to a quantum network."""
        # Mock the network connection
        with patch.object(network_manager, '_send_network_request') as mock_request:
            mock_request.return_value = {'status': 'connected', 'network': 'divina_l3'}
            
            result = await network_manager.connect_to_network('divina_l3')
            
            assert result['status'] == 'connected'
            assert 'divina_l3' in network_manager.sessions
    
    @pytest.mark.asyncio
    async def test_broadcast_memory(self, network_manager):
        """Test broadcasting a memory to multiple networks."""
        # Mock the network connection and memory processing
        with patch.object(network_manager, 'connect_to_network') as mock_connect, \
             patch.object(network_manager.memory_processor, 'encode_memory') as mock_encode:
            
            # Setup mocks
            mock_connect.return_value = {'status': 'connected'}
            mock_encode.return_value = MagicMock(metadata={'original_memory': {'test': 'memory'}})
            
            # Mock the session post method
            mock_response = MagicMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={'message_id': 'test123'})
            network_manager.session.post = AsyncMock(return_value=mock_response)
            
            # Test broadcast
            memory = {'content': 'Test memory'}
            result = await network_manager.broadcast_memory(
                memory=memory,
                networks=['divina_l3', 'novasanctum'],
                enable_quantum_processing=True
            )
            
            # Verify results
            assert 'network_results' in result
            assert 'divina_l3' in result['network_results']
            assert 'novasanctum' in result['network_results']
            assert result['network_results']['divina_l3']['status'] == 'success'
    
    @pytest.mark.asyncio
    async def test_find_similar_memories(self, network_manager):
        """Test finding similar memories across networks."""
        # Mock the memory processor
        mock_pattern = MagicMock()
        mock_pattern.similarity = 0.9
        mock_pattern.metadata = {'original_memory': {'content': 'Similar memory'}}
        
        with patch.object(network_manager.memory_processor, 'encode_memory') as mock_encode, \
             patch.object(network_manager.memory_processor, 'find_similar_patterns') as mock_find:
            
            # Setup mocks
            mock_encode.return_value = MagicMock()
            mock_find.return_value = [mock_pattern]
            
            # Test finding similar memories
            results = await network_manager.find_similar_memories(
                memory={'content': 'Test memory'},
                threshold=0.8,
                networks=['local']
            )
            
            # Verify results
            assert len(results) > 0
            assert results[0]['similarity'] >= 0.8
    
    @pytest.mark.asyncio
    async def test_quantum_entangle_memories(self, network_manager):
        """Test entangling two memories."""
        # Mock the memory processor
        with patch.object(network_manager.memory_processor, 'encode_memory') as mock_encode, \
             patch.object(network_manager.memory_processor, 'quantum_entanglement_analysis') as mock_analysis:
            
            # Setup mocks
            mock_encode.side_effect = [MagicMock(), MagicMock()]
            mock_analysis.return_value = {
                'are_entangled': True,
                'entanglement_entropy': 1.0,
                'fidelity': 0.99
            }
            
            # Test entangling memories
            memory1 = {'id': 'mem1', 'content': 'Memory 1'}
            memory2 = {'id': 'mem2', 'content': 'Memory 2'}
            
            result = await network_manager.quantum_entangle_memories(
                memory1=memory1,
                memory2=memory2,
                network='divina_l3',
                error_correction=True
            )
            
            # Verify results
            assert result['status'] == 'success'
            assert result['entangled'] is True
            assert result['network'] == 'divina_l3'
