.PHONY: help install install-dev test test-cov lint format type clean run init reset

help:
	@echo "BudgetCLI Development Tasks"
	@echo "============================"
	@echo "make install        Install dependencies"
	@echo "make install-dev    Install development dependencies"
	@echo "make test           Run tests"
	@echo "make test-cov       Run tests with coverage"
	@echo "make lint           Run linters"
	@echo "make format         Format code"
	@echo "make type           Type check"
	@echo "make clean          Clean build artifacts"
	@echo "make run            Run CLI"
	@echo "make init           Initialize database"
	@echo "make reset          Reset database"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest

test-cov:
	pytest --cov=budgetcli --cov-report=html --cov-report=term

lint:
	ruff check budgetcli

format:
	black budgetcli

type:
	mypy budgetcli

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info/
	rm -rf .pytest_cache/ .coverage htmlcov/

run:
	budget

init:
	budget init

reset:
	rm -f ~/.budgetcli/budget.db
	budget init

dev: install-dev format lint type test

all: clean install-dev format lint type test-cov
