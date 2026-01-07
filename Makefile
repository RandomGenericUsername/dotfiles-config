.PHONY: help install install-dev shell clean test test-unit test-integration test-cov

VENV := .venv
PYTHON := $(VENV)/bin/python
CONFIG := $(VENV)/bin/config
SHELL_NAME := $(shell basename $$SHELL)

help:
	@echo "Available targets:"
	@echo "  install        - Create venv and install dependencies"
	@echo "  install-dev    - Install with dev dependencies (pytest)"
	@echo "  shell          - Start a new shell with venv activated"
	@echo "  clean          - Remove venv and build artifacts"
	@echo "  test           - Run pytest tests"
	@echo "  test-unit      - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-cov       - Run tests with coverage report"

install:
	uv venv
	uv pip install -e .

install-dev:
	uv venv
	uv pip install -e ".[dev]"

shell:
	@echo "Starting new shell with venv activated..."
	@echo "Type 'exit' to return to your previous shell"
	@echo ""
	@. $(VENV)/bin/activate && exec $(SHELL_NAME)

clean:
	rm -rf $(VENV)
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test:
	uv run pytest -v

test-unit:
	uv run pytest -v tests/unit/

test-integration:
	uv run pytest -v tests/integration/

test-cov:
	uv run pytest -v --cov=src --cov-report=term-missing
