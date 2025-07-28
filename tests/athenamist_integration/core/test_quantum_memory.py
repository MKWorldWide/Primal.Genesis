"""
Tests for the quantum memory module.
"""
import pytest
import numpy as np
from qiskit.quantum_info import Statevector, partial_trace, entropy
from athenamist_integration.core.quantum_memory import (
    QuantumMemoryProcessor,
    QuantumMemoryPattern
)

class TestQuantumMemoryPattern:
    """Tests for the QuantumMemoryPattern class."""
    
    def test_initialization(self):
        """Test pattern initialization with default values."""
        pattern = QuantumMemoryPattern("01")
        assert pattern.state == "01"
        assert pattern.pattern_id is not None
        assert pattern.entanglement_entropy == 0.0
        assert pattern.metadata == {}
    
    def test_entanglement_entropy_calculation(self):
        """Test entanglement entropy calculation."""
        # Create a Bell state (maximally entangled)
        pattern = QuantumMemoryPattern("00")
        pattern.state = (Statevector.from_label("00") + Statevector.from_label("11")) / np.sqrt(2)
        entropy = pattern.calculate_entanglement_entropy()
        assert abs(entropy - 1.0) < 1e-6  # Should be maximally entangled

class TestQuantumMemoryProcessor:
    """Tests for the QuantumMemoryProcessor class."""
    
    @pytest.fixture
    def processor(self, mock_config):
        """Create a QuantumMemoryProcessor instance for testing."""
        return QuantumMemoryProcessor(mock_config['quantum_memory'])
    
    @pytest.mark.asyncio
    async def test_encode_memory(self, processor):
        """Test encoding a simple memory into a quantum pattern."""
        memory = {
            'content': 'Test memory',
            'timestamp': '2025-07-27T00:00:00Z'
        }
        
        pattern = await processor.encode_memory(memory)
        
        assert isinstance(pattern, QuantumMemoryPattern)
        assert pattern.pattern_id is not None
        assert pattern.entanglement_entropy >= 0.0
        assert pattern.metadata['original_memory'] == memory
    
    @pytest.mark.asyncio
    async def test_find_similar_patterns(self, processor):
        """Test finding similar patterns."""
        # Create test patterns
        patterns = []
        for i in range(3):
            pattern = QuantumMemoryPattern(f"{i:02b}")
            pattern.metadata = {'index': i}
            patterns.append(pattern)
        
        # Add patterns to processor
        for pattern in patterns:
            processor.patterns[pattern.pattern_id] = pattern
        
        # Find patterns similar to the first one
        target_pattern = patterns[0]
        similar = await processor.find_similar_patterns(target_pattern, threshold=0.5)
        
        assert len(similar) > 0
        assert similar[0].pattern_id == target_pattern.pattern_id
    
    @pytest.mark.asyncio
    async def test_quantum_entanglement_analysis(self, processor):
        """Test quantum entanglement analysis between two patterns."""
        # Create two patterns in a Bell state
        pattern1 = QuantumMemoryPattern("0")
        pattern2 = QuantumMemoryPattern("0")
        
        # Create a Bell state (|00> + |11>)/√2
        bell_state = (Statevector.from_label("00") + Statevector.from_label("11")) / np.sqrt(2)
        pattern1.state = partial_trace(bell_state, [1])  # Trace out second qubit
        pattern2.state = partial_trace(bell_state, [0])  # Trace out first qubit
        
        result = await processor.quantum_entanglement_analysis(pattern1, pattern2)
        
        assert result['are_entangled'] is True
        assert abs(result['entanglement_entropy'] - 1.0) < 1e-6  # Should be maximally entangled
    
    @pytest.mark.asyncio
    async def test_quantum_resistant_signature(self, processor):
        """Test generating and verifying a quantum-resistant signature."""
        data = b"Test data for signing"
        signature = await processor.generate_quantum_resistant_signature(data)
        
        # Verify the signature
        is_valid = await processor.verify_quantum_resistant_signature(
            data, signature['signature'], signature['public_key']
        )
        
        assert is_valid is True
        
        # Test with tampered data
        tampered_data = b"Tampered data"
        is_valid = await processor.verify_quantum_resistant_signature(
            tampered_data, signature['signature'], signature['public_key']
        )
        assert is_valid is False
