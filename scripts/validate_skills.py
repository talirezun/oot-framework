#!/usr/bin/env python3
"""
Validate every SKILL.md against the canonical frontmatter schema.

Run from repo root: `python3 scripts/validate_skills.py`.
Exit code 0 if all valid; 1 if any invalid.

Used by .github/workflows/lint-skills.yml.

Checks performed (per file unless noted):
  - Required frontmatter keys present (my-curator has a reduced set — it is
    imported verbatim from upstream and only carries the ØØT-specific keys).
  - `tier` in {1,2}; `status` in {hardened, scaffold}.
  - `tier` == `oot_tier` and `status` == `oot_status` (the duplicated keys can
    silently diverge — this catches that).
  - `name` field == folder name.
  - `oot_pack_id` matches `S<1-12>` and is unique across all packs (cross-file).
  - `last_updated` is a valid YYYY-MM-DD date and is not in the future.
  - Hardened packs (excluding my-curator): the canonical 10-section structure;
    an `examples/` dir with ≥1 `.md` file; ZERO TODO markers.
  - Scaffold packs: ≥1 visible TODO marker (an all-TODO-less scaffold is
    mislabeled) and the generation-marker blockquote.
"""
from __future__ import annotations

import datetime
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
    r"^## 1\.\s",  # Purpose
    r"^## 2\.\s",  # When to invoke
    r"^## 3\.\s",  # When NOT to invoke
    r"^## 4\.\s",  # Operational instructions
    r"^## 5\.\s",  # Brain interaction
    r"^## 6\.\s",  # Excel interaction
    r"^## 7\.\s",  # Routine integration
    r"^## 8\.\s",  # Don'ts
    r"^## 9\.\s",  # Quick reference
    r"^## 10\.\s",  # References
]

# TODO markers the framework uses to flag unfinished scaffold content.
# `<!-- TODO` = HTML-comment marker; `> **TODO` = blockquote marker.
TODO_PATTERNS = [r"<!--\s*TODO", r">\s*\*\*TODO"]

# The scaffold generation-marker blockquote (grep S7 for the exact shape).
GENERATION_MARKER_PATTERN = r">\s*\*\*Generation marker:\*\*"

PACK_ID_PATTERN = re.compile(r"^S([1-9]|1[0-2])$")


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


def _has_todo(content: str) -> bool:
    return any(re.search(p, content) for p in TODO_PATTERNS)


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

    # tier/oot_tier and status/oot_status agreement (the duplicated keys can
    # silently diverge). my-curator has no plain `tier`/`status`, so skip there.
    if not is_my_curator:
        if "tier" in fm and "oot_tier" in fm and fm["tier"] != fm["oot_tier"]:
            errors.append(
                f"{path}: tier ({fm['tier']!r}) and oot_tier ({fm['oot_tier']!r}) disagree"
            )
        if "status" in fm and "oot_status" in fm and fm["status"] != fm["oot_status"]:
            errors.append(
                f"{path}: status ({fm['status']!r}) and oot_status ({fm['oot_status']!r}) disagree"
            )

    # name field must equal the folder name (my-curator carries `name`; others too).
    folder = path.parent.name
    if "name" in fm and fm["name"] != folder:
        errors.append(f"{path}: name ({fm['name']!r}) must equal folder name ({folder!r})")

    # oot_pack_id must match S<1-12>.
    pack_id = fm.get("oot_pack_id", "")
    if pack_id and not PACK_ID_PATTERN.match(pack_id):
        errors.append(f"{path}: oot_pack_id must match S<1-12> (got {pack_id!r})")

    # last_updated date format + not-in-the-future.
    if "last_updated" in fm:
        raw = fm["last_updated"]
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", raw):
            errors.append(f"{path}: last_updated must be YYYY-MM-DD (got {raw!r})")
        else:
            try:
                when = datetime.date.fromisoformat(raw)
                if when > datetime.date.today():
                    errors.append(f"{path}: last_updated is in the future ({raw})")
            except ValueError:
                errors.append(f"{path}: last_updated is not a valid date ({raw})")

    # Hardened skills: canonical 10-section structure + examples dir + zero TODOs.
    if status == "hardened":
        # Skip my-curator (imported verbatim with different structure/content).
        if not is_my_curator:
            for pattern in REQUIRED_SECTIONS_HARDENED:
                if not re.search(pattern, content, re.MULTILINE):
                    errors.append(
                        f"{path}: missing canonical hardened section matching {pattern!r}"
                    )

            examples_dir = path.parent / "examples"
            example_mds = list(examples_dir.glob("*.md")) if examples_dir.is_dir() else []
            if not example_mds:
                errors.append(f"{path}: hardened pack must have an examples/ dir with ≥1 .md file")

            if _has_todo(content):
                errors.append(
                    f"{path}: hardened pack must not contain TODO markers "
                    f"(found `<!-- TODO` or `> **TODO`)"
                )

    # Scaffold skills: must carry ≥1 visible TODO marker (a TODO-less scaffold is
    # mislabeled) and the generation-marker blockquote.
    if status == "scaffold":
        if not _has_todo(content):
            errors.append(
                f"{path}: scaffold pack must contain ≥1 visible TODO marker "
                f"(declared unfinished but has none — mislabeled?)"
            )
        if not re.search(GENERATION_MARKER_PATTERN, content):
            errors.append(
                f"{path}: scaffold pack must carry the `> **Generation marker:**` blockquote"
            )

    return errors


def validate_pack_id_uniqueness(skill_files: list[Path]) -> list[str]:
    """Cross-file check: every oot_pack_id must be unique."""
    errors: list[str] = []
    seen: dict[str, Path] = {}
    for path in skill_files:
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not fm:
            continue
        pack_id = fm.get("oot_pack_id", "")
        if not pack_id:
            continue
        if pack_id in seen:
            errors.append(
                f"{path}: duplicate oot_pack_id {pack_id!r} " f"(also in {seen[pack_id]})"
            )
        else:
            seen[pack_id] = path
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

    # Cross-file: pack-id uniqueness.
    uniqueness_errors = validate_pack_id_uniqueness(sorted(skill_files))
    if uniqueness_errors:
        print("  ✗ cross-file pack-id uniqueness")
        for e in uniqueness_errors:
            print(f"      {e}")
        all_errors.extend(uniqueness_errors)

    if all_errors:
        print(f"\n{len(all_errors)} validation error(s).")
        return 1
    print("\n✓ All SKILL.md files valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
