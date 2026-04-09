# PowerShell setup script for LangGraph Ollama Agent on Windows

Write-Host "======================================"
Write-Host "LangGraph Ollama Agent Setup"
Write-Host "======================================"

# Check Python version
Write-Host "Checking Python version..."
$pythonVersion = python --version 2>&1
Write-Host "Python version: $pythonVersion"

# Create virtual environment
Write-Host "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..."
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# Create logs directory
Write-Host "Creating logs directory..."
New-Item -ItemType Directory -Force -Path logs | Out-Null

# Create .env if not exists
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..."
    Copy-Item ".env" ".env.backup" -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "======================================"
Write-Host "Setup Complete!"
Write-Host "======================================"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Activate the virtual environment:"
Write-Host "   .\venv\Scripts\Activate.ps1"
Write-Host ""
Write-Host "2. Update .env file with your configuration:"
Write-Host "   notepad .env"
Write-Host ""
Write-Host "3. Ensure Ollama is installed and running:"
Write-Host "   Start Ollama application"
Write-Host ""
Write-Host "4. Pull a model (if not already done):"
Write-Host "   ollama pull mistral"
Write-Host ""
Write-Host "5. Run the application:"
Write-Host "   python src/main.py --interactive"
Write-Host ""
