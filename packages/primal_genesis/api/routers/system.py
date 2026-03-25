"""
System Router

Read-only endpoints for system visibility using existing core services.

Author: Primal Genesis Engine Team
Version: 0.1.0
"""

from fastapi import APIRouter, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from ...core import VisibilityService, ConsoleBridge


# Dependency injection for core services
def get_visibility_service() -> VisibilityService:
    """Get visibility service instance."""
    return VisibilityService()


def get_console_bridge() -> ConsoleBridge:
    """Get console bridge instance."""
    return ConsoleBridge(VisibilityService())


router = APIRouter()


class SystemSnapshotResponse(BaseModel):
    """Response model for system snapshot."""
    timestamp: str
    console_version: str
    system_status: Dict[str, Any]
    modules: Dict[str, Any]
    policies: Dict[str, Any]
    memory: Dict[str, Any]
    activity: Dict[str, Any]


class ModuleOverviewResponse(BaseModel):
    """Response model for module overview."""
    timestamp: str
    summary: Dict[str, Any]
    modules_by_type: Dict[str, List[str]]
    module_details: List[Dict[str, Any]]


class RecentActivityResponse(BaseModel):
    """Response model for recent activity."""
    timestamp: str
    summary: Dict[str, Any]
    activities: List[Dict[str, Any]]


@router.get("/snapshot", response_model=SystemSnapshotResponse)
async def get_system_snapshot(
    console_bridge: ConsoleBridge = Depends(get_console_bridge)
) -> SystemSnapshotResponse:
    """
    Get complete system snapshot.
    
    Returns:
        SystemSnapshotResponse: Complete system state from console bridge
    """
    snapshot = console_bridge.get_console_summary()
    return SystemSnapshotResponse(**snapshot)


@router.get("/modules", response_model=ModuleOverviewResponse)
async def get_modules_overview(
    console_bridge: ConsoleBridge = Depends(get_console_bridge)
) -> ModuleOverviewResponse:
    """
    Get module overview with health metrics.
    
    Returns:
        ModuleOverviewResponse: Module information and health percentages
    """
    overview = console_bridge.get_module_overview()
    return ModuleOverviewResponse(**overview)


@router.get("/policies", response_model=Dict[str, Any])
async def get_policies_overview(
    visibility_service: VisibilityService = Depends(get_visibility_service)
) -> Dict[str, Any]:
    """
    Get policies overview.
    
    Returns:
        Dict with policy information from visibility service
    """
    return visibility_service.get_policy_overview()


@router.get("/memory/recent", response_model=RecentActivityResponse)
async def get_recent_memory(
    console_bridge: ConsoleBridge = Depends(get_console_bridge),
    limit: Optional[int] = 10
) -> RecentActivityResponse:
    """
    Get recent memory/activity.
    
    Args:
        limit: Maximum number of activities to return
        
    Returns:
        RecentActivityResponse: Recent activities formatted for display
    """
    activity = console_bridge.get_recent_activity(limit=limit)
    return RecentActivityResponse(**activity)
