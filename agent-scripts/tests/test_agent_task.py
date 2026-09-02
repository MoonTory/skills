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
SCRIPT = ROOT / "scripts/agent-task"
FIXTURES = ROOT / "fixtures/agent-task"
MAIN = runpy.run_path(str(SCRIPT))["main"]


def run(case, *extra, line="do-it"):
    argv = [str(SCRIPT), "--pane", "p1", "--line", line, "--fixture", str(FIXTURES / f"{case}.json"), "--quiet", *extra]
    stdout, stderr = io.StringIO(), io.StringIO()
    code = 0
    with patch.object(sys, "argv", argv), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try:
            MAIN()
        except SystemExit as error:
            code = error.code
    return SimpleNamespace(returncode=code, stdout=stdout.getvalue(), stderr=stderr.getvalue())


class AgentTaskTests(unittest.TestCase):
    def test_pi_ok(self):
        result = run("pi_ok")
        self.assertEqual(result.returncode, 0, result.stderr)
        detail = json.loads(result.stdout)["detail"]
        self.assertIn("prompted_at", detail)
        self.assertEqual(detail["status"], "idle")

    def test_prompt_retry(self):
        result = run("prompt_retry", "--no-startup")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["detail"]["status"], "done")

    def test_prompt_failed(self):
        result = run("prompt_failed", "--no-startup")
        self.assertEqual(result.returncode, 4)
        envelope = json.loads(result.stdout)
        self.assertEqual(envelope["event"], "prompt-failed")
        self.assertEqual(envelope["detail"]["screen"], "last screen")

    def test_working_timeout_does_not_send_twice(self):
        result = run("prompt_working_timeout", "--no-startup")
        self.assertEqual(result.returncode, 4, result.stderr)
        self.assertEqual(json.loads(result.stdout)["detail"]["screen"], "prompt remains on screen")

    def test_tool_failure_recovers(self):
        result = run("tool_recovered", "--no-startup")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["elapsed_s"], 4)

    def test_claude_marker_ignores_prompt_echo(self):
        result = run("claude_marker", "--no-startup", "--claude", line="end with Deviations")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["detail"]["session"]["kind"], "id")


if __name__ == "__main__":
    unittest.main()
