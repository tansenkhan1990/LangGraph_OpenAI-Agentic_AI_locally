#!/bin/bash

# Setup script for LangGraph Ollama Agent on Linux/macOS

set -e

echo "======================================"
echo "LangGraph Ollama Agent Setup"
echo "======================================"

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create logs directory
echo "Creating logs directory..."
mkdir -p logs

# Create .env if not exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env .env.backup
fi

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Update .env file with your configuration:"
echo "   nano .env"
echo ""
echo "3. Ensure Ollama is installed and running:"
echo "   ollama serve"
echo ""
echo "4. Pull a model (if not already done):"
echo "   ollama pull mistral"
echo ""
echo "5. Run the application:"
echo "   python src/main.py --interactive"
echo ""
