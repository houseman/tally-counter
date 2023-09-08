"""Nox configuration."""
import enum
import os

import nox

# Set to True if Nox is running in CI (GitHub Actions)
CI = os.environ.get("CI") is not None

# Supported Python versions
PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11"]


class Tag(str, enum.Enum):
    """Define acceptable tag values."""

    TEST = "test"
    LINT = "lint"


@nox.session(python=PYTHON_VERSIONS, tags=[Tag.TEST])
def pytest(session):
    """Run all unit tests."""
    session.install(".[test]")  # install library and test dependencies
    session.run("python", "-m", "pytest")  # Runs pytest


@nox.session(python=PYTHON_VERSIONS, tags=[Tag.TEST])
def doctest(session):
    """Run doc tests."""
    session.install(".[test]")  # install library and test dependencies
    # Run doctests from the base directory, ignoring unit tests in files matching glob
    # `tests/*.py`
    session.run(
        "python",
        "-m",
        "pytest",
        "--doctest-glob",
        "*.md",
        "--ignore-glob",
        "tests/*.py",
        "--no-cov",
        ".",
    )


@nox.session(python=PYTHON_VERSIONS, tags=[Tag.LINT])
def black(session):
    """Run the black formatter."""
    args = ["black", "."]

    if CI:
        # If running in CI, check only
        args.append("--check")

    session.install("black")
    session.run(*args)


@nox.session(python=PYTHON_VERSIONS, tags=[Tag.LINT])
def ruff(session):
    """Run the ruff linter."""
    args = ["ruff", "check", "."]

    if not CI:
        # If not in CI, fix errors that are fixable
        args.append("--fix")

    session.install("ruff")
    session.run(*args)


@nox.session(python=PYTHON_VERSIONS, tags=[Tag.LINT])
def mypy(session):
    """Run the mypy type checker."""
    args = ["mypy", "."]

    if CI:
        # If running in CI, check only
        args.append("--check")

    session.install("mypy")
    session.run(*args)
