# QA Command Center v2 - Dependencies & Setup

## Project Structure
```
ai-command-center-v2-ready/
├── docker-compose.yml          # Main service orchestration
├── requirements.txt            # All project dependencies
├── README.md                   # This file
├── orchestrator/
│   ├── main.py                # FastAPI orchestration service
│   └── requirements.txt        # Orchestrator-specific dependencies
├── dashboard/
│   ├── dashboard.py           # Streamlit analytics dashboard
│   └── requirements.txt        # Dashboard-specific dependencies
└── samples/
    └── [sample files]
```

## Dependencies

### Orchestrator Service (Port 8000)
- **fastapi** 0.104.1 - Modern Python web framework
- **uvicorn** 0.24.0 - ASGI web server
- **httpx** 0.25.2 - Async HTTP client
- **pydantic** 2.5.0 - Data validation
- **python-multipart** 0.0.6 - Multipart form data support

### Dashboard Service (Port 8501)
- **streamlit** 1.53.1 - Interactive data app framework
- **pandas** 2.3.3 - Data manipulation library
- **plotly** 6.5.2 - Interactive visualizations
- **requests** 2.32.5 - HTTP library

### External Services
- **ollama** - LLM runtime (port 11434)
- **open-webui** - Ollama web interface (port 3000)

## Available LLM Models

1. **mistral:latest** - High-performance language model
2. **neural-chat** - Conversational AI model
3. **orca-mini** - Lightweight model
4. **Qwen2.5** - Advanced Chinese-optimized model
5. **nomic-embed-text:latest** - Text embedding model
6. **deepseek-coder** - Code generation specialist
7. **llama3** - Meta's latest language model

## Service Ports

| Service | Port | URL |
|---------|------|-----|
| Ollama | 11434 | http://localhost:11434 |
| Open WebUI | 3000 | http://localhost:3000 |
| QA Orchestrator API | 8000 | http://localhost:8000 |
| QA Dashboard | 8501 | http://localhost:8501 |

## API Endpoints

### Models Management
- `GET /models/available` - List available models to pull
- `GET /models/list` - List all installed models
- `POST /models/pull` - Pull a new LLM model (background task)
- `POST /models/remove` - Remove an installed model

### Query & Execution
- `POST /query` - Query a specific model
- `POST /run` - Run QA tests with configured models
- `GET /status` - Get system status

### Configuration
- `GET /config` - Get current agent configuration
- `POST /config/update` - Update agent settings

## Installation & Running

### Prerequisites
- Docker and Docker Compose installed
- At least 30GB disk space (for multiple LLM models)
- 8GB+ RAM recommended

### Startup
```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f qa-dashboard

# Stop services
docker compose down
```

### Without Volume Deletion
```bash
# Stop services (keep data)
docker compose down

# Stop and remove volumes (CAUTION: deletes data)
docker compose down -v
```

## Usage Examples

### Via Dashboard
1. Navigate to http://localhost:8501
2. Use "🤖 Models" tab to view/manage available models
3. Use "📋 Tests" tab to run QA tests
4. Monitor results in "📊 Dashboard" tab

### Via API
```bash
# Get available models
curl http://localhost:8000/models/available

# Pull a model (background task)
curl -X POST http://localhost:8000/models/pull \
  -H "Content-Type: application/json" \
  -d '{"model_name": "mistral:latest"}'

# Query a model
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral:latest",
    "prompt": "What is 2+2?",
    "stream": false
  }'
```

## Requirements File Usage

### Root requirements.txt
Contains all project dependencies. Use for:
- Local development setup
- CI/CD pipelines
- Documentation

### Service-Specific requirements.txt
Located in `orchestrator/` and `dashboard/` directories for Docker builds.

### Install Dependencies Locally
```bash
# Install all dependencies
pip install -r requirements.txt

# Or service-specific
pip install -r orchestrator/requirements.txt
pip install -r dashboard/requirements.txt
```

## Version Information
- QA Confidence Dashboard v2.0
- Multi-LLM Support enabled
- FastAPI Backend
- Streamlit Frontend

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    QA Command Center v2                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Dashboard (8501) ──────┬─────────── Orchestrator (8000)    │
│  (Streamlit)           │            (FastAPI)               │
│                        │                                     │
│                        └──────────── Ollama (11434)          │
│                                      └─ LLM Models           │
│                                                               │
│                    ┌─── Open WebUI (3000)                   │
│                    │    (Web Interface)                      │
│                    │                                          │
└────────────────────┼──────────────────────────────────────────┘
                     │
                     └─ Ollama API
```

## Troubleshooting

### Port already in use
Kill the process on that port or change the mapping in docker-compose.yml

### Out of disk space
Models can be large (2GB-13GB each). Ensure adequate space before pulling.

### Container won't start
Check logs with: `docker logs <container_name>`

### Connection to Ollama fails
Ensure Ollama container is healthy: `docker ps`

## Notes
- Models are stored in Docker volumes (`ollama` volume)
- Data persists across container restarts (unless `docker compose down -v` is used)
- GPU support requires additional Docker configuration
