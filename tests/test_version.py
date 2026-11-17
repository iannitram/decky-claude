"""release: our version is 1.1.0 or above, the same in package.json and plugin.json."""
import json
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLOOR = (1, 1, 0)


def _text(name):
    with open(os.path.join(ROOT, name)) as f:
        return f.read()


def _version(name):
    return json.loads(_text(name))["version"]


def _tuple(v):
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", v)
    if not m:
        raise AssertionError(f"version {v!r} is not three numbers joined by dots")
    return tuple(int(p) for p in m.groups())


class Version(unittest.TestCase):
    def test_package_json_at_or_above_floor(self):
        self.assertGreaterEqual(_tuple(_version("package.json")), FLOOR)

    def test_plugin_json_at_or_above_floor(self):
        self.assertGreaterEqual(_tuple(_version("plugin.json")), FLOOR)

    def test_both_files_agree(self):
        self.assertEqual(_version("package.json"), _version("plugin.json"))

    def test_names_kept(self):
        self.assertEqual(json.loads(_text("package.json"))["name"], "decky-claude")
        self.assertEqual(json.loads(_text("plugin.json"))["name"], "decky-claude")

    def test_format_kept(self):
        for name in ("package.json", "plugin.json"):
            text = _text(name)
            self.assertTrue(text.startswith('{\n  "name": "decky-claude",\n  "version": "'), name)
            self.assertTrue(text.endswith("}\n"), name)
            self.assertEqual(text.count('"version"'), 1, name)


if __name__ == "__main__":
    unittest.main()
