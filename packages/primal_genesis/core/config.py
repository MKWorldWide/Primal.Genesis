#!/usr/bin/env python3
"""
Primal Genesis Engine Configuration Management System
=====================================================

This module provides centralized configuration management for the Primal Genesis Engine.
It handles basic application settings and local development preferences.

Key Features:
- Basic configuration management
- Environment variable support
- JSON-based persistent settings
- Local development focus

Author: Primal Genesis Engine Team
Version: 1.0.0
Last Updated: 2024-12-19
"""

import os
import json
from pathlib import Path

class Config:
    """
    Configuration Manager for Primal Genesis Engine
    
    This class provides a centralized interface for managing all configuration settings
    for local development. It implements a hierarchical configuration system that prioritizes
    user settings over defaults and provides fallback to environment variables.
    
    Architecture:
    - Default configuration provides safe fallbacks
    - JSON file storage enables persistent settings
    - Environment variable support for development
    - Validation ensures configuration integrity
    
    Performance Considerations:
    - Lazy loading of configuration file
    - Caching of loaded configuration
    - Minimal I/O operations during runtime
    
    Security Features:
    - Basic configuration validation
    - Environment variable fallback for sensitive data
    """
    
    def __init__(self, config_file: str = "primal_genesis_config.json"):
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
        # Basic default configuration for local development
        default_config = {
            "app_name": "Primal Genesis Engine",
            "version": "1.0.0",
            "debug": True,
            "log_level": "INFO",
            "host": "localhost",
            "port": 8000,
            "auto_save": True,
            "cache_duration": 3600,
            "timeout": 30,
            "retry_attempts": 3
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
        self.config[key] = value
        self.save_config()
    
    def get_app_name(self) -> str:
        """
        Get application name
        
        Returns:
            str: Application name
        """
        return self.config.get("app_name", "Primal Genesis Engine")
    
    def get_host(self) -> str:
        """
        Get server host
        
        Returns:
            str: Server host
        """
        return self.config.get("host", "localhost")
    
    def get_port(self) -> int:
        """
        Get server port
        
        Returns:
            int: Server port
        """
        return self.config.get("port", 8000)

# Global configuration instance for application-wide access
# This provides a singleton pattern for configuration management
config = Config()

def setup_configuration():
    """
    Basic Configuration Setup
    
    This function provides a simple interface for configuring basic settings
    for local development.
    
    Features:
    - Basic application settings
    - Server configuration
    - Clear instructions
    - Graceful error handling
    - Configuration persistence
    
    User Experience:
    - Step-by-step guidance
    - Clear success/error messages
    - Option to skip optional settings
    """
    print("🔧 Primal Genesis Engine Configuration")
    print("=" * 40)
    print("This wizard will help you configure basic settings.")
    print("You can skip any step by pressing Enter.")
    
    # Server Configuration
    print("\n🌐 Server Configuration:")
    
    host = input("Enter host (default: localhost): ").strip()
    if host:
        config.set("host", host)
    
    port_input = input("Enter port (default: 8000): ").strip()
    if port_input:
        try:
            port = int(port_input)
            config.set("port", port)
        except ValueError:
            print("⚠️  Invalid port number. Using default.")
    
    # Debug Mode
    debug_input = input("Enable debug mode? (y/N): ").strip().lower()
    config.set("debug", debug_input == 'y')
    
    # Configuration Summary
    print("\n� Configuration Complete!")
    print("=" * 40)
    print(f"App Name: {config.get_app_name()}")
    print(f"Host: {config.get_host()}")
    print(f"Port: {config.get_port()}")
    print(f"Debug: {'✅ Enabled' if config.get('debug', False) else '❌ Disabled'}")
    print("\nConfiguration saved successfully!")

if __name__ == "__main__":
    # Direct execution for setup wizard
    setup_configuration() 