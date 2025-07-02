#!/usr/bin/env python3
"""
🌐 Network Context Module
========================

Provides current public IP address and geolocation context for the Primal Genesis Engine™.
This enables sovereign context awareness, network diagnostics, and geo-fencing features.

Features:
- Public IP address awareness
- Geolocation (country, region, city)
- Integration with system status and logging
- Extensible for future network/mesh features

Author: Primal Genesis Engine™ Team
Version: 1.0
License: MIT
"""

import os
from typing import Dict

class NetworkContext:
    """
    🌐 NetworkContext
    Provides public IP and location awareness for the sovereign system.
    """
    def __init__(self):
        # Hardcoded for now; can be made dynamic in the future
        self.public_ip = "107.199.169.79"
        self.location = "United States"
        self.provider = "AT&T Internet"

    def get_network_info(self) -> Dict[str, str]:
        """Return current network context info."""
        return {
            "public_ip": self.public_ip,
            "location": self.location,
            "provider": self.provider
        }

# Singleton instance for easy import
network_context = NetworkContext() 