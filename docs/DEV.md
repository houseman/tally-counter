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
test                 Run unit tests
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

> **Note**
> Updated `*requirements.txt` files _should be added to source control_

```shell
make update
```

### Linting

Run all `pre-commit` hooks in all supported Python versions

```shell
 make lint
```

### Unit Tests

Run all unit tests (including doctests) in all supported Python versions

```shell
 make test
```

## Deployment

A GitHub [Action](../.github/workflows/publish.yml) will upload new releases (created in GitHub) to Pypi.
