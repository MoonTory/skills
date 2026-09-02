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
SCRIPT = ROOT / "scripts/wait-merged"
FIXTURES = ROOT / "fixtures/wait-merged"
MAIN = runpy.run_path(str(SCRIPT))["main"]


def run(case, *extra):
    argv = [str(SCRIPT), "--pr", "51", "--fixture", str(FIXTURES / f"{case}.json"), "--quiet", *extra]
    stdout, stderr = io.StringIO(), io.StringIO()
    code = 0
    with patch.object(sys, "argv", argv), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try:
            MAIN()
        except SystemExit as error:
            code = error.code
    return SimpleNamespace(returncode=code, stdout=stdout.getvalue(), stderr=stderr.getvalue())


class WaitMergedTests(unittest.TestCase):
    def test_merged(self):
        result = run("merged")
        output = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(output["event"], "merged")
        self.assertEqual(output["detail"], {
            "sha": "merge456", "merged_at": "2000-01-01T00:00:30Z", "head": "head123",
        })

    def test_closed(self):
        result = run("closed")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["event"], "closed")

    def test_timeout(self):
        result = run("timeout", "--timeout", "60")
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["event"], "timeout")

    def test_tool_failure_recovers(self):
        result = run("tool_recovered")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["elapsed_s"], 30)

    def test_timeout_zero_checks_once(self):
        result = run("merged", "--timeout", "0")
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["event"], "timeout")


if __name__ == "__main__":
    unittest.main()
