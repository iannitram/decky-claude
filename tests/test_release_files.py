"""release: the zip ships every root module; pipeline docs never trigger a release."""
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "release.yml")

EXPECTED_CP = (
    "cp -r dist plugin.json package.json main.py mcp_server.py deck_common.py "
    "machine_profile.py terminal_session.py transcript.py cli_install.py diagnose.py "
    "LICENSE README.md out/decky-claude/"
)
KEPT_IGNORES = ("README.md", "CLAUDE.md", "docs/**", "scripts/prototypes/**", "assets/**", ".github/**")
NEW_IGNORES = (
    "SPEC.md", "ROADMAP.md", "PIPELINE.md", "CHANGELOG.md", "GLOSSARY.md",
    "AGENTS.md", "IDEA.md", "ci-runs-on.md", "tests/**",
)


def _lines():
    with open(WORKFLOW) as f:
        return f.read().splitlines()


def _cp_line():
    found = [l.strip() for l in _lines() if l.strip().startswith("cp -r dist ")]
    if len(found) != 1:
        raise AssertionError(f"expected exactly one 'cp -r dist' line, found {len(found)}")
    return found[0]


def _paths_ignore():
    lines = _lines()
    start = next(i for i, l in enumerate(lines) if l.strip() == "paths-ignore:")
    out = []
    for l in lines[start + 1:]:
        s = l.strip()
        if s.startswith("#"):
            continue
        if not s.startswith("- "):
            break
        out.append(s[2:].strip().strip('"').strip("'"))
    return out


class ReleaseFiles(unittest.TestCase):
    def test_cp_line_is_exact(self):
        self.assertEqual(_cp_line(), EXPECTED_CP)

    def test_every_root_python_module_ships(self):
        shipped = set(_cp_line().split()[2:-1])
        root_py = {f for f in os.listdir(ROOT) if f.endswith(".py")}
        self.assertEqual(sorted(root_py - shipped), [])

    def test_old_ignores_kept(self):
        ignores = _paths_ignore()
        for p in KEPT_IGNORES:
            self.assertIn(p, ignores)

    def test_pipeline_docs_ignored(self):
        ignores = _paths_ignore()
        for p in NEW_IGNORES:
            self.assertIn(p, ignores)

    def test_no_duplicate_ignores(self):
        ignores = _paths_ignore()
        self.assertEqual(len(ignores), len(set(ignores)))


if __name__ == "__main__":
    unittest.main()
