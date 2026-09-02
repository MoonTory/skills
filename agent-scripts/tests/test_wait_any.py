import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/wait-any"
FIXTURES = ROOT / "fixtures/wait-any"


def run(case):
    return subprocess.run([SCRIPT, "--pane", "p1", "--pane", "p2", "--fixture", FIXTURES / f"{case}.json", "--quiet"], text=True, capture_output=True)


class WaitAnyTests(unittest.TestCase):
    def test_first_wins(self):
        result = run("first_wins")
        self.assertEqual(result.returncode, 0, result.stderr)
        envelope = json.loads(result.stdout)
        self.assertEqual(envelope["target"], "pane:p1")
        self.assertEqual(envelope["detail"]["pending"], ["pane:p2"])

    def test_timeout(self):
        result = run("timeout")
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["event"], "timeout")

    def test_tool_failure_recovers(self):
        result = run("tool_recovered")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["target"], "pane:p1")


if __name__ == "__main__":
    unittest.main()
