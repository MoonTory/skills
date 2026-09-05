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


def lines(result):
    return [json.loads(line) for line in result.stdout.splitlines()]


def events(result):
    return [line["event"] for line in lines(result)]


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
        output = lines(result)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(events(result), ["watching", "merged"])
        self.assertEqual(output[0]["detail"], {"head": "head123", "state": "OPEN"})
        self.assertEqual(output[-1]["detail"], {
            "sha": "merge456", "merged_at": "2000-01-01T00:00:30Z", "head": "head123",
        })

    def test_closed(self):
        result = run("closed")
        output = lines(result)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(output[-1]["event"], "closed")
        self.assertTrue(all(set(line) == {"script", "event", "target", "elapsed_s", "at", "detail"} for line in output))

    def test_timeout(self):
        result = run("timeout", "--timeout", "60")
        output = lines(result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(events(result), ["watching", "timeout"])
        self.assertTrue(all(set(line) == {"script", "event", "target", "elapsed_s", "at", "detail"} for line in output))

    def test_tool_failure_recovers(self):
        result = run("tool_recovered")
        output = lines(result)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output[-1]["elapsed_s"], 30)
        self.assertTrue(all(set(line) == {"script", "event", "target", "elapsed_s", "at", "detail"} for line in output))

    def test_timeout_zero_checks_once(self):
        result = run("merged", "--timeout", "0")
        output = lines(result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(output[-1]["event"], "timeout")
        self.assertTrue(all(set(line) == {"script", "event", "target", "elapsed_s", "at", "detail"} for line in output))


if __name__ == "__main__":
    unittest.main()
