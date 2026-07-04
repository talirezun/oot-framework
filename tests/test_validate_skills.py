"""Tests for scripts/validate_skills.py.

Two guarantees:
  1. The real tree passes (all 12 SKILL.md files valid).
  2. The validator actually FAILS on bad frontmatter (it is not a no-op).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATOR = REPO_ROOT / "scripts" / "validate_skills.py"


def test_real_tree_passes_12_of_12():
    """The committed skills/ tree must validate cleanly (exit 0, 12 files)."""
    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"validate_skills.py failed on the real tree:\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    # Sanity: the validator reports how many files it validated.
    assert "Validating 12 SKILL.md files" in result.stdout, (
        f"expected 12 SKILL.md files; got:\n{result.stdout}"
    )
    assert "All SKILL.md files valid" in result.stdout


def _import_validator():
    """Import validate_skills as a module for direct-function tests."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("validate_skills", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_bad_frontmatter_is_rejected(tmp_path):
    """A SKILL.md missing required keys / with a bad tier must produce errors."""
    validator = _import_validator()

    bad = tmp_path / "SKILL.md"
    bad.write_text(
        "---\n"
        "name: broken-pack\n"
        "description: missing most required keys and an invalid tier\n"
        "tier: 9\n"
        "status: nonsense\n"
        "last_updated: not-a-date\n"
        "---\n\n"
        "# Broken\n",
        encoding="utf-8",
    )

    errors = validator.validate_skill_md(bad)
    assert errors, "validator returned no errors for clearly-broken frontmatter"

    joined = "\n".join(errors)
    # Missing required keys are flagged.
    assert "missing required key" in joined
    # Invalid tier is flagged.
    assert "tier must be 1 or 2" in joined
    # Invalid status is flagged.
    assert "status must be" in joined
    # Bad date format is flagged.
    assert "last_updated must be YYYY-MM-DD" in joined


def test_missing_frontmatter_is_rejected(tmp_path):
    """A file with no YAML frontmatter at all must be rejected."""
    validator = _import_validator()

    bad = tmp_path / "SKILL.md"
    bad.write_text("# No frontmatter here\n\nJust a heading.\n", encoding="utf-8")

    errors = validator.validate_skill_md(bad)
    assert errors
    assert "missing or malformed YAML frontmatter" in "\n".join(errors)
