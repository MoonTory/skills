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
SCRIPT = ROOT / "scripts/wait-agent"
FIXTURES = ROOT / "fixtures/wait-agent"
MAIN = runpy.run_path(str(SCRIPT))["main"]


def run(case, *extra):
    argv = [str(SCRIPT), "--pane", "p1", "--fixture", str(FIXTURES / f"{case}.json"), "--quiet", *extra]
    stdout, stderr = io.StringIO(), io.StringIO()
    code = 0
    with patch.object(sys, "argv", argv), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try:
            MAIN()
        except SystemExit as error:
            code = error.code
    return SimpleNamespace(returncode=code, stdout=stdout.getvalue(), stderr=stderr.getvalue())


class WaitAgentTests(unittest.TestCase):
    def test_idle(self):
        result = run("idle")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["detail"]["status"], "idle")

    def test_blocked(self):
        result = run("blocked")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["detail"]["status"], "blocked")

    def test_timeout(self):
        self.assertEqual(run("timeout").returncode, 3)

    def test_claude_marker(self):
        result = run("claude_marker", "--claude")
        self.assertEqual(result.returncode, 0)
        envelope = json.loads(result.stdout)
        self.assertEqual(envelope["detail"]["session"]["kind"], "id")
        self.assertIs(envelope["detail"]["marker"], True)
        self.assertEqual(envelope["elapsed_s"], 0)

    def test_claude_marker_echoed_while_working(self):
        result = run("claude_marker_echoed", "--claude")
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["event"], "timeout")

    def test_claude_marker_after_status_flips(self):
        result = run("claude_marker_late", "--claude")
        self.assertEqual(result.returncode, 0, result.stderr)
        envelope = json.loads(result.stdout)
        self.assertIs(envelope["detail"]["marker"], True)
        self.assertEqual(envelope["elapsed_s"], 2)

    def test_claude_marker_never_arrives(self):
        result = run("claude_marker_missing", "--claude", "--timeout", "4", "--interval", "2")
        self.assertEqual(result.returncode, 3)
        envelope = json.loads(result.stdout)
        self.assertEqual(envelope["event"], "timeout")
        self.assertEqual(envelope["detail"], {"marker": False, "status": "done"})

    def test_tool_failure_recovers(self):
        result = run("tool_recovered")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["elapsed_s"], 2)


if __name__ == "__main__":
    unittest.main()
