#!/usr/bin/env bash
# ØØT bootstrap — zero-to-wizard in one command.
#
# Designed to be pasted into a Terminal on a fresh laptop:
#
#   curl -fsSL https://raw.githubusercontent.com/talirezun/oot-framework/main/installer/bootstrap.sh | bash
#
# What this does, in order:
#   1. Detects OS (macOS / Linux / WSL).
#   2. Checks for git, python ≥3.11, curl, gpg. If any are missing, prints the
#      exact copy-paste command to install them and exits cleanly.
#   3. Clones the framework to ~/.oot/oot-framework (or `git pull` if already there).
#   4. Creates a Python venv at ~/.oot/venv.
#   5. pip-installs the wizard's nice-UI dependencies (questionary, rich, pyyaml,
#      openpyxl, httpx) inside that venv.
#   6. Hands off to the wizard via `exec`.
#
# Safe to re-run. Idempotent. Never uses sudo. Never auto-installs Homebrew.
# Pass --resume / --dry-run / --track=privacy through; they reach the wizard.
#
# Author: ØØT framework / Claude Code (Opus 4.7) co-authored 2026-05-11.

set -euo pipefail

# ----- config ---------------------------------------------------------------

readonly REPO_URL="${OOT_REPO_URL:-https://github.com/talirezun/oot-framework.git}"
readonly REPO_BRANCH="${OOT_REPO_BRANCH:-main}"
readonly OOT_HOME="${OOT_HOME:-$HOME/.oot}"
readonly REPO_DIR="$OOT_HOME/oot-framework"
readonly VENV_DIR="$OOT_HOME/venv"
readonly MIN_PY_MAJOR=3
readonly MIN_PY_MINOR=11

# ----- terminal styling -----------------------------------------------------

if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  readonly C_RESET=$'\033[0m'
  readonly C_BOLD=$'\033[1m'
  readonly C_DIM=$'\033[2m'
  readonly C_CYAN=$'\033[36m'
  readonly C_GREEN=$'\033[32m'
  readonly C_YELLOW=$'\033[33m'
  readonly C_RED=$'\033[31m'
else
  readonly C_RESET= C_BOLD= C_DIM= C_CYAN= C_GREEN= C_YELLOW= C_RED=
fi

banner()  { printf '\n%s%s%s\n' "$C_CYAN$C_BOLD" "$*" "$C_RESET"; }
step()    { printf '\n%s▸ %s%s\n' "$C_CYAN" "$*" "$C_RESET"; }
ok()      { printf '  %s✓%s %s\n' "$C_GREEN" "$C_RESET" "$*"; }
note()    { printf '  %s%s%s\n' "$C_DIM" "$*" "$C_RESET"; }
warn()    { printf '  %s⚠%s  %s\n' "$C_YELLOW" "$C_RESET" "$*"; }
fail()    { printf '\n%s✗ %s%s\n' "$C_RED$C_BOLD" "$*" "$C_RESET" >&2; }
die()     { fail "$*"; exit 1; }

# ----- OS detection ---------------------------------------------------------

detect_os() {
  case "$(uname -s)" in
    Darwin)
      OS="macos"
      OS_PRETTY="macOS $(sw_vers -productVersion 2>/dev/null || echo '?')"
      ;;
    Linux)
      if grep -qi microsoft /proc/version 2>/dev/null; then
        OS="wsl"; OS_PRETTY="Windows Subsystem for Linux"
      else
        OS="linux"; OS_PRETTY="Linux ($(. /etc/os-release 2>/dev/null && echo "$PRETTY_NAME" || echo 'generic'))"
      fi
      ;;
    *)
      OS="unknown"; OS_PRETTY="$(uname -s) (untested)"
      ;;
  esac
  ok "Detected: $OS_PRETTY"
}

# ----- prerequisite check ---------------------------------------------------

# Find the first python ≥3.11 on PATH. Echoes the binary name on success.
find_python() {
  for cand in python3.13 python3.12 python3.11 python3; do
    if command -v "$cand" >/dev/null 2>&1; then
      local ver
      ver="$("$cand" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "0.0")"
      local major="${ver%%.*}"
      local minor="${ver##*.}"
      if [ "$major" -gt "$MIN_PY_MAJOR" ] 2>/dev/null \
         || { [ "$major" = "$MIN_PY_MAJOR" ] && [ "$minor" -ge "$MIN_PY_MINOR" ]; }; then
        echo "$cand"
        return 0
      fi
    fi
  done
  return 1
}

# Print per-OS install instructions for missing tools.
install_hint() {
  local missing=("$@")
  printf '\n%sTo install the missing tools, copy-paste this into Terminal:%s\n\n' "$C_BOLD" "$C_RESET"
  case "$OS" in
    macos)
      # Prefer Homebrew on macOS, but explain how to get it.
      if ! command -v brew >/dev/null 2>&1; then
        cat <<EOF
  ${C_BOLD}1. Install Homebrew (one-time, ~5 min):${C_RESET}

     /bin/bash -c "\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

  ${C_BOLD}2. Then install the missing tools:${C_RESET}

EOF
      fi
      # Map our internal names to Homebrew formula names.
      local brew_pkgs=()
      for t in "${missing[@]}"; do
        case "$t" in
          python) brew_pkgs+=("python@3.13") ;;
          gpg)    brew_pkgs+=("gnupg") ;;
          git|curl) brew_pkgs+=("$t") ;;
        esac
      done
      printf '     brew install %s\n\n' "${brew_pkgs[*]}"
      ;;
    linux|wsl)
      local apt_pkgs=()
      for t in "${missing[@]}"; do
        case "$t" in
          python) apt_pkgs+=("python3" "python3-venv" "python3-pip") ;;
          gpg)    apt_pkgs+=("gnupg") ;;
          git|curl) apt_pkgs+=("$t") ;;
        esac
      done
      printf '  ${C_DIM}# Debian / Ubuntu / WSL:${C_RESET}\n'
      printf '  sudo apt-get update && sudo apt-get install -y %s\n' "${apt_pkgs[*]}"
      printf '\n  ${C_DIM}# Fedora / RHEL:${C_RESET}\n'
      local dnf_pkgs=()
      for t in "${missing[@]}"; do
        case "$t" in
          python) dnf_pkgs+=("python3") ;;
          gpg)    dnf_pkgs+=("gnupg2") ;;
          git|curl) dnf_pkgs+=("$t") ;;
        esac
      done
      printf '  sudo dnf install -y %s\n\n' "${dnf_pkgs[*]}"
      ;;
    *)
      printf '  Install: %s\n  (Use your system package manager.)\n\n' "${missing[*]}"
      ;;
  esac
  printf '%sThen re-run this command:%s\n\n  curl -fsSL https://raw.githubusercontent.com/talirezun/oot-framework/main/installer/bootstrap.sh | bash\n\n' "$C_BOLD" "$C_RESET"
}

check_prereqs() {
  step "Checking prerequisites"

  local missing=()

  # git / curl / gpg
  for tool in git curl gpg; do
    if command -v "$tool" >/dev/null 2>&1; then
      ok "$tool: $("$tool" --version 2>&1 | head -n1)"
    else
      warn "$tool: NOT FOUND"
      missing+=("$tool")
    fi
  done

  # python ≥3.11
  if PY_BIN="$(find_python)"; then
    ok "$PY_BIN: $("$PY_BIN" --version)"
  else
    warn "python ≥${MIN_PY_MAJOR}.${MIN_PY_MINOR}: NOT FOUND"
    missing+=("python")
    PY_BIN=""
  fi

  if [ "${#missing[@]}" -gt 0 ]; then
    fail "Missing prerequisites: ${missing[*]}"
    install_hint "${missing[@]}"
    exit 1
  fi
}

# ----- clone or update repo -------------------------------------------------

clone_or_update_repo() {
  step "Fetching the framework"

  mkdir -p "$OOT_HOME"
  if [ -d "$REPO_DIR/.git" ]; then
    note "Repo already present at $REPO_DIR — pulling latest."
    if ! git -C "$REPO_DIR" pull --ff-only --quiet origin "$REPO_BRANCH" 2>/dev/null; then
      warn "git pull failed (local changes? network?). Continuing with the existing checkout."
    fi
  else
    note "Cloning $REPO_URL → $REPO_DIR"
    git clone --depth 1 --branch "$REPO_BRANCH" --quiet "$REPO_URL" "$REPO_DIR"
  fi
  ok "Framework at: $REPO_DIR"
}

# ----- python venv + wizard deps -------------------------------------------

setup_venv() {
  step "Setting up Python environment"

  if [ ! -d "$VENV_DIR" ]; then
    note "Creating venv at $VENV_DIR"
    "$PY_BIN" -m venv "$VENV_DIR"
  else
    note "Venv already exists at $VENV_DIR"
  fi

  local pip="$VENV_DIR/bin/pip"

  note "Upgrading pip (quietly)..."
  "$pip" install --quiet --upgrade pip >/dev/null

  note "Installing wizard dependencies (questionary, rich, pyyaml, openpyxl, httpx)..."
  "$pip" install --quiet --upgrade questionary rich pyyaml openpyxl httpx >/dev/null
  ok "Wizard environment ready."
}

# ----- handoff to the wizard ------------------------------------------------

run_wizard() {
  banner "Launching the ØØT wizard"
  note "From here on, the Python wizard takes over. It is resumable —"
  note "if you quit, re-run this same bootstrap command to pick up where you left off."
  printf '\n'

  local venv_python="$VENV_DIR/bin/python"
  local wizard="$REPO_DIR/installer/wizard.py"

  if [ ! -f "$wizard" ]; then
    die "wizard.py not found at $wizard — the repo clone may be incomplete. Try: rm -rf $REPO_DIR and re-run."
  fi

  export OOT_BOOTSTRAP_LAUNCHED=1
  export OOT_REPO_DIR="$REPO_DIR"

  # When invoked via `curl ... | bash`, our stdin is the curl pipe (now empty),
  # so any interactive prompt in the wizard would fail with EOF. Reopen stdin
  # from the controlling terminal so questionary / input() work.
  # Test that /dev/tty is actually readable (existence isn't enough — on macOS
  # /dev/tty is a magic device that fails to open when there's no controlling
  # terminal, e.g. running in CI or a subprocess without a tty).
  if ( : </dev/tty ) 2>/dev/null; then
    exec "$venv_python" "$wizard" "$@" </dev/tty
  else
    fail "No controlling terminal — the wizard needs an interactive shell."
    note "If you saw this from 'curl ... | bash' inside Terminal.app, please report it."
    note "Workaround: download the script first, then run it directly:"
    printf '\n  curl -fsSL https://raw.githubusercontent.com/talirezun/oot-framework/main/installer/bootstrap.sh -o /tmp/oot-bootstrap.sh\n  bash /tmp/oot-bootstrap.sh\n\n'
    exit 1
  fi
}

# ----- main -----------------------------------------------------------------

main() {
  banner "ØØT — Organisation of Tomorrow — Bootstrap"
  printf '%sZero-to-wizard installer. ~2 minutes of prerequisites, then a guided 15-step setup.%s\n' "$C_DIM" "$C_RESET"

  detect_os
  check_prereqs
  clone_or_update_repo
  setup_venv
  run_wizard "$@"
}

main "$@"
