#!/bin/bash

# Build script for Modern Python project

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}==== $1 ====${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Default values
CLEAN=false
DOCS=false
DIST=false
DOCKER=false
ALL=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --clean|-c)
            CLEAN=true
            shift
            ;;
        --docs|-d)
            DOCS=true
            shift
            ;;
        --dist)
            DIST=true
            shift
            ;;
        --docker)
            DOCKER=true
            shift
            ;;
        --all|-a)
            ALL=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  -c, --clean    Clean build artifacts"
            echo "  -d, --docs     Build documentation"
            echo "  --dist         Build distribution packages"
            echo "  --docker       Build Docker images"
            echo "  -a, --all      Build everything"
            echo "  -h, --help     Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# If --all is specified, enable all options
if [ "$ALL" = true ]; then
    CLEAN=true
    DOCS=true
    DIST=true
    DOCKER=true
fi

# Clean build artifacts
if [ "$CLEAN" = true ]; then
    print_header "Cleaning Build Artifacts"
    
    # Remove Python artifacts
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type f -name "*.pyo" -delete 2>/dev/null || true
    find . -type f -name "*.pyd" -delete 2>/dev/null || true
    find . -type f -name ".coverage" -delete 2>/dev/null || true
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "*.egg" -exec rm -rf {} + 2>/dev/null || true
    
    # Remove build directories
    rm -rf build/ dist/ htmlcov/ .pytest_cache/ .ruff_cache/ .mypy_cache/
    rm -rf docs/_build/ docs/api/
    
    print_success "Build artifacts cleaned"
fi

# Run linting and tests
print_header "Running Quality Checks"

# Lint check
print_info "Running linter..."
if bash scripts/lint.sh --check; then
    print_success "Linting passed"
else
    print_error "Linting failed"
    exit 1
fi

# Run tests
print_info "Running tests..."
if bash scripts/test.sh; then
    print_success "Tests passed"
else
    print_error "Tests failed"
    exit 1
fi

# Build documentation
if [ "$DOCS" = true ]; then
    print_header "Building Documentation"
    
    if [ -f "docs/Makefile" ]; then
        cd docs
        make clean
        make html
        cd ..
        print_success "Documentation built at docs/_build/html/index.html"
        
        # Check for broken links
        if command -v sphinx-build &> /dev/null; then
            print_info "Checking for broken links..."
            cd docs && make linkcheck && cd ..
        fi
    else
        print_error "Documentation configuration not found"
        exit 1
    fi
fi

# Build distribution packages
if [ "$DIST" = true ]; then
    print_header "Building Distribution Packages"
    
    # Check for build tools
    if ! command -v python -m build &> /dev/null; then
        print_info "Installing build tools..."
        uv pip install build wheel
    fi
    
    # Build wheel and sdist
    print_info "Building wheel and source distribution..."
    python -m build
    
    # List created packages
    echo "Created packages:"
    ls -la dist/
    
    print_success "Distribution packages built in dist/"
    
    # Validate packages
    if command -v twine &> /dev/null; then
        print_info "Validating packages..."
        twine check dist/*
        print_success "Package validation passed"
    fi
fi

# Build Docker images
if [ "$DOCKER" = true ]; then
    print_header "Building Docker Images"
    
    if [ -f ".devcontainer/docker-compose.yml" ]; then
        print_info "Building development container..."
        docker-compose -f .devcontainer/docker-compose.yml build
        print_success "Docker development image built"
        
        # Tag image with version
        VERSION=$(python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])")
        docker tag modern-python-dev:latest modern-python-dev:$VERSION
        print_success "Tagged image as modern-python-dev:$VERSION"
    else
        print_error "Docker configuration not found"
        exit 1
    fi
    
    # Build production image if Dockerfile exists
    if [ -f "Dockerfile" ]; then
        print_info "Building production image..."
        docker build -t modern-python:latest .
        print_success "Production Docker image built"
    fi
fi

# Summary
print_header "Build Summary"
echo "Build completed successfully!"
echo ""
echo "Artifacts created:"
[ "$DOCS" = true ] && echo "  - Documentation: docs/_build/html/"
[ "$DIST" = true ] && echo "  - Distribution packages: dist/"
[ "$DOCKER" = true ] && echo "  - Docker images: modern-python-dev:latest"
echo ""

# Next steps
echo "Next steps:"
[ "$DOCS" = true ] && echo "  - View docs: python -m http.server --directory docs/_build/html 8000"
[ "$DIST" = true ] && echo "  - Upload to PyPI: twine upload dist/*"
[ "$DOCKER" = true ] && echo "  - Run container: docker-compose -f .devcontainer/docker-compose.yml up"

print_success "All build tasks completed! 🚀"