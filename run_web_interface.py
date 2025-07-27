#!/usr/bin/env python3
"""
AthenaMist-Blended Web Interface Launcher
=========================================

This script launches the AthenaMist-Blended web interface with proper
configuration and error handling.

Features:
- Automatic dependency checking
- Configuration validation
- Error handling and recovery
- Development and production modes
- Port and host configuration

Usage:
    python3 run_web_interface.py [--host HOST] [--port PORT] [--debug]

Author: AthenaMist Development Team
Version: 2.0.0
Last Updated: 2024-12-19
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'jinja2',
        'websockets',
        'pydantic'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("💡 Install missing packages with: pip install -r requirements.txt")
        return False
    
    print("✅ All required dependencies are installed")
    return True

def check_configuration():
    """Check if configuration is properly set up"""
    config_file = Path("athenamist_config.json")
    
    if not config_file.exists():
        print("⚠️  Configuration file not found. Using default settings.")
        return True
    
    print("✅ Configuration file found")
    return True

def setup_environment():
    """Setup environment for web interface"""
    # Set working directory to web interface directory
    web_dir = Path("athenamist_integration/web")
    
    if not web_dir.exists():
        print(f"❌ Web interface directory not found: {web_dir}")
        return False
    
    # Change to web directory
    os.chdir(web_dir)
    print(f"📁 Working directory: {os.getcwd()}")
    
    return True

def launch_web_interface(host="0.0.0.0", port=8000, debug=False):
    """Launch the web interface"""
    try:
        print("🚀 Launching AthenaMist-Blended Web Interface...")
        print(f"🌐 Host: {host}")
        print(f"🔌 Port: {port}")
        print(f"🐛 Debug mode: {debug}")
        print()
        
        # Import and run the web application
        sys.path.append(str(Path(__file__).parent / "athenamist_integration" / "web"))
        
        from app import create_web_app
        
        app = create_web_app()
        app.run(host=host, port=port, debug=debug)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're in the correct directory and all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Error launching web interface: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Launch AthenaMist-Blended Web Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 run_web_interface.py                    # Launch with default settings
  python3 run_web_interface.py --host 127.0.0.1   # Launch on localhost only
  python3 run_web_interface.py --port 8080        # Launch on port 8080
  python3 run_web_interface.py --debug            # Launch in debug mode
        """
    )
    
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    
    args = parser.parse_args()
    
    print("🌟 AthenaMist-Blended Web Interface Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check configuration
    if not check_configuration():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Launch web interface
    if not launch_web_interface(args.host, args.port, args.debug):
        sys.exit(1)

if __name__ == "__main__":
    main() 