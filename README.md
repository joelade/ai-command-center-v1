
# AI Command Center 🧠🚀 (Version 2)

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
2. **Automatically pull all 7 LLM models** (may take 30-60 minutes)
3. Initialize the OpenWebUI interface

Then open:
http://localhost:3000

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
All models are **automatically downloaded on first startup** and ready for use:

1. **mistral:latest** (4.4 GB) - High-performance language model
2. **neural-chat** (4.1 GB) - Conversational AI model
3. **orca-mini** (2.0 GB) - Lightweight model
4. **deepseek-coder** (776 MB) - Code generation specialist
5. **llama3** (4.7 GB) - Meta's latest language model
6. **qwen2.5** (4.7 GB) - Advanced Chinese-optimized model
7. **nomic-embed-text:latest** - Text embedding model (for RAG)

## Getting Started

### Access the Web UI
Open your browser and navigate to: **http://localhost:3000**

### View the Dashboard
Access analytics and monitoring: **http://localhost:8501**

### API Access
- Ollama API: http://localhost:11434
- QA Orchestrator: http://localhost:8000

### Useful Commands

Check container status:
```bash
docker compose ps
```

View logs:
```bash
docker compose logs -f
```

Pull additional models:
```bash
docker exec ai-command-center-v2-ready-ollama-1 ollama pull <model-name>
```

Stop all services:
```bash
docker compose down
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

