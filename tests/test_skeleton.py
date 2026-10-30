"""One skipped test per Must that has Python code, so each issue fills in its own."""
import unittest


class Skeleton(unittest.TestCase):
    @unittest.skip("M1: cli_install.install")
    def test_install_cli(self): ...

    @unittest.skip("M2: transcript.parse_line")
    def test_transcript_parse(self): ...

    @unittest.skip("M3: terminal_session capture and resize")
    def test_terminal_capture(self): ...

    @unittest.skip("M6: diagnose.collect")
    def test_diagnose_collect(self): ...

    @unittest.skip("M8: _cleanup_working_dir leaves no files")
    def test_cleanup(self): ...


if __name__ == "__main__":
    unittest.main()
