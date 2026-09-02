import contextlib
import io
import json
import os
import tempfile
import unittest
from unittest.mock import patch

import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts"))
import waitlib


class WaitlibTests(unittest.TestCase):
    def test_backoff_values_and_cap(self):
        self.assertEqual([waitlib.backoff(n, 2) for n in range(1, 5)], [2, 4, 8, 16])
        self.assertEqual(waitlib.backoff(10, 2), 300)

    def test_envelope_shape(self):
        script = waitlib.Script("sample", "thing:x")
        script.parse([])
        with patch.object(waitlib, "launch_log"), contextlib.redirect_stdout(io.StringIO()) as output:
            script.emit("ok", {"x": 1})
        envelope = json.loads(output.getvalue())
        self.assertEqual(set(envelope), {"script", "event", "target", "elapsed_s", "at", "detail"})

    def test_exit_code_mapping(self):
        self.assertEqual((waitlib.EXIT_OK, waitlib.EXIT_GONE, waitlib.EXIT_TIMEOUT, waitlib.EXIT_TOOL), (0, 2, 3, 4))

    def test_fixture_prefix_assertion(self):
        with tempfile.NamedTemporaryFile("w", delete=False) as fixture:
            json.dump({"responses": [{"cmd": "other command", "exit": 0}]}, fixture)
            path = fixture.name
        self.addCleanup(os.unlink, path)
        with self.assertRaisesRegex(AssertionError, "built: wanted command"):
            waitlib.Runner(path).run(["wanted", "command"])

    def test_polling_failure_cutoff(self):
        responses = [
            {"cmd": "tool check", "stdout": "", "stderr": f"failure {number}", "exit": 4}
            for number in range(1, 6)
        ]
        with tempfile.NamedTemporaryFile("w", delete=False) as fixture:
            json.dump({"responses": responses}, fixture)
            path = fixture.name
        self.addCleanup(os.unlink, path)
        script = waitlib.Script("sample")
        script.parse(["--fixture", path])
        poller = waitlib.Poller(script, waitlib.Runner(path))
        output, progress = io.StringIO(), io.StringIO()
        with patch.object(waitlib, "launch_log"), contextlib.redirect_stdout(output), contextlib.redirect_stderr(progress):
            with self.assertRaises(SystemExit) as stopped:
                poller.run(["tool", "check"])
        self.assertEqual(stopped.exception.code, 4)
        self.assertEqual(json.loads(output.getvalue())["detail"]["error"], "failure 5")
        self.assertEqual(progress.getvalue().count("sample: poll tool check"), 5)
        self.assertEqual(script.clock.now(), 30)

    def test_timeout_zero_does_not_retry_tool_failure(self):
        responses = [
            {"cmd": "tool check", "stdout": "", "stderr": "first failure", "exit": 4},
            {"cmd": "tool check", "stdout": "recovered", "stderr": "", "exit": 0},
        ]
        with tempfile.NamedTemporaryFile("w", delete=False) as fixture:
            json.dump({"responses": responses}, fixture)
            path = fixture.name
        self.addCleanup(os.unlink, path)
        script = waitlib.Script("sample")
        script.parse(["--fixture", path, "--timeout", "0", "--quiet"])
        runner = waitlib.Runner(path)
        poller = waitlib.Poller(script, runner)
        with patch.object(waitlib, "launch_log"), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as stopped:
                poller.run(["tool", "check"])
        self.assertEqual(stopped.exception.code, 4)
        self.assertEqual(runner.run(["tool", "check"]), (0, "recovered", ""))
        self.assertEqual(script.clock.now(), 0)

    def test_backoff_past_deadline_exits_timeout_without_sleep(self):
        responses = [
            {"cmd": "tool check", "stdout": "", "stderr": "first failure", "exit": 4},
            {"cmd": "tool check", "stdout": "recovered", "stderr": "", "exit": 0},
        ]
        with tempfile.NamedTemporaryFile("w", delete=False) as fixture:
            json.dump({"responses": responses}, fixture)
            path = fixture.name
        self.addCleanup(os.unlink, path)
        script = waitlib.Script("sample", interval=2)
        script.parse(["--fixture", path, "--timeout", "1", "--quiet"])
        runner = waitlib.Runner(path)
        poller = waitlib.Poller(script, runner)
        output = io.StringIO()
        with patch.object(waitlib, "launch_log"), contextlib.redirect_stdout(output):
            with self.assertRaises(SystemExit) as stopped:
                poller.run(["tool", "check"])
        self.assertEqual(stopped.exception.code, 3)
        self.assertEqual(json.loads(output.getvalue())["event"], "timeout")
        self.assertEqual(runner.run(["tool", "check"]), (0, "recovered", ""))
        self.assertEqual(script.clock.now(), 0)

    def test_fixture_file_miss_never_reads_disk(self):
        with tempfile.NamedTemporaryFile("w", delete=False) as fixture:
            json.dump({"responses": [], "files": {}}, fixture)
            path = fixture.name
        self.addCleanup(os.unlink, path)
        with self.assertRaisesRegex(FileNotFoundError, "fixture has no file"):
            waitlib.Runner(path).text(__file__)


if __name__ == "__main__":
    unittest.main()
