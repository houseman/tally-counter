"""Nox configuration."""
import os

import nox

CI = os.environ.get("CI") is not None  # Set to True if running in CI

SUPPORTED_PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11"]


@nox.session(python=SUPPORTED_PYTHON_VERSIONS, tags=["test"])
def pytest(session):
    """Run unit tests."""
    session.install(".[test]")  # install test dependencies
    # session.install(".")  # Install this library
    session.run("python", "-m", "pytest")  # Runs pytest


@nox.session(python=SUPPORTED_PYTHON_VERSIONS, tags=["test"])
def doctest(session):
    """Run doc tests."""
    session.install(".[test]")  # install test dependencies
    session.install(".")  # Install this library
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


@nox.session(python=SUPPORTED_PYTHON_VERSIONS, tags=["lint"])
def ruff(session):
    """Run the ruff linter."""
    args = ["ruff", "check", "."]

    if not CI:
        # If not in CI, fix errors that are fixable
        args.append("--fix")

    session.install("ruff")
    session.run(*args)


@nox.session(python=SUPPORTED_PYTHON_VERSIONS, tags=["lint", "format"])
def black(session):
    """Run the black formatter."""
    args = ["black", "."]

    if CI:
        # If in CI, check only
        args.append("--check")

    session.install("black")
    session.run(*args)


@nox.session(python=SUPPORTED_PYTHON_VERSIONS, tags=["lint", "type"])
def mypy(session):
    """Run the mypy type checker."""
    args = ["mypy", "."]

    if CI:
        # If in CI, check only
        args.append("--check")

    session.install("mypy")
    session.run(*args)
