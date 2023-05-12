# === COLORS ===
RED     := $(shell tput -Txterm setaf 1)
GREEN   := $(shell tput -Txterm setaf 2)
YELLOW  := $(shell tput -Txterm setaf 3)
BLUE    := $(shell tput -Txterm setaf 4)
PURPLE  := $(shell tput -Txterm setaf 5)
CYAN    := $(shell tput -Txterm setaf 6)
WHITE   := $(shell tput -Txterm setaf 7)
BOLD   	:= $(shell tput -Txterm bold)
RESET   := $(shell tput -Txterm sgr0)

TEST_OPTS ?=
NOX_OPTS ?=
PIP_COMPILE_ARGS = --upgrade --no-emit-index-url --no-emit-trusted-host --resolver=legacy
SUPPORTED_PYTHON_VERSIONS = 3.8 3.9 3.10 3.11
MINIMUM_PYTHON_VERSION = 3.8

## Compile *requirements.txt files from *.in files, using pip-tools
pip-compile:
	@python -m piptools compile --version &> /dev/null || (echo "Installing pip-tools" && python -m pip install --quiet pip-tools)
	CUSTOM_COMPILE_COMMAND="make update-deps" python -m piptools compile  $(PIP_COMPILE_ARGS) --output-file requirements.txt pyproject.toml
	CUSTOM_COMPILE_COMMAND="make update-deps" python -m piptools compile  $(PIP_COMPILE_ARGS) --extra dev --pip-args "--constrain requirements.txt" --output-file dev-requirements.txt pyproject.toml

## Install dependencies and ensure they are synced
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

update-deps: update-pip pip-compile pip-sync update-pre-commit
install-deps: update-pip pip-sync

.PHONY: update-pip pip-compile pip-sync update-deps install-deps update-pre-commit

.PHONY: test test-all
test:
	@nox --version &> /dev/null || (echo "${RED}Failed: requires nox${RESET}" && exit 1)
	@echo "\n${BLUE}TEST >>> Python $(MINIMUM_PYTHON_VERSION)${RESET}"
	nox --python $(MINIMUM_PYTHON_VERSION) --reuse-existing-virtualenvs --session tests $(NOX_OPTS)
	@echo "\n${BLUE}TEST >>> DONE${RESET}"

test-all:
	@nox --version &> /dev/null || (echo "${RED}Failed: requires nox${RESET}" && exit 1)
	@echo "\n${BLUE}TEST >>> Python $(SUPPORTED_PYTHON_VERSIONS)${RESET}"
	nox --python $(SUPPORTED_PYTHON_VERSIONS) --reuse-existing-virtualenvs --session tests $(NOX_OPTS)
	@echo "\n${BLUE}TEST >>> DONE${RESET}"

.PHONY: lint lint-all
lint:
	@nox --version &> /dev/null || (echo "${RED}Failed: requires nox${RESET}" && exit 1)
	@echo "\n${BLUE}LINT >>> Python $(MINIMUM_PYTHON_VERSION)${RESET}"
	nox --python $(MINIMUM_PYTHON_VERSION) --reuse-existing-virtualenvs --no-install --session lint $(NOX_OPTS)
	@echo "\n${BLUE}LINT >>> DONE${RESET}"

lint-all:
	@nox --version &> /dev/null || (echo "${RED}Failed: requires nox${RESET}" && exit 1)
	@echo "\n${BLUE}LINT >>> Python $(SUPPORTED_PYTHON_VERSIONS)${RESET}"
	@nox --python $(SUPPORTED_PYTHON_VERSIONS) --reuse-existing-virtualenvs --no-install --session lint $(NOX_OPTS)
	@echo "\n${BLUE}LINT >>> DONE${RESET}"
