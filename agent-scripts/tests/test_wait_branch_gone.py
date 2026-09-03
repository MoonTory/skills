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
SCRIPT = ROOT / "scripts/wait-branch-gone"
FIXTURES = ROOT / "fixtures/wait-branch-gone"
MAIN = runpy.run_path(str(SCRIPT))["main"]


def run(case, *extra):
    argv = [
        str(SCRIPT), "--branch", "topic", "--repo", "/repo",
        "--fixture", str(FIXTURES / f"{case}.json"), "--quiet", *extra,
    ]
    stdout, stderr = io.StringIO(), io.StringIO()
    code = 0
    with patch.object(sys, "argv", argv), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try:
            MAIN()
        except SystemExit as error:
            code = error.code
    return SimpleNamespace(returncode=code, stdout=stdout.getvalue(), stderr=stderr.getvalue())


class WaitBranchGoneTests(unittest.TestCase):
    def test_gone_after_two(self):
        result = run("gone_after_two")
        output = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(output["event"], "gone")
        self.assertEqual(output["elapsed_s"], 60)

    def test_absent(self):
        result = run("absent")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["event"], "absent")

    def test_tool_failure_recovers(self):
        result = run("tool_recovered")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["elapsed_s"], 60)

    def test_timeout_zero_checks_once(self):
        result = run("gone_after_two", "--timeout", "0")
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["event"], "timeout")


if __name__ == "__main__":
    unittest.main()
