#!/bin/bash

# Linting and formatting script for Modern Python project

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

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Default values
FIX=false
FORMAT=false
CHECK_ONLY=false
WATCH=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --fix|-f)
            FIX=true
            shift
            ;;
        --format)
            FORMAT=true
            shift
            ;;
        --check|-c)
            CHECK_ONLY=true
            shift
            ;;
        --watch|-w)
            WATCH=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  -f, --fix      Auto-fix linting issues"
            echo "  --format       Format code with Ruff"
            echo "  -c, --check    Check only, don't modify files"
            echo "  -w, --watch    Watch for changes and auto-lint"
            echo "  -h, --help     Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check if ruff is available
if ! command -v ruff &> /dev/null; then
    print_error "Ruff not found. Please install it with: uv pip install ruff"
    exit 1
fi

# Function to run linting
run_lint() {
    local exit_code=0
    
    # Run Ruff check
    print_header "Running Ruff Linter"
    
    if [ "$CHECK_ONLY" = true ]; then
        echo "Running in check-only mode..."
        if ruff check . --diff; then
            print_success "No linting issues found"
        else
            print_error "Linting issues found"
            exit_code=1
        fi
    elif [ "$FIX" = true ]; then
        echo "Running with auto-fix..."
        if ruff check . --fix --show-fixes; then
            print_success "Linting completed (issues auto-fixed)"
        else
            print_warning "Some issues could not be auto-fixed"
            exit_code=1
        fi
    else
        if ruff check .; then
            print_success "No linting issues found"
        else
            print_error "Linting issues found (run with --fix to auto-fix)"
            exit_code=1
        fi
    fi
    
    # Run Ruff format
    if [ "$FORMAT" = true ] || [ "$FIX" = true ]; then
        print_header "Running Ruff Formatter"
        
        if [ "$CHECK_ONLY" = true ]; then
            if ruff format --check --diff .; then
                print_success "Code is properly formatted"
            else
                print_error "Code formatting issues found"
                exit_code=1
            fi
        else
            ruff format .
            print_success "Code formatted successfully"
        fi
    fi
    
    # Check import sorting
    print_header "Checking Import Sorting"
    if ruff check . --select I --diff; then
        print_success "Imports are properly sorted"
    else
        if [ "$FIX" = true ]; then
            ruff check . --select I --fix
            print_success "Imports sorted"
        else
            print_warning "Import sorting issues found (run with --fix)"
            exit_code=1
        fi
    fi
    
    # Type checking with mypy (if available)
    if command -v mypy &> /dev/null; then
        print_header "Running Type Checker (mypy)"
        if mypy src --ignore-missing-imports; then
            print_success "No type errors found"
        else
            print_warning "Type errors found"
            # Don't fail on type errors for now
        fi
    fi
    
    # Security check with bandit (if available)
    if command -v bandit &> /dev/null; then
        print_header "Running Security Linter (bandit)"
        if bandit -r src -ll; then
            print_success "No security issues found"
        else
            print_warning "Security issues found"
            # Don't fail on security issues for now
        fi
    fi
    
    return $exit_code
}

# Main execution
if [ "$WATCH" = true ]; then
    print_header "Watching for file changes..."
    echo "Press Ctrl+C to stop"
    
    # Use watchmedo if available, otherwise fall back to simple loop
    if command -v watchmedo &> /dev/null; then
        watchmedo shell-command \
            --patterns="*.py" \
            --recursive \
            --command="$0 --fix" \
            .
    else
        while true; do
            run_lint
            echo -e "\n${YELLOW}Waiting for changes... (Press Ctrl+C to stop)${NC}"
            sleep 5
        done
    fi
else
    # Run linting once
    if run_lint; then
        echo ""
        print_success "All checks passed! ✨"
        exit 0
    else
        echo ""
        print_error "Some checks failed. Please fix the issues."
        exit 1
    fi
fi