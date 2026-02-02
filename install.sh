
#!/bin/bash

set -e

echo "🚀 Installing AI Command Center v2..."

# Detect OS
OS="$(uname -s)"

install_docker_linux() {
  curl -fsSL https://get.docker.com | sh
  sudo usermod -aG docker $USER
}

if ! command -v docker &> /dev/null
then
    echo "Docker not found. Installing..."
    if [[ "$OS" == "Linux" ]]; then
        install_docker_linux
    else
        echo "Please install Docker Desktop from https://www.docker.com/products/docker-desktop/"
        exit 1
    fi
fi

if ! command -v docker-compose &> /dev/null
then
    echo "Installing docker-compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

echo "Checking disk space (models require ~30GB)..."
DISK_AVAILABLE=$(df . | tail -1 | awk '{print $4}')
if [ $DISK_AVAILABLE -lt 31457280 ]; then
    echo "⚠️  Warning: Low disk space detected. Models require at least 30GB."
fi

echo "Starting AI Command Center v2..."
docker compose up -d

echo ""
echo "✅ AI Command Center is running!"
echo ""
echo "📊 Service Ports:"
echo "   • Open WebUI (Ollama Web):    http://localhost:3000"
echo "   • QA Dashboard (Streamlit):   http://localhost:8501"
echo "   • QA Orchestrator API:        http://localhost:8000"
echo "   • Ollama API:                 http://localhost:11434"
echo ""
echo "🤖 Available LLM Models:"
echo "   • mistral:latest"
echo "   • neural-chat"
echo "   • orca-mini"
echo "   • Qwen2.5"
echo "   • nomic-embed-text:latest"
echo "   • deepseek-coder"
echo "   • llama3"
echo ""
echo "📖 Documentation: See DEPENDENCIES.md for details"
echo "🔧 Configuration: Check docker-compose.yml for service details"
echo ""
echo "💡 Next steps:"
echo "   1. Open http://localhost:8501 for the QA Dashboard"
echo "   2. Use the Models tab to select/pull LLM models"
echo "   3. Run tests from the Tests tab"
echo ""
echo "To view logs: docker compose logs -f qa-dashboard"
echo "To stop services: docker compose down"
