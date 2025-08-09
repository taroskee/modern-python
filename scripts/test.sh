#!/bin/bash

# Test execution script for Modern Python project

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_header() {
    echo -e "\n${YELLOW}==== $1 ====${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Default values
COVERAGE=false
VERBOSE=false
MARKERS=""
SPECIFIC_TEST=""
PARALLEL=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --coverage|-c)
            COVERAGE=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --marker|-m)
            MARKERS="$2"
            shift 2
            ;;
        --test|-t)
            SPECIFIC_TEST="$2"
            shift 2
            ;;
        --parallel|-p)
            PARALLEL=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  -c, --coverage    Run with coverage report"
            echo "  -v, --verbose     Verbose output"
            echo "  -m, --marker      Run tests with specific marker"
            echo "  -t, --test        Run specific test file or function"
            echo "  -p, --parallel    Run tests in parallel"
            echo "  -h, --help        Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Build pytest command
PYTEST_CMD="pytest"

# Add verbosity
if [ "$VERBOSE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -vv"
else
    PYTEST_CMD="$PYTEST_CMD -v"
fi

# Add coverage
if [ "$COVERAGE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD --cov=src --cov-report=term-missing --cov-report=html --cov-report=xml"
    print_header "Running Tests with Coverage"
else
    print_header "Running Tests"
fi

# Add markers
if [ -n "$MARKERS" ]; then
    PYTEST_CMD="$PYTEST_CMD -m \"$MARKERS\""
    print_header "Running tests with marker: $MARKERS"
fi

# Add specific test
if [ -n "$SPECIFIC_TEST" ]; then
    PYTEST_CMD="$PYTEST_CMD $SPECIFIC_TEST"
    print_header "Running specific test: $SPECIFIC_TEST"
fi

# Add parallel execution
if [ "$PARALLEL" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -n auto"
    print_header "Running tests in parallel"
fi

# Add standard options
PYTEST_CMD="$PYTEST_CMD --tb=short --strict-markers"

# Check if pytest is available
if ! command -v pytest &> /dev/null; then
    print_error "pytest not found. Please install it with: uv pip install pytest"
    exit 1
fi

# Run tests
echo "Executing: $PYTEST_CMD"
echo ""

if eval $PYTEST_CMD; then
    print_success "All tests passed!"
    
    if [ "$COVERAGE" = true ]; then
        echo ""
        print_header "Coverage Report"
        echo "HTML coverage report generated at: htmlcov/index.html"
        echo "XML coverage report generated at: coverage.xml"
        
        # Check coverage threshold
        COVERAGE_PERCENT=$(coverage report | grep TOTAL | awk '{print $4}' | sed 's/%//')
        if [ -n "$COVERAGE_PERCENT" ]; then
            if (( $(echo "$COVERAGE_PERCENT >= 80" | bc -l) )); then
                print_success "Coverage is ${COVERAGE_PERCENT}% (meets 80% threshold)"
            else
                print_error "Coverage is ${COVERAGE_PERCENT}% (below 80% threshold)"
                exit 1
            fi
        fi
    fi
else
    print_error "Tests failed!"
    exit 1
fi