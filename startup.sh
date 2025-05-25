#!/bin/bash
# startup.sh - Azure App Service startup script

echo "🚀 Starting Nestlé AI Chatbot deployment..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating required directories..."
mkdir -p graph
mkdir -p logs

# Build the knowledge graph if it doesn't exist
echo "🏗️ Checking for knowledge graph..."
if [ ! -f "graph/graph.pkl" ]; then
    echo "📊 Building knowledge graph..."
    python -c "from backend.graph_builder import build_graph; build_graph()"
else
    echo "✅ Knowledge graph already exists"
fi

# Set proper permissions
echo "🔒 Setting permissions..."
chmod +x app.py

# Start the application
echo "🌐 Starting FastAPI application..."
if [ "$ENVIRONMENT" = "development" ]; then
    echo "🔧 Running in development mode..."
    uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000} --reload
else
    echo "🚀 Running in production mode..."
    gunicorn app:app -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000} --timeout 120
fi