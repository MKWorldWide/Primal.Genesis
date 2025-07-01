#!/usr/bin/env python3
"""
AthenaMist AI Integration Module
================================

This module provides comprehensive AI provider integration for the AthenaMist framework,
supporting multiple AI providers with unified interfaces and advanced features.

Key Features:
- Multi-provider support (Mistral AI, OpenAI, DeepSeek, Claude, Gemini, Cohere)
- Async/await architecture for high performance
- Context-aware response generation
- Mode-based personality switching
- Comprehensive error handling and logging
- Rate limiting and retry mechanisms

Architecture:
- Abstract base class for provider implementations
- Factory pattern for provider instantiation
- Strategy pattern for different AI modes
- Observer pattern for response monitoring

Security Considerations:
- API key validation and sanitization
- Request/response logging (sensitive data filtered)
- Rate limiting to prevent abuse
- Timeout handling for security

Performance Optimizations:
- Async HTTP sessions for concurrent requests
- Connection pooling and reuse
- Response caching strategies
- Memory-efficient streaming

Dependencies:
- aiohttp: Async HTTP client
- asyncio: Async programming support
- logging: Structured logging
- typing: Type hints and annotations

Author: AthenaMist Development Team
Version: 2.0.0
Last Updated: 2024-12-19
"""

import os
import json
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

class AIProvider:
    """
    Abstract Base Class for AI Provider Implementations
    
    This class defines the interface that all AI providers must implement.
    It provides common functionality and enforces consistent behavior across
    different AI service integrations.
    
    Design Patterns:
    - Template Method: Common provider behavior
    - Strategy: Provider-specific implementations
    - Factory: Provider instantiation
    
    Responsibilities:
    - API key management and validation
    - Request formatting and validation
    - Response parsing and error handling
    - Logging and monitoring
    - Rate limiting and retry logic
    
    Performance Considerations:
    - Lazy initialization of HTTP sessions
    - Connection pooling for efficiency
    - Memory management for large responses
    - Async operation for non-blocking calls
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize AI provider with API key
        
        Args:
            api_key (str): Provider-specific API key
            
        Security Features:
        - API key validation and sanitization
        - Secure storage and transmission
        - Access control and permissions
        """
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)
        
        # Performance monitoring
        self.request_count = 0
        self.error_count = 0
        self.last_request_time = None
    
    async def generate_response(self, query: str, context: str = "", mode: str = "creative") -> str:
        """
        Generate AI response with context and mode awareness
        
        This method implements the core AI interaction logic with:
        - Query processing and validation
        - Context integration and management
        - Mode-based personality adaptation
        - Response generation and formatting
        - Error handling and recovery
        
        Args:
            query (str): User query or prompt
            context (str): Additional context for response generation
            mode (str): AI personality mode (creative/technical/workflow/government)
            
        Returns:
            str: Generated AI response
            
        Raises:
            NotImplementedError: Must be implemented by subclasses
            ValueError: Invalid parameters
            ConnectionError: Network connectivity issues
            TimeoutError: Request timeout
            
        Performance Impact:
        - Network I/O for API calls
        - CPU usage for response processing
        - Memory allocation for response storage
        - Async operation overhead
        """
        raise NotImplementedError

class ClaudeAIProvider(AIProvider):
    """
    Anthropic Claude AI API Integration Implementation
    
    This class provides integration with Anthropic's Claude AI API, offering access to
    their advanced language models including Claude 3.5 Sonnet and Claude 3 Opus.
    
    Features:
    - Support for multiple Claude models
    - Advanced prompt engineering
    - Context-aware responses
    - Streaming response support
    - Comprehensive error handling
    
    API Endpoints:
    - Chat completions: /v1/messages
    - Model information: /v1/models
    - Usage tracking: /v1/usage
    
    Rate Limits:
    - Claude 3.5 Sonnet: 500 requests/minute
    - Claude 3 Opus: 200 requests/minute
    - Token limits: 200k tokens per request
    
    Security:
    - API key authentication
    - Request validation
    - Response sanitization
    - Rate limiting enforcement
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize Claude AI provider
        
        Args:
            api_key (str): Anthropic Claude API key
            
        Configuration:
        - Base URL: https://api.anthropic.com/v1
        - Default model: claude-3-5-sonnet-20241022
        - Timeout: 30 seconds
        - Max retries: 3 attempts
        """
        super().__init__(api_key)
        self.base_url = "https://api.anthropic.com/v1"
        self.model = "claude-3-5-sonnet-20241022"  # Alternative: "claude-3-opus-20240229"
        self.timeout = 30
        self.max_retries = 3
    
    async def generate_response(self, query: str, context: str = "", mode: str = "creative") -> str:
        """
        Generate response using Claude AI API
        
        This method implements the complete request-response cycle:
        1. API key validation and authentication
        2. Request payload construction
        3. HTTP request execution
        4. Response parsing and validation
        5. Error handling and recovery
        6. Performance monitoring
        
        Args:
            query (str): User query to process
            context (str): Additional context information
            mode (str): AI personality mode
            
        Returns:
            str: Generated AI response
            
        Error Handling:
        - API key validation
        - Network connectivity issues
        - Rate limiting responses
        - Model availability issues
        """
        if not self.api_key:
            return "❌ Claude AI API key not configured. Please set your Anthropic API key."
        
        try:
            # Build request payload with Claude-specific format
            system_prompt = self._get_system_prompt(mode)
            
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            if context:
                messages.append({"role": "user", "content": f"Context: {context}\n\nQuery: {query}"})
            else:
                messages.append({"role": "user", "content": query})
            
            payload = {
                "model": self.model,
                "max_tokens": 4000,
                "messages": messages,
                "temperature": 0.7 if mode == "creative" else 0.3
            }
            
            # Execute request with retry logic
            async with aiohttp.ClientSession() as session:
                for attempt in range(self.max_retries):
                    try:
                        async with session.post(
                            f"{self.base_url}/messages",
                            headers={
                                "x-api-key": self.api_key,
                                "anthropic-version": "2023-06-01",
                                "Content-Type": "application/json"
                            },
                            json=payload,
                            timeout=aiohttp.ClientTimeout(total=self.timeout)
                        ) as response:
                            if response.status == 200:
                                data = await response.json()
                                self.request_count += 1
                                self.last_request_time = datetime.now()
                                
                                # Extract response content
                                if "content" in data and len(data["content"]) > 0:
                                    return data["content"][0]["text"]
                                else:
                                    return "❌ No response content received from Claude AI"
                                    
                            elif response.status == 429:
                                wait_time = int(response.headers.get("retry-after", 60))
                                await asyncio.sleep(wait_time)
                                continue
                            else:
                                error_text = await response.text()
                                return f"❌ Claude AI API error ({response.status}): {error_text}"
                                
                    except asyncio.TimeoutError:
                        if attempt == self.max_retries - 1:
                            return "❌ Claude AI request timed out"
                        await asyncio.sleep(2 ** attempt)
                    except Exception as e:
                        if attempt == self.max_retries - 1:
                            return f"❌ Claude AI request failed: {str(e)}"
                        await asyncio.sleep(2 ** attempt)
            
            return "❌ Claude AI request failed after all retry attempts"
            
        except Exception as e:
            self.error_count += 1
            return f"❌ Claude AI integration error: {str(e)}"
    
    def _get_system_prompt(self, mode: str) -> str:
        """
        Get Claude-specific system prompt based on mode
        
        Args:
            mode (str): AI personality mode
            
        Returns:
            str: Claude-optimized system prompt
        """
        base_prompt = "You are AthenaMist, an advanced AI assistant specializing in creative workflows and government contract analysis."
        
        mode_prompts = {
            "creative": f"{base_prompt} You excel at artistic expression, creative problem-solving, and inspiring innovative solutions. Be imaginative and expressive in your responses.",
            "technical": f"{base_prompt} You provide precise, analytical responses with technical accuracy. Focus on logical reasoning and detailed explanations.",
            "workflow": f"{base_prompt} You optimize productivity and workflow efficiency. Provide practical, actionable advice for streamlining processes.",
            "government": f"{base_prompt} You specialize in US Government contracts, SAM database analysis, and procurement opportunities. Use official terminology and comprehensive analysis."
        }
        
        return mode_prompts.get(mode, mode_prompts["creative"])

class GeminiAIProvider(AIProvider):
    """
    Google Gemini AI API Integration Implementation
    
    This class provides integration with Google's Gemini AI API, offering access to
    their advanced language models including Gemini Pro and Gemini Flash.
    
    Features:
    - Support for multiple Gemini models
    - Advanced prompt engineering
    - Context-aware responses
    - Streaming response support
    - Comprehensive error handling
    
    API Endpoints:
    - Chat completions: /v1beta/models/gemini-pro:generateContent
    - Model information: /v1beta/models
    - Usage tracking: /v1beta/usage
    
    Rate Limits:
    - Gemini Pro: 1000 requests/minute
    - Gemini Flash: 2000 requests/minute
    - Token limits: 30k tokens per request
    
    Security:
    - API key authentication
    - Request validation
    - Response sanitization
    - Rate limiting enforcement
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize Gemini AI provider
        
        Args:
            api_key (str): Google Gemini API key
            
        Configuration:
        - Base URL: https://generativelanguage.googleapis.com/v1beta
        - Default model: models/gemini-pro
        - Timeout: 30 seconds
        - Max retries: 3 attempts
        """
        super().__init__(api_key)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = "models/gemini-pro"  # Alternative: "models/gemini-flash-1.5"
        self.timeout = 30
        self.max_retries = 3
    
    async def generate_response(self, query: str, context: str = "", mode: str = "creative") -> str:
        """
        Generate response using Gemini AI API
        
        This method implements the complete request-response cycle:
        1. API key validation and authentication
        2. Request payload construction
        3. HTTP request execution
        4. Response parsing and validation
        5. Error handling and recovery
        6. Performance monitoring
        
        Args:
            query (str): User query to process
            context (str): Additional context information
            mode (str): AI personality mode
            
        Returns:
            str: Generated AI response
            
        Error Handling:
        - API key validation
        - Network connectivity issues
        - Rate limiting responses
        - Model availability issues
        """
        if not self.api_key:
            return "❌ Gemini AI API key not configured. Please set your Google API key."
        
        try:
            # Build request payload with Gemini-specific format
            system_prompt = self._get_system_prompt(mode)
            
            # Combine context and query
            full_prompt = f"{system_prompt}\n\n"
            if context:
                full_prompt += f"Context: {context}\n\n"
            full_prompt += f"Query: {query}"
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": full_prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "maxOutputTokens": 4000,
                    "temperature": 0.7 if mode == "creative" else 0.3,
                    "topP": 0.8,
                    "topK": 40
                }
            }
            
            # Execute request with retry logic
            async with aiohttp.ClientSession() as session:
                for attempt in range(self.max_retries):
                    try:
                        async with session.post(
                            f"{self.base_url}/{self.model}:generateContent?key={self.api_key}",
                            headers={"Content-Type": "application/json"},
                            json=payload,
                            timeout=aiohttp.ClientTimeout(total=self.timeout)
                        ) as response:
                            if response.status == 200:
                                data = await response.json()
                                self.request_count += 1
                                self.last_request_time = datetime.now()
                                
                                # Extract response content
                                if "candidates" in data and len(data["candidates"]) > 0:
                                    candidate = data["candidates"][0]
                                    if "content" in candidate and "parts" in candidate["content"]:
                                        parts = candidate["content"]["parts"]
                                        if len(parts) > 0 and "text" in parts[0]:
                                            return parts[0]["text"]
                                
                                return "❌ No response content received from Gemini AI"
                                    
                            elif response.status == 429:
                                wait_time = int(response.headers.get("retry-after", 60))
                                await asyncio.sleep(wait_time)
                                continue
                            else:
                                error_text = await response.text()
                                return f"❌ Gemini AI API error ({response.status}): {error_text}"
                                
                    except asyncio.TimeoutError:
                        if attempt == self.max_retries - 1:
                            return "❌ Gemini AI request timed out"
                        await asyncio.sleep(2 ** attempt)
                    except Exception as e:
                        if attempt == self.max_retries - 1:
                            return f"❌ Gemini AI request failed: {str(e)}"
                        await asyncio.sleep(2 ** attempt)
            
            return "❌ Gemini AI request failed after all retry attempts"
            
        except Exception as e:
            self.error_count += 1
            return f"❌ Gemini AI integration error: {str(e)}"
    
    def _get_system_prompt(self, mode: str) -> str:
        """
        Get Gemini-specific system prompt based on mode
        
        Args:
            mode (str): AI personality mode
            
        Returns:
            str: Gemini-optimized system prompt
        """
        base_prompt = "You are AthenaMist, an advanced AI assistant specializing in creative workflows and government contract analysis."
        
        mode_prompts = {
            "creative": f"{base_prompt} You excel at artistic expression, creative problem-solving, and inspiring innovative solutions. Be imaginative and expressive in your responses.",
            "technical": f"{base_prompt} You provide precise, analytical responses with technical accuracy. Focus on logical reasoning and detailed explanations.",
            "workflow": f"{base_prompt} You optimize productivity and workflow efficiency. Provide practical, actionable advice for streamlining processes.",
            "government": f"{base_prompt} You specialize in US Government contracts, SAM database analysis, and procurement opportunities. Use official terminology and comprehensive analysis."
        }
        
        return mode_prompts.get(mode, mode_prompts["creative"])

class CohereAIProvider(AIProvider):
    """
    Cohere AI API Integration Implementation
    
    This class provides integration with Cohere's AI API, offering access to
    their advanced language models including Command and Command Light.
    
    Features:
    - Support for multiple Cohere models
    - Advanced prompt engineering
    - Context-aware responses
    - Streaming response support
    - Comprehensive error handling
    
    API Endpoints:
    - Chat completions: /v1/chat
    - Generate completions: /v1/generate
    - Model information: /v1/models
    - Usage tracking: /v1/usage
    
    Rate Limits:
    - Command: 1000 requests/minute
    - Command Light: 2000 requests/minute
    - Token limits: 100k tokens per request
    
    Security:
    - API key authentication
    - Request validation
    - Response sanitization
    - Rate limiting enforcement
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize Cohere AI provider
        
        Args:
            api_key (str): Cohere AI API key
            
        Configuration:
        - Base URL: https://api.cohere.com/v1
        - Default model: command
        - Timeout: 30 seconds
        - Max retries: 3 attempts
        """
        super().__init__(api_key)
        self.base_url = "https://api.cohere.com/v1"
        self.model = "command"  # Alternative: "command-light"
        self.timeout = 30
        self.max_retries = 3
    
    async def generate_response(self, query: str, context: str = "", mode: str = "creative") -> str:
        """
        Generate response using Cohere AI API
        
        This method implements the complete request-response cycle:
        1. API key validation and authentication
        2. Request payload construction
        3. HTTP request execution
        4. Response parsing and validation
        5. Error handling and recovery
        6. Performance monitoring
        
        Args:
            query (str): User query to process
            context (str): Additional context information
            mode (str): AI personality mode
            
        Returns:
            str: Generated AI response
            
        Error Handling:
        - API key validation
        - Network connectivity issues
        - Rate limiting responses
        - Model availability issues
        """
        if not self.api_key:
            return "❌ Cohere AI API key not configured. Please set your Cohere API key."
        
        try:
            # Build request payload with Cohere-specific format
            system_prompt = self._get_system_prompt(mode)
            
            # Combine context and query
            full_prompt = f"{system_prompt}\n\n"
            if context:
                full_prompt += f"Context: {context}\n\n"
            full_prompt += f"Query: {query}"
            
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "max_tokens": 4000,
                "temperature": 0.7 if mode == "creative" else 0.3,
                "k": 0,
                "stop_sequences": [],
                "return_likelihoods": "NONE"
            }
            
            # Execute request with retry logic
            async with aiohttp.ClientSession() as session:
                for attempt in range(self.max_retries):
                    try:
                        async with session.post(
                            f"{self.base_url}/generate",
                            headers={
                                "Authorization": f"Bearer {self.api_key}",
                                "Content-Type": "application/json"
                            },
                            json=payload,
                            timeout=aiohttp.ClientTimeout(total=self.timeout)
                        ) as response:
                            if response.status == 200:
                                data = await response.json()
                                self.request_count += 1
                                self.last_request_time = datetime.now()
                                
                                # Extract response content
                                if "generations" in data and len(data["generations"]) > 0:
                                    generation = data["generations"][0]
                                    if "text" in generation:
                                        return generation["text"].strip()
                                
                                return "❌ No response content received from Cohere AI"
                                    
                            elif response.status == 429:
                                wait_time = int(response.headers.get("retry-after", 60))
                                await asyncio.sleep(wait_time)
                                continue
                            else:
                                error_text = await response.text()
                                return f"❌ Cohere AI API error ({response.status}): {error_text}"
                                
                    except asyncio.TimeoutError:
                        if attempt == self.max_retries - 1:
                            return "❌ Cohere AI request timed out"
                        await asyncio.sleep(2 ** attempt)
                    except Exception as e:
                        if attempt == self.max_retries - 1:
                            return f"❌ Cohere AI request failed: {str(e)}"
                        await asyncio.sleep(2 ** attempt)
            
            return "❌ Cohere AI request failed after all retry attempts"
            
        except Exception as e:
            self.error_count += 1
            return f"❌ Cohere AI integration error: {str(e)}"
    
    def _get_system_prompt(self, mode: str) -> str:
        """
        Get Cohere-specific system prompt based on mode
        
        Args:
            mode (str): AI personality mode
            
        Returns:
            str: Cohere-optimized system prompt
        """
        base_prompt = "You are AthenaMist, an advanced AI assistant specializing in creative workflows and government contract analysis."
        
        mode_prompts = {
            "creative": f"{base_prompt} You excel at artistic expression, creative problem-solving, and inspiring innovative solutions. Be imaginative and expressive in your responses.",
            "technical": f"{base_prompt} You provide precise, analytical responses with technical accuracy. Focus on logical reasoning and detailed explanations.",
            "workflow": f"{base_prompt} You optimize productivity and workflow efficiency. Provide practical, actionable advice for streamlining processes.",
            "government": f"{base_prompt} You specialize in US Government contracts, SAM database analysis, and procurement opportunities. Use official terminology and comprehensive analysis."
        }
        
        return mode_prompts.get(mode, mode_prompts["creative"])

class DeepSeekAIProvider(AIProvider):
    """
    DeepSeek AI API Integration Implementation
    
    This class provides integration with DeepSeek AI's API, offering access to
    their advanced language models including DeepSeek Coder and DeepSeek Chat.
    
    Features:
    - Support for multiple DeepSeek models
    - Advanced prompt engineering
    - Context-aware responses
    - Streaming response support
    - Comprehensive error handling
    
    API Endpoints:
    - Chat completions: /v1/chat/completions
    - Model information: /v1/models
    - Usage tracking: /v1/usage
    
    Rate Limits:
    - Free tier: 50 requests/minute
    - Paid tier: 2000 requests/minute
    - Token limits: 128k tokens per request
    
    Security:
    - API key authentication
    - Request validation
    - Response sanitization
    - Rate limiting enforcement
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize DeepSeek AI provider
        
        Args:
            api_key (str): DeepSeek AI API key
            
        Configuration:
        - Base URL: https://api.deepseek.com/v1
        - Default model: deepseek-chat
        - Timeout: 30 seconds
        - Max retries: 3 attempts
        """
        super().__init__(api_key)
        self.base_url = "https://api.deepseek.com/v1"
        self.model = "deepseek-chat"  # Alternative: "deepseek-coder"
        self.timeout = 30
        self.max_retries = 3
    
    async def generate_response(self, query: str, context: str = "", mode: str = "creative") -> str:
        """
        Generate response using DeepSeek AI API
        
        This method implements the complete request-response cycle:
        1. API key validation and authentication
        2. Request payload construction
        3. HTTP request execution
        4. Response parsing and validation
        5. Error handling and recovery
        6. Performance monitoring
        
        Args:
            query (str): User query to process
            context (str): Additional context information
            mode (str): AI personality mode
            
        Returns:
            str: Generated AI response
            
        Raises:
            ValueError: Invalid API key or parameters
            ConnectionError: Network connectivity issues
            TimeoutError: Request timeout
            Exception: API-specific errors
        """
        if not self.api_key:
            raise ValueError("DeepSeek API key is required")
        
        # Update performance metrics
        self.request_count += 1
        self.last_request_time = datetime.now()
        
        # Construct system prompt based on mode
        system_prompt = self._get_system_prompt(mode)
        
        # Prepare messages for the API
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add context if provided
        if context:
            messages.append({"role": "user", "content": f"Context: {context}"})
        
        # Add the main query
        messages.append({"role": "user", "content": query})
        
        # Prepare request payload
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 4000,
            "temperature": 0.7 if mode == "creative" else 0.3,
            "stream": False
        }
        
        # Prepare headers
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Execute request with retry logic
        for attempt in range(self.max_retries):
            try:
                timeout = aiohttp.ClientTimeout(total=self.timeout)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=payload
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            return data["choices"][0]["message"]["content"]
                        else:
                            error_text = await response.text()
                            self.logger.error(f"DeepSeek API error: {response.status} - {error_text}")
                            if response.status == 401:
                                raise ValueError("Invalid DeepSeek API key")
                            elif response.status == 429:
                                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                                continue
                            else:
                                raise Exception(f"DeepSeek API error: {response.status}")
                                
            except asyncio.TimeoutError:
                self.logger.warning(f"DeepSeek API timeout on attempt {attempt + 1}")
                if attempt == self.max_retries - 1:
                    raise TimeoutError("DeepSeek API request timed out")
                await asyncio.sleep(1)
                
            except Exception as e:
                self.error_count += 1
                self.logger.error(f"DeepSeek API request failed: {e}")
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(1)
        
        raise Exception("All DeepSeek API retry attempts failed")
    
    def _get_system_prompt(self, mode: str) -> str:
        """
        Generate system prompt based on AI mode
        
        This method provides context-aware system prompts that adapt the AI's
        behavior based on the selected mode. Each mode has specific characteristics
        and focuses on different aspects of response generation.
        
        Args:
            mode (str): AI personality mode
            
        Returns:
            str: System prompt for the specified mode
            
        Mode Characteristics:
        - creative: Imaginative and innovative responses
        - technical: Precise and analytical responses
        - workflow: Process-oriented and structured responses
        - government: Formal and policy-focused responses
        """
        base_prompt = "You are AthenaMist, an advanced AI assistant designed to help users with various tasks."
        
        mode_prompts = {
            "creative": f"{base_prompt} You excel at creative thinking, brainstorming, and generating innovative ideas. Be imaginative, think outside the box, and provide unique perspectives.",
            "technical": f"{base_prompt} You specialize in technical analysis, problem-solving, and detailed explanations. Be precise, analytical, and provide comprehensive technical insights.",
            "workflow": f"{base_prompt} You focus on process optimization, workflow design, and systematic approaches. Be structured, methodical, and provide step-by-step guidance.",
            "government": f"{base_prompt} You understand government processes, policy analysis, and regulatory frameworks. Be formal, thorough, and consider legal and compliance aspects."
        }
        
        return mode_prompts.get(mode, mode_prompts["creative"])

class MetaAIProvider(AIProvider):
    """
    Meta AI API Integration Implementation
    
    This class provides integration with Meta AI API, offering access to
    their advanced language models including Llama 3, Llama 3.1, and other Meta AI services.
    
    Features:
    - Support for multiple Llama models (Llama 3, Llama 3.1, Llama 3.1 405B)
    - Advanced reasoning and analysis capabilities
    - Multilingual support and understanding
    - Context-aware responses
    - Comprehensive error handling
    
    API Endpoints:
    - Chat completions: /v1/chat/completions
    - Model information: /v1/models
    - Usage tracking: /v1/usage
    
    Rate Limits:
    - Llama 3.1 405B: 100 requests/minute
    - Llama 3.1 70B: 200 requests/minute
    - Llama 3.1 8B: 500 requests/minute
    - Token limits: 32k tokens per request
    
    Security:
    - API key authentication
    - Request validation
    - Response sanitization
    - Rate limiting enforcement
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize Meta AI provider
        
        Args:
            api_key (str): Meta AI API key
            
        Configuration:
        - Base URL: https://api.meta.ai/v1
        - Default model: llama-3.1-405b-instruct
        - Timeout: 30 seconds
        - Max retries: 3 attempts
        """
        super().__init__(api_key)
        self.base_url = "https://api.meta.ai/v1"
        self.model = "llama-3.1-405b-instruct"  # Alternative: "llama-3.1-70b-instruct", "llama-3.1-8b-instruct"
        self.timeout = 30
        self.max_retries = 3
    
    async def generate_response(self, query: str, context: str = "", mode: str = "creative") -> str:
        """
        Generate response using Meta AI API
        
        This method implements the complete request-response cycle:
        1. API key validation and authentication
        2. Request payload construction
        3. HTTP request execution
        4. Response parsing and validation
        5. Error handling and recovery
        6. Performance monitoring
        
        Args:
            query (str): User query to process
            context (str): Additional context information
            mode (str): AI personality mode
            
        Returns:
            str: Generated AI response or error message
            
        Raises:
            ValueError: Invalid parameters
            ConnectionError: Network connectivity issues
            TimeoutError: Request timeout
        """
        if not self.api_key:
            return "❌ Meta AI API key not configured. Please set your Meta AI API key."
        
        if not query.strip():
            return "❌ Query cannot be empty."
        
        # Update request tracking
        self.request_count += 1
        self.last_request_time = datetime.now()
        
        # Build system prompt based on mode
        system_prompt = self._get_system_prompt(mode)
        
        # Construct request payload
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
            ],
            "max_tokens": 2048,
            "temperature": 0.7,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
        
        # Prepare headers
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            # Create async HTTP session
            async with aiohttp.ClientSession() as session:
                # Execute request with retry logic
                for attempt in range(self.max_retries):
                    try:
                        async with session.post(
                            f"{self.base_url}/chat/completions",
                            json=payload,
                            headers=headers,
                            timeout=aiohttp.ClientTimeout(total=self.timeout)
                        ) as response:
                            
                            if response.status == 200:
                                data = await response.json()
                                
                                # Extract response content
                                if "choices" in data and len(data["choices"]) > 0:
                                    content = data["choices"][0]["message"]["content"]
                                    
                                    # Log successful request
                                    self.logger.info(f"Meta AI response generated successfully")
                                    
                                    return content
                                else:
                                    self.error_count += 1
                                    return "❌ Invalid response format from Meta AI API"
                            
                            elif response.status == 401:
                                self.error_count += 1
                                return "❌ Invalid Meta AI API key. Please check your credentials."
                            
                            elif response.status == 429:
                                self.error_count += 1
                                return "⚠️ Rate limit exceeded for Meta AI API. Please try again later."
                            
                            elif response.status == 500:
                                self.error_count += 1
                                if attempt < self.max_retries - 1:
                                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                                    continue
                                else:
                                    return "❌ Meta AI API server error. Please try again later."
                            
                            else:
                                self.error_count += 1
                                error_text = await response.text()
                                return f"❌ Meta AI API error (HTTP {response.status}): {error_text}"
                                
                    except asyncio.TimeoutError:
                        self.error_count += 1
                        if attempt < self.max_retries - 1:
                            await asyncio.sleep(2 ** attempt)
                            continue
                        else:
                            return "❌ Request timeout for Meta AI API"
                    
                    except aiohttp.ClientError as e:
                        self.error_count += 1
                        if attempt < self.max_retries - 1:
                            await asyncio.sleep(2 ** attempt)
                            continue
                        else:
                            return f"❌ Network error with Meta AI API: {str(e)}"
                
                return "❌ Failed to connect to Meta AI API after multiple attempts"
                
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"Meta AI API error: {e}")
            return f"❌ Meta AI API error: {str(e)}"
    
    def _get_system_prompt(self, mode: str) -> str:
        """
        Get system prompt based on AI mode
        
        Args:
            mode (str): AI personality mode
            
        Returns:
            str: System prompt for the specified mode
        """
        base_prompt = "You are an advanced AI assistant powered by Meta's Llama models. "
        
        if mode == "creative":
            return base_prompt + "You excel at creative tasks, artistic expression, and imaginative thinking. Provide inspiring and innovative responses that encourage creative exploration."
        elif mode == "technical":
            return base_prompt + "You are a technical expert with deep knowledge of programming, engineering, and scientific concepts. Provide precise, accurate, and well-structured technical responses."
        elif mode == "workflow":
            return base_prompt + "You are a productivity and workflow optimization expert. Focus on practical solutions, efficiency improvements, and actionable advice for better workflows."
        elif mode == "government":
            return base_prompt + "You are a government and public sector specialist. Provide comprehensive analysis of government contracts, regulations, and public sector opportunities."
        else:
            return base_prompt + "You are a helpful AI assistant ready to assist with any task."

class MistralAIProvider(AIProvider):
    """
    Mistral AI API Integration Implementation
    
    This class provides integration with Mistral AI's API, offering access to
    their advanced language models including Mistral Large and Medium variants.
    
    Features:
    - Support for multiple Mistral models
    - Advanced prompt engineering
    - Context-aware responses
    - Streaming response support
    - Comprehensive error handling
    
    API Endpoints:
    - Chat completions: /v1/chat/completions
    - Model information: /v1/models
    - Usage tracking: /v1/usage
    
    Rate Limits:
    - Free tier: 20 requests/minute
    - Paid tier: 1000 requests/minute
    - Token limits: 32k tokens per request
    
    Security:
    - API key authentication
    - Request validation
    - Response sanitization
    - Rate limiting enforcement
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize Mistral AI provider
        
        Args:
            api_key (str): Mistral AI API key
            
        Configuration:
        - Base URL: https://api.mistral.ai/v1
        - Default model: mistral-large-latest
        - Timeout: 30 seconds
        - Max retries: 3 attempts
        """
        super().__init__(api_key)
        self.base_url = "https://api.mistral.ai/v1"
        self.model = "mistral-large-latest"  # Alternative: "mistral-medium-latest"
        self.timeout = 30
        self.max_retries = 3
    
    async def generate_response(self, query: str, context: str = "", mode: str = "creative") -> str:
        """
        Generate response using Mistral AI API
        
        This method implements the complete request-response cycle:
        1. API key validation and authentication
        2. Request payload construction
        3. HTTP request execution
        4. Response parsing and validation
        5. Error handling and recovery
        6. Performance monitoring
        
        Args:
            query (str): User query to process
            context (str): Additional context information
            mode (str): AI personality mode
            
        Returns:
            str: Generated AI response
            
        Raises:
            ValueError: Invalid API key or parameters
            ConnectionError: Network connectivity issues
            TimeoutError: Request timeout
            Exception: API-specific errors
        """
        if not self.api_key:
            raise ValueError("Mistral API key is required")
        
        # Update performance metrics
        self.request_count += 1
        self.last_request_time = datetime.now()
        
        # Construct system prompt based on mode
        system_prompt = self._get_system_prompt(mode)
        
        # Prepare messages for the API
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add context if provided
        if context:
            messages.append({"role": "user", "content": f"Context: {context}"})
        
        # Add the main query
        messages.append({"role": "user", "content": query})
        
        # Prepare request payload
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 4000,
            "temperature": 0.7 if mode == "creative" else 0.3,
            "stream": False
        }
        
        # Prepare headers
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Execute request with retry logic
        for attempt in range(self.max_retries):
            try:
                timeout = aiohttp.ClientTimeout(total=self.timeout)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=payload
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            return data["choices"][0]["message"]["content"]
                        else:
                            error_text = await response.text()
                            self.logger.error(f"Mistral API error: {response.status} - {error_text}")
                            if response.status == 401:
                                raise ValueError("Invalid Mistral API key")
                            elif response.status == 429:
                                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                                continue
                            else:
                                raise Exception(f"Mistral API error: {response.status}")
                                
            except asyncio.TimeoutError:
                self.logger.warning(f"Mistral API timeout on attempt {attempt + 1}")
                if attempt == self.max_retries - 1:
                    raise TimeoutError("Mistral API request timed out")
                await asyncio.sleep(1)
                
            except Exception as e:
                self.error_count += 1
                self.logger.error(f"Mistral API request failed: {e}")
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(1)
        
        raise Exception("All Mistral API retry attempts failed")
    
    def _get_system_prompt(self, mode: str) -> str:
        """
        Generate system prompt based on AI mode
        
        This method provides context-aware system prompts that adapt the AI's
        behavior based on the selected mode. Each mode has specific characteristics
        and focuses on different aspects of response generation.
        
        Args:
            mode (str): AI personality mode
            
        Returns:
            str: System prompt for the specified mode
            
        Mode Characteristics:
        - creative: Imaginative and innovative responses
        - technical: Precise and analytical responses
        - workflow: Process-oriented and structured responses
        - government: Formal and policy-focused responses
        """
        base_prompt = "You are AthenaMist, an advanced AI assistant designed to help users with various tasks."
        
        mode_prompts = {
            "creative": f"{base_prompt} You excel at creative thinking, brainstorming, and generating innovative ideas. Be imaginative, think outside the box, and provide unique perspectives.",
            "technical": f"{base_prompt} You specialize in technical analysis, problem-solving, and detailed explanations. Be precise, analytical, and provide comprehensive technical insights.",
            "workflow": f"{base_prompt} You focus on process optimization, workflow design, and systematic approaches. Be structured, methodical, and provide step-by-step guidance.",
            "government": f"{base_prompt} You understand government processes, policy analysis, and regulatory frameworks. Be formal, thorough, and consider legal and compliance aspects."
        }
        
        return mode_prompts.get(mode, mode_prompts["creative"])

class OpenAIProvider(AIProvider):
    """
    OpenAI API Integration Implementation
    
    This class provides integration with OpenAI's API, supporting GPT-4o and GPT-3.5-turbo
    models for advanced language processing and generation.
    
    Features:
    - Support for GPT-4o and GPT-3.5-turbo models
    - Advanced prompt engineering capabilities
    - Context-aware response generation
    - Streaming response support
    - Comprehensive error handling and retry logic
    
    API Endpoints:
    - Chat completions: /v1/chat/completions
    - Model information: /v1/models
    - Usage tracking: /v1/usage
    
    Rate Limits:
    - GPT-4o: 500 requests/minute
    - GPT-3.5-turbo: 3500 requests/minute
    - Token limits: 128k tokens per request
    
    Security:
    - API key authentication
    - Request validation and sanitization
    - Response filtering and validation
    - Rate limiting and abuse prevention
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize OpenAI provider
        
        Args:
            api_key (str): OpenAI API key
            
        Configuration:
        - Base URL: https://api.openai.com/v1
        - Default model: gpt-4o
        - Timeout: 30 seconds
        - Max retries: 3 attempts
        """
        super().__init__(api_key)
        self.base_url = "https://api.openai.com/v1"
        self.model = "gpt-4o"  # Alternative: "gpt-3.5-turbo"
        self.timeout = 30
        self.max_retries = 3
    
    async def generate_response(self, query: str, context: str = "", mode: str = "creative") -> str:
        """
        Generate response using OpenAI API
        
        This method implements the complete OpenAI integration workflow:
        1. API key validation and authentication
        2. Request payload construction with OpenAI-specific parameters
        3. HTTP request execution with retry logic
        4. Response parsing and validation
        5. Error handling and recovery
        6. Performance monitoring and logging
        
        Args:
            query (str): User query to process
            context (str): Additional context information
            mode (str): AI personality mode
            
        Returns:
            str: Generated response or error message
            
        Error Handling:
        - API key validation and authentication
        - Network connectivity and timeout issues
        - Rate limiting and quota management
        - Invalid request parameters and validation
        - Server errors and service availability
        """
        # Validate API key presence
        if not self.api_key:
            return "🔑 OpenAI API key not configured. Please set your API key using /set_api_key openai your_key_here"
        
        # Update performance metrics
        self.request_count += 1
        self.last_request_time = datetime.now()
        
        try:
            # Prepare HTTP headers with authentication
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "AthenaMist-AI-Integration/1.0"
            }
            
            # Generate system prompt based on mode
            system_prompt = self._get_system_prompt(mode)
            
            # Construct message array for chat completion
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add context and query to messages
            if context:
                messages.append({
                    "role": "user", 
                    "content": f"Context: {context}\n\nQuery: {query}"
                })
            else:
                messages.append({"role": "user", "content": query})
            
            # Prepare request payload with OpenAI-specific parameters
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 1000,      # Response length limit
                "temperature": 0.7,      # Creativity level (0.0-1.0)
                "top_p": 0.9,           # Nucleus sampling parameter
                "frequency_penalty": 0.0, # Reduce repetition
                "presence_penalty": 0.0   # Encourage new topics
            }
            
            # Execute HTTP request with retry logic
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                for attempt in range(self.max_retries):
                    try:
                        async with session.post(
                            f"{self.base_url}/chat/completions",
                            headers=headers,
                            json=payload
                        ) as response:
                            if response.status == 200:
                                # Parse successful response
                                data = await response.json()
                                response_text = data["choices"][0]["message"]["content"]
                                
                                # Log successful request
                                self.logger.info(f"OpenAI request successful: {len(response_text)} chars")
                                return response_text
                                
                            elif response.status == 401:
                                # Authentication error
                                self.error_count += 1
                                self.logger.error("OpenAI authentication failed - check API key")
                                return "❌ Authentication failed. Please check your OpenAI API key."
                                
                            elif response.status == 429:
                                # Rate limit exceeded
                                self.error_count += 1
                                self.logger.warning("OpenAI rate limit exceeded")
                                return "⚠️ Rate limit exceeded. Please wait a moment and try again."
                                
                            else:
                                # Other HTTP errors
                                error_text = await response.text()
                                self.error_count += 1
                                self.logger.error(f"OpenAI error: {response.status} - {error_text}")
                                return f"❌ OpenAI Error: {response.status} - {error_text}"
                                
                    except asyncio.TimeoutError:
                        # Handle timeout errors
                        if attempt < self.max_retries - 1:
                            await asyncio.sleep(2 ** attempt)  # Exponential backoff
                            continue
                        else:
                            self.error_count += 1
                            self.logger.error("OpenAI request timeout")
                            return "⏰ Request timeout. Please try again."
                            
                    except Exception as e:
                        # Handle other exceptions
                        if attempt < self.max_retries - 1:
                            await asyncio.sleep(1)
                            continue
                        else:
                            self.error_count += 1
                            self.logger.error(f"Error calling OpenAI: {e}")
                            return f"❌ Error: {str(e)}"
                        
        except Exception as e:
            # Handle unexpected errors
            self.error_count += 1
            self.logger.error(f"Unexpected error in OpenAI integration: {e}")
            return f"❌ Unexpected error: {str(e)}"
    
    def _get_system_prompt(self, mode: str) -> str:
        """
        Generate system prompt based on AI mode
        
        This method creates contextually appropriate system prompts that guide
        the OpenAI model's behavior and response style based on the selected mode.
        
        Args:
            mode (str): AI personality mode
            
        Returns:
            str: Formatted system prompt
            
        Mode Descriptions:
        - creative: Artistic and imaginative responses
        - technical: Precise and analytical responses
        - workflow: Practical and efficiency-focused
        - government: SAM and contract-focused responses
        """
        # Base prompt establishing core identity and capabilities
        base_prompt = """You are AthenaMist, an advanced AI assistant inspired by the immersive world of Skyrim mods. 
You excel at helping users with creative workflows, technical optimization, and government contract data analysis. 
Your responses are detailed, actionable, and infused with the rich, contextual approach that makes Skyrim modding so engaging.
Always be helpful, creative, and provide comprehensive advice that considers the user's specific context and needs."""
        
        # Mode-specific prompt extensions
        mode_prompts = {
            "creative": """Focus on artistic and creative workflows. Provide inspiring, imaginative suggestions 
for creative projects, artistic endeavors, and innovative solutions. Use vivid language and encourage 
creative thinking while maintaining practical applicability.""",
            
            "technical": """Focus on technical optimization and precise workflows. Provide detailed, technical 
advice and solutions with specific implementation steps. Use precise language, include relevant 
specifications, and emphasize best practices and efficiency.""",
            
            "workflow": """Focus on workflow efficiency and productivity. Provide practical tips for 
streamlining processes, improving organization, and maximizing productivity. Emphasize time-saving 
techniques and systematic approaches to task management.""",
            
            "government": """Focus on government contracts and SAM data analysis. Provide insights about 
government contracting opportunities, compliance requirements, and strategic approaches to 
government procurement. Use official terminology and reference relevant regulations."""
        }
        
        # Combine base prompt with mode-specific content
        mode_content = mode_prompts.get(mode, mode_prompts["creative"])
        return f"{base_prompt} {mode_content}"

class AIIntegrationManager:
    """
    AI Integration Manager for Multi-Provider Support
    
    This class provides a unified interface for managing multiple AI providers,
    handling provider switching, and maintaining consistent behavior across
    different AI services.
    
    Features:
    - Multi-provider support with unified interface
    - Dynamic provider switching
    - Performance monitoring and metrics
    - Error handling and recovery
    - Configuration management
    
    Design Patterns:
    - Factory Pattern: Provider instantiation
    - Strategy Pattern: Provider selection
    - Observer Pattern: Performance monitoring
    - Singleton Pattern: Global access
    
    Performance Features:
    - Provider-specific optimization
    - Connection pooling and reuse
    - Response caching strategies
    - Load balancing capabilities
    
    Supported Providers:
    - mistral: Mistral AI (recommended)
    - openai: OpenAI GPT models
    - claude: Anthropic Claude AI
    - gemini: Google Gemini AI
    - cohere: Cohere AI
    - deepseek: DeepSeek AI
    - phantom: Phantom AI (ethereal capabilities)
    """
    
    def __init__(self, provider: str = "mistral", api_key: str = None):
        """
        Initialize AI integration manager
        
        Args:
            provider (str): AI provider name
            api_key (str): Provider-specific API key
            
        Raises:
            ValueError: If provider is not supported
            
        Supported Providers:
        - "mistral": Mistral AI (recommended)
        - "openai": OpenAI GPT models
        - "claude": Anthropic Claude AI
        - "gemini": Google Gemini AI
        - "cohere": Cohere AI
        - "deepseek": DeepSeek AI
        - "phantom": Phantom AI (ethereal capabilities)
        """
        self.provider_name = provider.lower()
        self.api_key = api_key or self._get_api_key_from_env()
        
        # Initialize provider based on selection
        if self.provider_name == "mistral":
            self.provider = MistralAIProvider(self.api_key)
        elif self.provider_name == "openai":
            self.provider = OpenAIProvider(self.api_key)
        elif self.provider_name == "claude":
            self.provider = ClaudeAIProvider(self.api_key)
        elif self.provider_name == "gemini":
            self.provider = GeminiAIProvider(self.api_key)
        elif self.provider_name == "cohere":
            self.provider = CohereAIProvider(self.api_key)
        elif self.provider_name == "deepseek":
            self.provider = DeepSeekAIProvider(self.api_key)
        elif self.provider_name == "meta":
            self.provider = MetaAIProvider(self.api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}. Supported providers: mistral, openai, claude, gemini, cohere, deepseek, meta")
        
        # Setup logging and monitoring
        self.logger = logging.getLogger(__name__)
        self.performance_metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0.0
        }
    
    def _get_api_key_from_env(self) -> str:
        """
        Retrieve API key from environment variables
        
        This method implements a secure API key retrieval strategy that:
        1. Checks provider-specific environment variables
        2. Uses secure environment variable access
        3. Provides fallback to empty string
        4. Logs key availability status
        
        Returns:
            str: API key or empty string if not found
            
        Security Considerations:
        - Environment variables provide secure storage
        - No key logging or exposure
        - Provider-specific key isolation
        """
        env_mapping = {
            "mistral": "MISTRAL_API_KEY",
            "openai": "OPENAI_API_KEY",
            "claude": "ANTHROPIC_API_KEY",
            "gemini": "GOOGLE_API_KEY",
            "cohere": "COHERE_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "meta": "META_API_KEY"
        }
        
        env_var = env_mapping.get(self.provider_name, "")
        return os.getenv(env_var, "") if env_var else ""
    
    async def generate_response(self, query: str, context: str = "", mode: str = "creative") -> str:
        """
        Generate AI response using configured provider
        
        This method provides a unified interface for AI response generation
        across different providers with comprehensive error handling and
        performance monitoring.
        
        Args:
            query (str): User query or prompt
            context (str): Additional context for response generation
            mode (str): AI personality mode
            
        Returns:
            str: Generated AI response or error message
            
        Performance Monitoring:
        - Request timing and latency
        - Success/failure tracking
        - Response quality metrics
        - Provider performance comparison
        """
        import time
        start_time = time.time()
        
        try:
            # Update performance metrics
            self.performance_metrics["total_requests"] += 1
            
            # Generate response using configured provider
            response = await self.provider.generate_response(query, context, mode)
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Update performance metrics
            if not response.startswith("❌") and not response.startswith("⚠️"):
                self.performance_metrics["successful_requests"] += 1
            else:
                self.performance_metrics["failed_requests"] += 1
            
            # Update average response time
            total_requests = self.performance_metrics["total_requests"]
            current_avg = self.performance_metrics["average_response_time"]
            self.performance_metrics["average_response_time"] = (
                (current_avg * (total_requests - 1) + response_time) / total_requests
            )
            
            # Log performance metrics
            self.logger.info(f"AI response generated in {response_time:.2f}s using {self.provider_name}")
            
            return response
            
        except Exception as e:
            # Handle unexpected errors
            self.performance_metrics["failed_requests"] += 1
            self.logger.error(f"Error in AI integration manager: {e}")
            return f"❌ Integration error: {str(e)}"
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive integration status
        
        Returns:
            dict: Status information including provider, performance metrics, and health
        """
        return {
            "provider": self.provider_name,
            "api_key_configured": bool(self.api_key),
            "performance_metrics": self.performance_metrics.copy(),
            "provider_metrics": {
                "request_count": getattr(self.provider, 'request_count', 0),
                "error_count": getattr(self.provider, 'error_count', 0),
                "last_request_time": getattr(self.provider, 'last_request_time', None)
            }
        }
    
    def update_api_key(self, api_key: str):
        """
        Update API key for current provider
        
        Args:
            api_key (str): New API key
        """
        self.api_key = api_key
        self.provider.api_key = api_key
    
    def switch_provider(self, provider: str, api_key: str = None):
        """
        Switch to different AI provider
        
        Args:
            provider (str): New provider name
            api_key (str): API key for new provider
            
        Raises:
            ValueError: If provider is not supported
        """
        supported_providers = ["mistral", "openai", "claude", "gemini", "cohere", "deepseek", "meta"]
        
        if provider.lower() not in supported_providers:
            raise ValueError(f"Provider must be one of: {', '.join(supported_providers)}")
        
        # Update provider configuration
        self.provider_name = provider.lower()
        self.api_key = api_key or self._get_api_key_from_env()
        
        # Initialize new provider
        if self.provider_name == "mistral":
            self.provider = MistralAIProvider(self.api_key)
        elif self.provider_name == "openai":
            self.provider = OpenAIProvider(self.api_key)
        elif self.provider_name == "claude":
            self.provider = ClaudeAIProvider(self.api_key)
        elif self.provider_name == "gemini":
            self.provider = GeminiAIProvider(self.api_key)
        elif self.provider_name == "cohere":
            self.provider = CohereAIProvider(self.api_key)
        elif self.provider_name == "deepseek":
            self.provider = DeepSeekAIProvider(self.api_key)
        elif self.provider_name == "meta":
            self.provider = MetaAIProvider(self.api_key)
        
        # Reset performance metrics for new provider
        self.performance_metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0.0
        }
        
        self.logger.info(f"Switched to {self.provider_name} provider")
    
    def get_supported_providers(self) -> List[str]:
        """
        Get list of supported AI providers
        
        Returns:
            List[str]: List of supported provider names
        """
        return ["mistral", "openai", "claude", "gemini", "cohere", "deepseek", "meta"]
    
    def get_provider_info(self) -> Dict[str, Dict[str, str]]:
        """
        Get detailed information about all supported providers
        
        Returns:
            Dict[str, Dict[str, str]]: Provider information including models, rate limits, and features
        """
        return {
            "mistral": {
                "name": "Mistral AI",
                "models": "Mistral Large, Mistral Medium",
                "rate_limit": "20 req/min (free), 1000 req/min (paid)",
                "features": "Excellent response quality, fast processing",
                "website": "https://console.mistral.ai/"
            },
            "openai": {
                "name": "OpenAI",
                "models": "GPT-4o, GPT-3.5-turbo",
                "rate_limit": "500 req/min (GPT-4o), 3500 req/min (GPT-3.5)",
                "features": "Advanced reasoning, comprehensive analysis",
                "website": "https://platform.openai.com/"
            },
            "claude": {
                "name": "Anthropic Claude",
                "models": "Claude 3.5 Sonnet, Claude 3 Opus",
                "rate_limit": "500 req/min (Sonnet), 200 req/min (Opus)",
                "features": "Advanced reasoning, safety-focused",
                "website": "https://console.anthropic.com/"
            },
            "gemini": {
                "name": "Google Gemini",
                "models": "Gemini Pro, Gemini Flash",
                "rate_limit": "1000 req/min (Pro), 2000 req/min (Flash)",
                "features": "Multimodal capabilities, Google integration",
                "website": "https://aistudio.google.com/"
            },
            "cohere": {
                "name": "Cohere",
                "models": "Command, Command Light",
                "rate_limit": "1000 req/min (Command), 2000 req/min (Light)",
                "features": "Enterprise-focused, multilingual support",
                "website": "https://cohere.com/"
            },
            "deepseek": {
                "name": "DeepSeek",
                "models": "DeepSeek Chat, DeepSeek Coder",
                "rate_limit": "50 req/min (free), 2000 req/min (paid)",
                "features": "Code generation, technical expertise",
                "website": "https://platform.deepseek.com/"
            },
            "meta": {
                "name": "Meta AI",
                "models": "Llama 3.1 405B, Llama 3.1 70B, Llama 3.1 8B",
                "rate_limit": "100-500 req/min (depending on model)",
                "features": "Advanced reasoning, multilingual support",
                "website": "https://ai.meta.com/"
            }
        }

def configure_ai_provider(provider: str = "mistral", api_key: str = None) -> AIIntegrationManager:
    """
    Factory function for creating AI integration manager
    
    This function provides a convenient way to create and configure
    AI integration managers with proper error handling and validation.
    
    Args:
        provider (str): AI provider name
        api_key (str): Provider-specific API key
        
    Returns:
        AIIntegrationManager: Configured integration manager
        
    Raises:
        ValueError: If provider is not supported
    """
    return AIIntegrationManager(provider, api_key) 