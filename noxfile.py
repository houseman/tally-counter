import nox


@nox.session(python=["3.8", "3.9", "3.10", "3.11"])
def tests(session):
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
    session.run(
        "python",
        "-m",
        "pytest",
        "--cov",
        "--cov-report=term",
        "--cov-report=html",
        "--cov-report=xml",
        "--no-cov-on-fail",
        "-vv",
    )
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


@nox.session(python="3.8")
def lint(session):
    session.install("pre-commit")
    session.run(
        "pre-commit",
        "run",
        "--all",
    )
