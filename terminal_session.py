"""The tmux session that holds the one Claude Code session (ADR 0001).

Skeleton: signatures and contracts only. Stdlib only. `main.py` is the only
caller; it never runs tmux itself.
"""

SESSION_NAME = "decky-claude"


def start(argv: list[str], cwd: str, env: dict[str, str], cols: int = 80, rows: int = 24) -> None:
    """Start `argv` in a new detached tmux session; raise RuntimeError with a plain sentence if tmux is missing."""
    raise NotImplementedError


def is_running() -> bool:
    """True while the tmux session exists."""
    raise NotImplementedError


def send_keys(keys: list[str]) -> None:
    """Send named keys (Enter, Up, C-c, ...) to the session."""
    raise NotImplementedError


def send_text(text: str) -> None:
    """Type literal text into the session without interpreting it as keys."""
    raise NotImplementedError


def capture(scrollback_lines: int = 200) -> str:
    """Return the visible screen plus scrollback as plain text."""
    raise NotImplementedError


def resize(cols: int, rows: int) -> None:
    """Resize the session window to fit the panel."""
    raise NotImplementedError


def stop() -> None:
    """Kill the session; safe to call when it is not running."""
    raise NotImplementedError
