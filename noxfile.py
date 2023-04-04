import nox


@nox.session(python=["3.9", "3.10", "3.11"])
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
    session.run("python", "-m", "pytest")


@nox.session(python="3.9")
def lint(session):
    session.install("pre-commit")
    session.run(
        "pre-commit",
        "run",
        "--all",
    )
