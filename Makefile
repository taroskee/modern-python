# Modern Python Project Makefile
# Provides convenient commands for development tasks

.PHONY: help
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Environment setup
.PHONY: setup
setup: ## Set up development environment
	@echo "Setting up development environment..."
	@bash scripts/setup.sh

.PHONY: install
install: ## Install project dependencies
	@echo "Installing dependencies..."
	@uv pip install -e ".[dev,test,docs]"

.PHONY: install-dev
install-dev: ## Install development dependencies only
	@echo "Installing development dependencies..."
	@uv pip install -e ".[dev]"

.PHONY: update
update: ## Update all dependencies
	@echo "Updating dependencies..."
	@uv pip install --upgrade -e ".[dev,test,docs]"

# Code quality
.PHONY: lint
lint: ## Run linter (Ruff)
	@echo "Running linter..."
	@bash scripts/lint.sh

.PHONY: lint-fix
lint-fix: ## Run linter with auto-fix
	@echo "Running linter with auto-fix..."
	@bash scripts/lint.sh --fix

.PHONY: format
format: ## Format code with Ruff
	@echo "Formatting code..."
	@ruff format .

.PHONY: format-check
format-check: ## Check code formatting
	@echo "Checking code format..."
	@ruff format --check .

.PHONY: type
type: ## Run type checker (Pyright)
	@echo "Running type checker..."
	@pyright src

.PHONY: security
security: ## Run security checks
	@echo "Running security checks..."
	@bandit -r src -ll
	@safety check

# Testing
.PHONY: test
test: ## Run all tests
	@echo "Running tests..."
	@bash scripts/test.sh

.PHONY: test-verbose
test-verbose: ## Run tests with verbose output
	@echo "Running tests (verbose)..."
	@bash scripts/test.sh --verbose

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	@echo "Running tests with coverage..."
	@bash scripts/test.sh --coverage

.PHONY: test-unit
test-unit: ## Run unit tests only
	@echo "Running unit tests..."
	@pytest tests -m unit -v

.PHONY: test-integration
test-integration: ## Run integration tests only
	@echo "Running integration tests..."
	@pytest tests -m integration -v

.PHONY: test-watch
test-watch: ## Run tests in watch mode
	@echo "Running tests in watch mode..."
	@ptw -- -v

# Documentation
.PHONY: docs
docs: ## Build documentation
	@echo "Building documentation..."
	@cd docs && make clean && make html

.PHONY: docs-serve
docs-serve: docs ## Build and serve documentation
	@echo "Serving documentation at http://localhost:8000"
	@cd docs/_build/html && python -m http.server 8000

.PHONY: docs-watch
docs-watch: ## Watch and rebuild documentation
	@echo "Watching documentation..."
	@cd docs && sphinx-autobuild . _build/html --port 8888

.PHONY: docs-test
docs-test: ## Test documentation examples
	@echo "Testing documentation..."
	@cd docs && make doctest

.PHONY: docs-coverage
docs-coverage: ## Check documentation coverage
	@echo "Checking documentation coverage..."
	@cd docs && make coverage

# Building
.PHONY: build
build: clean lint test ## Build project
	@echo "Building project..."
	@bash scripts/build.sh --dist

.PHONY: build-all
build-all: ## Build everything (dist, docs, docker)
	@echo "Building everything..."
	@bash scripts/build.sh --all

.PHONY: dist
dist: ## Build distribution packages
	@echo "Building distribution packages..."
	@python -m build

.PHONY: docker
docker: ## Build Docker image
	@echo "Building Docker image..."
	@docker-compose -f .devcontainer/docker-compose.yml build

.PHONY: docker-up
docker-up: ## Start Docker containers
	@echo "Starting Docker containers..."
	@docker-compose -f .devcontainer/docker-compose.yml up -d

.PHONY: docker-down
docker-down: ## Stop Docker containers
	@echo "Stopping Docker containers..."
	@docker-compose -f .devcontainer/docker-compose.yml down

.PHONY: docker-shell
docker-shell: ## Open shell in Docker container
	@echo "Opening shell in Docker container..."
	@docker-compose -f .devcontainer/docker-compose.yml exec dev bash

# Cleaning
.PHONY: clean
clean: ## Clean build artifacts
	@echo "Cleaning build artifacts..."
	@rm -rf build/ dist/ *.egg-info
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete
	@find . -type f -name ".coverage" -delete
	@find . -type d -name "*.egg" -exec rm -rf {} + 2>/dev/null || true

.PHONY: clean-test
clean-test: ## Clean test artifacts
	@echo "Cleaning test artifacts..."
	@rm -rf .pytest_cache/ htmlcov/ .coverage coverage.xml
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

.PHONY: clean-docs
clean-docs: ## Clean documentation build
	@echo "Cleaning documentation..."
	@cd docs && make clean

.PHONY: clean-all
clean-all: clean clean-test clean-docs ## Clean all artifacts
	@echo "Cleaning all artifacts..."
	@rm -rf .ruff_cache/ .mypy_cache/

# Git hooks
.PHONY: pre-commit
pre-commit: ## Install pre-commit hooks
	@echo "Installing pre-commit hooks..."
	@pre-commit install

.PHONY: pre-commit-run
pre-commit-run: ## Run pre-commit on all files
	@echo "Running pre-commit..."
	@pre-commit run --all-files

# GitHub Actions
.PHONY: ci-status
ci-status: ## Check GitHub Actions CI status
	@echo "Recent GitHub Actions workflow runs:"
	@gh run list --limit 5

.PHONY: ci-view
ci-view: ## View latest CI run details
	@echo "Latest CI run details:"
	@gh run view

.PHONY: ci-watch
ci-watch: ## Watch current CI run
	@gh run watch

.PHONY: workflow-list
workflow-list: ## List all workflows
	@echo "Available workflows:"
	@gh workflow list

.PHONY: pr-status
pr-status: ## Check pull request status
	@echo "Pull request status:"
	@gh pr status

# Development workflow
.PHONY: dev
dev: install lint test ## Run development workflow
	@echo "Development workflow complete!"

.PHONY: check
check: lint format-check type test ## Run all checks
	@echo "All checks passed!"

.PHONY: fix
fix: lint-fix format ## Fix linting and formatting issues
	@echo "Fixed linting and formatting issues!"

.PHONY: ci
ci: clean check build ## Run CI workflow
	@echo "CI workflow complete!"

# Release
.PHONY: version
version: ## Show current version
	@python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])"

.PHONY: bump-patch
bump-patch: ## Bump patch version
	@echo "Bumping patch version..."
	@bump2version patch

.PHONY: bump-minor
bump-minor: ## Bump minor version
	@echo "Bumping minor version..."
	@bump2version minor

.PHONY: bump-major
bump-major: ## Bump major version
	@echo "Bumping major version..."
	@bump2version major

.PHONY: release
release: clean check build ## Prepare release
	@echo "Preparing release..."
	@echo "Don't forget to:"
	@echo "  1. Update CHANGELOG.md"
	@echo "  2. Commit changes"
	@echo "  3. Create git tag"
	@echo "  4. Push to repository"

# Utilities
.PHONY: shell
shell: ## Open Python shell
	@ipython

.PHONY: jupyter
jupyter: ## Start Jupyter Lab
	@echo "Starting Jupyter Lab..."
	@jupyter lab --no-browser --port=8888

.PHONY: tree
tree: ## Show project structure
	@tree -I '__pycache__|*.pyc|.git|.pytest_cache|.ruff_cache|.mypy_cache|htmlcov|*.egg-info|build|dist|.venv|venv|node_modules' -a

.PHONY: count
count: ## Count lines of code
	@echo "Counting lines of code..."
	@find . -name "*.py" -not -path "./.venv/*" -not -path "./venv/*" | xargs wc -l

.PHONY: todo
todo: ## Show TODO items in code
	@echo "TODO items:"
	@grep -r "TODO" --include="*.py" --exclude-dir=".venv" --exclude-dir="venv" .

# Default target
.DEFAULT_GOAL := help