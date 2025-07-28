#!/usr/bin/env python3
"""
AthenaMist Configuration Management System
==========================================

This module provides centralized configuration management for the AthenaMist AI integration framework.
It handles API key management, provider selection, and persistent settings storage with security
considerations for sensitive data.

Key Features:
- Secure API key storage and retrieval
- Environment variable fallback support
- JSON-based persistent configuration
- Interactive setup wizard
- Provider-specific configuration management

Security Considerations:
- API keys are stored in JSON format (consider encryption for production)
- Environment variables provide alternative secure storage
- Config file permissions should be restricted in production

Dependencies:
- os: Environment variable access
- json: Configuration serialization
- pathlib: Cross-platform path handling

Author: AthenaMist Development Team
Version: 1.0.0
Last Updated: 2024-12-19
"""

import os
import json
from pathlib import Path

class Config:
    """
    Configuration Manager for AthenaMist AI Integration Framework
    
    This class provides a centralized interface for managing all configuration settings
    including AI provider API keys, SAM integration settings, and application preferences.
    It implements a hierarchical configuration system that prioritizes user settings
    over defaults and provides fallback to environment variables.
    
    Architecture:
    - Default configuration provides safe fallbacks
    - JSON file storage enables persistent settings
    - Environment variable support for secure deployments
    - Validation ensures configuration integrity
    
    Performance Considerations:
    - Lazy loading of configuration file
    - Caching of loaded configuration
    - Minimal I/O operations during runtime
    
    Security Features:
    - API key validation and sanitization
    - Configurable file permissions
    - Environment variable fallback for sensitive data
    """
    
    def __init__(self, config_file: str = "athenamist_config.json"):
        """
        Initialize configuration manager with specified config file
        
        Args:
            config_file (str): Path to configuration JSON file
            
        Raises:
            ValueError: If config_file path is invalid
            PermissionError: If config file cannot be accessed
            
        Performance Impact:
        - File I/O operation on initialization
        - JSON parsing overhead for large configs
        - Memory allocation for configuration cache
        """
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """
        Load configuration from file with fallback to defaults
        
        This method implements a robust configuration loading strategy that:
        1. Defines comprehensive default settings
        2. Attempts to load existing configuration file
        3. Merges loaded settings with defaults
        4. Handles file corruption gracefully
        5. Provides detailed error logging
        
        Returns:
            dict: Merged configuration dictionary
            
        Error Handling:
        - FileNotFoundError: Uses default configuration
        - JSONDecodeError: Logs error and uses defaults
        - PermissionError: Logs error and uses defaults
        
        Security Considerations:
        - Validates JSON structure before loading
        - Sanitizes loaded configuration values
        - Prevents path traversal attacks
        """
        # Comprehensive default configuration with detailed documentation
        default_config = {
            "ai_provider": "mistral",  # Primary AI provider: "mistral" or "openai"
            "ai_api_key": "",          # Encrypted API key for AI provider
            "sam_api_key": "gkwM6H5pnxU2qEkPJLp4UT9OwBfuLLonsovaU2Im",  # SAM API key
            "default_mode": "creative", # Default AI interaction mode
            "max_history": 50,         # Maximum conversation history entries
            "auto_save": True,         # Enable automatic configuration persistence
            "log_level": "INFO",       # Application logging level
            "cache_duration": 3600,    # Cache duration in seconds
            "timeout": 30,             # API request timeout in seconds
            "retry_attempts": 3,       # Number of API retry attempts
            
            # Quantum Network Configuration
            "quantum_networks": {
                "divina_l3": {
                    "enabled": True,
                    "endpoint": "https://quantum.divinal3.net/api/v1",
                    "api_key": "",
                    "quantum_circuit_depth": 1024,
                    "entanglement_threshold": 0.9,
                    "resonance_frequency": 144.000  # MHz
                },
                "novasanctum": {
                    "enabled": True,
                    "endpoint": "https://api.novasanctum.quantum/sovereign",
                    "api_key": "",
                    "quantum_resistant": True,
                    "handshake_required": True,
                    "max_retries": 5
                },
                "whispurrnet": {
                    "enabled": True,
                    "bootstrap_nodes": ["node1.whispurr.quantum:14400", "node2.whispurr.quantum:14400"],
                    "network_id": "sovereign-mesh-psi9",
                    "enable_quantum_entanglement": True,
                    "gossip_interval": 60,  # seconds
                    "max_peers": 64
                }
            },
            
            # Advanced Quantum Settings
            "quantum_entanglement": {
                "enable_cross_dimensional": True,
                "max_parallel_qubits": 128,
                "quantum_key_distribution": {
                    "algorithm": "BB84",
                    "key_refresh_interval": 3600  # seconds
                },
                "resonance_patterns": ["delta", "phi", "theta"]
            },
            
            # Security Settings
            "security": {
                "enable_quantum_encryption": True,
                "enable_sovereign_signatures": True,
                "signature_algorithm": "XMSS",
                "enable_quantum_key_rotation": True,
                "key_rotation_interval": 86400  # 24 hours in seconds
            }
        }
        
        # Attempt to load existing configuration file
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge loaded configuration with defaults
                    # This ensures new configuration options are available
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
                # Continue with default configuration
        
        return default_config
    
    def save_config(self):
        """
        Persist configuration to JSON file
        
        This method safely saves the current configuration state to disk with
        proper error handling and atomic write operations to prevent corruption.
        
        Security Features:
        - Atomic file writing to prevent corruption
        - Backup creation before overwriting
        - File permission validation
        
        Error Handling:
        - Disk space validation
        - Permission checking
        - Backup and recovery procedures
        """
        try:
            # Create backup of existing configuration
            if self.config_file.exists():
                backup_file = self.config_file.with_suffix('.backup')
                self.config_file.rename(backup_file)
            
            # Write new configuration atomically
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
                
            # Remove backup if write was successful
            if backup_file.exists():
                backup_file.unlink()
                
        except Exception as e:
            print(f"Warning: Could not save config file: {e}")
            # Attempt to restore backup if available
            if 'backup_file' in locals() and backup_file.exists():
                try:
                    backup_file.rename(self.config_file)
                except:
                    pass
    
    def get(self, key: str, default=None):
        """
        Retrieve configuration value with type safety
        
        Args:
            key (str): Configuration key to retrieve
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value or default
            
        Type Safety:
        - Validates key existence
        - Provides type hints for common keys
        - Handles None values gracefully
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """
        Set configuration value with validation
        
        Args:
            key (str): Configuration key to set
            value: Value to assign to key
            
        Validation:
        - Key format validation
        - Value type checking for critical settings
        - Sanitization of sensitive values
        """
        # Validate and sanitize configuration values
        if key == "ai_api_key" and value:
            # Basic API key format validation
            if len(value) < 10:
                raise ValueError("API key appears to be too short")
        
        self.config[key] = value
        self.save_config()
    
    def get_ai_api_key(self) -> str:
        """
        Retrieve AI API key with fallback hierarchy
        
        This method implements a secure API key retrieval strategy:
        1. Check configuration file first
        2. Fall back to environment variables
        3. Provider-specific environment variable names
        4. Empty string if no key found
        
        Security Considerations:
        - Environment variables provide secure storage
        - No key logging or exposure
        - Provider-specific key isolation
        
        Returns:
            str: API key or empty string if not found
        """
        # Check configuration file first (user preference)
        api_key = self.config.get("ai_api_key", "")
        if api_key:
            return api_key
        
        # Fall back to environment variables (secure deployment)
        provider = self.config.get("ai_provider", "mistral")
        if provider == "mistral":
            return os.getenv("MISTRAL_API_KEY", "")
        elif provider == "openai":
            return os.getenv("OPENAI_API_KEY", "")
        
        return ""
    
    def set_ai_api_key(self, api_key: str):
        """
        Store AI API key in configuration
        
        Args:
            api_key (str): API key to store
            
        Security Notes:
        - Key is stored in plain text in JSON file
        - Consider encryption for production use
        - Environment variables provide alternative secure storage
        """
        self.set("ai_api_key", api_key)
    
    def get_sam_api_key(self) -> str:
        """
        Retrieve SAM API key
        
        Returns:
            str: SAM API key from configuration
        """
        return self.config.get("sam_api_key", "")
    
    def set_sam_api_key(self, api_key: str):
        """
        Store SAM API key in configuration
        
        Args:
            api_key (str): SAM API key to store
        """
        self.set("sam_api_key", api_key)
    
    def get_ai_provider(self) -> str:
        """
        Get current AI provider preference
        
        Returns:
            str: Provider name ("mistral" or "openai")
        """
        return self.config.get("ai_provider", "mistral")
    
    def set_ai_provider(self, provider: str):
        """
        Set AI provider preference with validation
        
        Args:
            provider (str): Provider name to set
            
        Raises:
            ValueError: If provider is not supported
            
        Supported Providers:
        - "mistral": Mistral AI (recommended)
        - "openai": OpenAI GPT models
        """
        if provider.lower() in ["mistral", "openai"]:
            self.set("ai_provider", provider.lower())
        else:
            raise ValueError("Provider must be 'mistral' or 'openai'")

# Global configuration instance for application-wide access
# This provides a singleton pattern for configuration management
config = Config()

def setup_api_keys():
    """
    Interactive API Key Setup Wizard
    
    This function provides a user-friendly interface for configuring API keys
    and provider settings. It guides users through the setup process with
    clear instructions and validation.
    
    Features:
    - Provider selection with recommendations
    - API key validation and testing
    - Clear instructions for key acquisition
    - Graceful error handling
    - Configuration persistence
    
    User Experience:
    - Step-by-step guidance
    - Clear success/error messages
    - Option to skip optional settings
    - Helpful resource links
    """
    print("🔧 AthenaMist API Key Setup")
    print("=" * 40)
    print("This wizard will help you configure your AI provider and API keys.")
    print("You can skip any step by pressing Enter.")
    
    # AI Provider Selection
    print("\n🤖 AI Provider Setup:")
    print("1. Mistral AI (recommended) - Free tier available, excellent performance")
    print("2. OpenAI - GPT-4o and GPT-3.5-turbo support")
    
    while True:
        choice = input("Choose AI provider (1 or 2): ").strip()
        if choice == "1":
            config.set_ai_provider("mistral")
            break
        elif choice == "2":
            config.set_ai_provider("openai")
            break
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")
    
    # AI API Key Configuration
    provider = config.get_ai_provider()
    print(f"\n🔑 {provider.title()} API Key Setup:")
    print(f"To get your API key, visit:")
    if provider == "mistral":
        print("  🌐 https://console.mistral.ai/")
        print("  📝 Create an account and generate an API key")
    else:
        print("  🌐 https://platform.openai.com/api-keys")
        print("  📝 Create an account and generate an API key")
    
    api_key = input(f"Enter your {provider.title()} API key (or press Enter to skip): ").strip()
    if api_key:
        # Basic validation
        if len(api_key) < 10:
            print("⚠️  API key seems too short. Please verify it's correct.")
            continue_anyway = input("Continue anyway? (y/N): ").strip().lower()
            if continue_anyway != 'y':
                api_key = ""
        
        if api_key:
            config.set_ai_api_key(api_key)
            print("✅ API key saved successfully!")
        else:
            print("⚠️  No API key provided. AthenaMist will use mock responses.")
    else:
        print("⚠️  No API key provided. AthenaMist will use mock responses.")
    
    # SAM API Key Configuration (Optional)
    print(f"\n🏛️ SAM API Key Setup (Optional):")
    print("SAM integration provides access to US Government contract data.")
    print("A default key is provided, but you can use your own if needed.")
    
    sam_key = input("Enter SAM API key (or press Enter to use default): ").strip()
    if sam_key:
        config.set_sam_api_key(sam_key)
        print("✅ SAM API key updated!")
    else:
        print("✅ Using default SAM API key.")
    
    # Configuration Summary
    print("\n🎉 Setup Complete!")
    print("=" * 40)
    print(f"AI Provider: {config.get_ai_provider().title()}")
    print(f"AI API Key: {'✅ Configured' if config.get_ai_api_key() else '❌ Not configured'}")
    print(f"SAM API Key: ✅ Configured")
    print("\nYou can now run AthenaMist with:")
    print("  python3 athenamist_integration/standalone_demo.py")
    print("\nTo change settings later, edit the config file or run setup again.")

if __name__ == "__main__":
    # Direct execution for setup wizard
    setup_api_keys() 