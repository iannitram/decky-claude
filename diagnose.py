"""Collect launch evidence for one game (M6).

Skeleton. Pure: reads files under the paths it is given, so tests feed fixtures.
Used by the MCP tool `game_diagnose` in mcp_server.py.
"""


def parse_vdf(text: str) -> dict:
    """Valve's text KeyValues (config.vdf, localconfig.vdf, appmanifest) as nested dicts of str; ValueError when unbalanced."""
    raise NotImplementedError


def collect(steam_dir: str, app_id: int) -> dict:
    """Evidence for `app_id` as {"app_id": int, "name": str | None, "compat_tool": str | None,
    "launch_options": str, "steam_log_lines": list[str], "proton_log_tail": list[str], "missing": list[str]}:
    compat tool, launch options, tail of its Proton log and Steam's log lines for it."""
    raise NotImplementedError


def summarize(evidence: dict) -> str:
    """Evidence as a short plain-language block Claude reasons from (no stack traces)."""
    raise NotImplementedError
