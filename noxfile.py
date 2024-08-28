"""Nox configuration."""

import nox

# Supported Python versions
PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12"]


@nox.session(python=PYTHON_VERSIONS)
def ci(session):
    """Run all CI checks."""
    session.run("make", "install", "ci", external=True)
