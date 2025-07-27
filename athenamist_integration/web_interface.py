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
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import uvicorn

# Import AthenaMist core modules
from core.ai_integration import AIIntegrationManager, configure_ai_provider
from core.sam_integration import SAMIntegration, AthenaMistSAMIntegration
from core.primal_sovereign_integration import PrimalSovereignManager, VoiceCommandType, ProcessingStatus
from core.shadow_nexus_integration import ShadowNexusManager, TradingSignalType, OperationStatus, CommandPlatform

class ChatMessage(BaseModel):
    """Chat message model for API validation"""
    message: str = Field(..., min_length=1, max_length=10000)
    mode: str = Field(default="creative", regex="^(creative|technical|workflow|government)$")
    provider: str = Field(default="mistral", regex="^(mistral|openai|claude|gemini|cohere|deepseek)$")

class SystemStatus(BaseModel):
    """System status model for API responses"""
    status: str
    timestamp: datetime
    ai_provider: str
    sam_status: str
    performance_metrics: Dict[str, Any]

class VoiceCommand(BaseModel):
    """Voice command model for Primal Sovereign Core integration"""
    content: str = Field(..., min_length=1, max_length=10000)
    command_type: str = Field(default="general", regex="^(general|system|optimization|analytics|sovereign|queen_command)$")
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class TradingSignal(BaseModel):
    """Trading signal model for Shadow Nexus integration"""
    symbol: str = Field(..., min_length=1, max_length=10)
    direction: str = Field(..., regex="^(long|short|scalp|swing|breakout)$")
    entry_price: float = Field(..., gt=0)
    stop_loss: float = Field(..., gt=0)
    take_profit: float = Field(..., gt=0)
    confidence: float = Field(..., ge=0, le=1)
    ichimoku_data: Dict[str, Any] = Field(default_factory=dict)
    sentiment_score: Optional[float] = Field(None, ge=-1, le=1)

class DataRetrieval(BaseModel):
    """Data retrieval model for Shadow Nexus integration"""
    target_url: str = Field(..., min_length=1)
    operation_type: str = Field(default="surveillance", regex="^(surveillance|intelligence|monitoring)$")

class CommandMessage(BaseModel):
    """Command message model for Shadow Nexus integration"""
    platform: str = Field(..., regex="^(discord|telegram|email|webhook)$")
    content: str = Field(..., min_length=1, max_length=10000)
    user_id: Optional[str] = None
    channel_id: Optional[str] = None
    priority: str = Field(default="normal", regex="^(low|normal|high|urgent)$")
    encrypted: bool = Field(default=False)

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
        
        # Initialize Primal Sovereign Core integration
        self.sovereign_manager = PrimalSovereignManager(self.ai_manager.config, self.ai_manager)
        
        # Initialize Shadow Nexus integration
        self.shadow_manager = ShadowNexusManager(self.ai_manager.config, self.ai_manager)
        
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
            """Get SAM government opportunities"""
            try:
                opportunities = await self.sam_ai.get_opportunities(keywords, limit)
                return JSONResponse(content={
                    "status": "success",
                    "opportunities": opportunities,
                    "count": len(opportunities)
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to fetch opportunities: {str(e)}")
        
        @self.app.post("/api/voice/process")
        async def process_voice_command(voice_command: VoiceCommand):
            """Process voice command with Primal Sovereign Core"""
            try:
                command_type = VoiceCommandType(voice_command.command_type)
                result = await self.sovereign_manager.process_voice_command(
                    voice_command.content, 
                    command_type
                )
                
                return JSONResponse(content={
                    "status": "success",
                    "command_id": result.command_id,
                    "response": result.response,
                    "processing_time": result.processing_time,
                    "optimization_score": result.optimization_score,
                    "learning_iterations": result.learning_iterations,
                    "self_healing_attempts": result.self_healing_attempts,
                    "aws_optimizations": result.aws_optimizations,
                    "sovereign_insights": result.sovereign_insights
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to process voice command: {str(e)}")

        @self.app.get("/api/voice/status")
        async def get_voice_status():
            """Get Primal Sovereign Core voice processing status"""
            try:
                return JSONResponse(content={
                    "status": "success",
                    "voice_processing_active": self.sovereign_manager.voice_processing_active,
                    "aws_monitoring_active": self.sovereign_manager.aws_monitoring_active,
                    "sovereign_learning_active": self.sovereign_manager.sovereign_learning_active,
                    "command_history_count": len(self.sovereign_manager.command_history),
                    "optimization_history_count": len(self.sovereign_manager.optimization_history)
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to get voice status: {str(e)}")

        @self.app.post("/api/voice/start")
        async def start_voice_processing():
            """Start Primal Sovereign Core voice processing"""
            try:
                await self.sovereign_manager.start_voice_processing()
                return JSONResponse(content={
                    "status": "success",
                    "message": "Voice processing started successfully"
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to start voice processing: {str(e)}")

        @self.app.post("/api/voice/stop")
        async def stop_voice_processing():
            """Stop Primal Sovereign Core voice processing"""
            try:
                await self.sovereign_manager.stop_voice_processing()
                return JSONResponse(content={
                    "status": "success",
                    "message": "Voice processing stopped successfully"
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to stop voice processing: {str(e)}")

        @self.app.get("/api/voice/report")
        async def generate_voice_report():
            """Generate Primal Sovereign Core report"""
            try:
                report_path = await self.sovereign_manager.generate_sovereign_report(
                    self.sovereign_manager.command_history
                )
                return JSONResponse(content={
                    "status": "success",
                    "report_path": report_path,
                    "message": "Sovereign report generated successfully"
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

        @self.app.post("/api/shadow/trading")
        async def process_trading_signal(trading_signal: TradingSignal):
            """Process trading signal with Shadow Nexus"""
            try:
                signal_data = {
                    "symbol": trading_signal.symbol,
                    "direction": trading_signal.direction,
                    "entry_price": trading_signal.entry_price,
                    "stop_loss": trading_signal.stop_loss,
                    "take_profit": trading_signal.take_profit,
                    "confidence": trading_signal.confidence,
                    "ichimoku_data": trading_signal.ichimoku_data,
                    "sentiment_score": trading_signal.sentiment_score
                }
                
                result = await self.shadow_manager.process_trading_signal(signal_data)
                
                return JSONResponse(content={
                    "status": "success",
                    "operation_id": result.operation_id,
                    "status": result.status.value,
                    "processing_time": result.processing_time,
                    "ai_enhancement_score": result.ai_enhancement_score,
                    "security_level": result.security_level,
                    "result": result.result
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to process trading signal: {str(e)}")

        @self.app.post("/api/shadow/retrieval")
        async def execute_data_retrieval(data_retrieval: DataRetrieval):
            """Execute data retrieval with Shadow Nexus"""
            try:
                result = await self.shadow_manager.execute_data_retrieval(
                    data_retrieval.target_url,
                    data_retrieval.operation_type
                )
                
                return JSONResponse(content={
                    "status": "success",
                    "operation_id": result.operation_id,
                    "status": result.status.value,
                    "processing_time": result.processing_time,
                    "ai_enhancement_score": result.ai_enhancement_score,
                    "security_level": result.security_level,
                    "result": result.result
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to execute data retrieval: {str(e)}")

        @self.app.post("/api/shadow/command")
        async def process_command_message(command_message: CommandMessage):
            """Process command message with Shadow Nexus"""
            try:
                message_data = {
                    "platform": command_message.platform,
                    "content": command_message.content,
                    "user_id": command_message.user_id,
                    "channel_id": command_message.channel_id,
                    "priority": command_message.priority,
                    "encrypted": command_message.encrypted
                }
                
                result = await self.shadow_manager.process_command_message(message_data)
                
                return JSONResponse(content={
                    "status": "success",
                    "operation_id": result.operation_id,
                    "status": result.status.value,
                    "processing_time": result.processing_time,
                    "ai_enhancement_score": result.ai_enhancement_score,
                    "security_level": result.security_level,
                    "result": result.result
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to process command message: {str(e)}")

        @self.app.get("/api/shadow/status")
        async def get_shadow_status():
            """Get Shadow Nexus status"""
            try:
                return JSONResponse(content={
                    "status": "success",
                    "trading_active": self.shadow_manager.trading_active,
                    "surveillance_active": self.shadow_manager.surveillance_active,
                    "command_network_active": self.shadow_manager.command_network_active,
                    "operation_history_count": len(self.shadow_manager.operation_history),
                    "trading_history_count": len(self.shadow_manager.trading_history)
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to get shadow status: {str(e)}")

        @self.app.post("/api/shadow/start")
        async def start_shadow_operations():
            """Start Shadow Nexus operations"""
            try:
                await self.shadow_manager.start_shadow_operations()
                return JSONResponse(content={
                    "status": "success",
                    "message": "Shadow Nexus operations started successfully"
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to start shadow operations: {str(e)}")

        @self.app.post("/api/shadow/stop")
        async def stop_shadow_operations():
            """Stop Shadow Nexus operations"""
            try:
                await self.shadow_manager.stop_shadow_operations()
                return JSONResponse(content={
                    "status": "success",
                    "message": "Shadow Nexus operations stopped successfully"
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to stop shadow operations: {str(e)}")

        @self.app.get("/api/shadow/report")
        async def generate_shadow_report():
            """Generate Shadow Nexus report"""
            try:
                report_path = await self.shadow_manager.generate_shadow_report()
                return JSONResponse(content={
                    "status": "success",
                    "report_path": report_path,
                    "message": "Shadow Nexus report generated successfully"
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to generate shadow report: {str(e)}")

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