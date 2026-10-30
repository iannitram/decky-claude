"""Turn a Claude Code JSONL transcript into chat messages for the chat view.

Skeleton. Pure: takes text in, returns data, so tests feed it fixtures.
"""


def parse_line(line: str) -> dict | None:
    """One JSONL line to {"role": "user"|"assistant"|"tool", "text": str, "id": str}, or None for lines the chat does not show."""
    raise NotImplementedError


def messages_since(path: str, offset: int = 0) -> tuple[list[dict], int]:
    """Messages appended to the transcript at `path` after byte `offset`, and the new offset."""
    raise NotImplementedError
