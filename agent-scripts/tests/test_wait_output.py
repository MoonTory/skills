import contextlib
import io
import json
import runpy
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/wait-output"
FIXTURES = ROOT / "fixtures/wait-output"
MAIN = runpy.run_path(str(SCRIPT))["main"]


def run(case):
    argv = [str(SCRIPT), "--pane", "p1", "--match", "MARK", "--fixture", str(FIXTURES / f"{case}.json"), "--quiet"]
    stdout, stderr = io.StringIO(), io.StringIO()
    code = 0
    with patch.object(sys, "argv", argv), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try:
            MAIN()
        except SystemExit as error:
            code = error.code
    return SimpleNamespace(returncode=code, stdout=stdout.getvalue(), stderr=stderr.getvalue())


class WaitOutputTests(unittest.TestCase):
    def test_matched(self):
        result = run("matched")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["event"], "matched")

    def test_timeout(self):
        result = run("timeout")
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["event"], "timeout")

    def test_pane_gone(self):
        result = run("pane_gone")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["event"], "gone")

    def test_echo_is_ignored(self):
        result = run("echo_ignored")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["detail"]["matched_line"], "MARK")

    def test_tool_failure_recovers(self):
        result = run("tool_recovered")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["elapsed_s"], 2)


if __name__ == "__main__":
    unittest.main()
