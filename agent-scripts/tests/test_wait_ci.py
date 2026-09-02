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
SCRIPT = ROOT / "scripts/wait-ci"
FIXTURES = ROOT / "fixtures/wait-ci"
MAIN = runpy.run_path(str(SCRIPT))["main"]


def run(case, *extra, mode=("--pr", "51")):
    argv = [str(SCRIPT), *mode, "--fixture", str(FIXTURES / f"{case}.json"), "--quiet", *extra]
    stdout, stderr = io.StringIO(), io.StringIO()
    code = 0
    with patch.object(sys, "argv", argv), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try:
            MAIN()
        except SystemExit as error:
            code = error.code
    return SimpleNamespace(returncode=code, stdout=stdout.getvalue(), stderr=stderr.getvalue())


class WaitCiTests(unittest.TestCase):
    def test_pr_green(self):
        result = run("pr_green")
        output = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0)
        self.assertEqual((output["event"], output["detail"]["head"], output["detail"]["run_id"]), ("green", "abc123", 42))
        self.assertEqual(output["detail"]["jobs"][-1]["bucket"], "skipping")

    def test_pr_red_with_link(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {"TMPDIR": directory}):
            result = run("pr_red_with_link", "--logs")
            output = json.loads(result.stdout)
            failed = output["detail"]["failed"][0]
            self.assertEqual(result.returncode, 0)
            self.assertEqual(output["event"], "red")
            self.assertEqual(failed["link"], "/actions/runs/43/job/11")
            self.assertEqual(Path(failed["log"]).read_text(encoding="utf-8"), "browser failed\n")

    def test_pr_head_changed(self):
        result = run("pr_head_changed")
        output = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(output["event"], "head-changed")
        self.assertEqual(output["detail"], {"was": "old123", "now": "new456"})

    def test_commit_appears_then_green(self):
        result = run("commit_appears_then_green", mode=("--commit", "abc123"))
        output = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0)
        self.assertEqual((output["event"], output["detail"]["run_id"]), ("green", 45))
        self.assertEqual(output["elapsed_s"], 35)

    def test_commit_no_run(self):
        result = run("commit_no_run", "--appear-timeout", "30", mode=("--commit", "abc123"))
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["event"], "no-run")

    def test_gh_failure_backoff(self):
        result = run("gh_failure_backoff")
        output = json.loads(result.stdout)
        self.assertEqual(result.returncode, 4)
        self.assertEqual(output["detail"]["error"], "gh unavailable 5")
        self.assertEqual(output["elapsed_s"], 300)

    def test_tool_failure_recovers(self):
        result = run("tool_recovered")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["elapsed_s"], 20)

    def test_timeout_zero_checks_once(self):
        result = run("pr_green", "--timeout", "0")
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["event"], "timeout")


if __name__ == "__main__":
    unittest.main()
