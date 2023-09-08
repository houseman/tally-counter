# Constants
PIP_ARGS = --upgrade
override PYTHON_VERSIONS ?= 3.8 3.9 3.10 3.11

.PHONY: .update-pip update install test lint

## Update pip
.update-pip:
	@python -m pip install $(PIP_ARGS) pip

update: .update-pip ## Update dependencies
	@python -m pip install $(PIP_ARGS) --force-reinstall --editable ".[dev,test]"

install: .update-pip ## Install dependencies
	@python -m pip install $(PIP_ARGS) --editable ".[dev,test]"

test: ## Run unit tests in all supported Python versions
	@python -m nox --version &> /dev/null || (echo "Installing nox" && python -m pip install $(PIP_ARGS) nox)
	@nox --python $(PYTHON_VERSIONS) --tag test

lint: ## Run linting in all supported Python versions
	@python -m nox --version &> /dev/null || (echo "Installing nox" && python -m pip install $(PIP_ARGS) nox)
	@nox --python $(PYTHON_VERSIONS) --tag lint

help: ## Show this help message
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
