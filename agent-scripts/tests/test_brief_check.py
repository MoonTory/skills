import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/brief-check"
FIXTURES = ROOT / "fixtures/brief-check"


def run(case):
    return subprocess.run([SCRIPT, "--brief", "/tmp/agent-scripts-test-brief.md", "--fixture", FIXTURES / f"{case}.json", "--quiet"], text=True, capture_output=True)


class BriefCheckTests(unittest.TestCase):
    def test_complete(self):
        result = run("complete")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["event"], "ok")

    def test_missing_two(self):
        result = run("missing_two")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["detail"]["fields"], ["verify", "timebox"])


if __name__ == "__main__":
    unittest.main()
