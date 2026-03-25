"""
FastAPI Application Entry Point

Creates the main FastAPI application with modular router structure.
This is the first API doorway into the engine, not the final framework.

Author: Primal Genesis Engine Team
Version: 0.1.0
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import health, system, runtime


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured application with routers
    """
    app = FastAPI(
        title="Primal Genesis Engine API",
        description="Minimal API exposure for Primal Genesis Engine",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware for development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health.router, prefix="/api/v1", tags=["Health"])
    app.include_router(system.router, prefix="/api/v1", tags=["System"])
    app.include_router(runtime.router, prefix="/api/v1", tags=["Runtime"])
    
    return app


# Create app instance for direct import
app = create_app()
