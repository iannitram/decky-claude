"""Find, install and update the `claude` CLI under the plugin's own directory (M1).

Skeleton. Writes only inside the plugin's data directory, never to the user's files.
"""


def find_installed(data_dir: str) -> str | None:
    """Path to a usable `claude` binary (plugin copy first, then PATH), or None."""
    raise NotImplementedError


def install(data_dir: str) -> str:
    """Install the CLI into `data_dir` and return its path; raise RuntimeError with a plain sentence and the fix on failure."""
    raise NotImplementedError


def update_available(data_dir: str) -> str | None:
    """The newer version string, or None when up to date or offline."""
    raise NotImplementedError
