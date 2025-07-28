# Developer Guide

Welcome to the Primal Genesis Engine developer guide! This document provides comprehensive information for developers working with the codebase, including setup instructions, coding standards, and development workflows.

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Project Structure](#project-structure)
3. [Coding Standards](#coding-standards)
4. [Testing Guidelines](#testing-guidelines)
5. [API Development](#api-development)
6. [Quantum Module Development](#quantum-module-development)
7. [Performance Optimization](#performance-optimization)
8. [Debugging](#debugging)
9. [Version Control](#version-control)
10. [Documentation](#documentation)

## Development Environment Setup

### Prerequisites

- Python 3.9+
- Git
- (Optional) Docker
- (Optional) Node.js (for frontend development)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/MKWorldWide/Primal-Genesis-Engine-Sovereign.git
   cd Primal-Genesis-Engine-Sovereign
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-test.txt
   pip install -e .  # Install in development mode
   ```

4. **Verify installation**:
   ```bash
   python -c "import athenamist_integration; print('Installation successful!')"
   ```

## Project Structure

```
primal-genesis-engine/
├── athenamist_integration/  # Core package
│   ├── core/                # Core functionality
│   │   ├── __init__.py
│   │   ├── quantum_network.py
│   │   ├── quantum_memory.py
│   │   └── quantum_sync.py
│   ├── api/                 # API endpoints
│   └── utils/               # Utility functions
├── tests/                   # Test suite
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── docs/                   # Documentation
├── scripts/                # Utility scripts
└── config/                 # Configuration files
```

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with the following additional guidelines:

- **Line length**: 120 characters
- **Docstrings**: Google style
- **Type hints**: Required for all function signatures
- **Imports**: Grouped and sorted (standard library, third-party, local)

### Code Formatting

We use the following tools for code formatting and quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Static type checking

Run the following commands to format and check your code:

```bash
make format  # Auto-format code
make lint    # Run linters
make type-check  # Run type checking
```

## Testing Guidelines

### Writing Tests

- Write tests for all new features and bug fixes
- Follow the Arrange-Act-Assert pattern
- Use descriptive test names
- Keep tests independent and isolated

### Running Tests

```bash
# Run all tests
make test

# Run a specific test file
pytest tests/unit/test_quantum_network.py -v

# Run tests with coverage
pytest --cov=athenamist_integration tests/
```

### Test Structure

```python
def test_functionality_description():
    # Arrange
    # Set up test data and environment
    
    # Act
    # Call the function/method being tested
    
    # Assert
    # Verify the results
    assert expected == actual
```

## API Development

### Adding New API Endpoints

1. Create a new route file in `athenamist_integration/api/routes/`
2. Define your FastAPI route handlers
3. Add the router to `athenamist_integration/api/main.py`
4. Write tests for your endpoints

Example endpoint:

```python
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/quantum/state/{state_id}")
async def get_quantum_state(state_id: str):
    """
    Retrieve a quantum state by ID.
    
    Args:
        state_id: The ID of the quantum state to retrieve
        
    Returns:
        The quantum state data
        
    Raises:
        HTTPException: If the state is not found
    """
    state = await quantum_state_service.get_state(state_id)
    if not state:
        raise HTTPException(status_code=404, detail="Quantum state not found")
    return state
```

## Quantum Module Development

### Creating a New Quantum Module

1. Create a new Python file in `athenamist_integration/core/quantum/`
2. Define your quantum operations as methods
3. Add type hints and docstrings
4. Write unit tests

Example quantum module:

```python
from qiskit import QuantumCircuit
from typing import List, Optional

class QuantumEntangler:
    """Handles quantum entanglement operations."""
    
    def create_bell_pair(self) -> QuantumCircuit:
        """
        Create a Bell pair (entangled qubits).
        
        Returns:
            QuantumCircuit: Circuit with a Bell pair
        """
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        return qc
```

## Performance Optimization

### Profiling

Use the following tools to identify performance bottlenecks:

```bash
# CPU profiling
python -m cProfile -o profile.stats your_script.py

# Memory profiling
python -m memory_profiler your_script.py
```

### Optimization Techniques

- Use async/await for I/O-bound operations
- Cache expensive computations
- Use generators for large datasets
- Optimize database queries

## Debugging

### Debugging Tools

- **pdb**: Python debugger
- **ipdb**: Enhanced debugger with IPython features
- **VS Code Debugger**: Integrated debugging in VS Code

### Common Issues

1. **Quantum simulation is slow**:
   - Use Aer's statevector simulator for small circuits
   - Reduce the number of shots when possible
   
2. **API timeouts**:
   - Increase timeout values in configuration
   - Implement retry logic with exponential backoff

## Version Control

### Branch Naming

Format: `type/description-issue`

Example: `feat/quantum-entanglement-42`

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Example:
```
feat(quantum): add support for quantum teleportation

- Implemented quantum teleportation circuit
- Added tests for teleportation fidelity
- Updated documentation

Fixes #42
```

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """Short description of the function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of the return value
        
    Raises:
        ValueError: If parameters are invalid
    """
```

### Updating Documentation

1. Update docstrings in the code
2. Update relevant markdown files in `docs/`
3. Rebuild the documentation if using Sphinx

## Getting Help

- Check the [documentation](https://github.com/MKWorldWide/Primal-Genesis-Engine-Sovereign/tree/main/docs)
- Search existing issues
- Open a new issue if your question hasn't been answered
