"""Nox configuration."""
import nox

SUPPORTED_PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11"]


@nox.session(python=SUPPORTED_PYTHON_VERSIONS)
def tests(session):
    """Run unit and doc tests."""
    session.install("pip-tools")
    session.run(
        "python",
        "-m",
        "piptools",
        "sync",
        "--quiet",
        "requirements.txt",
        "dev-requirements.txt",
    )
    session.install(".")  # Install this library
    session.run("python", "-m", "pytest")
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
        ".",
    )


@nox.session(python=SUPPORTED_PYTHON_VERSIONS)
def lint(session):
    """Run pre-commit linting."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all", env={"SKIP": "pytest-check"})
