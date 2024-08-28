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
test                 Run unit tests in all supported Python versions
update               Update dependencies
```
#### Install dependencies

To install required dependencies:
```shell
make install
```

#### Update dependencies

To update required dependencies:

```shell
make update
```

### Linting

Run linting tools:

```shell
make lint
```

### Unit Tests

Run unit tests (includes running doc tests):

```shell
make test
```

### Pre-commit hooks
To make use of the `pre0commit` hooks, run
```shell
pre-commit install
```
To update these hooks
```shell
pre-commit autoupdate
```

> **Important**
> Please commit updated `.pre-commit-config.yaml` files to your branch.

## Deployment

A GitHub [Action](../.github/workflows/publish.yml) will upload new releases to Pypi on merge to "main".
