#!/bin/bash
# Installation Script for MCP Job Application Intelligence System

echo "========================================================================"
echo " MCP Job Application Intelligence System - Installation"
echo "========================================================================"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check if Python 3.10+
required_version="3.10"
if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo "Error: Python 3.10 or higher is required"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"

# Install requirements
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements-full.txt
echo "✓ Dependencies installed"

# Create necessary directories
echo ""
echo "Creating directory structure..."
mkdir -p data/databases
mkdir -p data/profiles
mkdir -p generated_resumes
mkdir -p logs
mkdir -p templates
mkdir -p docs
echo "✓ Directories created"

# Check for .env file
echo ""
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cat > .env << 'EOF'
# Apify API Token (get from https://apify.com)
APIFY_API_TOKEN=your_apify_api_token_here

# Ollama URL (default: local installation)
OLLAMA_URL=http://localhost:11434/api/generate
EOF
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your APIFY_API_TOKEN"
else
    echo "✓ .env file already exists"
fi

# Check if Ollama is installed
echo ""
echo "Checking for Ollama installation..."
if command -v ollama &> /dev/null; then
    echo "✓ Ollama is installed"

    # Check if llama3.1:8b is available
    if ollama list | grep -q "llama3.1:8b"; then
        echo "✓ Llama 3.1 8B model is available"
    else
        echo ""
        echo "⚠️  Llama 3.1 8B model not found"
        read -p "Download Llama 3.1 8B model now? (yes/no): " download_model
        if [ "$download_model" = "yes" ]; then
            echo "Downloading Llama 3.1 8B model (this may take a while)..."
            ollama pull llama3.1:8b
            echo "✓ Model downloaded"
        fi
    fi
else
    echo "⚠️  Ollama not found"
    echo ""
    echo "Ollama is required for AI analysis and resume generation."
    echo "Install from: https://ollama.ai/"
    echo ""
    echo "After installing Ollama, run:"
    echo "  ollama pull llama3.1:8b"
fi

# Check for LaTeX
echo ""
echo "Checking for LaTeX installation..."
if command -v pdflatex &> /dev/null; then
    echo "✓ LaTeX is installed"
else
    echo "⚠️  LaTeX not found"
    echo ""
    echo "LaTeX is optional but recommended for PDF generation."
    echo "Install TeX Live: https://www.tug.org/texlive/"
fi

# Make scripts executable
echo ""
echo "Making scripts executable..."
chmod +x orchestrator.py
chmod +x cli_set_preferences.py
chmod +x setup.sh
echo "✓ Scripts are executable"

# Summary
echo ""
echo "========================================================================"
echo " Installation Complete!"
echo "========================================================================"
echo ""
echo "Next Steps:"
echo ""
echo "1. Configure Apify API token:"
echo "   - Get free API key from https://apify.com"
echo "   - Add to .env file: APIFY_API_TOKEN=your_token"
echo ""
echo "2. Initialize your profile:"
echo "   - Place your resume data in data/profiles/profile.json"
echo "   - Or use the Profile MCP Server to create/update it"
echo ""
echo "3. Set job search preferences:"
echo "   ./cli_set_preferences.py"
echo ""
echo "4. Start using the system:"
echo "   python orchestrator.py --workflow"
echo ""
echo "5. For help with MCP servers:"
echo "   python orchestrator.py --help-servers"
echo ""
echo "Documentation: See docs/README.md"
echo ""
