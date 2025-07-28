.PHONY: install install-dev test lint format type-check clean build publish docs

# Variables
PYTHON = python3
PIP = pip3
PACKAGE = athenamist_integration
TESTS = tests/

# Installation
install:
	@echo "Installing package in development mode..."
	$(PIP) install -e .

install-dev: install
	@echo "Installing development dependencies..."
	$(PIP) install -r requirements-test.txt

# Testing
test:
	@echo "Running tests..."
	$(PYTHON) -m pytest -v --cov=$(PACKAGE) --cov-report=term-missing --cov-report=xml $(TESTS)

test-html:
	@echo "Running tests with HTML report..."
	$(PYTHON) -m pytest -v --cov=$(PACKAGE) --cov-report=html $(TESTS)

# Linting and Formatting
lint:
	@echo "Running linters..."
	flake8 $(PACKAGE) $(TESTS)
	mypy $(PACKAGE) $(TESTS)

format:
	@echo "Formatting code..."
	black $(PACKAGE) $(TESTS)
	isort $(PACKAGE) $(TESTS)

# Type Checking
type-check:
	@echo "Running type checking..."
	mypy $(PACKAGE) $(TESTS)

# Cleanup
clean:
	@echo "Cleaning up..."
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -exec rm -rf {} +
	find . -type d -name '.mypy_cache' -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/ *.egg-info/

# Build and Publish
build:
	@echo "Building package..."
	$(PYTHON) -m build

publish-test:
	@echo "Publishing to test PyPI..."
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish:
	@echo "Publishing to PyPI..."
	twine upload dist/*

# Documentation
docs:
	@echo "Building documentation..."
	cd docs && make html

# Development Workflow
dev: install-dev lint test

# CI/CD
ci: lint test
