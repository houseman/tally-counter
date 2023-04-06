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

pip-compile:
	@python -m piptools compile --version &> /dev/null || (echo "Installing pip-tools" && python -m pip install --quiet pip-tools)
	CUSTOM_COMPILE_COMMAND="make update-deps" python -m piptools compile  $(PIP_COMPILE_ARGS) --output-file requirements.txt pyproject.toml
	CUSTOM_COMPILE_COMMAND="make update-deps" python -m piptools compile  $(PIP_COMPILE_ARGS) --extra dev --pip-args "--constrain requirements.txt" --output-file dev-requirements.txt pyproject.toml

## Install dependencies and ensure they are synced
pip-sync:
	@python -m piptools sync --version &> /dev/null || (echo "Installing pip-tools" && python -m pip install --quiet pip-tools)
	python -m piptools sync requirements.txt dev-requirements.txt
	python -m pip install --no-deps --disable-pip-version-check --quiet --editable .

update-deps: pip-compile pip-sync
install-deps: pip-sync

.PHONY: pip-compile pip-sync update-deps install-deps

.PHONY: test
test:
	@nox --version &> /dev/null || (echo "${RED}Failed: requires nox${RESET}" && exit 1)
	@echo "\n${BLUE}Test in Python 3.8${RESET}"
	nox --python 3.8 --reuse-existing-virtualenvs --session tests $(NOX_OPTS)

test-py-sup:
	@nox --version &> /dev/null || (echo "${RED}Failed: requires nox${RESET}" && exit 1)
	@echo "\n${BLUE}Test in all supported Python versions${RESET}"
	nox --python 3.8 3.9 3.10 3.11 --reuse-existing-virtualenvs --session tests $(NOX_OPTS)

.PHONY: lint
lint:
	@nox --version &> /dev/null || (echo "${RED}Failed: requires nox${RESET}" && exit 1)
	@echo "\n${BLUE}Run nox${RESET}"
	nox --python 3.8 --reuse-existing-virtualenvs --no-install --session lint $(NOX_OPTS)
	@echo "\n${BLUE}Done nox${RESET}"
