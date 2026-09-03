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
SCRIPT = ROOT / "scripts/agent-probe"
FIXTURES = ROOT / "fixtures/agent-probe"
MAIN = runpy.run_path(str(SCRIPT))["main"]


def run(case):
    argv = [str(SCRIPT), "--pane", "p1", "--fixture", str(FIXTURES / f"{case}.json"), "--quiet"]
    stdout, stderr = io.StringIO(), io.StringIO()
    code = 0
    with patch.object(sys, "argv", argv), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try:
            MAIN()
        except SystemExit as error:
            code = error.code
    return SimpleNamespace(returncode=code, stdout=stdout.getvalue(), stderr=stderr.getvalue())


class AgentProbeTests(unittest.TestCase):
    def test_pi_working(self):
        result = run("pi_working")
        self.assertEqual(result.returncode, 0, result.stderr)
        detail = json.loads(result.stdout)["detail"]
        self.assertEqual((detail["status"], detail["session_age_s"], detail["last_event"]), ("working", 41, "tool_result"))

    def test_claude_idle(self):
        result = run("claude_idle")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["detail"]["last_event"], "assistant")

    def test_gone(self):
        self.assertEqual(run("gone").returncode, 2)


if __name__ == "__main__":
    unittest.main()
