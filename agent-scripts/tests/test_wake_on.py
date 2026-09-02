import contextlib
import io
import json
import os
import runpy
import shlex
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/wake-on"
FIXTURE = ROOT / "fixtures/wake-on/queue_roundtrip.json"
MAIN = runpy.run_path(str(SCRIPT))["main"]


class WakeOnTests(unittest.TestCase):
    def test_queues_command(self):
        expected = json.loads(FIXTURE.read_text())["envelope"]
        source = f"print({json.dumps(json.dumps(expected))})"
        with tempfile.TemporaryDirectory() as directory:
            argv = [str(SCRIPT), "--fixture", str(FIXTURE), sys.executable, "-c", source]
            stdout = io.StringIO()
            with (
                patch.object(sys, "argv", argv),
                patch.dict(os.environ, {"TMPDIR": directory, "CLAUDE_SESSION_ID": "test-session"}),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                self.assertEqual(MAIN(), 0)
            queue_path = Path(directory) / "agent-scripts/wakes/test-session.tsv"
            timestamp, command = queue_path.read_text().rstrip("\n").split("\t", 1)
        output = json.loads(stdout.getvalue())
        self.assertEqual(output["event"], "queued")
        self.assertTrue(timestamp.endswith("Z"))
        self.assertEqual(shlex.split(command), [sys.executable, "-c", source])


if __name__ == "__main__":
    unittest.main()
