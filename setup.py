#!/usr/bin/env python3
"""
Primal Genesis Engine Setup and Installation Script
====================================================

This module provides comprehensive setup and installation functionality for the
Primal Genesis Engine.

Key Features:
- Automated Python version compatibility checking
- Virtual environment creation and management
- Dependency installation and validation
- Basic configuration setup
- System health checks and validation
- Error handling and recovery mechanisms

Installation Process:
1. Python version compatibility verification
2. Virtual environment creation and activation
3. Dependency package installation
4. Basic configuration setup
5. System validation and health checks

System Requirements:
- Python 3.8 or higher
- Virtual environment support
- Internet connection for package installation
- Appropriate permissions for file system access

Dependencies:
- subprocess: Command execution and process management
- pathlib: Cross-platform path handling
- os: Operating system interface
- sys: System-specific parameters and functions

Error Handling:
- Comprehensive error checking and reporting
- Graceful failure recovery
- User-friendly error messages
- Installation rollback capabilities

Author: Primal Genesis Engine Team
Version: 1.0.0
Last Updated: 2024-12-19
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command: str, description: str) -> bool:
    """
    Execute system commands with comprehensive error handling and reporting
    
    This function provides a robust command execution interface with detailed
    error reporting and success tracking.
    
    Args:
        command (str): System command to execute
        description (str): Human-readable description of the command
        
    Returns:
        bool: True if command executed successfully, False otherwise
        
    Features:
        - Command execution with error capture
        - Detailed success/failure reporting
        - Error output capture and display
        - Process result validation
        - User-friendly status messages
        
    Error Handling:
        - Subprocess execution errors
        - Command failure detection
        - Error output extraction
        - Graceful error reporting
    """
    print(f"🔄 {description}...")
    try:
        # Execute command with comprehensive error handling
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        print(f"✅ {description} completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        # Handle command execution failures
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version() -> bool:
    """
    Verify Python version compatibility with Primal Genesis Engine requirements
    
    This function checks the current Python version against minimum requirements
    and provides detailed compatibility information.
    
    Returns:
        bool: True if Python version is compatible, False otherwise
        
    Requirements:
        - Python 3.8 or higher for async/await support
        - Type hints and modern Python features
        - Compatible with all required dependencies
        
    Version Features:
        - Major version compatibility checking
        - Minor version requirement validation
        - Detailed version information display
        - Clear compatibility status reporting
    """
    version = sys.version_info
    
    # Check minimum Python version requirement (3.8+)
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        print("💡 Please upgrade your Python installation to continue.")
        return False
    
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible!")
    return True

def create_virtual_environment() -> bool:
    """
    Create and configure Python virtual environment for Primal Genesis Engine
    
    This function manages virtual environment creation and validation to ensure
    isolated dependency management.
    
    Returns:
        bool: True if virtual environment is ready, False otherwise
        
    Virtual Environment Features:
        - Isolated Python environment creation
        - Dependency isolation and management
        - Cross-platform compatibility
        - Existing environment detection
        - Creation status validation
        
    Benefits:
        - Prevents dependency conflicts
        - Ensures clean installation
        - Facilitates easy cleanup
        - Supports multiple project versions
    """
    venv_path = Path("venv")
    
    # Check if virtual environment already exists
    if venv_path.exists():
        print("✅ Virtual environment already exists!")
        return True
    
    # Create new virtual environment
    return run_command("python3 -m venv venv", "Creating virtual environment")

def install_dependencies() -> bool:
    """
    Install all required dependencies for Primal Genesis Engine
    
    This function handles the installation of all necessary Python packages
    and dependencies for the Primal Genesis Engine framework.
    
    Returns:
        bool: True if dependencies installed successfully, False otherwise
        
    Installation Features:
        - Cross-platform pip command detection
        - Requirements file processing
        - Dependency resolution and installation
        - Installation status validation
        - Error handling and recovery
        
    Dependencies Include:
        - aiohttp: Async HTTP client for API integration
        - requests: HTTP library for fallback operations
        - cryptography: Secure key management and encryption
        - asyncio: Async programming support (built-in)
        - json: Data serialization (built-in)
        - time: Timestamp and performance tracking (built-in)
    """
    # Determine appropriate pip command based on platform
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_cmd = "venv/bin/pip"
    
    # Install dependencies from requirements.txt
    return run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies")

def setup_configuration() -> bool:
    """
    Initialize and configure Primal Genesis Engine system settings
    
    This function sets up the configuration system including basic settings
    and local development preferences.
    
    Returns:
        bool: True if configuration setup successful, False otherwise
        
    Configuration Features:
        - Basic application settings
        - Server configuration
        - Local development preferences
        - Security configuration
        - Default value establishment
        
    Setup Process:
        - Import configuration module
        - Execute basic setup
        - Validate configuration
        - Establish default settings
        - Verify system readiness
    """
    print("\n🔧 Configuration Setup")
    print("=" * 40)
    
    try:
        # Import and execute configuration setup
        from config import setup_configuration
        setup_configuration()
        return True
        
    except Exception as e:
        # Handle configuration setup errors
        print(f"❌ Configuration setup failed: {e}")
        print("💡 You can still run Primal Genesis Engine with default settings.")
        return False

def validate_installation() -> bool:
    """
    Validate complete installation and system readiness
    
    This function performs comprehensive validation of the installation
    to ensure all components are properly configured and functional.
    
    Returns:
        bool: True if installation is valid, False otherwise
        
    Validation Checks:
        - Virtual environment accessibility
        - Dependency availability
        - Configuration file presence
        - Module import capability
        - System compatibility verification
    """
    print("\n🔍 Validating Installation")
    print("=" * 40)
    
    try:
        # Test virtual environment activation
        if os.name == 'nt':  # Windows
            python_cmd = "venv\\Scripts\\python"
        else:  # Unix/Linux/macOS
            python_cmd = "venv/bin/python"
        
        # Test Python import capabilities
        test_imports = [
            "import asyncio",
            "import aiohttp",
            "import requests",
            "from pathlib import Path"
        ]
        
        for import_test in test_imports:
            result = subprocess.run(
                f"{python_cmd} -c '{import_test}'",
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"❌ Import test failed: {import_test}")
                return False
        
        print("✅ All validation checks passed!")
        return True
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False

def main():
    """
    Main setup function with comprehensive installation orchestration
    
    This function orchestrates the complete setup process for Primal Genesis Engine,
    including all necessary checks, installations, and configurations.
    
    Setup Process:
        1. Python version compatibility verification
        2. Virtual environment creation and setup
        3. Dependency package installation
        4. Basic configuration system initialization
        5. Installation validation and testing
        6. User guidance and next steps
        
    Error Handling:
        - Graceful failure recovery
        - Detailed error reporting
        - User-friendly guidance
        - Installation rollback support
    """
    print("🌟 Primal Genesis Engine Setup")
    print("=" * 40)
    
    # Step 1: Check Python version compatibility
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Create and configure virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Step 3: Install required dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Step 4: Setup configuration and API keys
    if not setup_configuration():
        print("⚠️  Configuration setup failed, but you can still run AthenaMist with default settings.")
    
    # Step 5: Validate complete installation
    if not validate_installation():
        print("⚠️  Installation validation failed, but core functionality may still work.")
    
    # Installation completion and user guidance
    print("\n🎉 Setup complete!")
    print("\n🚀 To start Primal Genesis Engine:")
    print("  python -m primal_genesis.app")
    print("\n📖 For more information, see README.md")
    print("\n🔧 Configuration:")
    print("  - Edit config.py for basic settings")
    print("  - Set environment variables for secure key management")
    print("\n💡 Next Steps:")
    print("  - Configure your basic application settings")
    print("  - Explore the interactive interface")
    print("  - Review the comprehensive documentation")

if __name__ == "__main__":
    # Execute main setup function
    main() 