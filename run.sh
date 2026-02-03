#!/bin/bash

# Startup script for Content Search and Publishing System

echo "==================================="
echo "Content Search System - energo-audit.by"
echo "==================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and configure your API keys."
    echo ""
    echo "Run: cp .env.example .env"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data logs

# Check command line argument
MODE=${1:-scheduler}

echo ""
echo "🚀 Starting in mode: $MODE"
echo ""

# Run the application
python main.py --mode $MODE

# Deactivate virtual environment on exit
deactivate