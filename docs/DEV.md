# Developer Notes

> **Note**
> The **minimum** required and supported Python version is `3.8`.

## Development Environment
### Setup

Use `make` targets to automate tasks.
```shell
❯ make help
help                 Show this help message
install              Install dependencies
lint                 Run linting in all supported Python versions
nice                 Run linting in local environment
test                 Run unit tests in all supported Python versions
update               Update dependencies
```
#### Install dependencies

This target uses `pip-tools sync` to install required dependencies.
```shell
make install
```

#### Update dependencies

This target uses `pip-tools compile` to compile requirements, and `sync` to install required dependencies.

_Pre-commit hooks are also updated._

> **Important**
> Updated `*requirements.txt` files ***should be added to source control***.

```shell
make update
```

### Linting

Run all `pre-commit` hooks in all supported Python versions

```shell
make lint
```

The above target uses Nox to run linting for all supported Python versions. This can take a vit longer.
For a faster option
```shell
make nice
```
This will run linting in the local virtual environment,

### Unit Tests

Run all unit tests (including doctests) in all supported Python versions (using Nox)

```shell
 make test
```

## Deployment

A GitHub [Action](../.github/workflows/publish.yml) will upload new releases (created in GitHub) to Pypi.
