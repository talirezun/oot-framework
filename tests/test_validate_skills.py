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
    assert (
        "Validating 12 SKILL.md files" in result.stdout
    ), f"expected 12 SKILL.md files; got:\n{result.stdout}"
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


# ---------------------------------------------------------------------------
# Fixtures for the Phase 5B validator upgrades.
# ---------------------------------------------------------------------------

HARDENED_SECTIONS = "\n".join(f"## {n}. Section {n}\n\nBody.\n" for n in range(1, 11))


def _write_pack(
    tmp_path,
    folder_name,
    frontmatter,
    *,
    body="",
    with_examples=True,
):
    """Create skills/<folder_name>/SKILL.md and return its Path.

    `frontmatter` is a dict of key -> value (rendered verbatim as `key: value`).
    A one-file examples/ dir is created unless with_examples is False.
    """
    pack_dir = tmp_path / folder_name
    pack_dir.mkdir(parents=True, exist_ok=True)
    if with_examples:
        examples = pack_dir / "examples"
        examples.mkdir(exist_ok=True)
        (examples / "example-1.md").write_text("# Example\n", encoding="utf-8")

    fm_lines = "\n".join(f"{k}: {v}" for k, v in frontmatter.items())
    skill = pack_dir / "SKILL.md"
    skill.write_text(
        f"---\n{fm_lines}\n---\n\n# {folder_name}\n\n{body}\n",
        encoding="utf-8",
    )
    return skill


def _good_hardened_fm(name="good-pack", pack_id="S3"):
    return {
        "name": name,
        "description": "A well-formed hardened pack.",
        "version": "1.0.0",
        "tier": "1",
        "status": "hardened",
        "authors": "Dr. Tali Režun",
        "license": "CC BY-SA 4.0",
        "oot_pack_id": pack_id,
        "oot_tier": "1",
        "oot_status": "hardened",
        "last_updated": "2026-05-08",
    }


def _good_scaffold_fm(name="good-scaffold", pack_id="S9"):
    return {
        "name": name,
        "description": "A well-formed Tier-2 scaffold.",
        "version": "1.0.0",
        "tier": "2",
        "status": "scaffold",
        "authors": "Dr. Tali Režun",
        "license": "CC BY-SA 4.0",
        "oot_pack_id": pack_id,
        "oot_tier": "2",
        "oot_status": "scaffold",
        "last_updated": "2026-05-08",
    }


SCAFFOLD_BODY = (
    "> **Generation marker:** Tier-2 scaffold in v1.0; hardens in v1.x.\n\n"
    "> **TODO (v1.x):** flesh this out.\n"
)


def test_good_hardened_pack_passes(tmp_path):
    """Sanity: a correctly-formed hardened pack produces no errors."""
    validator = _import_validator()
    skill = _write_pack(tmp_path, "good-pack", _good_hardened_fm(), body=HARDENED_SECTIONS)
    assert validator.validate_skill_md(skill) == []


def test_good_scaffold_pack_passes(tmp_path):
    """Sanity: a correctly-formed scaffold pack produces no errors."""
    validator = _import_validator()
    skill = _write_pack(
        tmp_path,
        "good-scaffold",
        _good_scaffold_fm(),
        body=SCAFFOLD_BODY,
        with_examples=False,
    )
    assert validator.validate_skill_md(skill) == []


def test_tier_oot_tier_mismatch_fails(tmp_path):
    """tier and oot_tier disagreement must be flagged."""
    validator = _import_validator()
    fm = _good_hardened_fm()
    fm["oot_tier"] = "2"  # disagrees with tier: 1
    skill = _write_pack(tmp_path, "good-pack", fm, body=HARDENED_SECTIONS)
    joined = "\n".join(validator.validate_skill_md(skill))
    assert "tier" in joined and "oot_tier" in joined and "disagree" in joined


def test_status_oot_status_mismatch_fails(tmp_path):
    """status and oot_status disagreement must be flagged."""
    validator = _import_validator()
    fm = _good_hardened_fm()
    fm["oot_status"] = "scaffold"  # disagrees with status: hardened
    skill = _write_pack(tmp_path, "good-pack", fm, body=HARDENED_SECTIONS)
    joined = "\n".join(validator.validate_skill_md(skill))
    assert "status" in joined and "oot_status" in joined and "disagree" in joined


def test_bad_pack_id_fails(tmp_path):
    """oot_pack_id outside S1-S12 must be flagged."""
    validator = _import_validator()
    fm = _good_hardened_fm(pack_id="S13")
    skill = _write_pack(tmp_path, "good-pack", fm, body=HARDENED_SECTIONS)
    joined = "\n".join(validator.validate_skill_md(skill))
    assert "oot_pack_id must match S<1-12>" in joined


def test_name_folder_mismatch_fails(tmp_path):
    """The `name` field must equal the folder name."""
    validator = _import_validator()
    fm = _good_hardened_fm(name="wrong-name")
    skill = _write_pack(tmp_path, "good-pack", fm, body=HARDENED_SECTIONS)
    joined = "\n".join(validator.validate_skill_md(skill))
    assert "must equal folder name" in joined


def test_future_date_fails(tmp_path):
    """A last_updated in the future must be flagged."""
    import datetime

    validator = _import_validator()
    fm = _good_hardened_fm()
    future = datetime.date.today() + datetime.timedelta(days=365)
    fm["last_updated"] = future.isoformat()
    skill = _write_pack(tmp_path, "good-pack", fm, body=HARDENED_SECTIONS)
    joined = "\n".join(validator.validate_skill_md(skill))
    assert "last_updated is in the future" in joined


def test_hardened_with_todo_fails(tmp_path):
    """A hardened pack containing a TODO marker must be flagged."""
    validator = _import_validator()
    fm = _good_hardened_fm()
    body = HARDENED_SECTIONS + "\n> **TODO (v1.x):** should not be here.\n"
    skill = _write_pack(tmp_path, "good-pack", fm, body=body)
    joined = "\n".join(validator.validate_skill_md(skill))
    assert "must not contain TODO markers" in joined


def test_hardened_without_examples_fails(tmp_path):
    """A hardened pack with no examples/*.md must be flagged."""
    validator = _import_validator()
    fm = _good_hardened_fm()
    skill = _write_pack(tmp_path, "good-pack", fm, body=HARDENED_SECTIONS, with_examples=False)
    joined = "\n".join(validator.validate_skill_md(skill))
    assert "examples/ dir with ≥1 .md file" in joined


def test_scaffold_without_todo_fails(tmp_path):
    """A scaffold with no TODO marker is mislabeled and must be flagged."""
    validator = _import_validator()
    fm = _good_scaffold_fm()
    body = "> **Generation marker:** Tier-2 scaffold in v1.0; hardens in v1.x.\n"
    skill = _write_pack(tmp_path, "good-scaffold", fm, body=body, with_examples=False)
    joined = "\n".join(validator.validate_skill_md(skill))
    assert "scaffold pack must contain ≥1 visible TODO marker" in joined


def test_scaffold_without_generation_marker_fails(tmp_path):
    """A scaffold missing the generation-marker blockquote must be flagged."""
    validator = _import_validator()
    fm = _good_scaffold_fm()
    body = "> **TODO (v1.x):** flesh this out.\n"
    skill = _write_pack(tmp_path, "good-scaffold", fm, body=body, with_examples=False)
    joined = "\n".join(validator.validate_skill_md(skill))
    assert "Generation marker" in joined


def test_pack_id_uniqueness_across_packs(tmp_path):
    """Two packs with the same oot_pack_id must be flagged cross-file."""
    validator = _import_validator()
    s1 = _write_pack(
        tmp_path,
        "pack-a",
        _good_hardened_fm(name="pack-a", pack_id="S3"),
        body=HARDENED_SECTIONS,
    )
    s2 = _write_pack(
        tmp_path,
        "pack-b",
        _good_hardened_fm(name="pack-b", pack_id="S3"),
        body=HARDENED_SECTIONS,
    )
    errors = validator.validate_pack_id_uniqueness([s1, s2])
    assert errors
    assert "duplicate oot_pack_id" in "\n".join(errors)


def test_my_curator_carveout_still_works(tmp_path):
    """my-curator has a reduced key set and no 10-section / examples / TODO rules."""
    validator = _import_validator()
    fm = {
        "name": "my-curator",
        "description": "Imported verbatim from upstream.",
        "oot_pack_id": "S1",
        "oot_tier": "1",
        "oot_status": "hardened",
        "last_updated": "2026-05-15",
    }
    # No 10 sections, no examples dir — must still pass because it's my-curator.
    skill = _write_pack(tmp_path, "my-curator", fm, body="# my-curator\n", with_examples=False)
    assert validator.validate_skill_md(skill) == []
