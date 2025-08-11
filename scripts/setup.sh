#!/bin/bash

# Modern Python Development Environment Setup Script
# This script sets up the development environment for the project

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Check if running in Docker container
if [ -f /.dockerenv ]; then
    print_info "Running in Docker container"
    IN_DOCKER=true
else
    print_info "Running on host system"
    IN_DOCKER=false
fi

# Main setup function
main() {
    print_info "Starting Modern Python development environment setup..."
    
    # Check Python version
    print_info "Checking Python version..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python 3 not found. Please install Python 3.13 or later."
        exit 1
    fi
    
    # Check if uv is installed
    print_info "Checking for uv package manager..."
    if command -v uv &> /dev/null; then
        UV_VERSION=$(uv --version | cut -d' ' -f2)
        print_success "uv $UV_VERSION found"
    else
        print_info "Installing uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.cargo/bin:$PATH"
        print_success "uv installed successfully"
    fi
    
    # Create virtual environment if not in Docker
    if [ "$IN_DOCKER" = false ]; then
        print_info "Creating virtual environment..."
        if [ ! -d ".venv" ]; then
            uv venv .venv
            print_success "Virtual environment created"
        else
            print_info "Virtual environment already exists"
        fi
        
        # Activate virtual environment
        print_info "Activating virtual environment..."
        source .venv/bin/activate
        print_success "Virtual environment activated"
    fi
    
    # Install dependencies
    print_info "Installing project dependencies..."
    if [ -f "pyproject.toml" ]; then
        uv pip install -e ".[dev,test,docs]"
        print_success "Dependencies installed"
    else
        print_error "pyproject.toml not found"
        exit 1
    fi
    
    # Install common team libraries
    if [ -f "requirements-common.txt" ]; then
        print_info "Installing common team libraries..."
        uv pip install -r requirements-common.txt
        print_success "Common libraries installed"
    else
        print_info "requirements-common.txt not found, skipping common libraries"
    fi
    
    # Install personal development libraries
    if [ -f "requirements-dev.txt" ]; then
        print_info "Installing personal development libraries..."
        uv pip install -r requirements-dev.txt
        print_success "Personal libraries installed"
    else
        print_info "requirements-dev.txt not found, skipping personal libraries"
        if [ -f "requirements-dev.txt.example" ]; then
            print_info "Tip: Copy requirements-dev.txt.example to requirements-dev.txt to add personal libraries"
        fi
    fi
    
    # Install pre-commit hooks
    print_info "Setting up pre-commit hooks..."
    if command -v pre-commit &> /dev/null; then
        pre-commit install
        print_success "Pre-commit hooks installed"
    else
        print_info "Pre-commit not found, skipping hook installation"
    fi
    
    # Create necessary directories
    print_info "Creating project directories..."
    mkdir -p src tests docs/_static docs/_templates logs tmp
    print_success "Project directories created"
    
    # Initialize git if not already initialized
    if [ ! -d ".git" ]; then
        print_info "Initializing git repository..."
        git init
        git branch -M main
        print_success "Git repository initialized"
    fi
    
    # Set up environment variables
    if [ ! -f ".env" ] && [ -f ".env.example" ]; then
        print_info "Creating .env file from template..."
        cp .env.example .env
        print_success ".env file created (please update with your values)"
    fi
    
    # Run initial tests
    print_info "Running initial tests..."
    if command -v pytest &> /dev/null; then
        pytest --version
        print_success "pytest is ready"
    else
        print_error "pytest not found"
    fi
    
    # Check Ruff
    print_info "Checking code formatter and linter..."
    if command -v ruff &> /dev/null; then
        ruff --version
        print_success "Ruff is ready"
    else
        print_error "Ruff not found"
    fi
    
    # Build documentation
    print_info "Building documentation..."
    if [ -f "docs/Makefile" ]; then
        cd docs && make clean && make html && cd ..
        print_success "Documentation built successfully"
    else
        print_info "Documentation setup not found, skipping"
    fi
    
    print_success "Setup complete! 🚀"
    echo ""
    echo "Next steps:"
    echo "1. Update .env file with your configuration"
    echo "2. Run 'make test' to run tests"
    echo "3. Run 'make lint' to check code style"
    echo "4. Run 'make docs' to build documentation"
    echo ""
    
    if [ "$IN_DOCKER" = false ]; then
        echo "To activate the virtual environment in future sessions, run:"
        echo "  source .venv/bin/activate"
    fi
}

# Run main function
main "$@"