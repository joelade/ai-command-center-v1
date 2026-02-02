"""
AI Command Center v2 - QA Multi-Agent Orchestrator
Author: Joel Adelubi
Version: 2.0
Description: FastAPI orchestration service for multi-agent AI coordination
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import httpx
import asyncio
from typing import List, Optional
import subprocess

app = FastAPI(title="QA Orchestrator")

# Configuration
OLLAMA_BASE_URL = "http://ollama:11434"
AVAILABLE_MODELS = ["mistral:latest", "neural-chat", "orca-mini", "Qwen2.5", "nomic-embed-text:latest", "deepseek-coder", "llama3"]

class ModelInfo(BaseModel):
    name: str
    size: Optional[str] = None
    modified: Optional[str] = None
    digest: Optional[str] = None

class PullModelRequest(BaseModel):
    model_name: str

class QueryRequest(BaseModel):
    model: str
    prompt: str
    stream: bool = False

class AgentConfig(BaseModel):
    models: List[str]
    max_concurrent: int = 2

# Global state
agent_config = AgentConfig(models=[], max_concurrent=2)
active_models = []

@app.get("/")
def health():
    return {"status": "ok", "service": "QA Orchestrator"}

@app.get("/models/available")
def get_available_models():
    """Get list of available models to pull"""
    return {
        "available_models": AVAILABLE_MODELS,
        "description": "These are the recommended LLM models for QA testing"
    }

@app.get("/models/list")
async def list_models():
    """List all currently installed models"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            models = response.json().get("models", [])
            return {
                "installed_models": [m["name"].split(":")[0] for m in models],
                "total_models": len(models),
                "models_detail": models
            }
    except Exception as e:
        return {"error": str(e), "installed_models": []}

@app.post("/models/pull")
async def pull_model(request: PullModelRequest, background_tasks: BackgroundTasks):
    """Pull a new LLM model from registry"""
    model_name = request.model_name
    
    if model_name not in AVAILABLE_MODELS:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{model_name}' not in available models. Available: {AVAILABLE_MODELS}"
        )
    
    background_tasks.add_task(pull_model_background, model_name)
    return {
        "status": "pulling",
        "model": model_name,
        "message": f"Started pulling {model_name} in background"
    }

@app.post("/models/remove")
async def remove_model(request: ModelInfo):
    """Remove an installed model"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.delete(
                f"{OLLAMA_BASE_URL}/api/delete",
                json={"name": request.name}
            )
            return {
                "status": "removed",
                "model": request.name,
                "message": f"Model {request.name} successfully removed"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_model(request: QueryRequest):
    """Query a specific model"""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": request.model,
                    "prompt": request.prompt,
                    "stream": request.stream
                }
            )
            
            if request.stream:
                return {"status": "streaming", "model": request.model}
            else:
                return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/config")
def get_config():
    """Get current agent configuration"""
    return {
        "config": agent_config,
        "active_models": active_models,
        "ollama_url": OLLAMA_BASE_URL
    }

@app.post("/config/update")
async def update_config(config: AgentConfig):
    """Update agent configuration"""
    global agent_config
    agent_config = config
    return {"status": "updated", "config": config}

@app.post("/run")
async def run_agent(background_tasks: BackgroundTasks):
    """Run QA tests with configured models"""
    models = agent_config.models
    if not models:
        raise HTTPException(status_code=400, detail="No models configured")
    
    background_tasks.add_task(run_agent_background, models)
    return {
        "status": "started",
        "models": models,
        "message": "QA Agent started with multiple models"
    }

@app.get("/status")
async def get_status():
    """Get current agent status"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            models = response.json().get("models", [])
            return {
                "status": "running",
                "installed_models": len(models),
                "models": [m["name"] for m in models],
                "max_concurrent_tasks": agent_config.max_concurrent
            }
    except:
        return {"status": "error", "message": "Cannot connect to Ollama"}

async def pull_model_background(model_name: str):
    """Background task to pull a model"""
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            await client.post(
                f"{OLLAMA_BASE_URL}/api/pull",
                json={"name": model_name}
            )
            global active_models
            if model_name not in active_models:
                active_models.append(model_name)
    except Exception as e:
        print(f"Error pulling model {model_name}: {e}")

async def run_agent_background(models: List[str]):
    """Background task to run QA tests with multiple models"""
    try:
        print(f"Starting QA test execution with models: {models}")
        # Simulate QA test execution
        await asyncio.sleep(5)
        print(f"QA test completed with {len(models)} models")
    except Exception as e:
        print(f"Error running agent: {e}")
