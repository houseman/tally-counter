# Developer Notes

> **Note**
> The **minimum** required and supported Python version is `3.8`.
> The **maximum** supported Python version is `3.11`

## Development Environment
### Setup

Use `make` targets to automate tasks.

#### Install dependencies

This target uses `pip-tools sync` to install required dependencies.
```shell
make install-deps
```

#### Update dependencies

This target uses `pip-tools compile` to compile requirements, and `sync` to install required dependencies.

```shell
make update-deps
```

### Linting

Run all `pre-commit` hooks (except pytest) in a Python minimum-supported environment

```shell
 make lint
```

Run all `pre-commit` hooks (except pytest) in all supported Python environments

```shell
 make lint-all
```

### Unit Tests

Run all unit tests (including doctests) in a Python minimum-supported environment

```shell
 make test
```

Run all unit tests (including doctests) inn all supported Python environments

```shell
 make test-all
```
