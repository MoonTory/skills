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

    def test_timeout_zero_returns_current_status_without_settle_wait(self):
        result = run("timeout_zero", "--timeout", "0")
        self.assertEqual(result.returncode, 0, result.stderr)
        envelope = json.loads(result.stdout)
        self.assertEqual(envelope["event"], "settled")
        self.assertEqual(envelope["detail"]["status"], "working")

    def test_done_agent_is_prompted_once(self):
        result = run("status_done", "--no-startup", "--timeout", "0")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["detail"]["status"], "working")
        fixture = json.loads((FIXTURES / "status_done.json").read_text())
        prompts = [response for response in fixture["responses"] if response["cmd"].startswith("herdr agent prompt")]
        self.assertEqual(len(prompts), 1)

    def test_blocked_agent_is_not_prompted(self):
        result = run("status_blocked", "--no-startup")
        self.assertEqual(result.returncode, 2, result.stderr)
        envelope = json.loads(result.stdout)
        self.assertEqual(envelope["event"], "blocked")
        self.assertEqual(envelope["detail"]["status"], "blocked")
        fixture = json.loads((FIXTURES / "status_blocked.json").read_text())
        self.assertFalse(any(response["cmd"].startswith("herdr agent prompt") for response in fixture["responses"]))

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

    def test_claude_startup_matches_prompt_line_or_mode_footer(self):
        result = run("claude_startup", "--claude", "--timeout", "0")
        self.assertEqual(result.returncode, 0, result.stderr)
        fixture = json.loads((FIXTURES / "claude_startup.json").read_text())
        self.assertNotIn("? for shortcuts", fixture["responses"][0]["stdout"])
        self.assertIn("prompted_at", json.loads(result.stdout)["detail"])

    def test_claude_startup_waits_out_transient_blocked_and_unknown(self):
        result = run("claude_startup_blocked_then_idle", "--claude", "--timeout", "0")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("prompted_at", json.loads(result.stdout)["detail"])

    def test_claude_startup_regex_covers_each_ready_form(self):
        import re
        pattern = re.compile(runpy.run_path(str(SCRIPT))["CLAUDE_READY"])
        for text in ("❯ ", "⏵⏵ auto mode on (shift+tab to cycle)", "⏵⏵ accept edits on"):
            self.assertTrue(pattern.search(text), text)
        self.assertFalse(pattern.search("? for shortcuts"))

    def test_claude_startup_timeout_uses_timeout_ceiling(self):
        result = run("claude_startup_timeout", "--claude", "--timeout", "45")
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["detail"]["stage"], "startup")
        # the fixture only answers the exact 45 s wait, so any other ceiling misses it

    def test_claude_marker_ignores_prompt_echo(self):
        result = run("claude_marker", "--no-startup", "--claude", line="end with Deviations")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["detail"]["session"]["kind"], "id")


if __name__ == "__main__":
    unittest.main()
