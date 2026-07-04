"""Regression tests for the ØØT installer wizard's state machine.

Pure-Python, no network, no interactive prompts. Runs via:

    python3 -m pytest tests/ -q

These lock in the Phase-1A trust-critical fixes so they can't silently regress:
  (a) --dry-run must never write the on-disk state file.
  (b) mark_step_done / is_step_done round-trip.
  (c) --resume must not overwrite a saved track with the argparse default.
  (d) the GPG --with-colons key-ID parser.
  (e) the install-summary uses the real modules_chosen keys (not the old
      required/recommended/deferred keys).
  Plus: run()'s command echo masks credentials embedded in a URL.
"""

from __future__ import annotations

import importlib

import installer.wizard as wiz


# ---------------------------------------------------------------------------
# (a) --dry-run must not persist state
# ---------------------------------------------------------------------------


def test_dry_run_does_not_write_state(tmp_path, monkeypatch):
    """save_state() is a no-op when DRY_RUN is True."""
    state_file = tmp_path / "wizard-state.yaml"
    monkeypatch.setattr(wiz, "OOT_HOME", tmp_path)
    monkeypatch.setattr(wiz, "STATE_FILE", state_file)
    monkeypatch.setattr(wiz, "DRY_RUN", True)

    wiz.save_state({"hello": "world"})
    assert not state_file.exists(), "dry-run must not create the state file"

    # mark_step_done also routes through save_state → still no file.
    st: dict = {}
    wiz.mark_step_done(st, "step_00_welcome")
    assert not state_file.exists()
    # but the in-memory state still advanced so the step won't re-run.
    assert st["steps_completed"]["step_00_welcome"] == "done"


def test_real_run_does_write_state(tmp_path, monkeypatch):
    """Sanity counterpart: with DRY_RUN False the file is written."""
    if wiz.yaml is None:  # pragma: no cover - pyyaml is a hard test dep here
        import pytest

        pytest.skip("pyyaml not installed")
    state_file = tmp_path / "wizard-state.yaml"
    monkeypatch.setattr(wiz, "OOT_HOME", tmp_path)
    monkeypatch.setattr(wiz, "STATE_FILE", state_file)
    monkeypatch.setattr(wiz, "DRY_RUN", False)

    wiz.save_state({"hello": "world"})
    assert state_file.exists()
    loaded = wiz.load_state()
    assert loaded["hello"] == "world"


# ---------------------------------------------------------------------------
# (b) mark_step_done / is_step_done round-trip
# ---------------------------------------------------------------------------


def test_mark_and_is_step_done_roundtrip(tmp_path, monkeypatch):
    state_file = tmp_path / "wizard-state.yaml"
    monkeypatch.setattr(wiz, "OOT_HOME", tmp_path)
    monkeypatch.setattr(wiz, "STATE_FILE", state_file)
    monkeypatch.setattr(wiz, "DRY_RUN", False)

    st: dict = {}
    assert wiz.is_step_done(st, "step_03_locations") is False
    wiz.mark_step_done(st, "step_03_locations")
    assert wiz.is_step_done(st, "step_03_locations") is True

    # A step marked with a non-"done" outcome is not considered done.
    wiz.mark_step_done(st, "step_04_firm_profile", outcome="skipped")
    assert wiz.is_step_done(st, "step_04_firm_profile") is False


# ---------------------------------------------------------------------------
# (c) --resume must prefer the saved track over the argparse default
# ---------------------------------------------------------------------------


def test_resume_keeps_saved_privacy_track():
    """A resumed privacy install must NOT be flipped back to the cloud default."""
    state = {"firm_profile": {"track": "privacy", "name": "Acme"}}
    profile = wiz.resolve_track(state, cli_track="cloud", resume=True)
    assert profile["track"] == "privacy"
    assert profile["name"] == "Acme"  # other keys preserved


def test_resume_uses_cli_track_when_none_saved():
    state = {"firm_profile": {}}
    profile = wiz.resolve_track(state, cli_track="privacy", resume=True)
    assert profile["track"] == "privacy"


def test_fresh_run_uses_cli_track_even_over_saved():
    """Without --resume the CLI value wins (fresh start)."""
    state = {"firm_profile": {"track": "privacy"}}
    profile = wiz.resolve_track(state, cli_track="cloud", resume=False)
    assert profile["track"] == "cloud"


def test_resolve_track_does_not_mutate_input():
    state = {"firm_profile": {"track": "privacy"}}
    _ = wiz.resolve_track(state, cli_track="cloud", resume=False)
    # original state untouched (resolve_track returns a copy)
    assert state["firm_profile"]["track"] == "privacy"


# ---------------------------------------------------------------------------
# (d) GPG --with-colons key-ID parser
# ---------------------------------------------------------------------------

# A realistic fixture: two secret keys, each with sec/fpr/uid/ssb records.
_GPG_COLONS_FIXTURE = """\
sec:u:4096:1:AAAA1111BBBB2222:1700000000:1731536000::u:::scESC:::+:::23::0:
fpr:::::::::1111222233334444555566667777888899990000:
grp:::::::::0123456789ABCDEF0123456789ABCDEF01234567:
uid:u::::1700000000::ABCDEF::Acme Studio (ØØT Bot) <bot@acme.example>::::::::::0:
ssb:u:4096:1:CCCC3333DDDD4444:1700000000:1731536000:::::e:::+:::23:
sec:u:255:22:EEEE5555FFFF6666:1710000000:1741536000::u:::scESC:::+:::25::0:
fpr:::::::::AAAABBBBCCCCDDDDEEEEFFFF0000111122223333:
uid:u::::1710000000::FEDCBA::Second Key <two@acme.example>::::::::::0:
"""


def test_parse_gpg_key_ids_extracts_field5():
    ids = wiz.parse_gpg_key_ids(_GPG_COLONS_FIXTURE)
    assert ids == ["AAAA1111BBBB2222", "EEEE5555FFFF6666"]


def test_parse_gpg_key_ids_empty_on_no_keys():
    assert wiz.parse_gpg_key_ids("") == []
    # tru/cfg lines and a lone uid must not be mistaken for a sec record.
    assert wiz.parse_gpg_key_ids("tru::1:1700000000:0:3:1:5\nuid:::::::x::name::\n") == []


def test_parse_gpg_key_ids_ignores_public_key_records():
    # `pub:` (public-key) records must not be picked up — only `sec:`.
    pub_only = "pub:u:4096:1:DEADBEEFDEADBEEF:1700000000::::::scESC:::+:::23::0:\n"
    assert wiz.parse_gpg_key_ids(pub_only) == []


# ---------------------------------------------------------------------------
# (e) install summary uses the real modules_chosen keys
# ---------------------------------------------------------------------------


def test_step15_summary_uses_real_module_keys(tmp_path, monkeypatch):
    """Regression for the required/recommended/deferred key mismatch.

    step_05 writes modules_chosen with keys foundation/curator_mode/skills/
    routines/security. The summary must read those, not the old keys.
    """
    monkeypatch.setattr(wiz, "OOT_HOME", tmp_path)
    monkeypatch.setattr(wiz, "STATE_FILE", tmp_path / "wizard-state.yaml")
    monkeypatch.setattr(wiz, "DRY_RUN", False)

    state = {
        "firm_profile": {"name": "Acme", "track": "cloud"},
        "locations": {"firm_folder": str(tmp_path / "acme")},
        "modules_chosen": {
            "foundation": ["github_brain_repo", "signing_key"],
            "curator_mode": "install-fresh",
            "skills": ["S1", "S3"],
            "routines": ["R5", "R6"],
            "security": ["branch_protection"],
        },
    }
    wiz.step_15_summary(state, dry_run=False)

    summary = (tmp_path / "install-summary.md").read_text()
    # The real keys' values appear...
    assert "github_brain_repo" in summary
    assert "install-fresh" in summary
    assert "S1, S3" in summary
    assert "R5, R6" in summary
    assert "branch_protection" in summary
    # ...and the stale key labels are gone.
    assert "Required:" not in summary
    assert "Recommended:" not in summary


# ---------------------------------------------------------------------------
# bonus: run() masks credentials in its command echo
# ---------------------------------------------------------------------------


def test_mask_secrets_in_url():
    masked = wiz._mask_secrets_in_cmd(
        "git clone https://ghp_supersecrettoken123@github.com/acme/brain.git /tmp/x"
    )
    assert "ghp_supersecrettoken123" not in masked
    assert "***@github.com/acme/brain.git" in masked


def test_mask_secrets_user_colon_token_form():
    masked = wiz._mask_secrets_in_cmd(
        "git push https://user:ghp_tok@github.com/acme/brain.git main"
    )
    assert "ghp_tok" not in masked
    assert "***@github.com" in masked


def test_mask_secrets_leaves_plain_urls_alone():
    plain = "gh repo create acme/brain --private --source /tmp/acme"
    assert wiz._mask_secrets_in_cmd(plain) == plain
    url = "git remote add origin https://github.com/acme/brain.git"
    assert wiz._mask_secrets_in_cmd(url) == url


def test_module_imports_without_optional_deps():
    """The wizard must import even if questionary/rich aren't installed."""
    importlib.reload(wiz)
    assert hasattr(wiz, "main")


# ---------------------------------------------------------------------------
# (f) the two Phase-2 wizard steps exist and are registered in the navigator
# ---------------------------------------------------------------------------


def _steps_list_source() -> str:
    """Return the source of main(), which contains the STEPS list literal."""
    import inspect

    return inspect.getsource(wiz.main)


def test_new_step_functions_exist():
    """Brain-ingest + Klarna-gate step functions must be defined on the module."""
    assert callable(getattr(wiz, "step_12_brain_ingest", None))
    assert callable(getattr(wiz, "step_klarna_gate", None))


def test_new_steps_registered_in_steps_list():
    """Both new steps must appear in the STEPS navigator list in main()."""
    src = _steps_list_source()
    assert '"step_12_brain_ingest"' in src, "brain-ingest not registered in STEPS"
    assert '"step_klarna_gate"' in src, "klarna-gate not registered in STEPS"
    # Ordering: ingest before the bridge; klarna gate after routines, before smoke.
    assert src.index("step_12_brain_ingest") < src.index("step_12_secondbrain_sync")
    assert src.index("step_13_routines") < src.index("step_klarna_gate")
    assert src.index("step_klarna_gate") < src.index("step_14_smoke_test")


def test_klarna_gate_respects_dry_run(tmp_path, monkeypatch):
    """In --dry-run the Klarna-gate step must not copy files or persist state."""
    state_file = tmp_path / "wizard-state.yaml"
    monkeypatch.setattr(wiz, "OOT_HOME", tmp_path)
    monkeypatch.setattr(wiz, "STATE_FILE", state_file)
    monkeypatch.setattr(wiz, "DRY_RUN", True)

    # No third-party CLI in a dry run test.
    monkeypatch.setattr(wiz, "gh_available_and_authed", lambda: False)
    # Auto-answer every confirm as "yes" and never block on input.
    monkeypatch.setattr(wiz, "ask_confirm", lambda *a, **k: True)
    monkeypatch.setattr(wiz, "ask_navigation", lambda *a, **k: None)

    firm_folder = tmp_path / "acme"
    firm_folder.mkdir()
    state = {
        "firm_profile": {"github_plan_tier": "free", "klarna_gate_choice": "now"},
        "modules_chosen": {"routines": ["R7"]},
        "locations": {"firm_folder": str(firm_folder)},
        "ledger_repo_url": "https://github.com/acme/acme-ledger.git",
    }

    wiz.step_klarna_gate(state, dry_run=True)

    # Dry-run must not have copied the workflow into the (empty) firm folder...
    assert not (firm_folder / ".github").exists(), "dry-run must not copy gate files"
    # ...nor written the on-disk state file.
    assert not state_file.exists(), "dry-run must not persist state"
