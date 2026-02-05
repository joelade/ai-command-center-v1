# AI Command Center 🧠🚀 (Version 2)

**Author:** Joel Adelubi  
**Version:** 1.0  
**License:** Open Source

Local Palantir-style AI platform built with Open WebUI, Ollama, RAG, and autonomous agents.

## 🔒 Privacy & Security - 100% Local & Safe

This platform is **completely self-hosted** and runs entirely on your machine with **ZERO external dependencies**:

✅ **No Cloud Services** - Everything runs locally in Docker containers
✅ **No Data Collection** - Your data never leaves your computer
✅ **Telemetry Disabled** - All analytics and tracking are completely disabled
✅ **No API Keys Required** - No connection to external AI providers
✅ **Offline Operation** - Works without internet after initial setup
✅ **Open Source Models** - Built on community-maintained, transparent models
✅ **Full Control** - You own and control all your data

### What This Means
- **Your Conversations Stay Private**: Every prompt, response, and interaction is stored locally
- **No Monitoring**: No usage tracking, no telemetry, no analytics
- **Sovereign AI**: Complete independence from commercial AI providers
- **GDPR/CCPA Compliant**: No data sharing with third parties
- **Enterprise Ready**: Suitable for handling sensitive business information

## Features
- Local ChatGPT replacement (Ollama)
- AI Command Center UI (Open WebUI)
- Knowledge AI with RAG
- Multi-agent orchestration
- DevOps & automation ready
- Offline & sovereign AI
- Auto-installer script
- QA Multi-Agent Orchestrator (FastAPI)
- Vector-ready knowledge integration
- cy.prompt automation generation
- Risk & completeness scoring
- Dashboard service

## Quick Start (One Command)

```bash
curl -fsSL install.sh | bash
```

The installation script will:
1. Start all Docker services
2. **Automatically pull llama3 by default** (the recommended model)
3. Optionally pull additional models (see Configuration below)
4. Initialize the OpenWebUI interface

Then open:
http://localhost:3000

### Configuration: Which Models to Pull?

By default, only **llama3** is pulled (fast setup, ~4.7GB).

To pull **all 7 models**, set the environment variable before starting:

```bash
# Pull all models on startup
PULL_ALL_MODELS=1 docker compose up -d
```

Or edit `docker-compose.yml` and change:
```yaml
environment:
  - PULL_ALL_MODELS=1
```

# QA AI Command Center – Full Docker Stack

## ✅ Setup Status
- **Docker Services**: All running
- **Models**: Fully downloaded and ready
- **Total Disk Usage**: ~27GB

## Services
| Service | Status | Port | URL |
|---------|--------|------|-----|
| Ollama (LLM Runtime) | ✅ Running | 11434 | http://localhost:11434 |
| Open WebUI | ✅ Running | 3000 | http://localhost:3000 |
| QA Orchestrator API | ✅ Running | 8000 | http://localhost:8000 |
| QA Dashboard | ✅ Running | 8501 | http://localhost:8501 |

## Available LLM Models

### Default Model (Always Pulled)
- **llama3** (4.7 GB) - Meta's latest language model - Recommended for general use

### Optional Models (Pull with PULL_ALL_MODELS=1)
1. **mistral:latest** (4.4 GB) - High-performance language model
2. **neural-chat** (4.1 GB) - Conversational AI model
3. **orca-mini** (2.0 GB) - Lightweight model
4. **deepseek-coder** (776 MB) - Code generation specialist
5. **qwen2.5** (4.7 GB) - Advanced Chinese-optimized model
6. **nomic-embed-text:latest** - Text embedding model (for **RAG**)

## Service Details

### 🤖 QA Orchestrator API (FastAPI)
**Port:** 8000 | **URL:** http://localhost:8000

The orchestrator is a multi-agent coordination service that manages LLM models and executes QA tests across multiple models simultaneously.

#### Key Features:
- **Model Management**: Pull, list, and remove LLM models from the Ollama registry
- **Multi-Model Testing**: Run QA tests in parallel across configured models
- **Asynchronous Operations**: Background task processing for long-running operations
- **Configuration Management**: Manage active models and concurrent task limits
- **Query Interface**: Send prompts to any model and receive responses

#### Available Endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/models/available` | GET | List all available models that can be pulled |
| `/models/list` | GET | List all currently installed models |
| `/models/pull` | POST | Download and install a new model |
| `/models/remove` | POST | Remove an installed model |
| `/query` | POST | Send a prompt to a specific model |
| `/config` | GET | View current agent configuration |
| `/config/update` | POST | Update model configuration and task limits |
| `/run` | POST | Execute QA tests with all configured models |
| `/status` | GET | Get current system status and installed models |

#### Usage Examples:

**List Available Models:**
```bash
curl http://localhost:8000/models/available
```

**Pull a Model:**
```bash
curl -X POST http://localhost:8000/models/pull \
  -H "Content-Type: application/json" \
  -d '{"model_name": "mistral:latest"}'
```

**Query a Model:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral:latest",
    "prompt": "What is AI?",
    "stream": false
  }'
```

**Update Configuration:**
```bash
curl -X POST http://localhost:8000/config/update \
  -H "Content-Type: application/json" \
  -d '{
    "models": ["mistral:latest", "neural-chat"],
    "max_concurrent": 3
  }'
```

**Run QA Tests:**
```bash
curl -X POST http://localhost:8000/run
```

---

### 📊 QA Dashboard (Streamlit)
**Port:** 8501 | **URL:** http://localhost:8501

The dashboard provides a real-time analytics interface for monitoring QA test results, managing models, and viewing detailed test execution metrics.

#### Key Features:
- **Real-Time Metrics**: Completeness score, risk level, test coverage, response times
- **Visual Analytics**: Success rate trends, test case distribution, performance charts
- **Test Management**: Run test suites, monitor execution history, view detailed results
- **Model Dashboard**: View active models, performance metrics, pull new models
- **Comprehensive Reporting**: Test results summary, risk categorization, execution logs

#### Dashboard Components:

**Tab 1: Dashboard**
- Key metrics overview (Completeness, Risk, Coverage, Response Time)
- Test case distribution chart
- Success rate trend analysis
- Test results summary table
- Risk categories breakdown
- Recent test executions log

**Tab 2: Models**
- Available models to pull
- Active models status and performance
- Model download functionality
- Performance comparison table (response time, success rate, latency)

**Tab 3: Tests**
- Test suite selection and configuration
- Model selection for testing
- Test execution controls
- Test statistics overview
- Execution history with timestamps

#### How to Use:

1. **View Dashboard**: Open http://localhost:8501 in your browser
2. **Select Time Range**: Use sidebar controls to filter by Last 24h, 7d, 30d, or All Time
3. **Manage Models**: Go to "Models" tab to pull additional LLM models
4. **Run Tests**: Switch to "Tests" tab, select models and test suite, click "Run Tests"
5. **Monitor Results**: View real-time results and historical execution data

---

## Getting Started

### Step 1: Start All Services
All services start automatically with Docker Compose:
```bash
docker compose up -d
```

### Step 2: Access the Web Interfaces

| Service | URL | Purpose |
|---------|-----|---------|
| **Open WebUI** | http://localhost:3000 | Chat with AI models (ChatGPT replacement) |
| **QA Dashboard** | http://localhost:8501 | QA testing analytics and monitoring |

### Step 3: Use the QA System

1. **Check Available Models:**
   ```bash
   curl http://localhost:8000/models/available
   ```

2. **Pull Additional Models (if needed):**
   Use the QA Dashboard (Models tab) or API to download models

3. **Configure Models for Testing:**
   ```bash
   curl -X POST http://localhost:8000/config/update \
     -H "Content-Type: application/json" \
     -d '{"models": ["mistral:latest", "neural-chat"], "max_concurrent": 2}'
   ```

4. **Run QA Tests:**
   - Via Dashboard: Go to Tests tab → Select test suite → Click "Run Tests"
   - Via API: `curl -X POST http://localhost:8000/run`

5. **View Results:**
   Open the Dashboard (http://localhost:8501) to see real-time results

### Useful Commands

**Check container status:**
```bash
docker compose ps
```

**View service logs:**
```bash
docker compose logs -f orchestrator    # QA Orchestrator API
docker compose logs -f dashboard       # QA Dashboard
docker compose logs -f ollama          # LLM Runtime
```

**Pull additional models (if not already done):**
```bash
docker exec ai-command-center-v2-ready-ollama-1 ollama pull mistral:latest
docker exec ai-command-center-v2-ready-ollama-1 ollama pull neural-chat
docker exec ai-command-center-v2-ready-ollama-1 ollama pull orca-mini
docker exec ai-command-center-v2-ready-ollama-1 ollama pull deepseek-coder
docker exec ai-command-center-v2-ready-ollama-1 ollama pull qwen2.5
docker exec ai-command-center-v2-ready-ollama-1 ollama pull nomic-embed-text:latest
```

**Stop all services:**
```bash
docker compose down
```

**Remove all data (fresh start):**
```bash
docker compose down --volumes
```

## 🔐 Technical Privacy Details

### Telemetry Status - ALL DISABLED
- ✅ **HuggingFace Telemetry**: Disabled (`HF_HUB_DISABLE_TELEMETRY=1`)
- ✅ **Streamlit Analytics**: Disabled (headless mode)
- ✅ **Ollama Tracking**: Disabled by default
- ✅ **Log Collection**: Error-level logging only
- ✅ **External APIs**: No external calls unless explicitly configured

### Data Storage
- **All Data**: Stored in Docker volumes on your local machine
- **Ollama Models**: Stored in `/root/.ollama` volume
- **WebUI Data**: Stored in `/app/backend/data` volume
- **User Files**: Stored in mounted directories only

### Network Security
- **Localhost Only**: All services listen on `127.0.0.1` by default
- **No Internet Required**: After initial model download, operates completely offline
- **No Phone Home**: No periodic connectivity checks or version reporting
- **Firewall Ready**: Easily configure network isolation if needed

### Compliance
- **GDPR**: No personal data collection or sharing
- **HIPAA**: Suitable for healthcare data handling
- **CCPA**: No data sales or external sharing
- **SOC2**: Enterprise-grade data control

## ⚙️ Advanced Configuration

### Disable External Network Access (Maximum Security)
To run the platform with no external network access:
```bash
docker run --network none [other flags]
```

### Custom Data Retention
All data is stored locally. Delete volumes to completely remove all traces:
```bash
docker compose down --volumes
```

### Air-Gapped Deployment
For air-gapped environments:
1. Download models on a connected machine
2. Transfer Docker images and model volumes via external media
3. Deploy in isolated network

# AI Command Center v2

A FastAPI-based filesystem server implementing the Model Context Protocol (MCP).

**Author:** j.adelubi

## Features

- List files and directories
- Serve static files
- Get file contents via REST API
- Directory traversal support

## Usage

### Installation

```bash
pip install fastapi uvicorn python-multipart
```

### Running the Server

```bash
python main.py
```

The server will start on `http://0.0.0.0:3333`

### API Endpoints

- `GET /` - List all files in the root directory
- `GET /files/{path}` - Retrieve a specific file
- `GET /static/{path}` - Access static files

### Example Requests

```bash
# List files
curl http://localhost:3333/

# Get a file
curl http://localhost:3333/files/example.txt

# Access static content
curl http://localhost:3333/static/data.json
```

### Configuration

Set the data root directory by modifying the `create_app()` call:

```python
app = create_app(root="/your/custom/path")
```

Default root: `/app/data`

