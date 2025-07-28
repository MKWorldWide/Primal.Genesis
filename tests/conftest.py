"""
Test configuration and fixtures for the Primal Genesis Engine tests.
"""
import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    return {
        'quantum_networks': {
            'divina_l3': {
                'api_url': 'https://api.divinal3.test',
                'api_key': 'test_key',
                'enable_quantum_processing': True
            },
            'novasanctum': {
                'api_url': 'https://api.novasanctum.test',
                'api_key': 'test_key',
                'enable_quantum_processing': True
            },
            'whispurrnet': {
                'api_url': 'https://api.whispurrnet.test',
                'api_key': 'test_key',
                'enable_quantum_processing': True
            }
        },
        'quantum_memory': {
            'max_qubits': 5,
            'entanglement_threshold': 0.8
        },
        'security': {
            'quantum_resistant_algorithm': 'SHA3-512',
            'enable_entanglement_verification': True
        }
    }

@pytest.fixture
def mock_quantum_circuit():
    """Create a simple quantum circuit for testing."""
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc

@pytest.fixture
def mock_entangled_state():
    """Create a Bell state for testing entanglement."""
    return Statevector.from_label('00') + Statevector.from_label('11')

@pytest.fixture
def mock_quantum_memory_pattern():
    """Create a mock quantum memory pattern."""
    class MockPattern:
        def __init__(self):
            self.pattern_id = 'test_pattern_123'
            self.state = '00'
            self.entanglement_entropy = 1.0
            self.metadata = {
                'original_memory': {'content': 'Test memory'},
                'created_at': '2025-07-27T00:00:00Z'
            }
    return MockPattern()

@pytest.fixture
def mock_network_manager():
    """Create a mock network manager."""
    manager = MagicMock()
    manager.broadcast_memory = AsyncMock(return_value={
        'status': 'success',
        'network_results': {
            'divina_l3': {'status': 'success', 'message_id': 'msg_123'},
            'novasanctum': {'status': 'success', 'message_id': 'msg_456'}
        }
    })
    return manager

@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Add any additional fixtures needed for testing
