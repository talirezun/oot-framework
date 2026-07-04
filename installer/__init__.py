"""ØØT installer package.

Exposes the terminal wizard (`installer.wizard`) as an importable module so the
`oot-wizard` console-script entry point in pyproject.toml resolves, and so the
wizard's pure helpers can be unit-tested (see tests/test_wizard_state.py).
"""
