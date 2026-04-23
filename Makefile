.PHONY: help install install-dev build build-wheel build-binary clean test lint format dist release

PYTHON := python3
PIP := $(PYTHON) -m pip
VENV_DIR := .venv

help:
	@echo "Netscan - Development Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install          Install in production mode"
	@echo "  make install-dev      Install in development mode with all tools"
	@echo ""
	@echo "Building:"
	@echo "  make build            Build wheel distribution"
	@echo "  make build-binary     Build standalone binary with PyInstaller"
	@echo "  make dist             Create both wheel and binary distributions"
	@echo ""
	@echo "Development:"
	@echo "  make lint             Run code linting and type checking"
	@echo "  make format           Auto-format code with black and isort"
	@echo "  make test             Run tests (if available)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove build artifacts and cache"
	@echo "  make clean-all        Remove everything including virtual environment"

venv:
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created. Activate with: source $(VENV_DIR)/bin/activate"

install:
	$(PIP) install -e .

install-dev: venv
	$(VENV_DIR)/bin/pip install -e ".[dev]"
	$(VENV_DIR)/bin/pip install pyinstaller build twine
	@echo "Development environment ready!"
	@echo "Activate with: source $(VENV_DIR)/bin/activate"

build: clean
	$(PYTHON) -m build --wheel

build-binary: clean
	@echo "Building standalone binary..."
	$(PYTHON) -m PyInstaller netscan.spec
	@echo "Binary created in dist/netscan"

dist: clean
	@echo "Building distributions..."
	$(PYTHON) -m build
	$(PYTHON) -m PyInstaller netscan.spec
	@echo "Distributions ready in dist/"

lint:
	$(PYTHON) -m flake8 netscan/ --max-line-length=88
	$(PYTHON) -m mypy netscan/ || true

format:
	$(PYTHON) -m black netscan/
	$(PYTHON) -m isort netscan/

test:
	@echo "No tests configured yet. Add pytest configuration to run tests."

clean:
	rm -rf build/ dist/ *.egg-info .eggs .pytest_cache .mypy_cache __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

clean-all: clean
	rm -rf $(VENV_DIR)

.DEFAULT_GOAL := help
