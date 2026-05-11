#!/usr/bin/env python3
"""ØØT Installer Wizard v1.1.0 — terminal-based, guided install.

Entry point: `python3 installer/wizard.py` or `oot-wizard` (after `pip install -e .`).

Path B of the install-path overhaul. For founders who explicitly avoid using a
coding agent (Path A) but want a guided form rather than the manual docs (Path C).
Mirrors the 14-step structure of `installer/agent-assisted/cloud-install-plan.md`.

Flags:
  --resume     Resume from the first incomplete step in ~/.oot/wizard-state.yaml.
  --dry-run    Walk through prompts without executing any consequential action.
  --track {cloud,privacy}   Skip the track-selection prompt.

State file: ~/.oot/wizard-state.yaml (separate from the agent plans' install-state.yaml
to avoid confusion when a founder switches paths mid-install).

Design philosophy:
- Programmatic where safe (tool detection, folder creation, git scaffolding,
  GPG key generation, file edits).
- Web-UI walkthrough where the user must approve a third-party action
  (GitHub repo creation, branch protection, GPG public-key upload, MCP
  installation in Claude Desktop).
- Resume-friendly: every step that completes writes its outcome to the state
  file. --resume picks up at the first non-`done` step.
- Honest about constraints: if the wizard can't do something, it tells the
  user exactly what to do manually and waits for confirmation.

Author: ØØT framework / Claude Code (Opus 4.7) co-authored 2026-05-10.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# ----- soft imports (degrade gracefully if optional deps missing) -----------

try:
    import yaml  # pyyaml
except ImportError:
    yaml = None  # type: ignore[assignment]

try:
    import questionary  # type: ignore[import-untyped]
    _HAS_QUESTIONARY = True
except ImportError:
    _HAS_QUESTIONARY = False

try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.table import Table
    _HAS_RICH = True
    _CONSOLE = Console()
except ImportError:
    _HAS_RICH = False
    _CONSOLE = None  # type: ignore[assignment]


# ----- constants ------------------------------------------------------------

WIZARD_VERSION = "1.1.0"
OOT_HOME = Path(os.environ.get("OOT_HOME", Path.home() / ".oot"))
STATE_FILE = OOT_HOME / "wizard-state.yaml"
VENV_DIR = OOT_HOME / "venv"

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_EXCEL = REPO_ROOT / "templates" / "excel"

# Python version fallback chain — try strictest first, accept ≥3.11
PYTHON_CANDIDATES = ["python3.13", "python3.12", "python3.11", "python3"]


# ----- helpers --------------------------------------------------------------

def header(text: str, level: int = 1) -> None:
    """Print a section header, styled if rich is available."""
    if _HAS_RICH:
        if level == 1:
            _CONSOLE.print(Panel(text, style="bold cyan", padding=(0, 2)))
        else:
            _CONSOLE.print(f"\n[bold]{'─' * 4} {text} {'─' * 4}[/bold]\n")
    else:
        bar = "=" * 70 if level == 1 else "-" * 50
        print(f"\n{bar}\n{text}\n{bar}\n")


def info(text: str) -> None:
    if _HAS_RICH:
        _CONSOLE.print(text)
    else:
        print(text)


def warn(text: str) -> None:
    if _HAS_RICH:
        _CONSOLE.print(f"[yellow]⚠[/yellow]  {text}")
    else:
        print(f"⚠ {text}")


def err(text: str) -> None:
    if _HAS_RICH:
        _CONSOLE.print(f"[red]✗[/red] {text}")
    else:
        print(f"✗ {text}", file=sys.stderr)


def ok(text: str) -> None:
    if _HAS_RICH:
        _CONSOLE.print(f"[green]✓[/green] {text}")
    else:
        print(f"✓ {text}")


def ask_text(prompt: str, default: Optional[str] = None) -> str:
    if _HAS_QUESTIONARY:
        return questionary.text(prompt, default=default or "").ask() or (default or "")
    suffix = f" [{default}]" if default else ""
    answer = input(f"{prompt}{suffix}: ").strip()
    return answer or (default or "")


def ask_confirm(prompt: str, default: bool = True) -> bool:
    if _HAS_QUESTIONARY:
        return bool(questionary.confirm(prompt, default=default).ask())
    suffix = "[Y/n]" if default else "[y/N]"
    answer = input(f"{prompt} {suffix} ").strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


def ask_select(prompt: str, choices: list[str], default: Optional[str] = None) -> str:
    if _HAS_QUESTIONARY:
        return questionary.select(prompt, choices=choices, default=default).ask()
    info(prompt)
    for i, c in enumerate(choices, 1):
        info(f"  {i}. {c}")
    while True:
        a = input(f"Pick 1-{len(choices)}{f' (default {choices.index(default)+1})' if default and default in choices else ''}: ").strip()
        if not a and default:
            return default
        try:
            idx = int(a) - 1
            if 0 <= idx < len(choices):
                return choices[idx]
        except ValueError:
            pass
        warn(f"Invalid selection: {a!r}")


def ask_checkbox(prompt: str, choices: list[tuple[str, str, bool]]) -> list[str]:
    """Multi-select. Each choice is (key, label, preselected).

    Returns the list of keys the user kept selected.
    """
    if _HAS_QUESTIONARY:
        q_choices = [
            questionary.Choice(title=label, value=key, checked=preselected)
            for key, label, preselected in choices
        ]
        result = questionary.checkbox(prompt, choices=q_choices).ask()
        return result if result is not None else [k for k, _, p in choices if p]
    info(prompt)
    info("  (Enter the numbers to toggle, comma-separated. Press Enter to accept defaults.)")
    selected = {k for k, _, p in choices if p}
    for i, (key, label, preselected) in enumerate(choices, 1):
        marker = "[x]" if key in selected else "[ ]"
        info(f"  {i}. {marker} {label}")
    raw = input("Toggle (e.g. 2,4) or Enter to confirm: ").strip()
    if raw:
        for tok in raw.split(","):
            try:
                idx = int(tok.strip()) - 1
                if 0 <= idx < len(choices):
                    k = choices[idx][0]
                    selected.discard(k) if k in selected else selected.add(k)
            except ValueError:
                pass
    return [k for k, _, _ in choices if k in selected]


def ask_path(prompt: str, default: Optional[str] = None, must_exist: bool = False) -> Path:
    while True:
        raw = ask_text(prompt, default=default)
        path = Path(raw).expanduser().resolve()
        if must_exist and not path.exists():
            warn(f"Path does not exist: {path}. Try again.")
            continue
        return path


def run(cmd: list[str], dry_run: bool = False, capture: bool = False, check: bool = False) -> tuple[int, str]:
    """Run a shell command. Returns (returncode, stdout). On dry-run, prints and returns (0, '')."""
    cmd_str = " ".join(cmd)
    if dry_run:
        info(f"  [dim](dry-run)[/dim] {cmd_str}" if _HAS_RICH else f"  (dry-run) {cmd_str}")
        return 0, ""
    info(f"  $ {cmd_str}")
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            check=check,
        )
        return result.returncode, (result.stdout or "")
    except subprocess.CalledProcessError as e:
        err(f"Command failed (exit {e.returncode}): {cmd_str}")
        if e.stderr:
            err(e.stderr.strip())
        return e.returncode, (e.stdout or "")
    except FileNotFoundError:
        err(f"Command not found: {cmd[0]}")
        return 127, ""


def which(cmd: str) -> Optional[str]:
    return shutil.which(cmd)


# ----- detection of existing installs ---------------------------------------

def detect_existing_modules(state: dict[str, Any]) -> dict[str, Any]:
    """Probe the machine for components the framework cares about.

    Returns a dict that downstream steps and the module-selection UI consult so
    we never propose to install something the user already has.
    """
    found: dict[str, Any] = {}

    # Claude Desktop (macOS-only check; Linux/Windows just records 'unknown').
    macos_app = Path("/Applications/Claude.app")
    found["claude_desktop"] = {"present": macos_app.exists(), "path": str(macos_app) if macos_app.exists() else None}

    # Claude Code CLI.
    claude_cli = which("claude")
    found["claude_cli"] = {"present": bool(claude_cli), "path": claude_cli}

    # The Curator (cross-check Step 3 plus probe filesystem).
    loc = state.get("locations", {})
    curator_vault = loc.get("curator_vault")
    has_existing = loc.get("existing_curator")
    curator_app = Path("/Applications/The Curator.app")
    if not curator_app.exists():
        curator_app = Path("/Applications/Curator.app")  # fallback name guess
    found["curator"] = {
        "app_present": curator_app.exists(),
        "app_path": str(curator_app) if curator_app.exists() else None,
        "vault_known": bool(curator_vault) and Path(curator_vault).exists() if curator_vault else False,
        "vault_path": curator_vault,
        "user_said_existing": bool(has_existing),
    }

    # Signing key (gpg).
    rc, out = run(["gpg", "--list-secret-keys", "--keyid-format=long"], capture=True, check=False)
    sec_keys = [ln.strip() for ln in out.splitlines() if ln.strip().startswith("sec ")] if rc == 0 else []
    found["gpg_signing_key"] = {"present": bool(sec_keys), "count": len(sec_keys), "lines": sec_keys[:3]}

    # Global git identity.
    rc, email = run(["git", "config", "--global", "user.email"], capture=True, check=False)
    rc2, name = run(["git", "config", "--global", "user.name"], capture=True, check=False)
    found["git_identity"] = {
        "email": email.strip() if rc == 0 else None,
        "name": name.strip() if rc2 == 0 else None,
        "configured": rc == 0 and rc2 == 0 and bool(email.strip()) and bool(name.strip()),
    }

    # GitHub CLI auth.
    if which("gh"):
        rc, _ = run(["gh", "auth", "status"], capture=True, check=False)
        found["gh_auth"] = {"installed": True, "authenticated": rc == 0}
    else:
        found["gh_auth"] = {"installed": False, "authenticated": False}

    # Bitwarden CLI.
    bw = which("bw")
    found["bitwarden_cli"] = {"present": bool(bw), "path": bw}

    # Node.js (needed for Curator's MCP server + many Skills' tooling).
    rc, ver = run(["node", "--version"], capture=True, check=False) if which("node") else (1, "")
    found["node"] = {"present": rc == 0, "version": ver.strip()}

    state["detected"] = found
    return found


def render_detection_report(found: dict[str, Any]) -> None:
    """Pretty-print what we found on the user's machine."""
    info("\nWhat we found already installed on your machine:\n")
    rows = [
        ("Claude Desktop",     found["claude_desktop"]["present"],   found["claude_desktop"].get("path") or "—"),
        ("Claude Code CLI",    found["claude_cli"]["present"],       found["claude_cli"].get("path") or "—"),
        ("The Curator app",    found["curator"]["app_present"] or found["curator"]["user_said_existing"],
                                                                     found["curator"].get("app_path") or (found["curator"].get("vault_path") or "—")),
        ("GPG signing key",    found["gpg_signing_key"]["present"],
                                                                     f"{found['gpg_signing_key']['count']} key(s)" if found['gpg_signing_key']['count'] else "—"),
        ("Git identity",       found["git_identity"]["configured"],  f"{found['git_identity'].get('name') or '?'} <{found['git_identity'].get('email') or '?'}>"),
        ("GitHub CLI (gh)",    found["gh_auth"]["installed"] and found["gh_auth"]["authenticated"],
                                                                     "authenticated" if found["gh_auth"]["authenticated"] else ("installed" if found["gh_auth"]["installed"] else "—")),
        ("Bitwarden CLI",      found["bitwarden_cli"]["present"],    found["bitwarden_cli"].get("path") or "—"),
        ("Node.js",            found["node"]["present"],             found["node"].get("version") or "—"),
    ]
    for label, present, detail in rows:
        mark = "✓" if present else "·"
        if _HAS_RICH:
            colour = "green" if present else "dim"
            _CONSOLE.print(f"  [{colour}]{mark}[/{colour}] {label:<22} [dim]{detail}[/dim]")
        else:
            print(f"  {mark} {label:<22} {detail}")
    info("")


# ----- state file -----------------------------------------------------------

def load_state() -> dict[str, Any]:
    if not STATE_FILE.exists() or yaml is None:
        return {}
    try:
        with STATE_FILE.open() as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        warn(f"Could not parse state file at {STATE_FILE}: {e}. Starting fresh.")
        return {}


def save_state(state: dict[str, Any]) -> None:
    if yaml is None:
        warn("pyyaml not installed; state file not persisted. Run `pip install pyyaml` to enable resumability.")
        return
    OOT_HOME.mkdir(parents=True, exist_ok=True)
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    with STATE_FILE.open("w") as f:
        yaml.safe_dump(state, f, default_flow_style=False, sort_keys=False)


def mark_step_done(state: dict[str, Any], step_key: str, outcome: str = "done") -> None:
    state.setdefault("steps_completed", {})[step_key] = outcome
    save_state(state)


def is_step_done(state: dict[str, Any], step_key: str) -> bool:
    return state.get("steps_completed", {}).get(step_key) == "done"


# ----- the 14 steps ---------------------------------------------------------

def step_00_welcome(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_00_welcome"):
        return
    header("ØØT — Organisation of Tomorrow — Installer Wizard")
    info(f"\nWizard version: {WIZARD_VERSION}\n")
    launched_via_bootstrap = os.environ.get("OOT_BOOTSTRAP_LAUNCHED") == "1"
    if launched_via_bootstrap:
        info(
            "Welcome — the bootstrap is done. The framework is at\n"
            f"  {REPO_ROOT}\n"
            "and the Python environment is at\n"
            f"  {VENV_DIR}\n\n"
            "From here, this wizard asks you ~15 questions and walks you through every\n"
            "click and copy-paste. Expect ~2-4 hours total (mostly waiting on you to\n"
            "open browser tabs and approve things). You can quit anytime — re-run the\n"
            "same bootstrap command to resume where you left off.\n\n"
            "What you'll need within reach:\n"
            "  - A web browser (GitHub, Anthropic, Google Cloud).\n"
            "  - 20 minutes of reading. Open these in browser tabs now if you can:\n"
            "      MANIFESTO.md            (15 min — the framework's intellectual core)\n"
            "      docs/MODULES.md         (10 min — what you're installing, in plain English)\n"
            "      governance/KLARNA-TEST.md (10 min — the signature discipline)\n"
        )
    else:
        info(
            "This wizard guides you through installing the ØØT framework end-to-end.\n"
            "Resumable: re-run with --resume to pick up where you left off.\n"
            "Dry-run: --dry-run shows what would happen without doing it.\n\n"
            "Read these first if you haven't:\n"
            "  - MANIFESTO.md (15 min) — the framework's intellectual core.\n"
            "  - docs/MODULES.md (10 min) — what to install and what's optional.\n"
            "  - governance/KLARNA-TEST.md (10 min) — the signature discipline.\n\n"
            "If you have a coding agent (Claude Code, Augment Code, Aider, OpenCode,\n"
            "Cline, etc.), the agent-assisted path at installer/agent-assisted/ is\n"
            "faster (~60-90 min wall-clock) and recommended. This wizard is for\n"
            "founders who explicitly prefer a guided form over an agent.\n\n"
            "Tip: for a true one-line install on a fresh machine, run instead:\n"
            "  curl -fsSL https://raw.githubusercontent.com/talirezun/oot-framework/main/installer/bootstrap.sh | bash\n"
        )
    if not ask_confirm("Continue with the wizard?", default=True):
        info("Aborting.")
        sys.exit(0)
    mark_step_done(state, "step_00_welcome")


def step_01_preflight(state: dict[str, Any], dry_run: bool) -> str:
    """Returns the absolute path of the Python interpreter to use."""
    header("Step 1 / 14 — Preflight: required tools", level=2)

    info("Checking required CLI tools...\n")
    found_python = None
    for cand in PYTHON_CANDIDATES:
        path = which(cand)
        if path:
            rc, out = run([cand, "--version"], dry_run=False, capture=True)
            if rc == 0:
                ok(f"{cand}: {out.strip()} ({path})")
                if not found_python:
                    found_python = path
                    state["oot_python"] = path
        else:
            info(f"  not found: {cand}")
    if not found_python:
        err("No Python ≥3.11 found. Install Python 3.13 from https://www.python.org/downloads/ "
            "or via Homebrew on macOS: brew install python@3.13")
        sys.exit(1)

    required = {"git": "version control", "curl": "HTTP client", "gpg": "signed commits", "node": "MCP runtime"}
    missing = []
    for tool, desc in required.items():
        path = which(tool)
        if path:
            rc, out = run([tool, "--version"], dry_run=False, capture=True)
            ok(f"{tool}: {out.strip().splitlines()[0]}")
        else:
            err(f"{tool}: NOT FOUND ({desc})")
            missing.append(tool)

    if missing:
        warn(f"\nMissing required tools: {missing}")
        info("Install on macOS:\n  brew install " + " ".join(t for t in missing if t in {"gpg": 1, "node": 1}.keys() or t in ["git", "curl"]))
        info("Install on Debian/Ubuntu:\n  sudo apt install " + " ".join("gnupg" if t == "gpg" else "nodejs" if t == "node" else t for t in missing))
        if ask_confirm("Install missing tools and re-run wizard?", default=True):
            sys.exit(0)
        warn("Continuing without missing tools — some steps will fail.")

    state.setdefault("preflight", {})["python"] = found_python
    state["preflight"]["tools_present"] = {t: bool(which(t)) for t in required}
    state["preflight"]["optional"] = {t: bool(which(t)) for t in ("gh", "jq", "yq")}
    mark_step_done(state, "step_01_preflight")
    return found_python


def step_02_python_venv(state: dict[str, Any], dry_run: bool, oot_python: str) -> None:
    if is_step_done(state, "step_02_python_venv"):
        return
    header("Step 2 / 14 — Python virtual environment", level=2)
    info(
        "Setting up a Python venv at ~/.oot/venv for the framework's dependencies.\n"
        "Homebrew Python 3.13 enforces PEP 668 — pip install --user is rejected,\n"
        "so we use a venv to isolate the framework's deps from your system Python.\n"
    )
    if not VENV_DIR.exists():
        run([oot_python, "-m", "venv", str(VENV_DIR)], dry_run=dry_run, check=True)
    venv_pip = VENV_DIR / "bin" / "pip"
    if not dry_run and venv_pip.exists():
        run([str(venv_pip), "install", "openpyxl", "pyyaml", "httpx", "questionary", "rich"],
            dry_run=False, capture=False, check=False)
    state["venv_path"] = str(VENV_DIR)
    ok(f"venv ready at {VENV_DIR}")
    mark_step_done(state, "step_02_python_venv")


def step_03_locations(state: dict[str, Any], dry_run: bool) -> dict[str, str]:
    if is_step_done(state, "step_03_locations"):
        return state.get("locations", {})
    header("Step 3 / 14 — Choose locations", level=2)

    info("Three folder questions: where the firm's operational stuff lives, where your\n"
         "knowledge graph (Curator) lives, and how the two relate.\n")

    firm_slug_default = ask_text("Firm slug (lowercase-hyphenated, e.g. 'acme-studio')",
                                  default=None)
    if not firm_slug_default:
        warn("Firm slug is required.")
        sys.exit(1)
    firm_folder_default = str(Path.home() / firm_slug_default)
    firm_folder = ask_path(
        f"Firm operational repo folder", default=firm_folder_default
    )

    has_curator = ask_confirm(
        "Do you already have the Curator desktop app installed with a populated second-brain?",
        default=False,
    )
    curator_vault = None
    curator_config = "B"
    if has_curator:
        # Try to auto-detect
        guesses = [
            Path.home() / "second-brain",
            Path.home() / "Documents" / "second-brain",
        ]
        found = next((g for g in guesses if g.exists()), None)
        cv_default = str(found) if found else str(Path.home() / "second-brain")
        curator_vault = ask_path("Curator vault folder path", default=cv_default, must_exist=True)
        curator_config = ask_select(
            "Curator integration mode (see docs/MODULES.md for the trade-off):",
            choices=[
                "A — Separate vault and firm repo (recommended for existing Curator users)",
                "B — Unified: firm repo IS the Curator vault (recommended for greenfield)",
            ],
            default="A — Separate vault and firm repo (recommended for existing Curator users)",
        )[0]  # take first char "A" or "B"
    else:
        curator_vault = firm_folder  # Configuration B by default for greenfield
        info("No existing Curator detected — defaulting to Configuration B (firm folder = Curator vault root).")

    curator_domain = ask_text(
        "Curator domain slug for this firm",
        default=firm_slug_default,
    )

    locations = {
        "framework_repo": str(REPO_ROOT),
        "firm_slug": firm_slug_default,
        "firm_folder": str(firm_folder),
        "curator_vault": str(curator_vault) if curator_vault else "",
        "curator_domain": curator_domain,
        "curator_config": curator_config,
        "existing_curator": has_curator,
    }
    state["locations"] = locations
    mark_step_done(state, "step_03_locations")
    return locations


def step_04_firm_profile(state: dict[str, Any], dry_run: bool) -> dict[str, Any]:
    if is_step_done(state, "step_04_firm_profile"):
        return state.get("firm_profile", {})
    header("Step 4 / 14 — Firm profile", level=2)

    profile = {}
    profile["name"] = ask_text("Firm full name (e.g. 'Acme Studio')")
    profile["partner_count_estimate"] = ask_select(
        "Partner count over next 12 months:",
        choices=["solo", "small (2-5)", "medium (5-10)", "large (10+)"],
        default="solo",
    )
    profile["jurisdictions"] = ask_text(
        "Jurisdictions (ISO 2-letter codes, comma-separated, e.g. 'SI,HR')",
        default="",
    )
    profile["eu_high_risk"] = ask_select(
        "EU AI Act high-risk Annex III exposure (employment / essential services / biometrics):",
        choices=["yes", "no", "not-sure"],
        default="not-sure",
    )
    profile["klarna_gate_choice"] = ask_select(
        "Configure Klarna gate today, or defer until first AI-replaces-human PR?",
        choices=["now", "later"],
        default="later",
    )
    profile["track"] = state.get("firm_profile", {}).get("track", "cloud")
    state["firm_profile"] = profile
    mark_step_done(state, "step_04_firm_profile")
    return profile


def step_05_module_selection(state: dict[str, Any], dry_run: bool) -> dict[str, Any]:
    if is_step_done(state, "step_05_module_selection"):
        return state.get("modules_chosen", {})
    header("Step 5 / 14 — Module selection (choose what to install)", level=2)

    profile = state.get("firm_profile", {})
    eu = profile.get("eu_high_risk") in {"yes", "not-sure"}
    klarna_now = profile.get("klarna_gate_choice") == "now"
    big_firm = profile.get("partner_count_estimate", "").startswith(("medium", "large"))

    # First: probe the machine and tell the user what we found.
    found = detect_existing_modules(state)
    render_detection_report(found)

    info(
        "Now pick the modules. Defaults are pre-checked based on your firm profile.\n"
        "Anything already detected above will be REUSED — not reinstalled.\n"
        "Use Space to toggle, Enter to confirm.\n"
    )

    # ----- Foundation (essentially required to have any working framework) ---
    info("─" * 60)
    info("FOUNDATION — the minimum to have any working ØØT install")
    info("─" * 60)
    foundation_choices: list[tuple[str, str, bool]] = [
        ("github_brain_repo",   "GitHub Brain repo (your firm's operational data)",   True),
        ("signing_key",         "GPG signing key for signed commits "
                                + ("(found one already — will reuse)" if found["gpg_signing_key"]["present"]
                                   else "(will create a new one)"),                    True),
        ("my_curator_mcp",      "my-curator MCP wired into Claude Desktop",            True),
        ("spreadsheet_app",     "Spreadsheet viewer (Excel / Numbers / LibreOffice / Sheets)", True),
    ]
    foundation = ask_checkbox("Foundation modules:", foundation_choices)
    if not all(m in foundation for m in ("github_brain_repo", "my_curator_mcp")):
        warn("You opted out of GitHub Brain repo and/or my-curator MCP. The framework will not work without these.")
        if not ask_confirm("Continue anyway (advanced — you'll need to wire equivalents yourself)?", default=False):
            info("Aborting. Re-run to start fresh.")
            sys.exit(0)

    # ----- The Curator app (3 options) --------------------------------------
    info("\n" + "─" * 60)
    info("THE CURATOR — second-brain desktop app (essential for the Brain)")
    info("─" * 60)
    if found["curator"]["user_said_existing"] or found["curator"]["app_present"]:
        curator_default = "use-existing"
        info("Existing Curator detected — defaulting to use-existing.")
    else:
        curator_default = "install-fresh"
    curator_choice = ask_select(
        "How should we handle the Curator app?",
        choices=[
            "use-existing      (reuse the Curator you already have)",
            "install-fresh     (run Curator's one-line installer in Step 11)",
            "skip-for-now      (install later yourself — most steps will still work, but R5 won't)",
        ],
        default={
            "use-existing":   "use-existing      (reuse the Curator you already have)",
            "install-fresh":  "install-fresh     (run Curator's one-line installer in Step 11)",
        }[curator_default],
    )
    curator_mode = curator_choice.split()[0]  # 'use-existing' / 'install-fresh' / 'skip-for-now'

    # ----- Skill packs ------------------------------------------------------
    info("\n" + "─" * 60)
    info("SKILL PACKS — domain knowledge bundles your Routines + agents use")
    info("─" * 60)
    info("Tier-1 packs are production-ready. Tier-2 packs (S7-S11) ship as scaffolds in v1.0\n"
         "and will be hardened in v1.x — you can install them now and they'll auto-update.\n")
    skill_choices: list[tuple[str, str, bool]] = [
        ("S1",  "S1  my-curator (Brain operations)",            True),
        ("S2",  "S2  context-engineering",                       True),
        ("S3",  "S3  compensation-attribution (variable pay)",   True),
        ("S4",  "S4  code-qa",                                   klarna_now or True),
        ("S5",  "S5  reporting-business-review",                 True),
        ("S6",  "S6  change-management",                         klarna_now or True),
        ("S12", "S12 privacy-self-sovereign",                    profile.get("track") == "privacy"),
        ("S7",  "S7  governance-compliance (Tier-2 scaffold)",   eu),
        ("S8",  "S8  legal-operations (Tier-2 scaffold)",        big_firm),
        ("S9",  "S9  marketing (Tier-2 scaffold)",               False),
        ("S10", "S10 finance-treasury (Tier-2 scaffold)",        big_firm),
        ("S11", "S11 sales-bd (Tier-2 scaffold)",                False),
    ]
    skills = ask_checkbox("Skill packs to install:", skill_choices)

    # ----- Routines ---------------------------------------------------------
    info("\n" + "─" * 60)
    info("ROUTINES — Anthropic Claude Code Routines that run on schedule")
    info("─" * 60)
    info("Day-1 capable: R5, R6, R7. Others need partner data first (we'll set them up later).\n")
    routine_choices: list[tuple[str, str, bool]] = [
        ("R5", "R5 Brain Health Check (Sunday 09:00) — recommended for every firm",     True),
        ("R6", "R6 EU AI Act Audit Trail (daily 23:00) — recommended for any firm with EU exposure",
                                                                                          eu or True),
        ("R7", "R7 Klarna Test gate (PR webhook) — only if you're configuring Klarna now",
                                                                                          klarna_now),
        ("R1", "R1 Daily Output Capture — deferred until first partner onboarded",       False),
        ("R2", "R2 Weekly BR Prep — deferred until R1 has ≥7 days of data",              False),
        ("R3", "R3 Partner Acknowledgement Polling — deferred to month-1",               False),
        ("R4", "R4 Monthly Compensation Calc — deferred to month-1",                     False),
        ("R8", "R8 Quarterly Sentiment Sweep — deferred to quarter-1",                   False),
    ]
    routines = ask_checkbox("Routines to configure now:", routine_choices)

    # ----- Optional security ------------------------------------------------
    info("\n" + "─" * 60)
    info("OPTIONAL SECURITY — recommended-but-optional in Gen 1")
    info("─" * 60)
    sec_choices: list[tuple[str, str, bool]] = [
        ("branch_protection", "GitHub branch protection on main "
                              + ("(enforced — Team plan)" if profile.get("github_plan_tier") == "team"
                                 else "(advisory only on Free — but still worth setting)"),
                                                                                          True),
        ("bitwarden",          "Bitwarden password manager + CLI"
                              + (" (CLI already installed)" if found["bitwarden_cli"]["present"] else ""),
                                                                                          found["bitwarden_cli"]["present"]),
        ("yubikey",            "Yubikey for org-admin 2FA (recommended with ≥2 admins)",  big_firm),
        ("trezor",             "Trezor for crypto-key storage (Gen-2 — not used in v1.0)", False),
    ]
    security = ask_checkbox("Optional security modules:", sec_choices)

    # ----- Render the plan + ask to confirm ---------------------------------
    modules: dict[str, Any] = {
        "foundation":      foundation,
        "curator_mode":    curator_mode,   # 'use-existing' | 'install-fresh' | 'skip-for-now'
        "skills":          skills,
        "routines":        routines,
        "security":        security,
        # Convenience flags downstream steps consult:
        "install_curator": curator_mode == "install-fresh",
        "skip_curator":    curator_mode == "skip-for-now",
        "use_existing_curator": curator_mode == "use-existing",
        "install_signing_key": "signing_key" in foundation and not found["gpg_signing_key"]["present"],
        "install_branch_protection": "branch_protection" in security,
    }
    state["modules_chosen"] = modules

    info("\n" + "─" * 60)
    info("YOUR PLAN")
    info("─" * 60)
    info(f"  Foundation:   {', '.join(foundation) or '(none)'}")
    info(f"  Curator:      {curator_mode}")
    info(f"  Skill packs:  {', '.join(skills) or '(none)'}")
    info(f"  Routines now: {', '.join(routines) or '(none)'}")
    info(f"  Security:     {', '.join(security) or '(none)'}")
    info("")
    if not ask_confirm("Proceed with this plan?", default=True):
        info("Re-run the wizard to adjust your selections (it'll skip earlier steps).")
        sys.exit(0)
    mark_step_done(state, "step_05_module_selection")
    return modules


def step_06_github_plan_tier(state: dict[str, Any], dry_run: bool) -> str:
    if is_step_done(state, "step_06_github_plan_tier"):
        return state.get("firm_profile", {}).get("github_plan_tier", "free")
    header("Step 6 / 14 — GitHub plan-tier choice (CRITICAL)", level=2)
    info(
        "GitHub Free private repos do NOT enforce branch protection rules.\n"
        "The rule shows in the UI but it's advisory only. This affects whether\n"
        "R6's audit-trail-immutability claim actually holds for your firm.\n\n"
        "Three valid configurations (per ADR-001-cloud-routine-excel-writeback):\n"
        "  team   — GitHub Team plan ($4/user/month). Branch protection enforced.\n"
        "           RECOMMENDED DEFAULT for any firm taking R6 seriously.\n"
        "  public — Free, but firm operational data is publicly visible to anyone.\n"
        "           Workable only for fully-open-source orgs.\n"
        "  free   — GitHub Free + private. Branch protection advisory only.\n"
        "           Acceptable for solo / 2-person v1 pilot only.\n"
    )
    choice = ask_select(
        "GitHub plan tier:",
        choices=["team", "public", "free"],
        default="free",
    )
    state.setdefault("firm_profile", {})["github_plan_tier"] = choice
    if choice == "free":
        warn("Branch protection will be advisory only. Plan to upgrade to Team within 90 days "
             "or before adding a third committer, whichever comes first.")
    elif choice == "team":
        info("If not yet on Team: upgrade at https://github.com/settings/billing/plans before continuing.")
        if not ask_confirm("Confirm you have GitHub Team active (or will upgrade now)?", default=True):
            warn("Continuing — you can come back to this step.")
    mark_step_done(state, "step_06_github_plan_tier")
    return choice


def step_07_anthropic_check(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_07_anthropic_check"):
        return
    header("Step 7 / 14 — Anthropic check", level=2)

    macos_app = Path("/Applications/Claude.app")
    if macos_app.exists():
        ok("Claude Desktop installed (macOS)")
    else:
        warn("Claude Desktop not found at /Applications/Claude.app")
        info("Download: https://claude.com/download")
        if not ask_confirm("Install Claude Desktop, sign in, then continue?", default=True):
            warn("Skipping. R5/R6/R1/R2 configuration will need Claude Desktop.")

    if which("claude"):
        ok(f"Claude Code CLI: {which('claude')}")
    else:
        warn("Claude Code CLI not found. Install per https://docs.claude.com/en/docs/claude-code")
        info("(Optional — you can configure Routines via the web dashboard at https://claude.ai/code/routines instead. Routines run on Anthropic's cloud either way; CLI is just one of three management interfaces.)")

    plan = ask_select(
        "Anthropic plan tier:",
        choices=["pro", "max", "team", "enterprise"],
        default="pro",
    )
    state.setdefault("firm_profile", {})["anthropic_plan"] = plan
    profile = state["firm_profile"]
    if plan == "pro" and (profile.get("partner_count_estimate", "").startswith("medium")
                          or profile.get("klarna_gate_choice") == "now"):
        warn("Pro plan caps Routines at 5/day. With your firm size + Klarna gate, "
             "you'll exceed that. Strongly recommend Max plan.")
    mark_step_done(state, "step_07_anthropic_check")


def step_08_brain_repo(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_08_brain_repo"):
        return
    header("Step 8 / 14 — Create the Brain GitHub repo", level=2)
    locations = state["locations"]
    profile = state["firm_profile"]
    firm_slug = locations["firm_slug"]
    firm_folder = Path(locations["firm_folder"])

    info(
        f"Step 1 of 5 — Create the empty repo on github.com (web UI):\n\n"
        f"  1. Open https://github.com/new in your browser.\n"
        f"  2. Repository name: {firm_slug}-brain\n"
        f"  3. Description: ØØT Brain repo for {profile['name']}\n"
        f"  4. Visibility: Private (or Public if you chose 'public' at Step 6)\n"
        f"  5. Initialize: leave all three checkboxes UNCHECKED (no README, no .gitignore, no licence)\n"
        f"  6. Click Create repository.\n"
    )
    if not ask_confirm("Repo created on GitHub.com?", default=True):
        info("Pausing. Re-run with --resume after the repo is created.")
        sys.exit(0)
    repo_url = ask_text(
        "Repo HTTPS URL (e.g. https://github.com/<you>/<repo>.git)",
        default=f"https://github.com/<you>/{firm_slug}-brain.git",
    )
    state["brain_repo_url"] = repo_url

    info("\nStep 2 of 5 — Local folder + git init")
    if not firm_folder.exists():
        firm_folder.mkdir(parents=True)
        ok(f"Created {firm_folder}")
    elif (firm_folder / ".git").exists():
        warn(f"{firm_folder} already has a .git directory; skipping init.")
    if not (firm_folder / ".git").exists():
        run(["git", "init", "-b", "main"], dry_run=dry_run, check=False)
        os.chdir(firm_folder)
        run(["git", "init", "-b", "main"], dry_run=dry_run, check=False)

    os.chdir(firm_folder)
    info("\nStep 3 of 5 — Email matching for signed commits")
    info("GitHub marks commits Verified only if the commit-author email matches the GPG key UID.\n"
         "Use a real email here; we'll match the GPG key to it at Step 9.")
    email = ask_text("Email for commit authorship in this repo", default="")
    name = ask_text("Name for commit authorship", default=profile.get("name", ""))
    state.setdefault("brain_repo_email", email)
    if email and not dry_run:
        run(["git", "config", "--local", "user.email", email], dry_run=False)
        run(["git", "config", "--local", "user.name", name], dry_run=False)
    if not dry_run:
        run(["git", "remote", "add", "origin", repo_url], dry_run=False, check=False)

    info("\nStep 4 of 5 — Scaffold firm/ folder + copy Excel templates")
    subfolders = ["excel", "output-logs", "audit-logs", "business-reviews",
                  "klarna-tests", "compensation", "brain-health", "partners"]
    for sub in subfolders:
        (firm_folder / "firm" / sub).mkdir(parents=True, exist_ok=True)
        if sub != "excel":
            gitkeep = firm_folder / "firm" / sub / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.touch()
    # Copy Excel templates
    excel_dst = firm_folder / "firm" / "excel"
    if not dry_run:
        for xlsx in TEMPLATES_EXCEL.glob("*.xlsx"):
            shutil.copy2(xlsx, excel_dst / xlsx.name)
        ok(f"Copied {len(list(excel_dst.glob('*.xlsx')))} .xlsx templates to firm/excel/")

    # README at repo root
    readme = firm_folder / "README.md"
    if not readme.exists():
        readme_text = (
            f"# {profile['name']} — operational Brain repo\n\n"
            f"ØØT framework cloud-track install. Holds the firm's `.xlsx` "
            f"operational state (`firm/excel/`) and Routine-written markdown "
            f"(`firm/output-logs/`, `firm/audit-logs/`, etc.). Mutated by "
            f"Routines via openpyxl + signed commits per "
            f"[ADR-001](https://github.com/talirezun/oot-framework/blob/main/docs/internal/ADR-001-cloud-routine-excel-writeback.md).\n\n"
            f"Curator integration: Configuration {locations['curator_config']}.\n\n"
            f"Created: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}.\n"
        )
        if not dry_run:
            readme.write_text(readme_text)
            ok(f"Wrote README at {readme}")

    info("\nStep 5 of 5 — Initial commit + push")
    info("This first commit will be UNSIGNED. The signing key gets generated at Step 9.")
    if ask_confirm("Stage everything and commit?", default=True):
        run(["git", "add", "."], dry_run=dry_run, check=False)
        run(["git", "commit", "-m",
             "scaffold: initial Brain folder + Excel templates from framework v1.0.0"],
            dry_run=dry_run, check=False)
        if ask_confirm("Push to origin/main now? (Will prompt for GitHub credentials if not cached.)", default=True):
            run(["git", "push", "-u", "origin", "main"], dry_run=dry_run, check=False)

    mark_step_done(state, "step_08_brain_repo")


def step_09_signing_key(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_09_signing_key"):
        return
    header("Step 9 / 14 — Generate signing key + upload to GitHub", level=2)

    modules = state.get("modules_chosen", {})
    if "signing_key" not in modules.get("foundation", []):
        info("Signing key opted out at Step 5. Skipping.")
        mark_step_done(state, "step_09_signing_key")
        return
    if not modules.get("install_signing_key", True):
        info("Existing GPG signing key detected at Step 5 — skipping key generation.")
        info("If you want to use a *different* key, run: gpg --gen-key, then re-run wizard from Step 9.\n"
             "We'll still configure git to sign with your existing key. Listing your keys now:")
        run(["gpg", "--list-secret-keys", "--keyid-format=long"], capture=False, check=False)
        existing_key = ask_text("Paste the key ID (the long hex after 'sec rsa4096/' or 'sec ed25519/')").strip()
        if existing_key:
            state["signing_key_id"] = existing_key
            locations = state["locations"]
            firm_folder = Path(locations["firm_folder"])
            if firm_folder.exists() and not dry_run:
                os.chdir(firm_folder)
                run(["git", "config", "--local", "user.signingkey", existing_key], check=False)
                run(["git", "config", "--local", "commit.gpgsign", "true"], check=False)
                gpg_path = which("gpg")
                if gpg_path:
                    run(["git", "config", "--local", "gpg.program", gpg_path], check=False)
                ok("Configured git in your firm folder to sign with the existing key.")
        mark_step_done(state, "step_09_signing_key")
        return

    profile = state["firm_profile"]
    locations = state["locations"]
    firm_folder = Path(locations["firm_folder"])
    email = state.get("brain_repo_email", "")
    name = profile.get("name", "Firm Bot")

    info(
        "Generating a 4096-bit RSA GPG signing key with no passphrase (convenience\n"
        "for the install; for production you'd want a passphrase + pinentry).\n"
    )
    if not ask_confirm("Generate the key now?", default=True):
        info("Skipping. Re-run with --resume.")
        return
    if not dry_run:
        batch = (
            "%no-protection\n"
            "Key-Type: RSA\nKey-Length: 4096\n"
            "Subkey-Type: RSA\nSubkey-Length: 4096\n"
            f"Name-Real: {name} (ØØT Bot)\n"
            f"Name-Comment: ØØT installation {datetime.now(timezone.utc).strftime('%Y-%m-%d')}\n"
            f"Name-Email: {email}\n"
            "Expire-Date: 1y\n%commit\n"
        )
        batch_path = Path("/tmp/oot-gpg-batch.txt")
        batch_path.write_text(batch)
        run(["gpg", "--batch", "--gen-key", str(batch_path)], dry_run=False, check=False)
        batch_path.unlink(missing_ok=True)

    rc, out = run(["gpg", "--list-secret-keys", "--keyid-format", "LONG"],
                  dry_run=dry_run, capture=True)
    info(out)
    info("\nFind the key ID — the 16-character hex string after `rsa4096/` on the `sec` line.")
    key_id = ask_text("GPG key ID", default="")
    state["signing_key_id"] = key_id

    if not dry_run and key_id:
        # Export public key to file the user can open
        pub_path = Path("/tmp/oot-gpg-public.asc")
        rc, out = run(["gpg", "--armor", "--export", key_id], capture=True, check=False)
        if rc == 0 and out:
            pub_path.write_text(out)
            ok(f"Public key written to {pub_path}")
            # Try to open in user's text editor
            opener = "open" if sys.platform == "darwin" else ("xdg-open" if sys.platform.startswith("linux") else None)
            if opener:
                run([opener, str(pub_path)], dry_run=False, check=False)
                info(f"\nThe key is now open in your text editor. Cmd+A, Cmd+C to copy.")
            else:
                info(f"\nThe key is at {pub_path}. Open it in any text editor and copy the entire block.")

    info(
        "\nUpload the public key to GitHub:\n"
        "  1. Open https://github.com/settings/gpg/new in your browser.\n"
        f"  2. Title: {profile['name']} — ØØT signing key\n"
        "  3. Key: paste the block (Cmd+V).\n"
        "  4. Click Add GPG key. Confirm with your password.\n"
    )
    if not ask_confirm("Public key uploaded?", default=True):
        info("Pausing. Re-run with --resume.")
        sys.exit(0)

    info("\nConfiguring git to sign commits in this repo...")
    if not dry_run and key_id:
        os.chdir(firm_folder)
        run(["git", "config", "--local", "user.signingkey", key_id], check=False)
        run(["git", "config", "--local", "commit.gpgsign", "true"], check=False)
        gpg_path = which("gpg")
        if gpg_path:
            run(["git", "config", "--local", "gpg.program", gpg_path], check=False)

    info("\nVerifying with a test signed commit...")
    if not dry_run:
        os.chdir(firm_folder)
        sig_test = firm_folder / "firm" / ".signing-test"
        sig_test.write_text(f"Signed-commit verification at {datetime.now(timezone.utc).isoformat()}\n")
        run(["git", "add", "firm/.signing-test"], check=False)
        run(["git", "commit", "-S", "-m", "verify: signing key works"], check=False)
        run(["git", "log", "--show-signature", "-1"], capture=False, check=False)

        if ask_confirm("Push the verification commit?", default=True):
            run(["git", "push", "origin", "main"], check=False)
            info(
                f"\n→ Open {state.get('brain_repo_url', '<repo>')}/commits/main in your browser.\n"
                f"  The latest commit should have a green Verified badge.\n"
                f"  If not: see docs/00-quickstart-cloud.md 'Step 6' troubleshooting."
            )
    mark_step_done(state, "step_09_signing_key")


def step_10_branch_protection(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_10_branch_protection"):
        return
    header("Step 10 / 14 — Branch protection (web UI)", level=2)
    modules = state.get("modules_chosen", {})
    if not modules.get("install_branch_protection", True):
        info("Branch protection opted out at Step 5. Skipping.")
        info("You can configure it later at any time: GitHub repo → Settings → Branches.")
        mark_step_done(state, "step_10_branch_protection")
        return
    plan_tier = state["firm_profile"].get("github_plan_tier", "free")
    repo_url = state.get("brain_repo_url", "<repo>")

    if plan_tier == "free":
        warn("On GitHub Free + private, branch protection is advisory only. Configure it anyway "
             "(structurally correct for the day you upgrade to Team).")
    info(
        f"\nOpen {repo_url.removesuffix('.git')}/settings/branches in your browser.\n"
        "Click 'Add classic branch protection rule' (or 'Add ruleset' in newer UI).\n\n"
        "Branch name pattern: main\n\n"
        "Configure these checkboxes EXACTLY:\n"
        "  ☑  Require signed commits     ← REJECTS unsigned commits (ADR-001 keystone)\n"
        "  ☐  Allow force pushes          ← KEEPS history immutable\n"
        "  ☐  Allow deletions             ← Branch can't be deleted (audit trail safety)\n"
        "  ☐  Require pull request before merging   ← Allow Routine writes; turn on once stable\n"
        "\nClick Create.\n"
    )
    if not ask_confirm("Branch protection rule created?", default=True):
        info("Pausing.")
        sys.exit(0)
    mark_step_done(state, "step_10_branch_protection")


def step_11_curator(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_11_curator"):
        return
    header("Step 11 / 14 — Curator integration (the second-brain app)", level=2)
    locations = state["locations"]
    modules = state.get("modules_chosen", {})
    mode = modules.get("curator_mode", "install-fresh" if not locations.get("existing_curator") else "use-existing")

    if mode == "skip-for-now":
        info(
            "Curator skipped per your Step 5 selection.\n\n"
            "What this means:\n"
            "  - The Brain repo, signing keys, and most of the framework still work.\n"
            "  - R5 Brain Health Check will NOT have a Brain to scan until you install Curator.\n"
            "  - The my-curator MCP in Claude Desktop will fail until the Curator app is running.\n\n"
            "When you're ready to install:\n"
            "  curl -fsSL https://raw.githubusercontent.com/talirezun/the-curator/main/install.sh | bash\n\n"
            f"Then re-run this wizard with --resume; we'll pick up at this step and finish wiring it\n"
            f"to your firm folder ({locations.get('firm_folder')}).\n"
        )
        mark_step_done(state, "step_11_curator")
        return

    info(
        "The Curator is the desktop app that turns your firm's documents into a\n"
        "queryable knowledge graph (the 'Brain' in framework terms). Claude Code\n"
        "talks to it via the my-curator MCP server. Without it, the Routines\n"
        "have no Brain to read or write — so this step is essential.\n\n"
        "Repo + docs: https://github.com/talirezun/the-curator\n"
    )

    if mode == "use-existing" or locations.get("existing_curator"):
        info(
            "\n— Configuration A: existing Curator detected —\n\n"
            f"We will add a new domain `{locations['curator_domain']}` to your\n"
            f"existing vault at {locations['curator_vault']}.\n\n"
            "In the Curator app (open it now if it's not running):\n"
            "  1. Click 'Domains' in the left sidebar → 'Create domain'.\n"
            f"  2. Name:        {locations['curator_domain']}\n"
            f"  3. Description: {state['firm_profile']['name']} — operational Brain\n"
            "  4. Click Create.\n\n"
            "Then in Claude Desktop, open a new chat and type:\n"
            "  > Use my-curator. List domains.\n"
            f"You should see `{locations['curator_domain']}` listed alongside any\n"
            "domains you already had.\n"
        )
    else:
        info(
            "\n— Configuration B: greenfield install —\n\n"
            "Step 11a — Install the Curator desktop app.\n"
            "  The Curator ships its own one-line installer. Open a *new* Terminal\n"
            "  window (keep this wizard running here), then paste:\n\n"
            "    curl -fsSL https://raw.githubusercontent.com/talirezun/the-curator/main/install.sh | bash\n\n"
            "  This installs the Curator app + its local MCP server. On macOS the\n"
            "  installer drops the app in /Applications and registers it with launchd\n"
            "  so it starts automatically. Total time: 3-5 minutes.\n\n"
            "  If the one-liner doesn't fit your setup, download the installer for\n"
            "  your OS from: https://github.com/talirezun/the-curator/releases/latest\n\n"
            "Step 11b — First-run setup.\n"
            "  Open the Curator app. The first-run wizard asks for:\n"
            "    - API key for ingest (Gemini Flash Lite recommended — free tier at\n"
            "      https://aistudio.google.com/ — or Anthropic Claude if you prefer).\n"
            f"    - Vault folder. Point it at: {locations['firm_folder']}\n"
            f"    - First domain name: {locations['curator_domain']}\n\n"
            "  If macOS prompts for filesystem permission:\n"
            "    System Settings → Privacy & Security → Files and Folders → Curator\n"
            "    → toggle the relevant folder access ON. Then quit and reopen Curator.\n\n"
            "Step 11c — Wire my-curator MCP into Claude Desktop.\n"
            "  The Curator's first-run wizard shows you an MCP config snippet to copy.\n"
            "  In Claude Desktop:\n"
            "    Settings (⌘,) → Developer → Edit Config → paste into mcpServers block.\n"
            "  Then quit Claude Desktop fully (⌘Q) and reopen. The my-curator MCP\n"
            "  should show a green checkmark in the bottom-left tools panel.\n\n"
            "  Verify in a new Claude chat:\n"
            "    > Use my-curator. List domains.\n"
            f"  Expected output: `{locations['curator_domain']}` listed.\n"
        )
    if not ask_confirm("Curator integration complete (Curator running + MCP green)?", default=True):
        info("Pausing here. Re-run the bootstrap (or `python3 installer/wizard.py --resume`) to continue.")
        sys.exit(0)
    mark_step_done(state, "step_11_curator")


def step_12_routines(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_12_routines"):
        return
    header("Step 12 / 14 — Configure Day-1 Routines", level=2)
    modules = state.get("modules_chosen", {})
    chosen = modules.get("routines", [])

    schedules = {
        "R5": ("Sunday 09:00",      "Brain Health Check"),
        "R6": ("daily 23:00",       "EU AI Act Audit Trail"),
        "R7": ("PR webhook",        "Klarna Test gate"),
        "R1": ("daily 18:00",       "Daily Output Capture"),
        "R2": ("Friday 08:00",      "Weekly BR Prep"),
        "R3": ("monthly 1st",       "Partner Acknowledgement Polling"),
        "R4": ("monthly 1st",       "Monthly Compensation Calc"),
        "R8": ("quarterly",         "Quarterly Sentiment Sweep"),
    }
    day1_chosen = [r for r in chosen if r in ("R5", "R6", "R7")]
    deferred = [r for r in chosen if r not in ("R5", "R6", "R7")]

    if not day1_chosen:
        info("No Day-1 Routines selected at Step 5. Skipping the walkthrough.")
        if deferred:
            info(f"Deferred (need partner data first): {', '.join(deferred)}.")
        info("You can configure Routines anytime via Claude Code → /schedule or https://claude.ai/code/routines")
        mark_step_done(state, "step_12_routines")
        return

    info(
        "Each Routine is configured via Claude Code → /schedule, or the web dashboard at\n"
        "https://claude.ai/code/routines, or the Claude Code desktop app's 'New Remote Task'\n"
        "feature. Routines run on Anthropic's cloud regardless.\n\n"
        f"You selected: {', '.join(day1_chosen)} for Day-1.\n"
        + (f"Deferred (will set up later when prerequisites are met): {', '.join(deferred)}.\n" if deferred else "")
    )
    for r in day1_chosen:
        sched, name = schedules[r]
        info(f"\n--- {r} ({name}) setup walkthrough ---")
        info(f"  See routines/cloud/{r}.md for the prompt body and full checklist.")
        info(f"  Trigger: {sched}.")
        info(f"  In Claude Code: /schedule → New Routine → upload prompt body.")
        info(f"  Configure GitHub connector with Brain repo + signing key.")
        info(f"  Manual fire to test.")
        ask_confirm(f"{r} configured and verified?", default=True)
    mark_step_done(state, "step_12_routines")


def step_13_smoke_test(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_13_smoke_test"):
        return
    header("Step 13 / 14 — Smoke test", level=2)
    locations = state["locations"]
    firm_folder = Path(locations["firm_folder"])
    info("Running smoke test against your firm folder...")

    if not firm_folder.exists():
        warn(f"Firm folder {firm_folder} doesn't exist. Skipping.")
        mark_step_done(state, "step_13_smoke_test")
        return

    os.chdir(firm_folder)
    info("\n[1/3] Most recent commit signature:")
    run(["git", "log", "--show-signature", "-1"], capture=False, check=False)

    info("\n[2/3] Excel templates open cleanly:")
    venv_python = VENV_DIR / "bin" / "python"
    if venv_python.exists() and not dry_run:
        cmd = [str(venv_python), "-c", (
            "import openpyxl\n"
            "from pathlib import Path\n"
            f"brain = Path('{firm_folder}') / 'firm' / 'excel'\n"
            "ok = fail = 0\n"
            "for f in sorted(brain.glob('*.xlsx')):\n"
            "    try:\n"
            "        wb = openpyxl.load_workbook(f); n = len(wb.sheetnames); wb.close()\n"
            "        ok += 1; print(f'  ✓ {f.name} — {n} sheets')\n"
            "    except Exception as e:\n"
            "        fail += 1; print(f'  ✗ {f.name} — {e}')\n"
            "print(f'Result: {ok} ok, {fail} fail')\n"
        )]
        run(cmd, capture=False, check=False)

    info("\n[3/3] Brain folder structure:")
    for sub in ["excel", "output-logs", "audit-logs", "business-reviews",
                "klarna-tests", "compensation", "brain-health", "partners"]:
        path = firm_folder / "firm" / sub
        marker = "✓" if path.exists() else "✗"
        info(f"  {marker} firm/{sub}/")
    mark_step_done(state, "step_13_smoke_test")


def step_14_summary(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_14_summary"):
        return
    header("Step 14 / 14 — Install summary", level=2)
    summary_path = OOT_HOME / "install-summary.md"
    profile = state.get("firm_profile", {})
    locations = state.get("locations", {})
    modules = state.get("modules_chosen", {})

    summary = (
        f"# ØØT Install Summary — {profile.get('name', '<firm>')}\n\n"
        f"**Track:** {profile.get('track', 'cloud')}\n"
        f"**Installed:** {datetime.now(timezone.utc).isoformat()}\n"
        f"**By:** wizard v{WIZARD_VERSION}\n"
        f"\n## Firm profile\n\n"
        f"- Firm: {profile.get('name')}\n"
        f"- Partner count: {profile.get('partner_count_estimate')}\n"
        f"- Jurisdictions: {profile.get('jurisdictions')}\n"
        f"- EU high-risk: {profile.get('eu_high_risk')}\n"
        f"- Anthropic plan: {profile.get('anthropic_plan')}\n"
        f"- GitHub plan tier: {profile.get('github_plan_tier')}\n"
        f"\n## Locations\n\n"
        f"- Firm folder: `{locations.get('firm_folder')}`\n"
        f"- Curator vault: `{locations.get('curator_vault')}`\n"
        f"- Curator domain: `{locations.get('curator_domain')}`\n"
        f"- Curator config: {locations.get('curator_config')}\n"
        f"\n## Modules\n\n"
        f"- Required: {', '.join(modules.get('required', []))}\n"
        f"- Recommended: {', '.join(modules.get('recommended', [])) or '(none)'}\n"
        f"- Deferred: {', '.join(modules.get('deferred', [])) or '(none)'}\n"
        f"\n## GitHub repo\n\n"
        f"{state.get('brain_repo_url', '<not configured>')}\n"
        f"\n## Signing key\n\n"
        f"GPG key ID: `{state.get('signing_key_id', '<not generated>')}`\n"
    )
    if not dry_run:
        OOT_HOME.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(summary)
        ok(f"Install summary written to {summary_path}")
    mark_step_done(state, "step_14_summary")
    info("\nInstall complete. Next steps:")
    info("  - Read docs/03-onboarding-a-partner.md for the first partner onboarding.")
    info("  - Read docs/MODULES.md for what to add over the next 30 / 90 / 180 days.")
    info("  - Re-run this wizard with --resume if anything was deferred.")


# ----- main -----------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="ØØT installer wizard v" + WIZARD_VERSION)
    parser.add_argument("--resume", action="store_true",
                        help="Resume from the first incomplete step in ~/.oot/wizard-state.yaml")
    parser.add_argument("--dry-run", action="store_true",
                        help="Walk through prompts without executing consequential actions")
    parser.add_argument("--track", choices=["cloud", "privacy"], default="cloud",
                        help="Track. Cloud is the default; privacy track support is partial in v1.1 (most steps still apply).")
    args = parser.parse_args()

    if not _HAS_QUESTIONARY:
        warn("`questionary` not installed. Falling back to plain input(). "
             "For nicer prompts, run: pip install questionary rich")
    if not _HAS_RICH:
        warn("`rich` not installed. Falling back to plain print(). "
             "For nicer output, run: pip install rich")

    state = load_state() if args.resume else {}
    if not args.resume and STATE_FILE.exists():
        if not ask_confirm(
            f"Existing wizard state at {STATE_FILE}. Overwrite (start fresh) instead of --resume?",
            default=False,
        ):
            info("Resuming from existing state. Use --resume to suppress this prompt.")
            state = load_state()

    state.setdefault("wizard_version", WIZARD_VERSION)
    state.setdefault("started_at", datetime.now(timezone.utc).isoformat())
    state.setdefault("firm_profile", {})["track"] = args.track
    save_state(state)

    try:
        step_00_welcome(state, args.dry_run)
        oot_python = step_01_preflight(state, args.dry_run)
        step_02_python_venv(state, args.dry_run, oot_python)
        step_03_locations(state, args.dry_run)
        step_04_firm_profile(state, args.dry_run)
        step_05_module_selection(state, args.dry_run)
        step_06_github_plan_tier(state, args.dry_run)
        step_07_anthropic_check(state, args.dry_run)
        step_08_brain_repo(state, args.dry_run)
        step_09_signing_key(state, args.dry_run)
        step_10_branch_protection(state, args.dry_run)
        step_11_curator(state, args.dry_run)
        step_12_routines(state, args.dry_run)
        step_13_smoke_test(state, args.dry_run)
        step_14_summary(state, args.dry_run)
    except KeyboardInterrupt:
        warn("\nInterrupted. State saved at " + str(STATE_FILE) + ". Re-run with --resume to continue.")
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
