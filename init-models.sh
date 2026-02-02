#!/bin/bash

# AI Command Center - Model Initialization Script
# Author: Joel Adelubi
# Version: 2.0
# This script automatically pulls all necessary models for OpenWebUI

echo "🤖 Starting Ollama service..."
/bin/ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama to initialize..."
sleep 10

# Check if Ollama is responding
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags > /dev/null; then
        echo "✅ Ollama is ready!"
        break
    fi
    echo "   Attempt $i/30 - waiting for Ollama..."
    sleep 2
done

# Array of models to pull
# DEFAULT MODEL (Always pulled)
DEFAULT_MODEL="llama3"

# OPTIONAL MODELS (Set PULL_ALL_MODELS=1 to enable, or use OPTIONAL_MODELS env var)
OPTIONAL_MODELS=(
    "mistral:latest"
    "neural-chat"
    "orca-mini"
    "deepseek-coder"
    "qwen2.5"
    "nomic-embed-text:latest"
)
if [ "$PULL_ALL" = "1" ]; then
    echo "Mode: All models (DEFAULT + OPTIONAL)"
else
    echo "Mode: Default model only (llama3)"
    echo "To pull all models, set: PULL_ALL_MODELS=1"
fi
echo "This may take 30-60 minutes depending on your internet connection."
echo ""

for MODEL in "${MODELS_TO_PULL[@]}"; do
    if [ "$MODEL" = "$DEFAULT_MODEL" ]; then
        echo "🔄 Pulling DEFAULT MODEL: $MODEL..."
    else
        echo "🔄 Pulling optional model: $MODEL..."
    fiODEL")
else
    MODELS_TO_PULL=("$DEFAULT_MODEL" $OPTIONAL_MODELS_LIST)
fi

if [ "$PULL_ALL" = "1" ]; then
    MODELS_TO_PULL=("$DEFAULT_MODEL" "${OPTIONAL_MODELS[@]}")
fi

echo ""
echo "📥 Pulling models for OpenWebUI..."
echo "This may take 30-60 minutes depending on your internet connection."
echo ""

for MODEL in "${MODELS[@]}"; do
    echo "🔄 Pulling $MODEL..."
    ollama pull "$MODEL"
    if [ $? -eq 0 ]; then
        echo "✅ Successfully pulled $MODEL"
    else
        echo "❌ Failed to pull $MODEL"
    fi
    echo ""
done

echo "✅ Model initialization complete!"
echo "🎉 All models are ready for use in OpenWebUI"
echo ""
echo "📊 Access the services:"
echo "   • OpenWebUI: http://localhost:3000"
echo "   • Dashboard: http://localhost:8501"
echo "   • Ollama API: http://localhost:11434"

# Keep the container running
wait $OLLAMA_PID
