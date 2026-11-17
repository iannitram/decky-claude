"""release: the self-updater reads this fork's releases, not upstream's."""
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPECTED_REPO = "iannitram/decky-claude"
EXPECTED_API = '_UPDATE_API = f"https://api.github.com/repos/{_UPDATE_REPO}/releases/latest"'
EXPECTED_ASSET = '_UPDATE_ASSET = "decky-claude.zip"'


def _lines(rel="main.py"):
    with open(os.path.join(ROOT, *rel.split("/"))) as f:
        return f.read().splitlines()


def _code_map_row():
    rows = [l for l in _lines("docs/code-map.md") if l.startswith("| `src/sidebarTab.tsx`")]
    if len(rows) != 1:
        raise AssertionError(f"expected one code map row for src/sidebarTab.tsx, found {len(rows)}")
    return rows[0]


class UpdateRepo(unittest.TestCase):
    def test_update_repo_is_this_fork(self):
        found = [m.group(1) for m in (re.match(r'^_UPDATE_REPO = "([^"]*)"$', l) for l in _lines()) if m]
        self.assertEqual(found, [EXPECTED_REPO])

    def test_upstream_repo_is_not_named(self):
        hits = [l for l in _lines() if "TuxLux40/decky-claude" in l]
        self.assertEqual(hits, [])

    def test_api_line_unchanged(self):
        self.assertEqual(_lines().count(EXPECTED_API), 1)

    def test_asset_line_unchanged(self):
        self.assertEqual(_lines().count(EXPECTED_ASSET), 1)

    def test_code_map_row_names_this_fork(self):
        row = _code_map_row()
        self.assertIn("`_UPDATE_REPO`: this fork's)", row)
        self.assertNotIn("upstream's today", row)

    def test_code_map_row_status_present(self):
        self.assertTrue(_code_map_row().endswith("| release | present |"))


if __name__ == "__main__":
    unittest.main()
