# Constants
PIP_ARGS = --upgrade

.PHONY: .update-pip update install test doctest lint ci help

## Update pip
.update-pip:
	@python -m pip install $(PIP_ARGS) pip setuptools uv

update: .update-pip ## Update dependencies in local environment
	@python -m uv pip install $(PIP_ARGS) --force-reinstall --editable ".[dev,test]"

install: ## Install dependencies
	@python -m uv pip install $(PIP_ARGS) --editable ".[dev,test]"

test: doctest ## Run unit tests
	@python -m pytest

doctest: ## Run doc tests
	@python -m pytest --doctest-glob *.md --ignore-glob tests/*.py --no-cov .

lint: ## Run linting
	python -m ruff format $(if $(CI),--check)
	python -m ruff check $(if $(CI),,--fix)
	@python -m mypy

ci: export CI=true
ci: update test doctest lint ## Run all CI checks

help: ## Show this help message
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
