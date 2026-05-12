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


def info_plain(text: str) -> None:
    """Like info() but never parses rich markup.

    Use for text that contains literal `[x]`, `[ ]`, `[N]`, or other tokens
    that rich would silently swallow as style tags. The checkbox picker uses
    this for every line it prints with selection markers.
    """
    if _HAS_RICH:
        _CONSOLE.print(text, markup=False)
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
    """Multi-select using a self-documenting plain-text picker.

    Each choice is (key, label, preselected). Returns the keys the user kept on.

    Why we don't use questionary.checkbox: its `●` / `○` selection glyphs read
    ambiguously in some Terminal fonts (real user report 2026-05-11 — looked
    identical to them), and the cursor-row background highlight gets misread as
    "this row is selected" when actually it just means "your cursor is here."

    This picker fixes that by:
      - Reprinting the FULL list of items with their current state after every
        toggle. The user always sees an unambiguous `[x]` vs `[ ]` next to each
        item; nothing depends on subtle glyph differences or color contrast.
      - Accepting space- or comma-separated numbers to toggle ("1 3 5" or
        "1,3,5"). Plus `a` (all on), `n` (none), `i` (invert), `q` (cancel — keep
        the current selection unchanged from the previous loop iteration).
      - Confirming with an empty Enter, which echoes "you selected ..." back so
        the user can sanity-check before moving on.

    Works identically with or without questionary/rich installed.
    """
    preselected_labels = [label for _, label, p in choices if p]
    skipped_labels = [label for _, label, p in choices if not p]

    if _HAS_RICH:
        _CONSOLE.print(f"\n[bold cyan]── {prompt}[/bold cyan]")
        _CONSOLE.print("[dim]" + "─" * (len(prompt) + 4) + "[/dim]")
    else:
        info("\n── " + prompt)
        info("─" * (len(prompt) + 4))

    if preselected_labels:
        info("  We've pre-CHECKED these (= recommended defaults — WILL install):")
        for lab in preselected_labels:
            info_plain(f"    [x] {lab}")
    if skipped_labels:
        info("  These start UNCHECKED (= recommended skip):")
        for lab in skipped_labels:
            info_plain(f"    [ ] {lab}")
    info("")
    info_plain("  You'll now see a numbered list with the same [x] / [ ] markers.")
    info("  Type the number(s) to TOGGLE items on/off, then press Enter when done.")
    info("")

    selected = {k for k, _, p in choices if p}
    while True:
        # Reprint the current state of every item.
        info("")
        info(f"  Current selection ({len(selected)} of {len(choices)} on):")
        for i, (key, label, _) in enumerate(choices, 1):
            mark = "[x]" if key in selected else "[ ]"
            line = f"    {i:>2}. {mark}  {label}"
            if _HAS_RICH:
                colour = "green" if key in selected else "dim"
                # IMPORTANT: rich treats `[...]` as a style tag, so we'd
                # silently lose `[x]`. `markup=False` disables that parsing.
                _CONSOLE.print(line, style=("bold " + colour), markup=False)
            else:
                print(line)

        info("")
        info("  Commands:")
        info("    <numbers>  toggle items (e.g. '1 3 5' or '1,3,5')")
        info("    a          turn ALL on")
        info("    n          turn NONE (all off)")
        info("    i          INVERT (flip every item)")
        info("    Enter      DONE — confirm the selection shown above")

        raw = input("\n  Your input: ").strip().lower()
        if not raw:
            break
        if raw == "a":
            selected = {k for k, _, _ in choices}
            continue
        if raw == "n":
            selected = set()
            continue
        if raw == "i":
            all_keys = {k for k, _, _ in choices}
            selected = all_keys - selected
            continue

        # Parse number tokens (comma- or space-separated).
        parsed_any = False
        for tok in raw.replace(",", " ").split():
            try:
                idx = int(tok) - 1
            except ValueError:
                warn(f"  Ignoring unknown input: {tok!r}")
                continue
            if 0 <= idx < len(choices):
                parsed_any = True
                k = choices[idx][0]
                if k in selected:
                    selected.discard(k)
                else:
                    selected.add(k)
            else:
                warn(f"  Number out of range: {tok}")
        if not parsed_any:
            warn("  (Nothing toggled.)")

    # Final confirmation echo
    chosen_labels = [label for k, label, _ in choices if k in selected]
    skipped = [label for k, label, _ in choices if k not in selected]
    info("")
    info("  ✓ Confirmed. You selected (will install / configure):")
    for lab in chosen_labels or ["(nothing)"]:
        info_plain(f"    [x] {lab}")
    if skipped:
        info("  Skipping:")
        for lab in skipped:
            info_plain(f"    [ ] {lab}")
    info("")
    return [k for k, _, _ in choices if k in selected]


# ----- back-navigation between steps ----------------------------------------

class _GoBack(Exception):
    """Raised by a step to request the wizard return to the previous step.

    Caught by the main step-runner, which clears the current step's done-flag
    plus the previous step's done-flag, then loops back into the previous step.
    """


def ask_navigation(label: str = "this step") -> None:
    """End-of-step navigation prompt.

    Returns normally if the user wants to continue.
    Raises _GoBack if the user wants to revise the previous step.
    sys.exit(0) if the user wants to quit (state is already saved).
    """
    choice = ask_select(
        f"Done with {label}. What next?",
        choices=[
            "→  Continue to next step",
            "←  Go back to previous step (revise an earlier answer)",
            "✗  Quit now (your progress is saved; resume with the same one-liner)",
        ],
        default="→  Continue to next step",
    )
    if choice.startswith("←"):
        raise _GoBack()
    if choice.startswith("✗"):
        info("Saving and exiting. Resume with the same bootstrap one-liner anytime.")
        sys.exit(0)
    # Continue


def clear_step_done(state: dict[str, Any], *step_keys: str) -> None:
    """Forget completion for the given step keys, then save state."""
    done = state.get("steps_completed", {})
    for k in step_keys:
        done.pop(k, None)
    save_state(state)


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


# ----- explainer panels -----------------------------------------------------

def explainer(title: str, body: str, tone: str = "info") -> None:
    """Render a small bordered "what is this step / why does it matter" panel.

    Goal: a non-technical founder reads the body and understands what's about
    to happen and why, before being asked to make a decision. Always shown
    BEFORE the first interactive prompt of a step.

    tone is "info" (default cyan), "warn" (yellow), or "danger" (red).
    """
    colour = {"info": "cyan", "warn": "yellow", "danger": "red"}.get(tone, "cyan")
    if _HAS_RICH:
        _CONSOLE.print(Panel(body.strip(), title=f"  {title}  ", title_align="left",
                              border_style=colour, padding=(0, 2)))
        return
    bar = "─" * 70
    print(f"\n┌─ {title} {bar[: max(0, 67 - len(title))]}")
    for line in body.strip().splitlines():
        print(f"│ {line}")
    print(f"└{bar}")


# ----- gh CLI automation helpers --------------------------------------------

_GH_STATUS_CACHE: dict[str, Any] = {}


def gh_available_and_authed() -> bool:
    """True iff the `gh` CLI is installed AND `gh auth status` is clean.

    Result is cached for the lifetime of the wizard process. We call this from
    Steps 8/9/10/12; without caching the user would see `$ gh auth status`
    echoed four times for no good reason. The status doesn't change mid-run.
    """
    if "ok" in _GH_STATUS_CACHE:
        return _GH_STATUS_CACHE["ok"]
    if not which("gh"):
        _GH_STATUS_CACHE["ok"] = False
        return False
    # Direct subprocess to skip the run() helper's command-echo for this probe.
    try:
        result = subprocess.run(
            ["gh", "auth", "status"], capture_output=True, text=True, check=False,
        )
        _GH_STATUS_CACHE["ok"] = result.returncode == 0
    except FileNotFoundError:
        _GH_STATUS_CACHE["ok"] = False
    return _GH_STATUS_CACHE["ok"]


def gh_user_login() -> Optional[str]:
    """Return the authenticated GitHub username, or None if not available."""
    if not gh_available_and_authed():
        return None
    if "login" in _GH_STATUS_CACHE:
        return _GH_STATUS_CACHE["login"]
    try:
        result = subprocess.run(
            ["gh", "api", "user", "--jq", ".login"],
            capture_output=True, text=True, check=False,
        )
        login = result.stdout.strip() if result.returncode == 0 else None
    except FileNotFoundError:
        login = None
    _GH_STATUS_CACHE["login"] = login
    return login


def offer_gh_automation(action_description: str, default: bool = True) -> bool:
    """Ask the user whether to take a `gh`-automated path for this action.

    Returns False if gh isn't available/authed (so callers can skip prompting).
    Returns the user's choice otherwise.
    """
    if not gh_available_and_authed():
        return False
    return ask_confirm(
        f"Use the `gh` CLI to {action_description} automatically? "
        "(recommended — faster, less click-error; N = walk through the github.com web UI instead)",
        default=default,
    )


# ----- macOS asyncio + stdin fixups -----------------------------------------

def _force_select_event_loop_on_macos() -> None:
    """Make asyncio use select() instead of kqueue on macOS.

    macOS's kqueue backend rejects EVFILT_READ registration on certain TTY
    file descriptors inherited via exec or shell stdin-redirect. Symptom:
    deep inside prompt_toolkit (the engine under `questionary`), the first
    interactive prompt blows up with:

        OSError: [Errno 22] Invalid argument
        at asyncio/selector_events.py: _selector.control([kev], 0, 0)

    `select()` works on the same fds without complaint. Setting the event
    loop policy before any asyncio loop is created means `asyncio.run()`
    (called internally by prompt_toolkit) picks up the select-backed loop.
    """
    if sys.platform != "darwin":
        return
    try:
        import asyncio
        import selectors

        class _SelectEventLoopPolicy(asyncio.DefaultEventLoopPolicy):  # type: ignore[name-defined]
            def new_event_loop(self):  # noqa: D401
                return asyncio.SelectorEventLoop(selectors.SelectSelector())

        asyncio.set_event_loop_policy(_SelectEventLoopPolicy())
    except Exception:
        # If anything goes wrong, fall back to the default policy. We don't
        # want to abort the wizard just because we couldn't tweak asyncio.
        pass


def _reattach_stdin_to_tty_if_needed() -> None:
    """If our stdin isn't a TTY but /dev/tty is available, attach it.

    Belt-and-suspenders alongside the bootstrap's `< /dev/tty` redirect.
    Handles the corner case where wizard.py is launched some other way
    without a real interactive stdin (e.g. `python wizard.py < script`
    or `curl | bash` without the redirect).
    """
    try:
        if sys.stdin is not None and sys.stdin.isatty():
            return
    except (ValueError, OSError):
        pass
    try:
        tty_fd = os.open("/dev/tty", os.O_RDONLY)
    except OSError:
        return
    try:
        os.dup2(tty_fd, 0)
    finally:
        os.close(tty_fd)
    try:
        sys.stdin = os.fdopen(0, "r")
    except OSError:
        pass


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

_STATE_KEY_RENAMES = {
    # v1.0.0 → v1.0.1 rename: "Brain repo" → "Ledger" in user-facing terms.
    # Internal state keys keep backward compat — old keys are silently
    # promoted to the new keys at load time so anyone with mid-install state
    # from before the rename doesn't lose progress.
    "brain_repo_url":    "ledger_repo_url",
    "brain_repo_owner":  "ledger_repo_owner",
    "brain_repo_name":   "ledger_repo_name",
    "brain_repo_email":  "ledger_repo_email",
}


def _migrate_state_keys(state: dict[str, Any]) -> dict[str, Any]:
    """Backward-compat: promote pre-rename state keys to current names."""
    for old, new in _STATE_KEY_RENAMES.items():
        if old in state and new not in state:
            state[new] = state.pop(old)
    return state


def load_state() -> dict[str, Any]:
    if not STATE_FILE.exists() or yaml is None:
        return {}
    try:
        with STATE_FILE.open() as f:
            raw = yaml.safe_load(f) or {}
        return _migrate_state_keys(raw)
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

    explainer(
        "What this step does and why",
        "We need four small command-line tools on your machine before anything else:\n\n"
        "  git    — version control. Tracks every change to your Ledger.\n"
        "  python ≥3.11 — runs this wizard + the framework's Excel-writing scripts.\n"
        "  curl   — downloads things (the framework, Curator, etc.).\n"
        "  gpg    — generates and uses the signing key that makes commits verifiable.\n\n"
        "If any are missing, the wizard prints exact copy-paste commands to install\n"
        "them via your OS package manager (brew/apt/dnf). No auto-sudo, no surprises.",
    )

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


def step_02_python_venv(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_02_python_venv"):
        return
    header("Step 2 / 14 — Python virtual environment", level=2)
    explainer(
        "What this step does and why",
        "We create an isolated Python environment at ~/.oot/venv and install the\n"
        "framework's dependencies (openpyxl for Excel, pyyaml for state files,\n"
        "questionary/rich for the wizard UI, httpx for HTTP). Modern Python on macOS\n"
        "and Debian rejects `pip install` outside a venv (PEP 668) — this is the\n"
        "right way around it without messing with your system Python.\n\n"
        "If you ran the bootstrap one-liner, this is mostly already done — we just\n"
        "verify it's healthy.",
    )
    oot_python = state.get("preflight", {}).get("python") or state.get("oot_python") or sys.executable
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

    explainer(
        "What this step does and why",
        "Two folders matter to ØØT:\n\n"
        "  1. Firm folder (the Ledger)  — a local git clone of your firm's\n"
        "     operational data (Excel files, output logs, audit logs). This is what\n"
        "     Routines read and write. Default: ~/<firm-slug>/\n\n"
        "  2. Curator vault  — where The Curator app stores the knowledge-graph\n"
        "     markdown pages it generates from your documents. This is your\n"
        "     'second brain'.\n\n"
        "Two configurations:\n"
        "  A — Separate: vault and firm repo are different folders. Use this if you\n"
        "      already have a populated Curator vault you don't want to disturb.\n"
        "  B — Unified: the firm folder IS the Curator vault root. Cleanest for\n"
        "      a greenfield install — everything in one place.",
    )

    info("Three folder questions: where the firm's operational stuff lives, where your\n"
         "knowledge graph (Curator) lives, and how the two relate.\n")

    # Pull prior answers (if any) as defaults so going-back is friction-free.
    prior = state.get("locations", {})

    firm_slug_default = ask_text("Firm slug (lowercase-hyphenated, e.g. 'acme-studio')",
                                  default=prior.get("firm_slug") or None)
    if not firm_slug_default:
        warn("Firm slug is required.")
        sys.exit(1)
    firm_folder_default = prior.get("firm_folder") or str(Path.home() / firm_slug_default)
    firm_folder = ask_path(
        f"Firm operational repo folder", default=firm_folder_default
    )

    has_curator = ask_confirm(
        "Do you already have the Curator desktop app installed with a populated second-brain?",
        default=bool(prior.get("existing_curator", False)),
    )
    curator_vault = None
    curator_config = prior.get("curator_config", "B")
    if has_curator:
        guesses = [
            Path.home() / "second-brain",
            Path.home() / "Documents" / "second-brain",
        ]
        found = next((g for g in guesses if g.exists()), None)
        cv_default = prior.get("curator_vault") or (str(found) if found else str(Path.home() / "second-brain"))
        curator_vault = ask_path("Curator vault folder path", default=cv_default, must_exist=True)
        cfg_default = (
            "A — Separate vault and firm repo (recommended for existing Curator users)"
            if curator_config == "A"
            else "A — Separate vault and firm repo (recommended for existing Curator users)"
        )
        curator_config = ask_select(
            "Curator integration mode (see docs/MODULES.md for the trade-off):",
            choices=[
                "A — Separate vault and firm repo (recommended for existing Curator users)",
                "B — Unified: firm repo IS the Curator vault (recommended for greenfield)",
            ],
            default=cfg_default,
        )[0]
    else:
        curator_vault = firm_folder
        info("No existing Curator detected — defaulting to Configuration B (firm folder = Curator vault root).")

    curator_domain = ask_text(
        "Curator domain slug for this firm",
        default=prior.get("curator_domain") or firm_slug_default,
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
    ask_navigation("location choices")
    return locations


def step_04_firm_profile(state: dict[str, Any], dry_run: bool) -> dict[str, Any]:
    if is_step_done(state, "step_04_firm_profile"):
        return state.get("firm_profile", {})
    header("Step 4 / 14 — Firm profile", level=2)

    explainer(
        "What this step does and why",
        "We ask 5 questions about your firm. Your answers shape what gets installed\n"
        "by default at Step 5 (which Skills, which Routines, what plan-tier guidance\n"
        "we give you):\n\n"
        "  - Firm name + partner count + jurisdictions  — for the Ledger README and\n"
        "    later compensation/onboarding flows.\n"
        "  - EU AI Act exposure  — if yes, we add S7 (governance) + R6 (audit trail)\n"
        "    to the recommended defaults.\n"
        "  - Klarna gate timing  — if 'now', we add R7 (PR webhook) + S4 (code-qa) +\n"
        "    S6 (change-management) to the defaults.\n\n"
        "Honest answers help you, not us — nothing is sent off-machine.",
    )

    prior = state.get("firm_profile", {})
    profile: dict[str, Any] = {}
    profile["name"] = ask_text("Firm full name (e.g. 'Acme Studio')",
                                default=prior.get("name", ""))
    profile["partner_count_estimate"] = ask_select(
        "Partner count over next 12 months:",
        choices=["solo", "small (2-5)", "medium (5-10)", "large (10+)"],
        default=prior.get("partner_count_estimate") or "solo",
    )
    profile["jurisdictions"] = ask_text(
        "Jurisdictions (ISO 2-letter codes, comma-separated, e.g. 'SI,HR')",
        default=prior.get("jurisdictions", ""),
    )
    profile["eu_high_risk"] = ask_select(
        "EU AI Act high-risk Annex III exposure (employment / essential services / biometrics):",
        choices=["yes", "no", "not-sure"],
        default=prior.get("eu_high_risk") or "not-sure",
    )
    profile["klarna_gate_choice"] = ask_select(
        "Configure Klarna gate today, or defer until first AI-replaces-human PR?",
        choices=["now", "later"],
        default=prior.get("klarna_gate_choice") or "later",
    )
    profile["track"] = prior.get("track", "cloud")
    state["firm_profile"] = profile
    mark_step_done(state, "step_04_firm_profile")
    ask_navigation("firm profile")
    return profile


def step_05_module_selection(state: dict[str, Any], dry_run: bool) -> dict[str, Any]:
    if is_step_done(state, "step_05_module_selection"):
        return state.get("modules_chosen", {})
    header("Step 5 / 14 — Module selection (choose what to install)", level=2)

    profile = state.get("firm_profile", {})
    eu = profile.get("eu_high_risk") in {"yes", "not-sure"}
    klarna_now = profile.get("klarna_gate_choice") == "now"
    big_firm = profile.get("partner_count_estimate", "").startswith(("medium", "large"))

    # Probe once, up-front.
    found = detect_existing_modules(state)
    render_detection_report(found)

    info(
        "You'll now make four sets of choices (Foundation / Curator / Skills /\n"
        "Routines / Optional security). Each is shown with recommended defaults\n"
        "pre-checked. At the end you'll see a summary and can re-do anything\n"
        "before we commit.\n"
    )

    # Helper to keep the four-checkbox + curator-select cycle re-runnable.
    def _run_selection_cycle(prior: dict[str, Any] | None = None) -> dict[str, Any]:
        """Run all five selection prompts. Returns the modules dict.

        `prior` (if given) is consulted for re-do defaults so the user doesn't
        lose their previous picks when they ask to revise.
        """
        prior = prior or {}
        prior_foundation = set(prior.get("foundation", [])) if prior else set()
        prior_skills     = set(prior.get("skills", []))     if prior else set()
        prior_routines   = set(prior.get("routines", []))   if prior else set()
        prior_security   = set(prior.get("security", []))   if prior else set()
        prior_curator    = prior.get("curator_mode")

        def _pre(key: str, default: bool, prior_set: set[str]) -> bool:
            return key in prior_set if prior_set else default

        # Foundation — looped until user keeps at least the hard-required items
        # OR explicitly opts to continue "advanced".
        while True:
            foundation_choices: list[tuple[str, str, bool]] = [
                ("github_brain_repo",
                    "GitHub Ledger (your firm's operational data — the heart of the framework)",
                    _pre("github_brain_repo", True, prior_foundation)),
                ("signing_key",
                    "GPG signing key for signed commits "
                    + ("(found one already — will reuse)" if found["gpg_signing_key"]["present"]
                       else "(will create a new one in Step 9)"),
                    _pre("signing_key", True, prior_foundation)),
                ("my_curator_mcp",
                    "my-curator MCP wired into Claude Desktop (lets Claude read your Brain)",
                    _pre("my_curator_mcp", True, prior_foundation)),
                ("spreadsheet_app",
                    "Spreadsheet viewer (Excel / Numbers / LibreOffice / Sheets) — you almost certainly already have one",
                    _pre("spreadsheet_app", True, prior_foundation)),
            ]
            foundation = ask_checkbox("FOUNDATION — minimum for a working ØØT install", foundation_choices)
            missing_required = [m for m in ("github_brain_repo", "my_curator_mcp") if m not in foundation]
            if not missing_required:
                break
            warn(f"⚠  You unchecked: {', '.join(missing_required)}.")
            warn("These are essential — without them, the framework will not work.")
            choice = ask_select(
                "What would you like to do?",
                choices=[
                    "Re-do the foundation checkboxes (recommended — probably accidental)",
                    "Continue anyway (advanced — you'll wire equivalents yourself)",
                ],
                default="Re-do the foundation checkboxes (recommended — probably accidental)",
            )
            if choice.startswith("Continue"):
                break
            # else: loop and re-prompt
            prior_foundation = set(foundation)  # keep their other picks as new defaults

        # Curator mode — 3 options
        if prior_curator:
            curator_default_key = prior_curator
        elif found["curator"]["user_said_existing"] or found["curator"]["app_present"]:
            curator_default_key = "use-existing"
            info("(Existing Curator detected — defaulting to 'use-existing'.)")
        else:
            curator_default_key = "install-fresh"
        curator_choices_labels = [
            "use-existing      (reuse the Curator you already have)",
            "install-fresh     (run Curator's one-line installer in Step 11)",
            "skip-for-now      (install later yourself — most steps still work, R5 won't)",
        ]
        curator_default = next((c for c in curator_choices_labels if c.startswith(curator_default_key)),
                                curator_choices_labels[0])
        curator_choice = ask_select(
            "THE CURATOR — second-brain desktop app — how should we handle it?",
            choices=curator_choices_labels,
            default=curator_default,
        )
        curator_mode = curator_choice.split()[0]

        # Skill packs
        skill_choices: list[tuple[str, str, bool]] = [
            ("S1",  "S1  my-curator (Brain operations)",                      _pre("S1",  True,  prior_skills)),
            ("S2",  "S2  context-engineering",                                _pre("S2",  True,  prior_skills)),
            ("S3",  "S3  compensation-attribution (variable pay)",            _pre("S3",  True,  prior_skills)),
            ("S4",  "S4  code-qa",                                            _pre("S4",  True,  prior_skills)),
            ("S5",  "S5  reporting-business-review",                          _pre("S5",  True,  prior_skills)),
            ("S6",  "S6  change-management",                                  _pre("S6",  True,  prior_skills)),
            ("S12", "S12 privacy-self-sovereign",                             _pre("S12", profile.get("track") == "privacy", prior_skills)),
            ("S7",  "S7  governance-compliance (Tier-2 scaffold)",            _pre("S7",  eu, prior_skills)),
            ("S8",  "S8  legal-operations (Tier-2 scaffold)",                 _pre("S8",  big_firm, prior_skills)),
            ("S9",  "S9  marketing (Tier-2 scaffold)",                        _pre("S9",  False, prior_skills)),
            ("S10", "S10 finance-treasury (Tier-2 scaffold)",                 _pre("S10", big_firm, prior_skills)),
            ("S11", "S11 sales-bd (Tier-2 scaffold)",                         _pre("S11", False, prior_skills)),
        ]
        skills = ask_checkbox("SKILL PACKS — domain knowledge bundles your Routines + agents use", skill_choices)

        # Routines
        routine_choices: list[tuple[str, str, bool]] = [
            ("R5", "R5 Brain Health Check (Sunday 09:00) — recommended for every firm",   _pre("R5", True, prior_routines)),
            ("R6", "R6 EU AI Act Audit Trail (daily 23:00) — recommended; required if EU exposure",
                                                                                            _pre("R6", True, prior_routines)),
            ("R7", "R7 Klarna Test gate (PR webhook) — only if you're configuring Klarna now",
                                                                                            _pre("R7", klarna_now, prior_routines)),
            ("R1", "R1 Daily Output Capture — needs first partner onboarded (set up later)", _pre("R1", False, prior_routines)),
            ("R2", "R2 Weekly BR Prep — needs R1 to have ≥7 days of data (set up later)",   _pre("R2", False, prior_routines)),
            ("R3", "R3 Partner Acknowledgement Polling — month-1+ (set up later)",          _pre("R3", False, prior_routines)),
            ("R4", "R4 Monthly Compensation Calc — month-1+ (set up later)",                _pre("R4", False, prior_routines)),
            ("R8", "R8 Quarterly Sentiment Sweep — quarter-1+ (set up later)",              _pre("R8", False, prior_routines)),
        ]
        routines_picked = ask_checkbox("ROUTINES — Claude Code Routines running on schedule", routine_choices)

        # Optional security
        sec_choices: list[tuple[str, str, bool]] = [
            ("branch_protection",
                "GitHub branch protection on main "
                + ("(enforced — Team plan)" if profile.get("github_plan_tier") == "team"
                   else "(advisory only on Free — still worth setting)"),
                _pre("branch_protection", True, prior_security)),
            ("bitwarden",
                "Bitwarden password manager + CLI"
                + (" (CLI already installed)" if found["bitwarden_cli"]["present"] else ""),
                _pre("bitwarden", found["bitwarden_cli"]["present"], prior_security)),
            ("yubikey",
                "Yubikey for org-admin 2FA (recommended with ≥2 admins)",
                _pre("yubikey", big_firm, prior_security)),
            ("trezor",
                "Trezor for crypto-key storage (Gen-2 — not used in v1.0)",
                _pre("trezor", False, prior_security)),
        ]
        security = ask_checkbox("OPTIONAL SECURITY — recommended-but-optional in Gen 1", sec_choices)

        return {
            "foundation":      foundation,
            "curator_mode":    curator_mode,
            "skills":          skills,
            "routines":        routines_picked,
            "security":        security,
            "install_curator": curator_mode == "install-fresh",
            "skip_curator":    curator_mode == "skip-for-now",
            "use_existing_curator": curator_mode == "use-existing",
            "install_signing_key": "signing_key" in foundation and not found["gpg_signing_key"]["present"],
            "install_branch_protection": "branch_protection" in security,
        }

    # Run the cycle, then loop on user request until they accept.
    modules: dict[str, Any] = {}
    while True:
        modules = _run_selection_cycle(prior=modules if modules else None)

        info("\n" + "─" * 60)
        info("YOUR PLAN")
        info("─" * 60)
        info(f"  Foundation:   {', '.join(modules['foundation']) or '(none)'}")
        info(f"  Curator:      {modules['curator_mode']}")
        info(f"  Skill packs:  {', '.join(modules['skills']) or '(none)'}")
        info(f"  Routines now: {', '.join(modules['routines']) or '(none)'}")
        info(f"  Security:     {', '.join(modules['security']) or '(none)'}")
        info("")

        next_step = ask_select(
            "Are you happy with this plan?",
            choices=[
                "→  Yes, proceed",
                "↻  Re-do the module selections (with these as new defaults)",
                "←  Go back to the previous step (firm profile)",
                "✗  Quit now (progress saved)",
            ],
            default="→  Yes, proceed",
        )
        if next_step.startswith("→"):
            break
        if next_step.startswith("↻"):
            continue   # rerun the cycle with current modules as defaults
        if next_step.startswith("←"):
            state["modules_chosen"] = modules  # save current draft so re-entry can default to it
            save_state(state)
            raise _GoBack()
        if next_step.startswith("✗"):
            state["modules_chosen"] = modules
            save_state(state)
            info("Saving and exiting. Resume with the same bootstrap one-liner.")
            sys.exit(0)

    state["modules_chosen"] = modules
    mark_step_done(state, "step_05_module_selection")
    return modules


def step_06_github_plan_tier(state: dict[str, Any], dry_run: bool) -> str:
    if is_step_done(state, "step_06_github_plan_tier"):
        return state.get("firm_profile", {}).get("github_plan_tier", "free")
    header("Step 6 / 14 — GitHub plan-tier choice (CRITICAL)", level=2)
    explainer(
        "What this step does and why  ⚠️  (structural choice)",
        "GitHub Free + private repos display branch-protection rules in the UI but\n"
        "DO NOT enforce them. A bad actor with push access could `git push --force`\n"
        "and rewrite your audit trail; GitHub Free wouldn't stop them. For ADR-001's\n"
        "tamper-evidence claim to hold, branch protection must be enforced — which\n"
        "means GitHub Team ($4/user/month) or higher, OR a public repo.\n\n"
        "Three valid choices:\n"
        "  team   — $4/user/mo. Branch protection is ENFORCED. Recommended default.\n"
        "  public — Free, but your firm operational data is publicly visible.\n"
        "  free   — Free + private. Branch protection ADVISORY only.\n"
        "           Acceptable for a solo / 2-person pilot; upgrade within 90 days.\n\n"
        "This choice affects whether your audit trail is actually trustworthy.",
        tone="warn",
    )
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
    prior_tier = state.get("firm_profile", {}).get("github_plan_tier") or "free"
    choice = ask_select(
        "GitHub plan tier:",
        choices=["team", "public", "free"],
        default=prior_tier,
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
    ask_navigation("GitHub plan choice")
    return choice


def step_07_anthropic_check(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_07_anthropic_check"):
        return
    header("Step 7 / 14 — Anthropic check", level=2)
    explainer(
        "What this step does and why",
        "Two Anthropic products you'll need:\n\n"
        "  - Claude Desktop  — the chat app. This is where the my-curator MCP runs.\n"
        "    Download free: https://claude.com/download\n\n"
        "  - Claude Code CLI (or web dashboard at claude.ai/code/routines) — used to\n"
        "    create and manage Routines at Step 12. Either works.\n\n"
        "Plan tiers:\n"
        "  pro   — 5 Routine runs/day. OK for solo founders with no R7.\n"
        "  max   — 15/day. Recommended for any firm taking R7 / Klarna gate seriously.\n"
        "  team / enterprise — higher caps + shared billing. Pick if you've already chosen one.\n\n"
        "We don't ask for your API key — Routines authenticate via your Anthropic\n"
        "account, not via API keys.",
    )

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

    prior_plan = state.get("firm_profile", {}).get("anthropic_plan") or "pro"
    plan = ask_select(
        "Anthropic plan tier:",
        choices=["pro", "max", "team", "enterprise"],
        default=prior_plan,
    )
    state.setdefault("firm_profile", {})["anthropic_plan"] = plan
    profile = state["firm_profile"]
    if plan == "pro" and (profile.get("partner_count_estimate", "").startswith("medium")
                          or profile.get("klarna_gate_choice") == "now"):
        warn("Pro plan caps Routines at 5/day. With your firm size + Klarna gate, "
             "you'll exceed that. Strongly recommend Max plan.")
    mark_step_done(state, "step_07_anthropic_check")
    info("\nNext: Step 8 will start creating real things (Ledger on disk + on GitHub).")
    info("After Step 8 launches, going back gets harder — it would mean undoing side effects.")
    info("This is your last clean checkpoint to revise earlier answers.\n")
    ask_navigation("Anthropic check (last clean checkpoint before side-effects begin)")


def step_08_brain_repo(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_08_brain_repo"):
        return
    header("Step 8 / 14 — Create the Ledger GitHub repo", level=2)

    locations = state["locations"]
    profile = state["firm_profile"]
    firm_slug = locations["firm_slug"]
    firm_folder = Path(locations["firm_folder"])
    plan_tier = profile.get("github_plan_tier", "free")
    visibility = "public" if plan_tier == "public" else "private"

    explainer(
        "What this step does and why",
        "Your firm's operational data — Excel files, output logs, audit logs, partner\n"
        "ledgers — lives in a GitHub repository. The framework's Routines read from it\n"
        "and write back to it via signed commits (that's how the audit trail stays\n"
        "tamper-evident). This step does FOUR things:\n\n"
        "  1. Creates a folder on YOUR machine (the local clone).\n"
        "  2. Scaffolds the firm/ subfolder structure (excel/, output-logs/, etc.)\n"
        "     and copies in the 9 Excel templates from the framework.\n"
        "  3. Makes the first commit (unsigned for now — signing key comes next step).\n"
        "  4. Creates the GitHub repo and pushes everything to it.\n\n"
        "If your `gh` CLI is installed and you're logged in, step 4 is one command and\n"
        "5 seconds. Otherwise we walk you through clicking through github.com.",
    )

    # --- Substep 1: local folder + git init -------------------------------
    info("\n[1/4] Local folder + git init")
    if not firm_folder.exists():
        firm_folder.mkdir(parents=True)
        ok(f"Created {firm_folder}")
    os.chdir(firm_folder)
    if not (firm_folder / ".git").exists():
        run(["git", "init", "-b", "main"], dry_run=dry_run, check=False)
        ok("git init")
    else:
        info(f"  (Already a git repo at {firm_folder} — skipping init.)")

    # --- Substep 2: author identity + scaffold + Excel templates ----------
    info("\n[2/4] Commit author identity + folder scaffold + Excel templates")
    explainer(
        "Why we ask for an email here",
        "GitHub marks a commit 'Verified' (green badge) only when the commit-author\n"
        "email matches an email on the GPG key you'll upload at Step 9. So use a real\n"
        "email you control — e.g. the one tied to your GitHub account. You can use a\n"
        "GitHub noreply address (the privacy-friendly one in Settings → Emails).",
    )
    prior_email = state.get("ledger_repo_email", "")
    email = ask_text("Email for commit authorship in this repo", default=prior_email or "")
    name = ask_text("Name for commit authorship", default=profile.get("name", ""))
    state["ledger_repo_email"] = email
    if email and not dry_run:
        run(["git", "config", "--local", "user.email", email], dry_run=False, check=False)
        run(["git", "config", "--local", "user.name", name], dry_run=False, check=False)

    subfolders = ["excel", "output-logs", "audit-logs", "business-reviews",
                  "klarna-tests", "compensation", "brain-health", "partners"]
    for sub in subfolders:
        (firm_folder / "firm" / sub).mkdir(parents=True, exist_ok=True)
        if sub != "excel":
            gitkeep = firm_folder / "firm" / sub / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.touch()
    excel_dst = firm_folder / "firm" / "excel"
    if not dry_run:
        for xlsx in TEMPLATES_EXCEL.glob("*.xlsx"):
            shutil.copy2(xlsx, excel_dst / xlsx.name)
        ok(f"Copied {len(list(excel_dst.glob('*.xlsx')))} .xlsx templates to firm/excel/")

    readme = firm_folder / "README.md"
    if not readme.exists():
        readme_text = (
            f"# {profile['name']} — operational Ledger\n\n"
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

    # --- Substep 3: initial commit ----------------------------------------
    info("\n[3/4] Initial unsigned commit")
    info("  (The first commit is unsigned. Step 9 generates the signing key + reconfigures\n"
         "   git to sign every subsequent commit. All Routine-written commits will be signed.)")
    if not dry_run:
        run(["git", "add", "."], check=False)
        # If nothing to commit, this is a no-op (existing repo).
        run(["git", "commit", "-m",
             "scaffold: initial Ledger folder + Excel templates from framework v1.0.0"],
            check=False)

    # --- Substep 4: create the GitHub repo + push -------------------------
    info("\n[4/4] Create the GitHub repo + push")
    repo_name_default = f"{firm_slug}-brain"
    repo_name = ask_text("Repository name on GitHub", default=repo_name_default)

    repo_created_via_gh = False
    if gh_available_and_authed():
        login = gh_user_login() or "(you)"
        full_repo = f"{login}/{repo_name}"
        info(f"  ✓ `gh` CLI detected (authenticated as {login}).")
        if ask_confirm(
            f"Create the repo {full_repo} ({visibility}) automatically via `gh`, "
            "and push our initial commit? (recommended — faster, no clicking)",
            default=True,
        ):
            info(f"  Creating {full_repo}...")
            rc, out = run(
                ["gh", "repo", "create", full_repo,
                 f"--{visibility}",
                 "--description", f"ØØT Ledger for {profile['name']}",
                 "--source", str(firm_folder),
                 "--remote", "origin",
                 "--push"],
                dry_run=dry_run, capture=True, check=False,
            )
            if rc == 0:
                ok(f"Repo created: https://github.com/{full_repo}")
                state["ledger_repo_url"] = f"https://github.com/{full_repo}.git"
                state["ledger_repo_owner"] = login
                state["ledger_repo_name"] = repo_name
                repo_created_via_gh = True
            else:
                warn("`gh repo create` failed. Output:")
                if out:
                    info(out)
                warn("Falling back to the web UI walkthrough.")
        else:
            info("  OK — using the web UI path.")
    else:
        if not which("gh"):
            info("  `gh` CLI not installed. We'll walk through the github.com web UI instead.")
            info("  (Install gh anytime via `brew install gh` for one-command repo creation.)")
        else:
            info("  `gh` is installed but not authenticated. Run `gh auth login` separately to\n"
                 "  enable automation next time. For now we'll walk through the web UI.")

    if not repo_created_via_gh:
        info(
            "\n  Manual GitHub repo creation:\n"
            f"    1. Open https://github.com/new in your browser.\n"
            f"    2. Repository name:        {repo_name}\n"
            f"    3. Description:            ØØT Ledger for {profile['name']}\n"
            f"    4. Visibility:             {visibility.capitalize()}\n"
            f"    5. Initialize:             leave ALL THREE checkboxes UNCHECKED\n"
            f"                               (no README, no .gitignore, no licence —\n"
            f"                                we've already made the initial commit locally)\n"
            f"    6. Click 'Create repository'.\n"
        )
        if not ask_confirm("Repo created on GitHub.com?", default=True):
            info("Pausing. Re-run the bootstrap to resume.")
            sys.exit(0)
        repo_url = ask_text(
            "Repo HTTPS URL (copy the URL bar — e.g. https://github.com/you/your-brain)",
            default=f"https://github.com/<you>/{repo_name}.git",
        )
        if not repo_url.endswith(".git"):
            repo_url = repo_url.rstrip("/") + ".git"
        state["ledger_repo_url"] = repo_url
        # Add remote + push
        if not dry_run:
            os.chdir(firm_folder)
            run(["git", "remote", "remove", "origin"], capture=True, check=False)  # idempotent
            run(["git", "remote", "add", "origin", repo_url], check=False)
            ok("Added remote 'origin'.")
        if ask_confirm("Push to origin/main now? (May prompt for GitHub credentials.)", default=True):
            run(["git", "push", "-u", "origin", "main"], dry_run=dry_run, check=False)

    mark_step_done(state, "step_08_brain_repo")


def step_09_signing_key(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_09_signing_key"):
        return
    header("Step 9 / 14 — Generate signing key + upload to GitHub", level=2)

    explainer(
        "What this step does and why",
        "A GPG signing key is what lets GitHub mark a commit 'Verified' (green badge).\n"
        "Once we configure git to sign every commit, every Routine-written change to\n"
        "your Ledger gets a cryptographic stamp tying it to this key. With branch\n"
        "protection in place (Step 10) that gives you a tamper-evident audit trail —\n"
        "the core of the framework's compliance story (ADR-001 / EU AI Act §12).\n\n"
        "We'll: (1) generate a 4096-bit RSA key in your gpg keychain, (2) export the\n"
        "public half, (3) upload it to GitHub (automatically via `gh gpg-key add` if\n"
        "your gh CLI is logged in, otherwise via the web UI), (4) tell git in your\n"
        "Ledger to sign with this key, (5) make a test signed commit and push it.\n\n"
        "The key has no passphrase (so Routines can sign non-interactively). This is\n"
        "fine for a bot identity; a human signing key would use a passphrase + pinentry.",
    )

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
    email = state.get("ledger_repo_email", "")
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

    pub_path: Optional[Path] = None
    if not dry_run and key_id:
        # Export public key to file (also used by gh gpg-key add).
        pub_path = Path("/tmp/oot-gpg-public.asc")
        rc, out = run(["gpg", "--armor", "--export", key_id], capture=True, check=False)
        if rc == 0 and out:
            pub_path.write_text(out)
            ok(f"Public key written to {pub_path}")

    uploaded_via_gh = False
    if pub_path and gh_available_and_authed():
        if ask_confirm(
            "Upload the public key to GitHub automatically via `gh gpg-key add`? "
            "(recommended — no copy-paste, no opening browser)",
            default=True,
        ):
            rc, out = run(["gh", "gpg-key", "add", str(pub_path)],
                          dry_run=dry_run, capture=True, check=False)
            if rc == 0:
                ok("GPG key uploaded to GitHub.")
                uploaded_via_gh = True
            else:
                warn("`gh gpg-key add` failed. Output:")
                if out:
                    info(out)
                warn("Falling back to manual upload.")

    if not uploaded_via_gh:
        if pub_path:
            opener = "open" if sys.platform == "darwin" else ("xdg-open" if sys.platform.startswith("linux") else None)
            if opener:
                run([opener, str(pub_path)], dry_run=False, check=False)
                info(f"\nThe key is now open in your text editor. Cmd+A, Cmd+C to copy the whole block.")
            else:
                info(f"\nThe key is at {pub_path}. Open it in any text editor and copy the entire block.")
        info(
            "\nUpload the public key to GitHub manually:\n"
            "  1. Open https://github.com/settings/gpg/new in your browser.\n"
            f"  2. Title: {profile['name']} — ØØT signing key\n"
            "  3. Key: paste the block (Cmd+V).\n"
            "  4. Click 'Add GPG key'. Confirm with your password if asked.\n"
        )
        if not ask_confirm("Public key uploaded?", default=True):
            info("Pausing. Re-run the bootstrap to resume.")
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
                f"\n→ Open {state.get('ledger_repo_url', '<repo>')}/commits/main in your browser.\n"
                f"  The latest commit should have a green Verified badge.\n"
                f"  If not: see docs/00-quickstart-cloud.md 'Step 6' troubleshooting."
            )
    mark_step_done(state, "step_09_signing_key")


def step_10_branch_protection(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_10_branch_protection"):
        return
    header("Step 10 / 14 — Branch protection on main", level=2)
    modules = state.get("modules_chosen", {})
    if not modules.get("install_branch_protection", True):
        info("Branch protection opted out at Step 5. Skipping.")
        info("You can configure it later anytime: GitHub repo → Settings → Branches.")
        mark_step_done(state, "step_10_branch_protection")
        return
    plan_tier = state["firm_profile"].get("github_plan_tier", "free")
    repo_url = state.get("ledger_repo_url", "")
    owner = state.get("ledger_repo_owner")
    repo_name = state.get("ledger_repo_name")

    explainer(
        "What this step does and why",
        "Branch protection on `main` is what makes your audit trail trustworthy.\n"
        "Specifically, we'll set these rules:\n\n"
        "  ✓ Require signed commits      — rejects unsigned pushes (ADR-001 keystone)\n"
        "  ✗ Allow force pushes          — preserves immutable history\n"
        "  ✗ Allow deletions             — main branch can't be deleted\n"
        "  ✗ Require pull request        — Routines can commit directly (turn on later)\n\n"
        f"Your GitHub plan: {plan_tier}.\n"
        + ("⚠  GitHub Free + private repos do NOT enforce these rules — they're\n"
           "   advisory only. We configure them anyway so your repo is structurally\n"
           "   correct the day you upgrade to Team ($4/user/month). Per ADR-001 the\n"
           "   audit-trail-immutability claim requires enforced protection."
           if plan_tier == "free" else
           "Enforcement is active on your plan — these rules will actually be enforced."),
    )

    applied_via_gh = False
    if gh_available_and_authed() and owner and repo_name:
        if ask_confirm(
            "Apply branch protection automatically via `gh api`? "
            "(recommended — sets all four rules in one call)",
            default=True,
        ):
            # PUT /repos/{owner}/{repo}/branches/{branch}/protection
            # Note: required_status_checks/restrictions must be null; the API
            # rejects missing keys, so we send the full minimal payload.
            payload = {
                "required_status_checks": None,
                "enforce_admins": True,
                "required_pull_request_reviews": None,
                "restrictions": None,
                "required_signatures": True,
                "allow_force_pushes": False,
                "allow_deletions": False,
            }
            payload_path = Path("/tmp/oot-branch-protection.json")
            import json as _json
            payload_path.write_text(_json.dumps(payload))
            rc, out = run(
                ["gh", "api", "-X", "PUT",
                 f"repos/{owner}/{repo_name}/branches/main/protection",
                 "-H", "Accept: application/vnd.github+json",
                 "--input", str(payload_path)],
                dry_run=dry_run, capture=True, check=False,
            )
            # required_signatures sometimes needs a follow-up call on newer API versions
            if rc == 0:
                run(["gh", "api", "-X", "POST",
                     f"repos/{owner}/{repo_name}/branches/main/protection/required_signatures",
                     "-H", "Accept: application/vnd.github.zzzax-preview+json"],
                    dry_run=dry_run, capture=True, check=False)
                ok("Branch protection applied on main.")
                applied_via_gh = True
            else:
                warn("`gh api` failed. Output:")
                if out:
                    info(out)
                warn("Falling back to the web UI walkthrough.")
            payload_path.unlink(missing_ok=True)

    if not applied_via_gh:
        settings_url = (repo_url.removesuffix(".git") or "<repo>") + "/settings/branches"
        info(
            f"\nManual branch-protection setup:\n"
            f"  1. Open {settings_url} in your browser.\n"
            "  2. Click 'Add classic branch protection rule' (or 'Add ruleset').\n"
            "  3. Branch name pattern: main\n"
            "  4. Configure these checkboxes EXACTLY:\n"
            "       ☑  Require signed commits     ← REJECTS unsigned commits (ADR-001)\n"
            "       ☐  Allow force pushes          ← KEEPS history immutable\n"
            "       ☐  Allow deletions             ← Branch can't be deleted\n"
            "       ☐  Require pull request before merging\n"
            "  5. Click 'Create'.\n"
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
            "  - The Ledger, signing keys, and most of the framework still work.\n"
            "  - R5 Brain Health Check will NOT have a Brain to scan until you install Curator.\n"
            "  - The my-curator MCP in Claude Desktop will fail until the Curator app is running.\n\n"
            "When you're ready to install:\n"
            "  curl -fsSL https://raw.githubusercontent.com/talirezun/the-curator/main/install.sh | bash\n\n"
            f"Then re-run this wizard with --resume; we'll pick up at this step and finish wiring it\n"
            f"to your firm folder ({locations.get('firm_folder')}).\n"
        )
        mark_step_done(state, "step_11_curator")
        return

    explainer(
        "What this step does and why",
        "The Curator is the desktop app that turns your firm's documents into a\n"
        "queryable knowledge graph (the 'Brain' in framework terms). Claude talks\n"
        "to it via the my-curator MCP server running locally on your machine.\n"
        "Without it, the Routines have nothing to read or write — so this step is\n"
        "essential.\n\n"
        "Configuration B (greenfield, what you picked): we install Curator, point\n"
        "it at your firm folder, configure ingest with a free Gemini API key, and\n"
        "wire its MCP into Claude Desktop. Some bits are programmatic; the first-run\n"
        "wizard (API key + permissions) needs human eyes.\n\n"
        "Repo + docs: https://github.com/talirezun/the-curator",
    )

    if mode == "use-existing" or locations.get("existing_curator"):
        info(
            "\n— Configuration A: existing Curator detected —\n\n"
            f"We will add a new domain `{locations['curator_domain']}` to your\n"
            f"existing vault at {locations['curator_vault']}.\n\n"
            "In the Curator app (open it now if it's not running):\n"
            "  1. Click 'Domains' in the left sidebar → 'Create domain'.\n"
            f"  2. Name:        {locations['curator_domain']}\n"
            f"  3. Description: {state['firm_profile']['name']} — operational Ledger\n"
            "  4. Click Create.\n\n"
            "Then in Claude Desktop, open a new chat and type:\n"
            "  > Use my-curator. List domains.\n"
            f"You should see `{locations['curator_domain']}` listed alongside any\n"
            "domains you already had.\n"
        )
    else:
        info("\n— Configuration B: greenfield install —")
        info("\n[11a] Install the Curator desktop app.")
        installed = False
        if ask_confirm(
            "Run Curator's one-line installer from here? "
            "(Recommended — saves opening a new Terminal. Downloads + installs the app.)",
            default=True,
        ):
            info("  Fetching Curator's installer (this is the same one-liner from the project's README)...")
            # We can't `curl | bash` directly without giving up our wizard's stdin/stdout
            # cleanly, but we CAN download the script and exec it as a child process.
            installer_url = "https://raw.githubusercontent.com/talirezun/the-curator/main/install.sh"
            tmp_installer = Path("/tmp/oot-curator-install.sh")
            rc, _ = run(["curl", "-fsSL", "-o", str(tmp_installer), installer_url],
                        dry_run=dry_run, capture=True, check=False)
            if rc == 0 and tmp_installer.exists():
                ok(f"Downloaded → {tmp_installer}")
                info("  Running the installer now (3-5 minutes; you may see Curator's own progress output)...\n")
                rc2, _ = run(["bash", str(tmp_installer)],
                             dry_run=dry_run, capture=False, check=False)
                if rc2 == 0:
                    ok("Curator app installed.")
                    installed = True
                else:
                    warn("Curator installer returned non-zero. Check its output above for the failure mode.")
            else:
                warn("Could not download the Curator installer (no network? GitHub rate-limit?).")
            tmp_installer.unlink(missing_ok=True)
        if not installed:
            info(
                "\n  Manual install option:\n"
                "    Open a *new* Terminal window (keep this wizard running here), then paste:\n\n"
                "      curl -fsSL https://raw.githubusercontent.com/talirezun/the-curator/main/install.sh | bash\n\n"
                "    Or download the per-OS installer from:\n"
                "      https://github.com/talirezun/the-curator/releases/latest\n"
            )
            ask_confirm("Curator app installed?", default=True)

        info("\n[11b] First-run setup (this part is GUI-only — you'll click through it).")
        info("  Open the Curator app. Its first-run wizard asks for:")
        info("    - API key for ingest (Gemini Flash Lite is recommended — free tier at")
        info("      https://aistudio.google.com/ — or Anthropic Claude if you prefer).")
        info(f"    - Vault folder. Point it at: {locations['firm_folder']}")
        info(f"    - First domain name: {locations['curator_domain']}")
        info("\n  If macOS prompts for filesystem permission:")
        info("    System Settings → Privacy & Security → Files and Folders → Curator")
        info("    → toggle relevant folder access ON. Then quit and reopen Curator.")

        info("\n[11c] Wire my-curator MCP into Claude Desktop.")
        info("  The Curator's first-run wizard shows you an MCP config snippet to copy.")
        info("  In Claude Desktop:")
        info("    Settings (⌘,) → Developer → Edit Config → paste into mcpServers block.")
        info("  Then quit Claude Desktop fully (⌘Q) and reopen. The my-curator MCP")
        info("  should show a green checkmark in the bottom-left tools panel.")
        info("\n  Verify in a new Claude chat:")
        info("    > Use my-curator. List domains.")
        info(f"  Expected output: `{locations['curator_domain']}` listed.")
    if not ask_confirm("Curator integration complete (Curator running + MCP green)?", default=True):
        info("Pausing here. Re-run the bootstrap to resume.")
        sys.exit(0)
    mark_step_done(state, "step_11_curator")


def step_12_routines(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_12_routines"):
        return
    header("Step 12 / 14 — Configure Day-1 Routines", level=2)
    modules = state.get("modules_chosen", {})
    chosen = modules.get("routines", [])

    schedules = {
        "R5": ("Sunday 09:00",      "Brain Health Check",         "firm/brain-health"),
        "R6": ("daily 23:00",       "EU AI Act Audit Trail",      "firm/audit-logs"),
        "R7": ("PR webhook",        "Klarna Test gate",           None),  # verified differently
        "R1": ("daily 18:00",       "Daily Output Capture",       "firm/output-logs"),
        "R2": ("Friday 08:00",      "Weekly BR Prep",             "firm/business-reviews"),
        "R3": ("monthly 1st",       "Partner Acknowledgement",    "firm/partners"),
        "R4": ("monthly 1st",       "Monthly Compensation Calc",  "firm/compensation"),
        "R8": ("quarterly",         "Quarterly Sentiment Sweep",  "firm/brain-health"),
    }
    day1_chosen = [r for r in chosen if r in ("R5", "R6", "R7")]
    deferred = [r for r in chosen if r not in ("R5", "R6", "R7")]

    explainer(
        "What this step does and why",
        "Routines are Anthropic's hosted scheduled agents — they run on Anthropic's\n"
        "cloud (not your laptop) and commit signed changes back to your Ledger.\n"
        "Day-1 Routines we recommend:\n\n"
        "  R5  Brain Health Check  — Sundays 09:00; writes firm/brain-health/<YYYY-WW>.md\n"
        "  R6  EU AI Act Audit Trail — daily 23:00; writes firm/audit-logs/<YYYY-MM-DD>.md\n"
        "  R7  Klarna Test gate    — PR webhook; blocks merges that fail the Klarna test\n\n"
        "Routine creation is the ONE step we can't fully automate yet — there's no\n"
        "headless `claude routines create` command. You'll create each Routine\n"
        "interactively via Claude Code's `/schedule` command or the web dashboard at\n"
        "https://claude.ai/code/routines. After each, we'll verify the Routine\n"
        "actually worked by checking your Ledger for the file it should commit.",
    )

    if not day1_chosen:
        info("No Day-1 Routines selected at Step 5. Skipping the walkthrough.")
        if deferred:
            info(f"Deferred (need partner data first): {', '.join(deferred)}.")
        info("You can configure Routines anytime via Claude Code → /schedule or https://claude.ai/code/routines")
        mark_step_done(state, "step_12_routines")
        return

    info(
        f"\nYou selected: {', '.join(day1_chosen)} for Day-1."
        + (f"\nDeferred (will set up later when prerequisites are met): {', '.join(deferred)}." if deferred else "")
    )

    owner = state.get("ledger_repo_owner")
    repo_name = state.get("ledger_repo_name")
    can_verify_via_gh = gh_available_and_authed() and owner and repo_name

    for r in day1_chosen:
        sched, name, watch_dir = schedules[r]
        info(f"\n--- {r} ({name}) — setup ---")
        info(f"  Routine prompt body:  routines/cloud/{r}.md  ({REPO_ROOT / 'routines' / 'cloud' / (r + '.md')})")
        info(f"  Schedule:             {sched}")
        info(f"  GitHub connector:     {state.get('ledger_repo_url', '<repo>')} (with signing key from Step 9)")
        info("\n  In Claude Code (CLI or desktop app):")
        info("    /schedule  →  New Routine  →  upload the prompt body file above")
        info("    Attach the my-curator MCP. Configure the GitHub connector with your")
        info("    Ledger URL and the signing key from Step 9. Save.")
        info("\n  Web alternative: https://claude.ai/code/routines  →  'New Routine'")
        info("\n  Once saved: click 'Run now' (or `/run-now` in the CLI) to do a test fire.")

        configured = ask_confirm(f"{r} created and manually fired once?", default=True)
        if not configured:
            warn(f"{r} skipped. Re-run wizard later to come back to it.")
            continue

        # Programmatic verification — check for the file the Routine should have committed.
        if can_verify_via_gh and watch_dir:
            info(f"\n  Verifying {r} by checking {watch_dir}/ in your Ledger...")
            rc, out = run(
                ["gh", "api", f"repos/{owner}/{repo_name}/contents/{watch_dir}",
                 "--jq", ".[] | .name"],
                capture=True, check=False,
            )
            if rc == 0 and out.strip():
                files = [ln for ln in out.strip().splitlines() if ln and ln != ".gitkeep"]
                if files:
                    ok(f"Found {len(files)} file(s) in {watch_dir}/ — Routine appears to be working.")
                    info(f"     Latest: {files[-1]}")
                else:
                    warn(f"  {watch_dir}/ exists but has no Routine-written files yet.")
                    info(f"     The Routine may still be running. Check logs at: https://claude.ai/code/routines")
                    info(f"     Or verify manually: {state.get('ledger_repo_url', '<repo>').removesuffix('.git')}/tree/main/{watch_dir}")
            else:
                warn(f"  Could not read {watch_dir}/ via gh API (it may not exist yet, or the Routine errored).")
                info(f"     Inspect logs: https://claude.ai/code/routines")
        elif r == "R7":
            info("  R7 verification: this is a PR-webhook routine; no file output to check.")
            info("     Verify by opening a test PR with an AI-replaces-human label and watching for the oot/klarna-test status check.")
        else:
            info("  (Programmatic verification needs the `gh` CLI authenticated. Skip — manual verification:")
            info(f"     Visit {state.get('ledger_repo_url', '<repo>').removesuffix('.git')}/tree/main/{watch_dir or 'firm'}")
            info("     and look for the file the Routine should have written.)")

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

    info("\n[3/3] Ledger folder structure:")
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
        f"{state.get('ledger_repo_url', '<not configured>')}\n"
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

    # Must run BEFORE any questionary / prompt_toolkit call. Avoids macOS
    # kqueue rejecting our TTY fd (see _force_select_event_loop_on_macos doc).
    _force_select_event_loop_on_macos()
    _reattach_stdin_to_tty_if_needed()

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

    # Step navigator. Each entry: (state-key, human-label, fn).
    # `_GoBack` raised from a step rewinds one position; later steps' state is
    # preserved so the user only re-confirms what they want to change.
    steps = [
        ("step_00_welcome",          "Welcome",               step_00_welcome),
        ("step_01_preflight",        "Preflight",             step_01_preflight),
        ("step_02_python_venv",      "Python venv",           step_02_python_venv),
        ("step_03_locations",        "Locations",             step_03_locations),
        ("step_04_firm_profile",     "Firm profile",          step_04_firm_profile),
        ("step_05_module_selection", "Module selection",      step_05_module_selection),
        ("step_06_github_plan_tier", "GitHub plan tier",      step_06_github_plan_tier),
        ("step_07_anthropic_check",  "Anthropic check",       step_07_anthropic_check),
        ("step_08_brain_repo",       "Ledger",            step_08_brain_repo),
        ("step_09_signing_key",      "Signing key",           step_09_signing_key),
        ("step_10_branch_protection","Branch protection",     step_10_branch_protection),
        ("step_11_curator",          "Curator",               step_11_curator),
        ("step_12_routines",         "Routines",              step_12_routines),
        ("step_13_smoke_test",       "Smoke test",            step_13_smoke_test),
        ("step_14_summary",          "Summary",               step_14_summary),
    ]

    try:
        i = 0
        while i < len(steps):
            key, label, fn = steps[i]
            try:
                fn(state, args.dry_run)
            except _GoBack:
                if i == 0:
                    warn("Already at the first step — nothing to go back to.")
                    continue
                prev_key, prev_label, _ = steps[i - 1]
                info(f"← Going back to: {prev_label}")
                clear_step_done(state, key, prev_key)
                i -= 1
                continue
            i += 1
    except KeyboardInterrupt:
        warn("\nInterrupted. State saved at " + str(STATE_FILE) + ". Re-run with --resume to continue.")
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
