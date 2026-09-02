import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/close-track"
FIXTURES = ROOT / "fixtures/close-track"


def run(case, *extra):
    return subprocess.run([SCRIPT, "--tab", "t1", "--fixture", FIXTURES / f"{case}.json", "--quiet", *extra], text=True, capture_output=True)


class CloseTrackTests(unittest.TestCase):
    def test_closed(self):
        result = run("closed")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["detail"]["panes"], 2)

    def test_busy(self):
        result = run("busy")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["event"], "busy")


if __name__ == "__main__":
    unittest.main()
