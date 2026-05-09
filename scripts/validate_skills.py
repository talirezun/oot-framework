#!/usr/bin/env python3
"""
Validate every SKILL.md against the canonical frontmatter schema.

Run from repo root: `python3 scripts/validate_skills.py`.
Exit code 0 if all valid; 1 if any invalid.

Used by .github/workflows/lint-skills.yml.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

REQUIRED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "version",
    "tier",
    "status",
    "authors",
    "license",
    "oot_pack_id",
    "oot_tier",
    "oot_status",
    "last_updated",
}

REQUIRED_SECTIONS_HARDENED = [
    r"^## 1\.\s",   # Purpose
    r"^## 2\.\s",   # When to invoke
    r"^## 3\.\s",   # When NOT to invoke
    r"^## 4\.\s",   # Operational instructions
    r"^## 5\.\s",   # Brain interaction
    r"^## 6\.\s",   # Excel interaction
    r"^## 7\.\s",   # Routine integration
    r"^## 8\.\s",   # Don'ts
    r"^## 9\.\s",   # Quick reference
    r"^## 10\.\s",  # References
]


def parse_frontmatter(content: str) -> dict[str, str] | None:
    """Extract YAML frontmatter as a flat dict (value stays as string)."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not m:
        return None
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def validate_skill_md(path: Path) -> list[str]:
    """Return a list of validation errors; empty list = valid."""
    errors: list[str] = []
    content = path.read_text(encoding="utf-8")

    fm = parse_frontmatter(content)
    if fm is None:
        errors.append(f"{path}: missing or malformed YAML frontmatter")
        return errors

    # my-curator is imported verbatim from upstream; only require ØØT-specific keys.
    is_my_curator = "my-curator" in str(path)
    required_keys = (
        {"name", "description", "oot_pack_id", "oot_tier", "oot_status", "last_updated"}
        if is_my_curator
        else REQUIRED_FRONTMATTER_KEYS
    )

    # Required keys
    for key in required_keys:
        if key not in fm:
            errors.append(f"{path}: frontmatter missing required key `{key}`")

    # tier value (my-curator uses oot_tier; everything else uses tier)
    if not is_my_curator:
        tier = fm.get("tier", "")
        if tier not in {"1", "2"}:
            errors.append(f"{path}: tier must be 1 or 2 (got {tier!r})")

    # status value (my-curator uses oot_status; everything else uses status)
    if not is_my_curator:
        status = fm.get("status", "")
        if status not in {"hardened", "scaffold"}:
            errors.append(f"{path}: status must be 'hardened' or 'scaffold' (got {status!r})")
    else:
        status = fm.get("oot_status", "")

    # last_updated date format
    if "last_updated" in fm:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", fm["last_updated"]):
            errors.append(f"{path}: last_updated must be YYYY-MM-DD (got {fm['last_updated']!r})")

    # Hardened skills: require canonical 10-section structure
    if status == "hardened":
        # Skip my-curator (imported verbatim with different structure)
        if "my-curator" not in str(path):
            for pattern in REQUIRED_SECTIONS_HARDENED:
                if not re.search(pattern, content, re.MULTILINE):
                    errors.append(f"{path}: missing canonical hardened section matching {pattern!r}")

    return errors


def main() -> int:
    skill_files = list(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        print("No SKILL.md files found.", file=sys.stderr)
        return 1

    print(f"Validating {len(skill_files)} SKILL.md files...")
    all_errors: list[str] = []
    for path in sorted(skill_files):
        errors = validate_skill_md(path)
        rel = path.relative_to(REPO_ROOT)
        if errors:
            print(f"  ✗ {rel}")
            for e in errors:
                print(f"      {e}")
            all_errors.extend(errors)
        else:
            print(f"  ✓ {rel}")

    if all_errors:
        print(f"\n{len(all_errors)} validation error(s).")
        return 1
    print("\n✓ All SKILL.md files valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
