# Constants
PIP_ARGS = --upgrade --quiet
override PYTHON_VERSIONS ?= 3.8 3.9 3.10 3.11

.PHONY: .update-pip update install test lint

## Update pip
.update-pip:
	python -m pip install $(PIP_ARGS) pip

update: .update-pip ## Update dependencies
	python -m pip install $(PIP_ARGS) --force-reinstall ".[dev]" ".[test]"
	python -m pip install $(PIP_ARGS) --force-reinstall --editable .

install: .update-pip ## Install dependencies
	python -m pip install $(PIP_ARGS) ".[dev]" ".[test]"
	python -m pip install $(PIP_ARGS) --editable .

test: ## Run unit tests in all supported Python versions
	@python -m nox --version &> /dev/null || (echo "Installing nox" && python -m pip install $(PIP_ARGS) nox)
	nox --python $(PYTHON_VERSIONS) --reuse-existing-virtualenvs --tag test

lint: ## Run linting in all supported Python versions
	@python -m nox --version &> /dev/null || (echo "Installing nox" && python -m pip install $(PIP_ARGS) nox)
	nox --python $(PYTHON_VERSIONS) --reuse-existing-virtualenvs --no-install --tag lint

help: ## Show this help message
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
