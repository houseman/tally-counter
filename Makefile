TEST_OPTS ?=
NOX_OPTS ?=

# Constants
PIP_COMPILE_ARGS = --upgrade --no-emit-index-url --no-emit-trusted-host --resolver=legacy
SUPPORTED_PYTHON_VERSIONS = 3.8 3.9 3.10 3.11

.PHONY: update-pip pip-compile pip-sync update install update-pre-commit test test-all lint lint-all

## Compile *requirements.txt files from *.in files, using pip-tools
pip-compile:
	@python -m piptools compile --version &> /dev/null || (echo "Installing pip-tools" && python -m pip install --quiet pip-tools)
	CUSTOM_COMPILE_COMMAND="make update" python -m piptools compile  $(PIP_COMPILE_ARGS) --output-file requirements.txt pyproject.toml
	CUSTOM_COMPILE_COMMAND="make update" python -m piptools compile  $(PIP_COMPILE_ARGS) --extra dev --pip-args "--constrain requirements.txt" --output-file dev-requirements.txt pyproject.toml

## Install dependencies from *requirements.txt files into the environment
pip-sync:
	@python -m piptools sync --version &> /dev/null || (echo "Installing pip-tools" && python -m pip install --quiet pip-tools)
	python -m piptools sync requirements.txt dev-requirements.txt
	python -m pip install --no-deps --disable-pip-version-check --quiet --editable .

## Update pre-commit hooks
update-pre-commit:
	@python -m pre_commit --version &> /dev/null || (echo "Installing pre-commit" && python -m pip install --quiet pre-commit)
	python -m pre_commit autoupdate

## Update pip
update-pip:
	python -m pip install --upgrade pip pip-tools

update: update-pip pip-compile pip-sync update-pre-commit ## Update dependencies
install: update-pip pip-sync ## Install dependencies

test: ## Run unit tests
	@python -m nox --version &> /dev/null || (echo "Installing nox" && python -m pip install --quiet nox)
	# @nox --version &> /dev/null || (echo "${RED}Failed: requires nox${RESET}" && exit 1)
	nox --python $(SUPPORTED_PYTHON_VERSIONS) --reuse-existing-virtualenvs --session tests $(NOX_OPTS)

lint: # Run linting
	@python -m nox --version &> /dev/null || (echo "Installing nox" && python -m pip install --quiet nox)
	nox --python $(SUPPORTED_PYTHON_VERSIONS) --reuse-existing-virtualenvs --no-install --session lint $(NOX_OPTS)

help: ## Show this help message
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
