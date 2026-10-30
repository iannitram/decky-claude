"""Collect launch evidence for one game (M6).

Skeleton. Pure: reads files under the paths it is given, so tests feed fixtures.
Used by the MCP tool `game_diagnose` in mcp_server.py.
"""


def collect(steam_dir: str, app_id: int) -> dict:
    """Evidence for `app_id`: compat tool, launch options, tail of its Proton log and Steam's last exit line for it."""
    raise NotImplementedError


def summarize(evidence: dict) -> str:
    """Evidence as a short plain-language block Claude reasons from (no stack traces)."""
    raise NotImplementedError
