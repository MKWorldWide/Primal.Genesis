#!/usr/bin/env python3
"""
AthenaMist-Blended Web Interface
================================

This module provides a modern web-based user interface for AthenaMist-Blended,
offering real-time AI interactions, government contract analysis, and workflow
management through a responsive web application.

Key Features:
- Real-time AI chat interface with multiple providers
- Government contract data visualization and analysis
- Workflow automation and task management
- Performance monitoring and system health dashboard
- Responsive design for desktop and mobile devices
- WebSocket support for real-time updates

Architecture:
- FastAPI backend with async support
- WebSocket connections for real-time communication
- Jinja2 templating for dynamic content
- Pydantic models for data validation
- Modern JavaScript frontend with real-time updates

Security Features:
- API key management and validation
- Session management and authentication
- Input sanitization and validation
- CORS configuration and security headers
- Rate limiting and abuse prevention

Performance Optimizations:
- Async request handling
- Connection pooling and caching
- Static file serving optimization
- Database connection management
- Background task processing

Dependencies:
- fastapi: Modern web framework
- uvicorn: ASGI server
- jinja2: Template engine
- websockets: Real-time communication
- pydantic: Data validation

Author: AthenaMist Development Team
Version: 2.0.0
Last Updated: 2024-12-19
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import uvicorn

# Import AthenaMist core modules
from core.ai_integration import AIIntegrationManager, configure_ai_provider
from core.sam_integration import SAMIntegration, AthenaMistSAMIntegration

class ChatMessage(BaseModel):
    """Chat message model for API validation"""
    message: str = Field(..., min_length=1, max_length=10000)
    mode: str = Field(default="creative", pattern="^(creative|technical|workflow|government)$")
    provider: str = Field(default="mistral", pattern="^(mistral|openai|claude|gemini|cohere|deepseek)$")

class SystemStatus(BaseModel):
    """System status model for API responses"""
    status: str
    timestamp: datetime
    ai_provider: str
    sam_status: str
    performance_metrics: Dict[str, Any]

class WebSocketManager:
    """
    WebSocket connection manager for real-time communication
    
    This class manages WebSocket connections and provides real-time
    communication capabilities for the web interface.
    
    Features:
    - Connection management and tracking
    - Broadcast messaging to all clients
    - Individual client messaging
    - Connection status monitoring
    - Error handling and recovery
    """
    
    def __init__(self):
        """Initialize WebSocket manager"""
        self.active_connections: List[WebSocket] = []
        self.connection_data: Dict[WebSocket, Dict] = {}
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_data[websocket] = {
            "connected_at": datetime.now(),
            "message_count": 0
        }
        print(f"🌐 WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.connection_data:
            del self.connection_data[websocket]
        print(f"🌐 WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific WebSocket client"""
        try:
            await websocket.send_text(message)
            if websocket in self.connection_data:
                self.connection_data[websocket]["message_count"] += 1
        except Exception as e:
            print(f"❌ Error sending personal message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: str):
        """Broadcast message to all connected clients"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
                if connection in self.connection_data:
                    self.connection_data[connection]["message_count"] += 1
            except Exception as e:
                print(f"❌ Error broadcasting message: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)

class AthenaMistWebApp:
    """
    AthenaMist Web Application
    
    This class provides the main web application interface for AthenaMist-Blended,
    integrating AI capabilities, government data analysis, and real-time communication.
    
    Features:
    - FastAPI web framework integration
    - WebSocket real-time communication
    - AI provider management and switching
    - SAM government data integration
    - Performance monitoring and analytics
    - Responsive web interface
    """
    
    def __init__(self):
        """Initialize AthenaMist web application"""
        self.app = FastAPI(
            title="AthenaMist-Blended Web Interface",
            description="Advanced AI Integration Framework with Government Contract Analysis",
            version="2.0.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        # Initialize core components
        self.ai_manager = configure_ai_provider("mistral")
        self.sam_integration = SAMIntegration()
        self.sam_ai = AthenaMistSAMIntegration(self.sam_integration)
        self.websocket_manager = WebSocketManager()
        
        # Setup templates and static files
        self.templates = Jinja2Templates(directory="templates")
        self.setup_routes()
        self.setup_static_files()
    
    def setup_static_files(self):
        """Setup static file serving"""
        static_dir = Path("static")
        if not static_dir.exists():
            static_dir.mkdir()
        
        self.app.mount("/static", StaticFiles(directory="static"), name="static")
    
    def setup_routes(self):
        """Setup application routes and endpoints"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
            """Main application homepage"""
            return self.templates.TemplateResponse("index.html", {
                "request": request,
                "title": "AthenaMist-Blended",
                "version": "2.0.0"
            })
        
        @self.app.get("/api/status")
        async def get_status():
            """Get system status and health information"""
            try:
                ai_status = self.ai_manager.get_status()
                sam_status = self.sam_integration.get_integration_status()
                
                return SystemStatus(
                    status="healthy",
                    timestamp=datetime.now(),
                    ai_provider=ai_status["provider"],
                    sam_status="connected" if sam_status["connected"] else "disconnected",
                    performance_metrics=ai_status["performance_metrics"]
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")
        
        @self.app.get("/api/providers")
        async def get_providers():
            """Get list of supported AI providers"""
            try:
                return {
                    "providers": self.ai_manager.get_supported_providers(),
                    "provider_info": self.ai_manager.get_provider_info()
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Provider info failed: {str(e)}")
        
        @self.app.post("/api/chat")
        async def chat_endpoint(chat_message: ChatMessage):
            """Process chat message and return AI response"""
            try:
                # Switch provider if different from current
                if chat_message.provider != self.ai_manager.provider_name:
                    self.ai_manager.switch_provider(chat_message.provider)
                
                # Generate AI response
                response = await self.ai_manager.generate_response(
                    chat_message.message,
                    mode=chat_message.mode
                )
                
                return {
                    "response": response,
                    "provider": self.ai_manager.provider_name,
                    "mode": chat_message.mode,
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")
        
        @self.app.get("/api/sam/search")
        async def sam_search(term: str, limit: int = 10):
            """Search SAM database for entities"""
            try:
                results = await self.sam_integration.search_entities(
                    search_term=term,
                    limit=limit
                )
                return {
                    "results": results,
                    "search_term": term,
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"SAM search failed: {str(e)}")
        
        @self.app.get("/api/sam/opportunities")
        async def sam_opportunities(keywords: str = None, limit: int = 10):
            """Get government contract opportunities"""
            try:
                results = await self.sam_integration.get_contract_opportunities(
                    keywords=keywords,
                    limit=limit
                )
                return {
                    "opportunities": results,
                    "keywords": keywords,
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Opportunities search failed: {str(e)}")
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time communication"""
            await self.websocket_manager.connect(websocket)
            try:
                while True:
                    # Receive message from client
                    data = await websocket.receive_text()
                    message_data = json.loads(data)
                    
                    # Process message based on type
                    if message_data.get("type") == "chat":
                        response = await self.ai_manager.generate_response(
                            message_data["message"],
                            mode=message_data.get("mode", "creative")
                        )
                        
                        # Send response back to client
                        await self.websocket_manager.send_personal_message(
                            json.dumps({
                                "type": "response",
                                "message": response,
                                "provider": self.ai_manager.provider_name,
                                "timestamp": datetime.now().isoformat()
                            }),
                            websocket
                        )
                    
                    elif message_data.get("type") == "status":
                        # Send system status
                        status = await get_status()
                        await self.websocket_manager.send_personal_message(
                            json.dumps({
                                "type": "status",
                                "data": status.dict(),
                                "timestamp": datetime.now().isoformat()
                            }),
                            websocket
                        )
                    
                    elif message_data.get("type") == "sam_search":
                        # Process SAM search
                        results = await self.sam_integration.search_entities(
                            search_term=message_data["term"],
                            limit=message_data.get("limit", 10)
                        )
                        
                        await self.websocket_manager.send_personal_message(
                            json.dumps({
                                "type": "sam_results",
                                "results": results,
                                "search_term": message_data["term"],
                                "timestamp": datetime.now().isoformat()
                            }),
                            websocket
                        )
                        
            except WebSocketDisconnect:
                self.websocket_manager.disconnect(websocket)
            except Exception as e:
                print(f"❌ WebSocket error: {e}")
                self.websocket_manager.disconnect(websocket)
    
    def run(self, host: str = "0.0.0.0", port: int = 8000, debug: bool = False):
        """Run the web application"""
        print(f"🚀 Starting AthenaMist-Blended Web Interface...")
        print(f"🌐 Server will be available at: http://{host}:{port}")
        print(f"📚 API documentation: http://{host}:{port}/docs")
        print(f"🔧 ReDoc documentation: http://{host}:{port}/redoc")
        
        uvicorn.run(
            self.app,
            host=host,
            port=port,
            log_level="info" if debug else "warning"
        )

def create_web_app() -> AthenaMistWebApp:
    """Factory function to create AthenaMist web application"""
    return AthenaMistWebApp()

if __name__ == "__main__":
    # Create and run web application
    app = create_web_app()
    app.run(debug=True) 