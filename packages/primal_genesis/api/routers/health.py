"""
Health Router

Simple health check endpoint for API availability monitoring.

Author: Primal Genesis Engine Team
Version: 0.1.0
"""

from fastapi import APIRouter
from typing import Dict, Any
from datetime import datetime


router = APIRouter()


@router.get("/health", response_model=Dict[str, Any])
async def get_health() -> Dict[str, Any]:
    """
    Get API health status.
    
    Returns:
        Dict with health information and timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "0.1.0",
        "service": "primal-genesis-api",
        "execution_mode": "local-simulated"
    }
