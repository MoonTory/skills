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

    def test_closed_uses_pane_list_not_tab_get(self):
        fixture = json.loads((FIXTURES / "closed.json").read_text())
        self.assertNotIn("panes", json.loads(fixture["responses"][0]["stdout"])["result"]["tab"])
        self.assertEqual(fixture["responses"][1]["cmd"], "herdr pane list")

    def test_gone(self):
        result = run("gone")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["event"], "gone")

    def test_forced(self):
        result = run("forced", "--force")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["detail"]["panes"], 2)

    def test_bad_tab_list_is_tool_failure(self):
        result = run("bad_tab_list", "--force")
        self.assertEqual(result.returncode, 4)
        self.assertEqual(json.loads(result.stdout)["event"], "tool-failure")

    def test_busy(self):
        result = run("busy")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["event"], "busy")


if __name__ == "__main__":
    unittest.main()
