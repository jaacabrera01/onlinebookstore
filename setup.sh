#!/bin/bash
# Setup script for BookCart Automation Testing Framework

set -e

echo "=========================================="
echo "BookCart Test Automation Framework Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python --version
python_version=$(python --version 2>&1 | awk '{print $2}')

# Check if Python is 3.10+
if [[ $(echo $python_version | cut -d. -f1) -lt 3 ]] || [[ $(echo $python_version | cut -d. -f1) -eq 3 && $(echo $python_version | cut -d. -f2) -lt 10 ]]; then
    echo "❌ Python 3.10 or higher is required"
    exit 1
fi
echo "✓ Python version is compatible"
echo ""

# Create virtual environment if it doesn't exist
echo "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Install Playwright browsers
echo "Installing Playwright browsers..."
echo "This may take a few minutes..."
playwright install
echo "✓ Playwright installed"
echo ""

# Install Playwright system dependencies
echo "Installing Playwright system dependencies..."
python -m playwright install-deps
echo "✓ System dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created from .env.example"
    echo "  Please update .env with your configuration"
else
    echo "✓ .env file already exists"
fi
echo ""

# Create necessary directories
echo "Creating directories..."
mkdir -p test-results/screenshots logs allure-results
echo "✓ Directories created"
echo ""

# Run smoke tests to verify setup
echo "Running smoke tests to verify setup..."
echo ""
if pytest -m smoke -v --tb=short; then
    echo ""
    echo "=========================================="
    echo "✓ Setup completed successfully!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "1. Run all tests:        pytest tests/ -v"
    echo "2. Run smoke tests:      pytest -m smoke -v"
    echo "3. Run critical tests:   pytest -m critical -v"
    echo "4. View test report:     pytest tests/ --alluredir=allure-results && allure serve allure-results"
    echo ""
    echo "See README.md for more information"
else
    echo ""
    echo "=========================================="
    echo "⚠ Setup completed but smoke tests failed"
    echo "=========================================="
    echo ""
    echo "This might be expected if the application is down."
    echo "You can still run tests manually with:"
    echo "  pytest tests/ -v"
    echo ""
fi
