# Makefile for xblock-image

.PHONY: help clean requirements test quality lint install upgrade

help: ## Display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

clean: ## Remove generated files
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -rf {} + || true
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/

requirements: ## Install requirements for development
	pip install -qr requirements/pip-tools.in
	pip-compile requirements/base.in
	pip-compile requirements/dev.in
	pip-compile requirements/quality.in
	pip install -qr requirements/dev.txt

install: ## Install the package in development mode
	pip install -e .

test: ## Run tests
	pytest

coverage: ## Run tests with coverage
	pytest --cov=image --cov-report=html --cov-report=term

quality: ## Run quality checks
	pylint image/
	pycodestyle image/
	pydocstyle image/
	bandit -r image/

lint: quality ## Alias for quality

upgrade: ## Update requirements to latest versions
	pip install -qr requirements/pip-tools.in
	pip-compile --upgrade requirements/base.in
	pip-compile --upgrade requirements/dev.in  
	pip-compile --upgrade requirements/quality.in

build: ## Build the package
	python setup.py sdist bdist_wheel

publish: build ## Publish to PyPI
	twine upload dist/*

dev-install: requirements install ## Full development setup
