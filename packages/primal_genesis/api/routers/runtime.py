"""
Runtime Router

Controlled runtime execution endpoint that routes through existing core runtime.

Author: Primal Genesis Engine Team
Version: 0.1.0
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel

from ...core import CoreRuntime


# Dependency injection for core runtime
def get_core_runtime() -> CoreRuntime:
    """Get core runtime instance."""
    return CoreRuntime()


router = APIRouter()


class ExecutionRequest(BaseModel):
    """Request model for runtime execution."""
    module_name: str
    action_name: str
    payload: Optional[Dict[str, Any]] = None


class ExecutionResponse(BaseModel):
    """Response model for runtime execution."""
    executed: bool
    execution_mode: str
    outcome: str
    payload: Optional[Dict[str, Any]]
    execution_details: Dict[str, Any]
    message: Optional[str] = None
    error: Optional[str] = None


@router.post("/runtime/execute", response_model=ExecutionResponse)
async def execute_module_action(
    request: ExecutionRequest,
    runtime: CoreRuntime = Depends(get_core_runtime)
) -> ExecutionResponse:
    """
    Execute a module action through existing core runtime.
    
    Args:
        request: Execution request with module, action, and optional payload
        runtime: Core runtime instance
        
    Returns:
        ExecutionResponse: Structured execution result
        
    Raises:
        HTTPException: If execution fails due to invalid inputs
    """
    try:
        # Route through existing core runtime
        result = runtime.execute_module_action(
            module_name=request.module_name,
            action_name=request.action_name,
            payload=request.payload
        )
        
        return ExecutionResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Runtime execution failed: {str(e)}"
        )


@router.get("/runtime/check/{module_name}/{action_name}")
async def check_module_action(
    module_name: str,
    action_name: str,
    runtime: CoreRuntime = Depends(get_core_runtime)
) -> Dict[str, Any]:
    """
    Check if a module action is allowed without executing it.
    
    Args:
        module_name: Name of module to check
        action_name: Name of action to check
        runtime: Core runtime instance
        
    Returns:
        Dict with policy evaluation result
    """
    try:
        return runtime.check_module_action(module_name, action_name)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Policy check failed: {str(e)}"
        )
