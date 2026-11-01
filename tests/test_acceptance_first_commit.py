"""Acceptance tests for the 'make first commit' issue.

Covers:
- AC1: importable package `commander_forge` with `__version__` and `hello()`.
- AC2: at least one collected, passing pytest test (baseline had none).
- AC3: requirements.txt declares pytest; README.md describes project,
  usage and how to run tests.
"""

import re
from pathlib import Path

import commander_forge

REPO_ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------- AC1


def test_ac1_package_is_importable() -> None:
    assert commander_forge.__name__ == "commander_forge"


def test_ac1_has_version_string() -> None:
    version = commander_forge.__version__
    assert isinstance(version, str)
    assert re.match(r"^\d+\.\d+\.\d+", version), version


def test_ac1_hello_is_callable_and_returns_str() -> None:
    assert callable(commander_forge.hello)
    result = commander_forge.hello()
    assert isinstance(result, str)
    assert result.strip() != ""


def test_ac1_package_init_file_exists() -> None:
    init = REPO_ROOT / "commander_forge" / "__init__.py"
    assert init.is_file()


# ---------------------------------------------------------------- AC2


def test_ac2_at_least_one_collected_test_exists() -> None:
    """The repo must contain at least one pytest-discoverable test module."""
    test_files = sorted(
        p for p in REPO_ROOT.glob("tests/test_*.py") if p.name != Path(__file__).name
    )
    assert test_files, "no pytest-discoverable test files under tests/"


def test_ac2_smoke_tests_are_passing() -> None:
    """The baseline smoke tests exist and pass when invoked."""
    from tests import test_smoke

    test_funcs = [name for name in dir(test_smoke) if name.startswith("test_")]
    assert test_funcs, "tests/test_smoke.py collects no test functions"
    for name in test_funcs:
        getattr(test_smoke, name)()


def test_ac2_requirements_declare_pytest() -> None:
    """pytest is installed/declared so `python -m pytest` can run (AC2/AC3)."""
    requirements = (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8")
    assert re.search(r"^pytest\b", requirements, re.MULTILINE)


# ---------------------------------------------------------------- AC3


def test_ac3_readme_describes_project_usage_and_tests() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    lowered = readme.lower()

    # Describes the project (mentions it by name and has a description line).
    assert "commander_forge" in lowered

    # Describes usage.
    assert "usage" in lowered
    assert "hello" in lowered, "README should show how to use hello()"

    # Describes how to run tests, including the documented command.
    assert "test" in lowered
    assert "python -m pytest" in readme, "README should document the test command"
