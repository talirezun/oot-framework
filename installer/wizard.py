#!/usr/bin/env python3
"""ØØT Installer Wizard v1.1.0 — terminal-based, guided install.

Entry point: `python3 installer/wizard.py` or `oot-wizard` (after `pip install -e .`).

Path B of the install-path overhaul. For founders who explicitly avoid using a
coding agent (Path A) but want a guided form rather than the manual docs (Path C).
Mirrors the 17-step structure of `installer/agent-assisted/cloud-install-plan.md`.

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

WIZARD_VERSION = "1.2.0"
OOT_HOME = Path(os.environ.get("OOT_HOME", Path.home() / ".oot"))
STATE_FILE = OOT_HOME / "wizard-state.yaml"
VENV_DIR = OOT_HOME / "venv"

# Module-level dry-run flag. Set once in main() from --dry-run. When True,
# save_state()/mark_step_done() become no-ops so a dry-run never persists
# progress to ~/.oot/wizard-state.yaml (which would poison a later real run).
DRY_RUN = False

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
        # questionary.select(...).ask() returns None when the user hits Ctrl-C /
        # Esc. Returning None here would crash every caller that does
        # `.startswith(...)` on the result. Re-prompt once; a second cancel is
        # treated as an intentional quit (progress is already saved).
        answer = questionary.select(prompt, choices=choices, default=default).ask()
        if answer is None:
            warn("Cancelled. Press Ctrl-C again to quit, or pick an option.")
            answer = questionary.select(prompt, choices=choices, default=default).ask()
            if answer is None:
                info("Exiting. Your progress is saved — resume with the same one-liner.")
                sys.exit(0)
        return answer
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


def _mask_secrets_in_cmd(cmd_str: str) -> str:
    """Redact credentials embedded in a URL before echoing a command.

    Catches the `https://<token>@github.com/...` and `https://user:<token>@host`
    forms we build for authenticated clones/pushes. Without this the PAT would
    be printed verbatim in the `$ ...` echo and captured in any scrollback/log.
    """
    import re as _re
    # https://TOKEN@host  or  https://user:TOKEN@host  → keep host, hide creds.
    return _re.sub(
        r"(https?://)([^/\s@]+)@",
        lambda m: f"{m.group(1)}***@",
        cmd_str,
    )


def run(cmd: list[str], dry_run: bool = False, capture: bool = False, check: bool = False) -> tuple[int, str]:
    """Run a shell command. Returns (returncode, stdout). On dry-run, prints and returns (0, '')."""
    cmd_str = _mask_secrets_in_cmd(" ".join(cmd))
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


def run_critical(cmd: list[str], what: str, dry_run: bool = False,
                 capture: bool = False) -> bool:
    """Run a command whose failure must NOT be silently swallowed.

    Returns True on success (rc == 0), False on failure. On failure prints a
    friendly, actionable message telling the user to fix the underlying problem
    and re-run with --resume. Used for the money/trust-path commands: git push,
    gpg --gen-key, git commit -S — where a silent failure would leave the
    install in a broken-but-marked-done state.
    """
    rc, out = run(cmd, dry_run=dry_run, capture=capture, check=False)
    if dry_run:
        return True
    if rc != 0:
        err(f"{what} failed (exit {rc}).")
        if capture and out:
            info(out.strip())
        warn("This step did NOT complete. Fix the problem above, then re-run the "
             "installer with --resume to retry from here — we won't mark this step done.")
        return False
    return True


def parse_gpg_key_ids(colon_output: str) -> list[str]:
    """Extract long key IDs from `gpg --list-secret-keys --with-colons` output.

    Each secret key is a `sec:` record; field 5 (0-indexed 4) is the long key ID.
    Returns them most-recent-first as gpg lists them. Pure function — unit-tested
    against a fixture so we never regress the field index.
    """
    ids: list[str] = []
    for line in colon_output.splitlines():
        fields = line.split(":")
        if fields and fields[0] == "sec" and len(fields) > 4 and fields[4]:
            ids.append(fields[4])
    return ids


def auto_detect_signing_key_id(dry_run: bool = False) -> Optional[str]:
    """Return the machine's GPG signing key ID by parsing --with-colons output.

    Returns the single key if exactly one exists, or None if zero / ambiguous
    (multiple keys) so the caller can fall back to asking the user to pick.
    """
    rc, out = run(["gpg", "--list-secret-keys", "--with-colons"],
                  dry_run=dry_run, capture=True, check=False)
    if rc != 0:
        return None
    ids = parse_gpg_key_ids(out)
    if len(ids) == 1:
        return ids[0]
    return None


def which(cmd: str) -> Optional[str]:
    return shutil.which(cmd)


def venv_bin(venv_dir: Path, exe: str) -> Path:
    """Return the path to an executable inside a venv, cross-platform.

    POSIX venvs put executables under `bin/`; Windows venvs use `Scripts\\` and
    add a `.exe` suffix. Native Windows support for the wizard is only partial
    (the install plans assume POSIX / WSL), but at least the venv paths resolve
    correctly if someone runs it there.
    """
    if os.name == "nt":
        name = exe if exe.endswith(".exe") else f"{exe}.exe"
        return venv_dir / "Scripts" / name
    return venv_dir / "bin" / exe


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

# v1.0.1 → v1.1.0: a new Second Brain bridge step was inserted between Curator
# (11) and Routines (was 12). Existing state files have step_12_routines /
# step_13_smoke_test / step_14_summary marked done; renumber so the navigator
# keeps resuming at the right place.
_STATE_STEP_RENAMES = {
    "step_12_routines":    "step_13_routines",
    "step_13_smoke_test":  "step_14_smoke_test",
    "step_14_summary":     "step_15_summary",
}


def _migrate_state_keys(state: dict[str, Any]) -> dict[str, Any]:
    """Backward-compat: promote pre-rename state keys to current names."""
    for old, new in _STATE_KEY_RENAMES.items():
        if old in state and new not in state:
            state[new] = state.pop(old)
    # Renumber completed-step flags for the v1.1.0 step-insert.
    steps_completed = state.get("steps_completed", {})
    for old, new in _STATE_STEP_RENAMES.items():
        if old in steps_completed and new not in steps_completed:
            steps_completed[new] = steps_completed.pop(old)
    # If the user has step_13_routines marked done from a pre-bridge install
    # but the new bridge step isn't done, reset step_13_routines so they re-
    # configure the Routines with the new Second Brain connector. Stale
    # connectors won't have the new repo wired.
    if ("step_13_routines" in steps_completed
            and "step_12_secondbrain_sync" not in steps_completed):
        steps_completed.pop("step_13_routines", None)
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
    if DRY_RUN:
        # Dry-run never touches the on-disk state file. In-memory `state`
        # still carries answers forward so the walkthrough flows normally.
        return
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


def resolve_track(state: dict[str, Any], cli_track: str, resume: bool) -> dict[str, Any]:
    """Return the firm_profile dict with a correctly-resolved `track`.

    On --resume, a track already saved in the state file WINS over the argparse
    default. Argparse always supplies a `--track` value (default "cloud"), so a
    naive `profile["track"] = args.track` would silently flip a resumed
    privacy-track install back to cloud. When resuming with an existing saved
    track we keep it; otherwise (fresh run, or no saved track) we take the CLI
    value. Pure function so it can be unit-tested without argparse/IO.
    """
    profile = dict(state.get("firm_profile", {}) or {})
    saved = profile.get("track")
    if resume and saved:
        profile["track"] = saved
    else:
        profile["track"] = cli_track
    return profile


# ----- the 17 steps ---------------------------------------------------------

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
            "From here, this wizard asks you ~17 questions and walks you through every\n"
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
    if is_step_done(state, "step_01_preflight"):
        # Resume path: reuse the interpreter we already validated + saved.
        return (state.get("preflight", {}).get("python")
                or state.get("oot_python")
                or sys.executable)
    header("Step 1 / 17 — Preflight: required tools", level=2)

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
    header("Step 2 / 17 — Python virtual environment", level=2)
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
    venv_pip = venv_bin(VENV_DIR, "pip")
    if not dry_run and venv_pip.exists():
        run([str(venv_pip), "install", "openpyxl", "pyyaml", "httpx", "questionary", "rich"],
            dry_run=False, capture=False, check=False)
    state["venv_path"] = str(VENV_DIR)
    ok(f"venv ready at {VENV_DIR}")
    mark_step_done(state, "step_02_python_venv")


def step_03_locations(state: dict[str, Any], dry_run: bool) -> dict[str, str]:
    if is_step_done(state, "step_03_locations"):
        return state.get("locations", {})
    header("Step 3 / 17 — Choose locations", level=2)

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
    while not firm_slug_default.strip():
        warn("Firm slug is required — it names your local folder and both GitHub repos.")
        firm_slug_default = ask_text("Firm slug (lowercase-hyphenated, e.g. 'acme-studio')",
                                     default=prior.get("firm_slug") or None)
    firm_slug_default = firm_slug_default.strip()
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
            else "B — Unified: firm repo IS the Curator vault (recommended for greenfield)"
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
    header("Step 4 / 17 — Firm profile", level=2)

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
    header("Step 5 / 17 — Module selection (choose what to install)", level=2)

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
        info(f"  Foundation:        {', '.join(modules['foundation']) or '(none)'}")
        info(f"  Curator:           {modules['curator_mode']}")
        info(f"  Skill packs:       {', '.join(modules['skills']) or '(none)'}")
        info(f"  Routines now:      {', '.join(modules['routines']) or '(none)'}")
        info(f"  Security:          {', '.join(modules['security']) or '(none)'}")
        # Indicate whether the Second Brain bridge will be set up at Step 13.
        track = state.get("firm_profile", {}).get("track", "cloud")
        will_bridge = (
            track == "cloud"
            and modules["curator_mode"] != "skip-for-now"
            and "R5" in modules["routines"]
        )
        if will_bridge:
            info(f"  Second Brain:      bridge will be set up at Step 13 "
                 f"(R5 will reach the Curator graph via GitHub-sync)")
        elif track == "privacy":
            info(f"  Second Brain:      not needed — privacy MCP runs alongside Routines")
        elif modules["curator_mode"] == "skip-for-now":
            info(f"  Second Brain:      skipped — no Curator means no Second Brain to bridge")
        elif "R5" not in modules["routines"]:
            info(f"  Second Brain:      not set up (no R5 selected — R5 is the only "
                 f"Day-1 Routine that needs it)")
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
    header("Step 6 / 17 — GitHub plan-tier choice (CRITICAL)", level=2)
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
    header("Step 7 / 17 — Anthropic check", level=2)
    explainer(
        "What this step does and why",
        "Two Anthropic products you'll need:\n\n"
        "  - Claude Desktop  — the chat app. This is where the my-curator MCP runs.\n"
        "    Download free: https://claude.com/download\n\n"
        "  - Claude Code CLI (or web dashboard at claude.ai/code/routines) — used to\n"
        "    create and manage Routines at Step 14. Either works.\n\n"
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
    if plan == "pro" and (profile.get("partner_count_estimate", "").startswith(("medium", "large"))
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
    header("Step 8 / 17 — Create the Ledger + Firm Brain GitHub repos", level=2)

    locations = state["locations"]
    profile = state["firm_profile"]
    firm_slug = locations["firm_slug"]
    firm_folder = Path(locations["firm_folder"])
    plan_tier = profile.get("github_plan_tier", "free")
    visibility = "public" if plan_tier == "public" else "private"

    explainer(
        "What this step does and why",
        "Per ADR-002 your firm uses TWO GitHub repos:\n\n"
        "  - The Ledger (<firm-slug>-ledger): your operational state — Excel files,\n"
        "    output logs, audit logs. Mutated by Routines via signed commits per ADR-001.\n"
        "  - The Firm Brain (<firm-slug>-brain): a Curator Shared Brain instance —\n"
        "    synthesized firm IP (theses, decisions, ADRs, partner profiles).\n"
        "    Populated by partners pushing from their personal Curators; synthesized\n"
        "    weekly by the admin (you, the founder).\n\n"
        "This step does FIVE things:\n\n"
        "  1. Creates a folder on YOUR machine (the Ledger's local clone).\n"
        "  2. Scaffolds the firm/ subfolder structure (excel/, output-logs/, etc.)\n"
        "     and copies in the 9 Excel templates from the framework.\n"
        "  3. Makes the first commit (unsigned for now — signing key comes next step).\n"
        "  4. Creates the LEDGER GitHub repo and pushes everything to it.\n"
        "  5. Creates the FIRM BRAIN GitHub repo (empty — Curator populates it in Step 11).\n\n"
        "If your `gh` CLI is installed and you're logged in, steps 4+5 are one command\n"
        "each. Otherwise we walk you through clicking through github.com.",
    )

    # --- Substep 1: local folder + git init -------------------------------
    info("\n[1/4] Local folder + git init")
    if dry_run:
        info(f"  (dry-run) would create folder + git init at {firm_folder}")
    else:
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
    excel_dst = firm_folder / "firm" / "excel"
    if dry_run:
        info(f"  (dry-run) would scaffold firm/ subfolders {subfolders} and copy "
             f"{len(list(TEMPLATES_EXCEL.glob('*.xlsx')))} .xlsx templates into firm/excel/")
    else:
        for sub in subfolders:
            (firm_folder / "firm" / sub).mkdir(parents=True, exist_ok=True)
            if sub != "excel":
                gitkeep = firm_folder / "firm" / sub / ".gitkeep"
                if not gitkeep.exists():
                    gitkeep.touch()
        for xlsx in TEMPLATES_EXCEL.glob("*.xlsx"):
            shutil.copy2(xlsx, excel_dst / xlsx.name)
        ok(f"Copied {len(list(excel_dst.glob('*.xlsx')))} .xlsx templates to firm/excel/")

    readme = firm_folder / "README.md"
    if not dry_run and not readme.exists():
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
    info("\n[4/5] Create the Ledger GitHub repo + push")
    repo_name_default = f"{firm_slug}-ledger"
    repo_name = ask_text("Ledger repository name on GitHub", default=repo_name_default)

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
            if not run_critical(["git", "push", "-u", "origin", "main"],
                                "Push to origin/main", dry_run=dry_run, capture=True):
                info("Pausing. Re-run the bootstrap with --resume once the push succeeds.")
                sys.exit(0)

    # --- Substep 5: create the Firm Brain repo (empty) --------------------
    info("\n[5/5] Create the Firm Brain GitHub repo (empty — Curator populates it in Step 11)")
    explainer(
        "Why an empty repo here",
        "The Firm Brain is a Curator Shared Brain — Curator's admin wizard (Step 11)\n"
        "will populate it with `contributions/`, `collective/`, `state/`, etc. We just\n"
        "need the empty repo to exist on GitHub so Curator can push the initial scaffold.",
    )

    fb_repo_name_default = f"{firm_slug}-brain"
    fb_repo_name = ask_text("Firm Brain repository name on GitHub", default=fb_repo_name_default)

    # Confirm it differs from the Ledger repo name
    if fb_repo_name == repo_name:
        warn(
            f"The Firm Brain repo name ('{fb_repo_name}') is the same as the Ledger\n"
            f"repo name. They MUST be different. Picking '{fb_repo_name_default}-firm' instead — \n"
            f"or you can override with another name."
        )
        fb_repo_name = ask_text("Firm Brain repository name (must differ from Ledger)",
                                default=f"{firm_slug}-firm-brain")

    fb_repo_created_via_gh = False
    if gh_available_and_authed():
        login = gh_user_login() or "(you)"
        fb_full_repo = f"{login}/{fb_repo_name}"
        if ask_confirm(
            f"Create the Firm Brain repo {fb_full_repo} (private) automatically via `gh`? "
            "(recommended — empty repo, no push)",
            default=True,
        ):
            info(f"  Creating {fb_full_repo}...")
            rc, out = run(
                ["gh", "repo", "create", fb_full_repo,
                 "--private",
                 "--description", f"ØØT Firm Brain for {profile['name']} — Curator Shared Brain (synthesized firm IP)"],
                dry_run=dry_run, capture=True, check=False,
            )
            if rc == 0:
                ok(f"Firm Brain repo created: https://github.com/{fb_full_repo}")
                state["firm_brain_repo_url"] = f"https://github.com/{fb_full_repo}.git"
                state["firm_brain_repo_owner"] = login
                state["firm_brain_repo_name"] = fb_repo_name
                fb_repo_created_via_gh = True
            else:
                warn("`gh repo create` for Firm Brain failed. Output:")
                if out:
                    info(out)
                warn("Falling back to the web UI walkthrough.")

    if not fb_repo_created_via_gh:
        info(
            "\n  Manual Firm Brain repo creation:\n"
            f"    1. Open https://github.com/new in your browser.\n"
            f"    2. Repository name:        {fb_repo_name}\n"
            f"    3. Description:            ØØT Firm Brain for {profile['name']} — Curator Shared Brain\n"
            f"    4. Visibility:             Private (always private for the Firm Brain)\n"
            f"    5. Initialize:             leave ALL THREE checkboxes UNCHECKED\n"
            f"    6. Click 'Create repository'.\n"
        )
        if not ask_confirm("Firm Brain repo created on GitHub.com?", default=True):
            info("Pausing. Re-run the bootstrap to resume.")
            sys.exit(0)
        fb_repo_url = ask_text(
            "Firm Brain repo HTTPS URL",
            default=f"https://github.com/<you>/{fb_repo_name}.git",
        )
        if not fb_repo_url.endswith(".git"):
            fb_repo_url = fb_repo_url.rstrip("/") + ".git"
        state["firm_brain_repo_url"] = fb_repo_url

    mark_step_done(state, "step_08_brain_repo")


def step_09_signing_key(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_09_signing_key"):
        return
    header("Step 9 / 17 — Generate signing key + upload to GitHub", level=2)

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
             "We'll still configure git to sign with your existing key.")
        existing_key = auto_detect_signing_key_id(dry_run=dry_run)
        if existing_key:
            ok(f"Detected exactly one signing key: {existing_key}")
            if not ask_confirm(f"Use key {existing_key}?", default=True):
                existing_key = None
        if not existing_key:
            rc, out = run(["gpg", "--list-secret-keys", "--keyid-format=long"],
                          capture=True, check=False)
            info_plain(out)
            existing_key = ask_text(
                "Paste the key ID (the long hex after 'sec rsa4096/' or 'sec ed25519/')").strip()
        else:
            existing_key = existing_key.strip()
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
        gen_ok = run_critical(["gpg", "--batch", "--gen-key", str(batch_path)],
                              "GPG key generation", dry_run=False, capture=True)
        batch_path.unlink(missing_ok=True)
        if not gen_ok:
            info("Pausing. Fix the gpg error above, then re-run with --resume.")
            return  # NOT marked done — --resume retries this step

    # Auto-detect the key ID by parsing machine-readable colon output; only ask
    # the user if we can't unambiguously determine it (0 or >1 secret keys).
    key_id = auto_detect_signing_key_id(dry_run=dry_run)
    if key_id:
        ok(f"Detected your new signing key ID automatically: {key_id}")
        if not ask_confirm(f"Use key {key_id} for signing?", default=True):
            key_id = None
    if not key_id:
        rc, out = run(["gpg", "--list-secret-keys", "--keyid-format", "LONG"],
                      dry_run=dry_run, capture=True)
        info_plain(out)
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
        if not run_critical(["git", "commit", "-S", "-m", "verify: signing key works"],
                            "Signed test commit", capture=True):
            info("The signing key isn't working yet. Common causes: the key ID is wrong,\n"
                 "gpg can't find the key, or git isn't pointed at the right gpg.program.\n"
                 "Fix the error above, then re-run with --resume.")
            return  # NOT marked done — --resume retries this step
        run(["git", "log", "--show-signature", "-1"], capture=False, check=False)

        if ask_confirm("Push the verification commit?", default=True):
            if run_critical(["git", "push", "origin", "main"],
                            "Push verification commit", capture=True):
                info(
                    f"\n→ Open {state.get('ledger_repo_url', '<repo>')}/commits/main in your browser.\n"
                    f"  The latest commit should have a green Verified badge.\n"
                    f"  If not: see docs/00-quickstart-cloud.md 'Step 6' troubleshooting."
                )
            else:
                info("Pausing. Re-run with --resume once the push succeeds.")
                return  # NOT marked done
    mark_step_done(state, "step_09_signing_key")


def step_10_branch_protection(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_10_branch_protection"):
        return
    header("Step 10 / 17 — Branch protection on main", level=2)
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
            f"\nManual branch-protection setup (Ledger):\n"
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
        if not ask_confirm("Branch protection rule (Ledger) created?", default=True):
            info("Pausing.")
            sys.exit(0)

    # --- Now also do the Firm Brain repo (ADR-002) ------------------------
    header("Step 10b — Branch protection on the Firm Brain repo", level=3)
    explainer(
        "Why also on the Firm Brain",
        "Per ADR-002, the Firm Brain repo (<firm-slug>-brain) holds Curator's\n"
        "synthesized firm IP with UUID Provenance attribution and the GDPR Article 17\n"
        "revoke audit log. Without branch protection, force-push or unsigned-commit\n"
        "would compromise those guarantees. Same checkbox configuration as the Ledger.",
    )
    fb_url = state.get("firm_brain_repo_url", "")
    fb_owner = state.get("firm_brain_repo_owner")
    fb_name = state.get("firm_brain_repo_name")
    fb_applied_via_gh = False
    if gh_available_and_authed() and fb_owner and fb_name:
        if ask_confirm(
            f"Apply identical branch protection to the Firm Brain ({fb_owner}/{fb_name}) "
            "automatically via `gh api`?",
            default=True,
        ):
            fb_payload = {
                "required_status_checks": None,
                "enforce_admins": True,
                "required_pull_request_reviews": None,
                "restrictions": None,
                "required_signatures": True,
                "allow_force_pushes": False,
                "allow_deletions": False,
            }
            fb_payload_path = Path("/tmp/oot-firm-brain-branch-protection.json")
            import json as _json
            fb_payload_path.write_text(_json.dumps(fb_payload))
            rc, out = run(
                ["gh", "api", "-X", "PUT",
                 f"repos/{fb_owner}/{fb_name}/branches/main/protection",
                 "-H", "Accept: application/vnd.github+json",
                 "--input", str(fb_payload_path)],
                dry_run=dry_run, capture=True, check=False,
            )
            # On a freshly-created empty Firm Brain repo without a `main` branch yet,
            # branch protection cannot be applied. Curator's admin wizard (Step 11)
            # will create the initial commit on main; THEN we can apply protection.
            # If `gh api` fails with 404 here, surface that and defer.
            if rc == 0:
                run(["gh", "api", "-X", "POST",
                     f"repos/{fb_owner}/{fb_name}/branches/main/protection/required_signatures",
                     "-H", "Accept: application/vnd.github.zzzax-preview+json"],
                    dry_run=dry_run, capture=True, check=False)
                ok("Branch protection applied on Firm Brain main.")
                fb_applied_via_gh = True
            else:
                if "404" in (out or "") or "Branch not found" in (out or ""):
                    warn(
                        "Firm Brain has no `main` branch yet (the repo is empty until\n"
                        "Curator's admin wizard pushes the first commit in Step 11).\n"
                        "We'll re-apply branch protection on Firm Brain at the end of Step 11."
                    )
                    state["firm_brain_protection_deferred"] = True
                else:
                    warn("`gh api` failed for Firm Brain. Output:")
                    if out:
                        info(out)
            fb_payload_path.unlink(missing_ok=True)

    if not fb_applied_via_gh and not state.get("firm_brain_protection_deferred"):
        fb_settings_url = (fb_url.removesuffix(".git") or "<firm-brain-repo>") + "/settings/branches"
        info(
            f"\nManual branch-protection setup (Firm Brain):\n"
            f"  1. After Curator's admin wizard (Step 11) makes the first commit on the\n"
            f"     Firm Brain repo's main branch, open {fb_settings_url} in your browser.\n"
            f"  2. Apply the SAME branch protection checkboxes as the Ledger above.\n"
            f"  3. Click 'Create'.\n"
            f"  4. Tell the wizard `done` at the end of Step 11."
        )
        state["firm_brain_protection_deferred"] = True

    mark_step_done(state, "step_10_branch_protection")


def step_11_curator(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_11_curator"):
        return
    header("Step 11 / 17 — Curator integration (the second-brain app)", level=2)
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

    # --- Step 11b: Firm Brain admin wizard (Curator Shared Brain) ----------
    header("Step 11b — Firm Brain admin wizard (Curator Shared Brain v3.0.0-beta+)", level=3)
    explainer(
        "What this sub-step does and why",
        "Per ADR-002, your firm's collective knowledge — theses, decisions, ADRs,\n"
        "partner profiles, prompts — lives in the Firm Brain, a Curator Shared Brain\n"
        "instance in the repo you created at Step 8 (`<firm-slug>-brain`). You're the\n"
        "admin. This sub-step walks you through Curator's admin wizard, generates the\n"
        "admin_token + invite token, and verifies the Push → Synthesize → Pull loop.\n\n"
        "Requires Curator v3.0.0-beta+. Older Curator versions don't have the Shared\n"
        "Brain feature — upgrade Curator before continuing.",
    )

    fb_url = state.get("firm_brain_repo_url", "")

    # IP mode decision
    info("\n[11b/1] IP mode for the Firm Brain")
    info("  Curator's `data_handling_terms` field locks once invite tokens are distributed,")
    info("  so pick now:")
    info("    - `organisational` (recommended): copyright in contributions assigns to the firm.")
    info("      Standard for ØØT firms with full-time partners signing the Partner Charter.")
    info("    - `contributor_retains`: copyright stays with contributors; firm owns only the")
    info("      synthesized output. Best for advisor/contractor-heavy firms.")
    ip_mode = ask_select(
        "IP mode",
        choices=["organisational", "contributor_retains"],
        default="organisational",
    )
    state.setdefault("firm_profile", {})["firm_brain_ip_mode"] = ip_mode
    info(f"  ✓ IP mode set to: {ip_mode}")

    # Curator admin wizard (manual — runs in Curator's GUI)
    info("\n[11b/2] Run Curator's admin wizard")
    info(f"  In the Curator desktop app: Shared Brain → Admin Setup.")
    info(f"  Configure with these values:")
    info(f"    - GitHub repo URL:     {fb_url or '<your Firm Brain repo URL>'}")
    info(f"    - Brain name:          {state['firm_profile'].get('name', '<firm name>')}")
    info(f"    - data_handling_terms: {ip_mode}")
    info(f"    - allow_name_attribution: ☐ unchecked (UUID-pseudonymous baseline)")
    info(f"    - attribute_by_name (self):  ☐ unchecked")
    info("  Click 'Generate admin token + invite token'. Two values appear:")
    info("    - admin_token (gates GDPR Article 17 revoke endpoint)")
    info("    - invite token (sbi_...) — what you share with each partner during onboarding")

    if not ask_confirm("Both tokens displayed in Curator?", default=True):
        info("Pausing here. Re-run with --resume after running the admin wizard.")
        sys.exit(0)

    # Persist that tokens were generated (NEVER persist the values themselves)
    info("\n[11b/3] SAVE the tokens to Bitwarden NOW (do not skip this)")
    info("  Open Bitwarden and create two new entries in the 'founders' collection:")
    firm_slug = state.get("locations", {}).get("firm_slug", "<firm-slug>")
    info(f"    1. Name: '{firm_slug} — Curator Shared Brain admin_token'")
    info(f"       Paste the admin_token into the password field.")
    info(f"    2. Name: '{firm_slug} — Firm Brain invite token (sbi_)'")
    info(f"       Paste the invite token (you'll share this with each partner).")

    if not ask_confirm("Both tokens saved to Bitwarden founders collection?", default=True):
        warn("Tokens MUST be saved before continuing — losing the admin_token means you")
        warn("cannot perform GDPR Article 17 revocations without rotating the brain.")
        if not ask_confirm("OK to proceed anyway (you'll save them right after)?", default=False):
            sys.exit(0)
    state["firm_brain_admin_token_saved"] = True
    state["firm_brain_invite_token_saved"] = True

    # Founder runs their own contributor wizard
    info("\n[11b/4] Run your own contributor wizard (founders contribute too)")
    info("  In Curator: Shared Brain → Connect to Brain. Then the six-step wizard:")
    info("    1. Paste your invite token (sbi_...)")
    info("    2. Verify GitHub collaborator access (you own the repo, so this passes)")
    info(f"    3. Create a fine-grained PAT scoped to {fb_url or '<firm-brain-repo>'}")
    info("       (Contents: read+write; Metadata: read).")
    info(f"    4. Select your opted-in domain: {state.get('locations', {}).get('curator_domain', '<domain>')}")
    info(f"    5. Consent to the IP-mode terms ({ip_mode}).")
    info("    6. Save. Connection card with Push/Pull buttons appears.")

    info("\n  Save the PAT to Bitwarden under your **per-partner** collection,")
    info(f"  named '{firm_slug} — Firm Brain contributor PAT (founder)'.")
    if not ask_confirm("Founder contributor wizard complete + PAT saved?", default=True):
        info("Pausing. Re-run with --resume after completion.")
        sys.exit(0)

    # Verify the loop end-to-end
    info("\n[11b/5] Verify Push → Synthesize → Pull end-to-end")
    info("  In Curator (your opted-in domain), create a one-line page:")
    info("    concepts/theses.md  →  'First thesis: <something simple>'")
    info("  Click Push. Then verify on GitHub:")
    info(f"    {fb_url.removesuffix('.git') if fb_url else '<firm-brain-repo>'}/tree/main/contributions/")
    info("  You should see one JSON file (your DeltaSummary payload).")
    if not ask_confirm("First Push verified (JSON file visible in contributions/)?", default=True):
        warn("Push didn't land. Common causes: PAT missing Contents:write; branch protection")
        warn("rejecting unsigned commits; firewall blocking Curator's GitHub API call.")
        sys.exit(0)

    info("\n  Now run Synthesize (admin-only):")
    info("    In Curator: Shared Brain → Run Synthesize.")
    info("  Verify:")
    info(f"    {fb_url.removesuffix('.git') if fb_url else '<firm-brain-repo>'}/tree/main/collective/")
    info(f"    You should see the synthesized concepts/theses.md page with a Provenance block (UUID-attributed).")
    if not ask_confirm("First Synthesize verified (collective/ folder populated)?", default=True):
        sys.exit(0)
    state["firm_brain_first_synthesize_ok"] = True

    info("\n  Now click Pull. Curator downloads the synthesized result into a local")
    info(f"  read-only domain 'shared-{firm_slug}/'. Verify in Claude Desktop:")
    info("    > Use my-curator. List domains.")
    info(f"  You should see both '{state.get('locations', {}).get('curator_domain', '<domain>')}'")
    info(f"  (your personal opted-in domain) AND 'shared-{firm_slug}/' (the read-only mirror).")
    if not ask_confirm("Pull verified (mirror domain visible)?", default=True):
        sys.exit(0)

    # If we deferred branch protection on the Firm Brain at Step 10, apply it now
    if state.get("firm_brain_protection_deferred"):
        info("\n[11b/6] Apply branch protection to the Firm Brain (was deferred at Step 10)")
        info("  Curator's admin wizard has now committed to the Firm Brain repo's main branch,")
        info("  so branch protection can be applied.")
        fb_owner = state.get("firm_brain_repo_owner")
        fb_name = state.get("firm_brain_repo_name")
        applied = False
        if gh_available_and_authed() and fb_owner and fb_name:
            if ask_confirm("Apply branch protection automatically via `gh api`?", default=True):
                fb_payload = {
                    "required_status_checks": None,
                    "enforce_admins": True,
                    "required_pull_request_reviews": None,
                    "restrictions": None,
                    "required_signatures": True,
                    "allow_force_pushes": False,
                    "allow_deletions": False,
                }
                fb_payload_path = Path("/tmp/oot-firm-brain-branch-protection-deferred.json")
                import json as _json
                fb_payload_path.write_text(_json.dumps(fb_payload))
                rc, out = run(
                    ["gh", "api", "-X", "PUT",
                     f"repos/{fb_owner}/{fb_name}/branches/main/protection",
                     "-H", "Accept: application/vnd.github+json",
                     "--input", str(fb_payload_path)],
                    dry_run=dry_run, capture=True, check=False,
                )
                if rc == 0:
                    ok("Branch protection applied on Firm Brain main.")
                    applied = True
                else:
                    warn(f"`gh api` failed: {out}")
                fb_payload_path.unlink(missing_ok=True)
        if not applied:
            fb_settings_url = (fb_url.removesuffix(".git") or "<firm-brain-repo>") + "/settings/branches"
            info(f"  Manual: open {fb_settings_url} and apply the same checkbox configuration as Step 10.")
            ask_confirm("Firm Brain branch protection applied?", default=True)
        state.pop("firm_brain_protection_deferred", None)

    ok("Firm Brain admin setup complete.")
    mark_step_done(state, "step_11_curator")


def step_12_brain_ingest(state: dict[str, Any], dry_run: bool) -> None:
    """Guide the founder to ingest 5-10 seed documents into their firm domain.

    Mirrors cloud-install-plan.md Step 9 (Initial Brain ingest). Entirely a
    walkthrough — the Curator app does the ingestion; the wizard only explains
    what to pick and confirms completion. There is nothing safe to do
    programmatically here (the ingestion runs inside the Curator GUI against a
    cloud-LLM), so this step is confirmation-gated, not DRY_RUN-gated.
    """
    if is_step_done(state, "step_12_brain_ingest"):
        return
    header("Step 12 / 17 — Seed your Brain (initial document ingest)", level=2)

    locations = state.get("locations", {})
    modules = state.get("modules_chosen", {})
    curator_domain = locations.get("curator_domain", "<your-firm-domain>")

    # If the founder skipped Curator entirely, there's nothing to ingest into.
    if modules.get("skip_curator"):
        info("Curator skipped at Step 5 (skip-for-now) — no Brain to ingest into yet.")
        info("When you install Curator later, re-run the wizard and we'll come back here.")
        mark_step_done(state, "step_12_brain_ingest")
        return

    explainer(
        "What this step does and why",
        "A fresh Curator domain is empty — the Routines that read your Brain (R5\n"
        "Brain Health Check especially) have nothing to work with until you feed it\n"
        "a starting set of documents. This one-time ingest gives the knowledge graph\n"
        "its first real content and lets you confirm end-to-end that ingestion +\n"
        "the my-curator MCP are actually working before you wire up automation.\n\n"
        "Pick 5-10 documents that best represent your firm's knowledge. This is a\n"
        "GUI action inside the Curator app — the wizard just tells you what to pick\n"
        "and waits while you drag-and-drop.",
    )

    info(f"\nIngest into domain: {curator_domain}\n")
    info("Good starter documents (pick 5-10 you already have):")
    info("  1. A recent customer contract or SOW")
    info("  2. A strategic memo (your recent thinking / a founding thesis)")
    info("  3. A product spec or technical design doc")
    info("  4. A pitch deck (export to PDF first)")
    info("  5. A meeting transcript (export to plain text)")
    info("")
    info("In the Curator app:")
    info(f"  Ingest → drag-and-drop the files → select domain `{curator_domain}` → run.")
    info("  Ingestion uses your configured cloud-LLM (Gemini Flash Lite / Claude / etc.)")
    info("  and can take a few minutes for a batch this size.")

    if not ask_confirm("Ingestion complete for your starter documents?", default=True):
        info("Pausing here. When ingestion is done, re-run with --resume.")
        sys.exit(0)

    info("\nNow a quick health check. In Claude Desktop, paste:")
    info(f"  > Use my-curator. scan_wiki_health on domain={curator_domain}.")
    info(f"  > Then scan_semantic_duplicates on domain={curator_domain}. Report.")
    info("")
    info("Expected: a clean report. If it flags broken wikilinks, walk through")
    info("`fix_wiki_issue` for each (Claude can do this in the same chat).")

    ask_confirm("Health check run (clean, or issues noted)?", default=True)

    state["brain_ingest_done"] = True
    mark_step_done(state, "step_12_brain_ingest")
    ask_navigation("Brain ingest")


def step_12_secondbrain_sync(state: dict[str, Any], dry_run: bool) -> None:
    """Bridge step: hook Routines into the Second Brain via Curator's GitHub sync.

    The gap this fills: cloud Routines (running on Anthropic's infrastructure)
    cannot reach the user's local my-curator MCP. The bridge is the Curator's
    built-in two-way sync to a private GitHub repo — once that's running, cloud
    Routines clone the synced repo at execution time and read company-context
    knowledge from plain markdown files. See docs/AUTOMATION-PIPELINE.md.

    Migration note (ADR-002, v1.1.0+): the standalone <firm>-secondbrain repo is
    retired as a framework primitive. When the firm has a Firm Brain repo
    (<firm>-brain, created at step 8), prefer pointing the bridge at that repo
    (scan path: collective/<firm-domain>/wiki/) instead of provisioning a
    separate secondbrain repo. Full retirement of this step lands in v1.3.
    """
    if is_step_done(state, "step_12_secondbrain_sync"):
        return
    header("Step 13 / 17 — Connect Routines to your Second Brain (the bridge)", level=2)

    profile = state.get("firm_profile", {})
    track = profile.get("track", "cloud")
    modules = state.get("modules_chosen", {})
    locations = state.get("locations", {})

    # Privacy track has no gap — my-curator MCP runs locally alongside Routines.
    if track == "privacy":
        info("Privacy track detected. The my-curator MCP runs locally on your")
        info("always-on machine alongside the Routines themselves, so there is no gap")
        info("to bridge. Skipping this step.")
        info("(If you switch to cloud track later, re-run with --resume.)")
        mark_step_done(state, "step_12_secondbrain_sync")
        return

    # If user opted out of Curator entirely, skip — no Second Brain exists.
    if modules.get("skip_curator"):
        info("Curator skipped at Step 5 (skip-for-now). No Second Brain to bridge.")
        info("When you install Curator later, re-run the wizard and we'll wire it up.")
        mark_step_done(state, "step_12_secondbrain_sync")
        return

    curator_domain = locations.get("curator_domain") or profile.get("name", "<firm>").lower().replace(" ", "-")

    explainer(
        "What this step does and why",
        "Your Curator app stores the firm's Second Brain locally — its 17 MCP tools\n"
        "(semantic search, graph traversal, scan_wiki_health, etc.) only run on YOUR\n"
        "machine. Cloud-hosted Routines on Anthropic's infrastructure can't reach\n"
        "your local MCP. Without a bridge, the R5 Brain Health Check has no way to\n"
        "see your Second Brain — it just commits empty reports.\n\n"
        "The bridge: Curator already has a two-way GitHub sync feature. Enable it,\n"
        "and your Second Brain is mirrored to a private GitHub repo. Cloud Routines\n"
        "then clone that repo at execution time and read your markdown files\n"
        "directly. Read-only — Routines never write to your Second Brain.\n\n"
        f"What we'll do:\n"
        f"  1. Check your Curator app for an existing sync setup. If none, walk you\n"
        f"     through enabling it (target: <{profile.get('name', 'firm')}>-secondbrain).\n"
        f"  2. Have you create a fine-grained PAT with Contents:Read only on that\n"
        f"     repo — much safer than full repo scope.\n"
        f"  3. Verify a clone works.\n"
        f"  4. Save the repo URL + the curator domain ({curator_domain}) so Routines\n"
        f"     in Step 14 can be configured against it.\n\n"
        "Trade-off: cloud Routines lose the 17 MCP tools — they fall back to plain\n"
        "file reads + grep. For R5 (the only Day-1 Routine that actually needs the\n"
        "Second Brain) this is enough; broken-wikilink and orphan scans are file-\n"
        "level operations. The 17 tools come back via a stateless cloud-MCP variant\n"
        "in Gen-2 (or Anthropic's hosted Curator, whichever ships first).",
    )

    # ----- 1. Detect existing Curator sync -------------------------------
    curator_vault = locations.get("curator_vault")
    sync_config_path: Optional[Path] = None
    if curator_vault:
        candidate = Path(curator_vault).expanduser() / ".sync-config.json"
        if candidate.exists():
            sync_config_path = candidate

    existing_sync_url: Optional[str] = None
    if sync_config_path:
        try:
            import json as _json
            data = _json.loads(sync_config_path.read_text())
            existing_sync_url = (
                data.get("remoteUrl")
                or data.get("remote_url")
                or data.get("repo")
                or data.get("repoUrl")
            )
        except Exception as e:
            warn(f"Found {sync_config_path} but couldn't parse it: {e}")

    info("\n[1/4] Checking for existing Curator GitHub sync...")
    if existing_sync_url:
        ok(f"Detected an existing sync target: {existing_sync_url}")
        info("We'll reuse this repo as the Second Brain bridge target.")
        sync_url = existing_sync_url
    else:
        info("No existing sync config detected (or vault path not configured).")
        info("")
        info("  In the Curator app:")
        info("    1. Open the Sync tab in Settings (or Preferences → Sync).")
        info("    2. Click 'Enable GitHub sync' / 'Connect to GitHub'.")
        info(f"    3. Create a NEW private repository called  "
             f"  {profile.get('name', 'firm').lower().replace(' ', '-')}-secondbrain")
        info("       (or pick an existing private repo you want to sync to).")
        info("    4. Generate a PAT with `repo` scope (Curator uses this for two-way sync).")
        info("    5. Paste the PAT into Curator. Curator saves it locally in .sync-config.json.")
        info("    6. Click 'Sync Up' to do the initial push.")
        info("")
        if not ask_confirm("Curator sync is configured and the initial push succeeded?", default=True):
            info("Pausing here. When sync is configured, re-run with --resume.")
            sys.exit(0)
        default_url = f"https://github.com/<you>/{profile.get('name', 'firm').lower().replace(' ', '-')}-secondbrain"
        sync_url = ask_text(
            "Paste the Second Brain repo URL (HTTPS or git@)",
            default=default_url,
        ).strip()
        if not sync_url.endswith(".git") and "github.com" in sync_url:
            sync_url = sync_url.rstrip("/") + ".git"

    state["second_brain_repo_url"] = sync_url

    # Parse owner/name for later API calls + Routine connector config.
    sb_owner = sb_name = None
    try:
        # crude URL parse for github.com/<owner>/<name>(.git)
        import re
        m = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<name>[^/.]+)(\.git)?$", sync_url)
        if m:
            sb_owner = m.group("owner")
            sb_name = m.group("name")
            state["second_brain_repo_owner"] = sb_owner
            state["second_brain_repo_name"] = sb_name
    except Exception:
        pass

    # ----- 2. Have user create the read-only fine-grained PAT for Routines -
    info("\n[2/4] Create a fine-grained PAT for Routines (read-only).")
    info("  Routines need to clone the Second Brain repo at execution time. We'll")
    info("  use a fine-grained PAT scoped to ONLY that one repo with Contents:Read")
    info("  permission — much safer than a full `repo`-scope token.")
    info("")
    info("  In your browser:")
    info("    1. Open https://github.com/settings/personal-access-tokens/new")
    info("    2. Token name: 'oot-routines-secondbrain-read' (or similar)")
    info("    3. Expiration: 1 year (renew at expiry)")
    info("    4. Resource owner: yourself (or the firm's org, if relevant)")
    info("    5. Repository access: 'Only select repositories' → "
         + (f"{sb_owner}/{sb_name}" if sb_owner else "the Second Brain repo above"))
    info("    6. Permissions → Repository permissions → Contents: Read-only")
    info("       (leave everything else as 'No access')")
    info("    7. Generate token. Copy it immediately — GitHub only shows it once.")
    info("")
    info("  IMPORTANT: store this PAT in your password manager (Bitwarden / 1Password /")
    info("  keychain) — we'll NOT save it to the wizard state file. You'll paste it")
    info("  when configuring R5's GitHub connector in Step 14.")
    info("")

    pat_for_test = ""
    if ask_confirm("Paste the PAT here ONLY for a one-time clone verification? "
                   "(We won't write it to disk — it's used in memory then discarded.)",
                   default=True):
        pat_for_test = ask_text("PAT (will be used once then forgotten)", default="").strip()

    # ----- 3. Verify clone works -----------------------------------------
    info("\n[3/4] Verifying clone access...")
    verified = False
    if pat_for_test and sb_owner and sb_name and not dry_run:
        test_dir = Path("/tmp") / f"oot-sb-clone-test-{datetime.now(timezone.utc).strftime('%H%M%S')}"
        try:
            clone_url = f"https://{pat_for_test}@github.com/{sb_owner}/{sb_name}.git"
            rc, _ = run(
                ["git", "clone", "--depth", "1", "--quiet", clone_url, str(test_dir)],
                capture=True, check=False,
            )
            if rc == 0:
                # Check that the curator domain folder exists in the synced repo.
                domain_folder = test_dir / "wiki" / curator_domain
                if domain_folder.exists() and any(domain_folder.iterdir()):
                    ok(f"Clone succeeded. Found wiki/{curator_domain}/ with content.")
                    verified = True
                elif (test_dir / "wiki").exists():
                    warn(f"Clone succeeded, but wiki/{curator_domain}/ is empty or missing.")
                    info("  Tip: in the Curator app, make sure the firm domain is created,")
                    info("       then click 'Sync Up' again to push pages for that domain.")
                else:
                    warn("Clone succeeded but there's no wiki/ folder yet.")
                    info("  Add a few pages in the Curator app, then 'Sync Up'.")
            else:
                warn("Clone failed. Common causes: wrong PAT, PAT lacks Contents:Read,")
                warn("PAT scoped to a different repo, or the repo doesn't exist yet.")
        finally:
            # Scrub the working directory regardless of outcome (it never contained
            # the PAT itself, but defence in depth).
            import shutil as _shutil
            if test_dir.exists():
                _shutil.rmtree(test_dir, ignore_errors=True)
        # Discard the PAT from local scope — never written to state.
        pat_for_test = ""
    elif not pat_for_test:
        info("  Skipped verification (no PAT pasted). You can verify later by cloning")
        info(f"  {sync_url} manually with the PAT.")

    # ----- 4. Save state + summary --------------------------------------
    info("\n[4/4] Saved Second Brain bridge config.")
    state["second_brain_curator_domain"] = curator_domain
    state["second_brain_subfolder"] = f"wiki/{curator_domain}"
    state["second_brain_verified"] = verified

    info("")
    info("Summary of what's saved (to state file):")
    info(f"  Second Brain repo URL:     {sync_url}")
    info(f"  Curator domain scope:      wiki/{curator_domain}")
    info(f"  PAT:                       NOT saved (you'll paste it at Step 14)")
    info(f"  Clone-test verified:       {'yes' if verified else 'no (do this manually later)'}")
    info("")
    info("At Step 14 we'll configure R5 (and any other Routine that needs Second Brain")
    info("access) with a GitHub connector pointing at this repo. You'll paste the PAT")
    info("there, and the Routine clones the repo at every scheduled run.")

    mark_step_done(state, "step_12_secondbrain_sync")
    ask_navigation("Second Brain bridge")


def step_13_routines(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_13_routines"):
        return
    header("Step 14 / 17 — Configure Day-1 Routines", level=2)
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
        mark_step_done(state, "step_13_routines")
        return

    info(
        f"\nYou selected: {', '.join(day1_chosen)} for Day-1."
        + (f"\nDeferred (will set up later when prerequisites are met): {', '.join(deferred)}." if deferred else "")
    )

    owner = state.get("ledger_repo_owner")
    repo_name = state.get("ledger_repo_name")
    can_verify_via_gh = gh_available_and_authed() and owner and repo_name

    # Which Routines need the Second Brain bridge connector?
    sb_url = state.get("second_brain_repo_url")
    sb_subfolder = state.get("second_brain_subfolder", "wiki/<your-firm-domain>")
    routines_needing_secondbrain = {"R5"}  # R5 = Brain Health Check; depends on Second Brain access

    for r in day1_chosen:
        sched, name, watch_dir = schedules[r]
        info(f"\n--- {r} ({name}) — setup ---")
        info(f"  Routine prompt body:  routines/cloud/{r}.md  ({REPO_ROOT / 'routines' / 'cloud' / (r + '.md')})")
        info(f"  Schedule:             {sched}")
        info(f"  Primary GitHub connector (Ledger, read+write):")
        info(f"    {state.get('ledger_repo_url', '<repo>')} — signing key from Step 9")
        if r in routines_needing_secondbrain and sb_url:
            info(f"  Secondary GitHub connector (Second Brain, READ-ONLY):")
            info(f"    {sb_url}")
            info(f"    Scope:  {sb_subfolder}/")
            info(f"    PAT:    the fine-grained Contents:Read PAT you created at Step 13")
            info(f"            (paste it from your password manager when prompted)")
        info("\n  In Claude Code (CLI or desktop app):")
        info("    /schedule  →  New Routine  →  upload the prompt body file above")
        info("    Attach the my-curator MCP (privacy-track only — cloud Routines use")
        info("    the Second Brain bridge instead; see Step 13).")
        info("    Configure the GitHub connector(s) listed above. Save.")
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

    mark_step_done(state, "step_13_routines")


def step_klarna_gate(state: dict[str, Any], dry_run: bool) -> None:
    """(Optional) Install the Klarna gate workflow + auto-labeller into the Ledger.

    Mirrors cloud-install-plan.md Step 11. Copies .github/workflows/klarna-gate.yml
    and .github/labeler.yml from the framework repo into the firm's Ledger clone,
    signed-commits + pushes, then walks the user through the two manual pieces the
    firm MUST do itself: (a) adapt the workflow's guard + workbook path per its
    header comment block, (b) require the `oot/klarna-test` status check in branch
    protection via the web UI.

    Programmatic file-copy + git ops are DRY_RUN-gated (nothing lands on disk or
    GitHub in a dry run). Offered with a skip — this only matters once the firm
    expects AI-replaces-human PRs.
    """
    if is_step_done(state, "step_klarna_gate"):
        return
    header("Step 15 / 17 — (Optional) Install the Klarna gate", level=2)

    profile = state.get("firm_profile", {})
    modules = state.get("modules_chosen", {})
    locations = state.get("locations", {})
    firm_folder = Path(locations.get("firm_folder", ""))
    repo_url = state.get("ledger_repo_url", "<repo>")
    owner = state.get("ledger_repo_owner")
    repo_name = state.get("ledger_repo_name")

    explainer(
        "What this step does and why",
        "The Klarna gate is the framework's pre-merge discipline: any PR labelled\n"
        "`ai-replaces-human` must pass the Klarna Test (score >=14/20 + two sign-offs)\n"
        "before it can merge. It ships as a GitHub Actions workflow that posts the\n"
        "`oot/klarna-test` status check, plus an auto-labeller.\n\n"
        "This step copies both files into your Ledger and pushes them. Then it walks\n"
        "you through the two things ONLY YOU can do: adapting the workflow to your firm,\n"
        "and requiring the status check in branch protection.\n\n"
        "This only matters once you expect PRs that replace a human function with an\n"
        "AI one. Most founders defer it — you can skip and run this step later with\n"
        "--resume.",
    )

    # Honour the Step 4 choice, but always allow a skip here.
    klarna_now = (profile.get("klarna_gate_choice") == "now"
                  or "R7" in modules.get("routines", []))
    default_install = klarna_now
    if not ask_confirm(
        "Install the Klarna gate workflow + auto-labeller into your Ledger now?"
        + (" (recommended — you chose 'now' at Step 4)" if klarna_now
           else " (you can defer — most founders do)"),
        default=default_install,
    ):
        info("Skipping the Klarna gate. Re-run with --resume to install it later,")
        info("or copy .github/workflows/klarna-gate.yml + .github/labeler.yml from the")
        info("framework repo into your Ledger by hand when you're ready.")
        mark_step_done(state, "step_klarna_gate", outcome="skipped")
        return

    src_workflow = REPO_ROOT / ".github" / "workflows" / "klarna-gate.yml"
    src_labeler = REPO_ROOT / ".github" / "labeler.yml"
    dst_workflows_dir = firm_folder / ".github" / "workflows"
    dst_github_dir = firm_folder / ".github"

    info("\n[1/3] Copy klarna-gate.yml + labeler.yml into the Ledger + push")
    if dry_run:
        info(f"  (dry-run) would copy {src_workflow.name} → .github/workflows/ and "
             f"{src_labeler.name} → .github/ in {firm_folder}, then signed-commit + push")
    else:
        if not src_workflow.exists() or not src_labeler.exists():
            warn(f"Could not find the source files in the framework repo:")
            warn(f"  {src_workflow}  (exists: {src_workflow.exists()})")
            warn(f"  {src_labeler}   (exists: {src_labeler.exists()})")
            warn("Skipping the copy. Install the Klarna gate by hand later.")
            mark_step_done(state, "step_klarna_gate", outcome="failed")
            return
        dst_workflows_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_workflow, dst_workflows_dir / src_workflow.name)
        shutil.copy2(src_labeler, dst_github_dir / src_labeler.name)
        ok("Copied klarna-gate.yml + labeler.yml into .github/")
        os.chdir(firm_folder)
        run(["git", "add", ".github/"], check=False)
        if not run_critical(
            ["git", "commit", "-S", "-m", "config: Klarna gate workflow + auto-labeller"],
            "Signed commit of Klarna gate files", capture=True,
        ):
            info("Pausing. Fix the signing/commit error above, then re-run with --resume.")
            return  # NOT marked done
        if not run_critical(["git", "push", "origin", "main"],
                            "Push Klarna gate files", capture=True):
            info("Pausing. Re-run with --resume once the push succeeds.")
            return  # NOT marked done

    # --- 2. Firm-specific adaptation (the workflow ships as a template) -----
    info("\n[2/3] Adapt the workflow to YOUR firm (required — it ships as a template)")
    explainer(
        "Why you must edit two things in the workflow",
        "The klarna-gate.yml you just copied is scoped to the framework repo. Per its\n"
        "header comment block, adapt these before it will score your firm's PRs:",
    )
    info("  1. WORKBOOK PATH — in the workflow's `env:` block, change")
    info("     WORKBOOK_PATH: templates/excel/klarna-test.xlsx")
    info("     to your live Ledger path:")
    info("     WORKBOOK_PATH: firm/excel/klarna-test.xlsx   (per ADR-001)")
    info("  2. REPO GUARD — the `if:` guard on the scoring step short-circuits scoring")
    info("     when it sees the framework repo (FRAMEWORK_REPO: talirezun/oot-framework).")
    info("     Set FRAMEWORK_REPO to your own repo, or delete the guard, so scoring")
    info("     actually runs on your PRs.")
    info("  3. LABELER GLOBS — .github/labeler.yml decides which PRs get the")
    info("     `ai-replaces-human` label. Its globs are commented-out framework-scoped")
    info("     placeholders; adapt them to your firm's product paths (src/**, etc.).")
    info("")
    info("  Full guidance is in the header comment block at the top of")
    info("  .github/workflows/klarna-gate.yml in your Ledger.")
    ask_confirm("Read the header comment block and understand what to adapt?", default=True)

    # --- 3. Require the status check in branch protection (web UI) ----------
    info("\n[3/3] Require the `oot/klarna-test` status check in branch protection")
    explainer(
        "Why this is a manual web-UI step",
        "A GitHub Actions status check only *blocks* a merge if branch protection is\n"
        "configured to REQUIRE it. Adding a required status check is a repo-settings\n"
        "change we walk you through in the browser (same style as the Step 10\n"
        "branch-protection walkthrough).",
    )
    applied_via_gh = False
    if gh_available_and_authed() and owner and repo_name:
        if ask_confirm(
            "Add `oot/klarna-test` as a required status check automatically via `gh api`?",
            default=True,
        ):
            payload = {
                "strict": False,
                "contexts": ["oot/klarna-test"],
            }
            payload_path = Path("/tmp/oot-klarna-status-check.json")
            import json as _json
            payload_path.write_text(_json.dumps(payload))
            rc, out = run(
                ["gh", "api", "-X", "PATCH",
                 f"repos/{owner}/{repo_name}/branches/main/protection/required_status_checks",
                 "-H", "Accept: application/vnd.github+json",
                 "--input", str(payload_path)],
                dry_run=dry_run, capture=True, check=False,
            )
            if rc == 0:
                ok("Required status check `oot/klarna-test` added to branch protection.")
                applied_via_gh = True
            else:
                warn("`gh api` failed (branch protection may not exist yet, or Free plan). Output:")
                if out:
                    info(out)
                warn("Falling back to the web UI walkthrough.")
            payload_path.unlink(missing_ok=True)

    if not applied_via_gh:
        settings_url = (repo_url.removesuffix(".git") or "<repo>") + "/settings/branches"
        info(
            f"\nManual setup:\n"
            f"  1. Open {settings_url} in your browser.\n"
            "  2. Edit your `main` branch protection rule (from Step 10).\n"
            "  3. Check 'Require status checks to pass before merging'.\n"
            "  4. In the search box, type and select:  oot/klarna-test\n"
            "     (it appears once the workflow has run at least once — open a test PR\n"
            "      first if it's not listed yet.)\n"
            "  5. Save changes.\n"
        )
        if plan_tier_is_free(state):
            warn("On GitHub Free + private repos, required status checks are advisory only —")
            warn("same enforcement caveat as branch protection (Step 6). Upgrade to Team for")
            warn("real enforcement of the gate.")
        ask_confirm("Required status check configured (or noted to do after first PR)?", default=True)

    state["klarna_gate_installed"] = True
    mark_step_done(state, "step_klarna_gate")


def plan_tier_is_free(state: dict[str, Any]) -> bool:
    return state.get("firm_profile", {}).get("github_plan_tier", "free") == "free"


def step_14_smoke_test(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_14_smoke_test"):
        return
    header("Step 16 / 17 — Smoke test", level=2)
    locations = state["locations"]
    firm_folder = Path(locations["firm_folder"])
    info("Running smoke test against your firm folder...")

    if not firm_folder.exists():
        warn(f"Firm folder {firm_folder} doesn't exist. Skipping.")
        mark_step_done(state, "step_14_smoke_test")
        return

    info("\n[1/3] Most recent commit signature:")
    if dry_run:
        info("  (dry-run) would run: git log --show-signature -1")
    else:
        os.chdir(firm_folder)
        run(["git", "log", "--show-signature", "-1"], capture=False, check=False)

    info("\n[2/3] Excel templates open cleanly:")
    venv_python = venv_bin(VENV_DIR, "python")
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

    info("\n[3/4] Ledger folder structure:")
    for sub in ["excel", "output-logs", "audit-logs", "business-reviews",
                "klarna-tests", "compensation", "brain-health", "partners"]:
        path = firm_folder / "firm" / sub
        marker = "✓" if path.exists() else "✗"
        info(f"  {marker} firm/{sub}/")

    info("\n[4/4] Second Brain bridge:")
    sb_url = state.get("second_brain_repo_url")
    sb_verified = state.get("second_brain_verified")
    sb_subfolder = state.get("second_brain_subfolder")
    track = state.get("firm_profile", {}).get("track", "cloud")
    modules = state.get("modules_chosen", {})

    if track == "privacy":
        info("  · Privacy track: my-curator MCP runs locally alongside Routines.")
        info("    No bridge needed; full 17-tool MCP access from privacy-track Routines.")
    elif modules.get("skip_curator"):
        info("  · Curator skipped at Step 5 — no Second Brain to bridge.")
        info("    To enable later: install Curator, then re-run the wizard from Step 13.")
    elif not sb_url:
        warn("  Bridge state missing. Step 13 (Second Brain sync) may not have completed.")
        info("    To complete: re-run the bootstrap and let Step 13 run.")
    else:
        info(f"  ✓ Second Brain repo:  {sb_url}")
        info(f"  ✓ Domain scope:        {sb_subfolder or '(unset)'}")
        if sb_verified:
            info(f"  ✓ Clone verification:  passed at Step 13.")
        else:
            warn(f"  Clone verification:  NOT verified at Step 13.")
            info(f"    Test manually: open the repo URL above in your browser. You should")
            info(f"    see a `{sb_subfolder or 'wiki/<domain>'}/` folder with markdown files.")
        if gh_available_and_authed() and not dry_run:
            sb_owner = state.get("second_brain_repo_owner")
            sb_name = state.get("second_brain_repo_name")
            if sb_owner and sb_name:
                domain = (sb_subfolder or "wiki").split("/", 1)[-1] if "/" in (sb_subfolder or "") else ""
                api_path = f"repos/{sb_owner}/{sb_name}/contents/{sb_subfolder}" if sb_subfolder else f"repos/{sb_owner}/{sb_name}/contents/wiki"
                rc, out = run(["gh", "api", api_path, "--jq", ".[].name"],
                               capture=True, check=False)
                if rc == 0 and out.strip():
                    pages = [p for p in out.strip().splitlines() if p.endswith(".md")]
                    info(f"  ✓ Live API read:        found {len(pages)} markdown page(s) at "
                         f"{sb_subfolder or 'wiki/'}")
                    if pages:
                        sample = ", ".join(pages[:3])
                        info(f"     Sample:             {sample}{'...' if len(pages) > 3 else ''}")
                elif rc == 0:
                    warn(f"  Live API read:         folder exists but no pages yet. Add pages to your")
                    info(f"    Curator domain '{domain or '<firm>'}' and Sync Up to populate the bridge.")
                else:
                    info(f"  · Live API read:         skipped (gh API call failed — repo might be private)")
                    info(f"    Verify manually in your browser.")

    mark_step_done(state, "step_14_smoke_test")


def step_15_summary(state: dict[str, Any], dry_run: bool) -> None:
    if is_step_done(state, "step_15_summary"):
        return
    header("Step 17 / 17 — Install summary", level=2)
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
        f"- Foundation: {', '.join(modules.get('foundation', [])) or '(none)'}\n"
        f"- Curator mode: {modules.get('curator_mode', '(none)')}\n"
        f"- Skill packs: {', '.join(modules.get('skills', [])) or '(none)'}\n"
        f"- Routines: {', '.join(modules.get('routines', [])) or '(none)'}\n"
        f"- Security: {', '.join(modules.get('security', [])) or '(none)'}\n"
        f"\n## GitHub repos (two — per ADR-002)\n\n"
        f"- **Ledger** (operational state — Excel, audit logs):\n"
        f"  {state.get('ledger_repo_url', '<not configured>')}\n"
        f"- **Firm Brain** (Curator Shared Brain — synthesized firm IP):\n"
        f"  {state.get('firm_brain_repo_url', '<not configured>')}\n"
        f"\n## Firm Brain configuration\n\n"
        f"- IP mode: `{profile.get('firm_brain_ip_mode', '<not set>')}` "
        f"({'partners assign IP to firm' if profile.get('firm_brain_ip_mode') == 'organisational' else 'contributors retain IP' if profile.get('firm_brain_ip_mode') == 'contributor_retains' else '<unset>'})\n"
        f"- admin_token saved to Bitwarden: {'YES' if state.get('firm_brain_admin_token_saved') else 'NO — DO THIS NOW'}\n"
        f"- Invite token (sbi_) saved to Bitwarden: {'YES' if state.get('firm_brain_invite_token_saved') else 'NO — DO THIS NOW'}\n"
        f"- First Synthesize verified: {'YES' if state.get('firm_brain_first_synthesize_ok') else 'NO'}\n"
        f"\n## Signing key\n\n"
        f"GPG key ID: `{state.get('signing_key_id', '<not generated>')}`\n"
    )
    if not dry_run:
        OOT_HOME.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(summary)
        ok(f"Install summary written to {summary_path}")
    mark_step_done(state, "step_15_summary")
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

    if os.name == "nt":
        warn("Native Windows is only partially supported. The install plans and the\n"
             "framework's bash provisioning scripts assume a POSIX shell. For a smooth\n"
             "install, run this wizard inside WSL (Windows Subsystem for Linux):\n"
             "  https://learn.microsoft.com/windows/wsl/install\n"
             "Continuing on native Windows — some git/gpg steps may need manual fixups.")

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
    state["firm_profile"] = resolve_track(state, args.track, args.resume)
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
        ("step_12_brain_ingest",     "Brain ingest",          step_12_brain_ingest),
        ("step_12_secondbrain_sync", "Second Brain bridge",   step_12_secondbrain_sync),
        ("step_13_routines",         "Routines",              step_13_routines),
        ("step_klarna_gate",         "Klarna gate",           step_klarna_gate),
        ("step_14_smoke_test",       "Smoke test",            step_14_smoke_test),
        ("step_15_summary",          "Summary",               step_15_summary),
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
