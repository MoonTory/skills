import contextlib
import io
import json
import os
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/wait-linear"
FIXTURES = ROOT / "fixtures/wait-linear"
MAIN = runpy.run_path(str(SCRIPT))["main"]


def run(case, *extra, key=True):
    argv = [
        str(SCRIPT), "--ticket", "ADM-140", "--fixture", str(FIXTURES / f"{case}.json"),
        "--quiet", *extra,
    ]
    stdout, stderr = io.StringIO(), io.StringIO()
    code = 0
    environment = os.environ.copy()
    if key:
        environment["LINEAR_API_KEY"] = "x"
    else:
        environment.pop("LINEAR_API_KEY", None)
    with (
        patch.object(sys, "argv", argv),
        patch.dict(os.environ, environment, clear=True),
        contextlib.redirect_stdout(stdout),
        contextlib.redirect_stderr(stderr),
    ):
        try:
            MAIN()
        except SystemExit as error:
            code = error.code
    return SimpleNamespace(returncode=code, stdout=stdout.getvalue(), stderr=stderr.getvalue())


class WaitLinearTests(unittest.TestCase):
    def test_comment(self):
        result = run("comment")
        output = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output["event"], "comment")
        self.assertEqual(output["detail"], {
            "author": "Gustavo Quinta",
            "first_line": "Owner decision: use option A.",
            "id": "new-comment",
        })

    def test_state(self):
        result = run("state", "--until", "state", "--state", "Ready")
        output = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output["event"], "state")
        self.assertEqual(output["detail"], {"from": "Needs Input", "to": "Ready"})

    def test_missing_key_stops_before_request(self):
        result = run("no_key", key=False)
        output = json.loads(result.stdout)
        self.assertEqual(result.returncode, 4)
        self.assertEqual(output["event"], "tool-failure")
        self.assertIn("LINEAR_API_KEY", output["detail"]["error"])

    def test_not_found(self):
        result = run("not_found")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["event"], "not-found")

    def test_http_failure_backoff(self):
        result = run("http_backoff")
        output = json.loads(result.stdout)
        self.assertEqual(result.returncode, 4)
        self.assertEqual(output["event"], "tool-failure")
        self.assertEqual(output["elapsed_s"], 720)
        self.assertEqual(output["detail"]["error"], "HTTP 503 Service Unavailable 5")

    def test_tool_failure_recovers(self):
        result = run("tool_recovered")
        output = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output["event"], "state")
        self.assertEqual(output["elapsed_s"], 120)

    def test_timeout_zero_prints_baseline_once_without_key_leak(self):
        marker = "private-marker"
        with tempfile.TemporaryDirectory() as directory:
            brief = str(Path(directory) / "brief")
            argv = [
                str(SCRIPT), "--ticket", "ADM-140", "--fixture", str(FIXTURES / "comment.json"),
                "--timeout", "0", "--brief", brief,
            ]
            stdout, stderr = io.StringIO(), io.StringIO()
            with (
                patch.object(sys, "argv", argv),
                patch.dict(os.environ, {"LINEAR_API_KEY": marker}),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                self.assertEqual(MAIN(), 0)
            output = json.loads(stdout.getvalue())
            recorded = stdout.getvalue() + stderr.getvalue() + Path(f"{brief}.launch").read_text()
        self.assertEqual(output["event"], "baseline")
        self.assertEqual(output["detail"], {"state": "Needs Input", "comment_id": "old-comment"})
        self.assertNotIn(marker, recorded)
        self.assertEqual(stderr.getvalue().count("wait-linear: poll"), 1)


if __name__ == "__main__":
    unittest.main()
