import contextlib
import io
import json
import os
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/wake-run"
WAKE_ON = ROOT / "scripts/wake-on"
QUEUE_FIXTURE = ROOT / "fixtures/wake-on/queue_roundtrip.json"
EMPTY_FIXTURE = ROOT / "fixtures/wake-run/empty.json"
MAIN = runpy.run_path(str(SCRIPT))["main"]
QUEUE = runpy.run_path(str(WAKE_ON))["main"]


class WakeRunTests(unittest.TestCase):
    def test_queue_roundtrip(self):
        expected = json.loads(QUEUE_FIXTURE.read_text())["envelope"]
        source = f"print({json.dumps(json.dumps(expected))})"
        with tempfile.TemporaryDirectory() as directory:
            environment = {"TMPDIR": directory, "CLAUDE_SESSION_ID": "test-session"}
            queue_argv = [str(WAKE_ON), sys.executable, "-c", source]
            with (
                patch.object(sys, "argv", queue_argv),
                patch.dict(os.environ, environment),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                self.assertEqual(QUEUE(), 0)

            stdout, stderr = io.StringIO(), io.StringIO()
            with (
                patch.object(sys, "argv", [str(SCRIPT)]),
                patch.dict(os.environ, environment),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                code = MAIN()
            queue_path = Path(directory) / "agent-scripts/wakes/test-session.tsv"
            running_path = queue_path.with_suffix(".running")
            queue_exists = queue_path.exists()
            running_exists = running_path.exists()
        self.assertEqual(code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(json.loads(stderr.getvalue()), expected)
        self.assertFalse(queue_exists)
        self.assertFalse(running_exists)

    def test_empty_queue_exits_at_once(self):
        fixture = json.loads(EMPTY_FIXTURE.read_text())
        self.assertEqual(fixture["queue"], [])
        with tempfile.TemporaryDirectory() as directory:
            with (
                patch.object(sys, "argv", [str(SCRIPT), "--fixture", str(EMPTY_FIXTURE)]),
                patch.dict(os.environ, {"TMPDIR": directory, "CLAUDE_SESSION_ID": "empty-session"}),
                contextlib.redirect_stdout(io.StringIO()) as stdout,
                contextlib.redirect_stderr(io.StringIO()) as stderr,
            ):
                code = MAIN()
        self.assertEqual(code, 0)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
