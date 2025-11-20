"""Tests which assert the repo is formatted and linted correctly.

This does not test UDF functionality, but is for CI of this example
repo.

"""

import subprocess


def test_format() -> None:
    res = subprocess.run(
        [
            "ruff",
            "format",
            "--check",
        ]
    )
    assert res.returncode == 0, "some files not formatted; see stdout for list"


def test_lint() -> None:
    res = subprocess.run(
        [
            "ruff",
            "check",
            "--output-format=concise",
        ]
    )
    assert res.returncode == 0, "some files fail lint checks; see stdout for list"


def test_type_check() -> None:
    res = subprocess.run(
        [
            "mypy",
        ]
    )
    assert res.returncode == 0, "some files fail mypy; see stdout for list"
