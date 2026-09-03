import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/agent-answer"
FIXTURES = ROOT / "fixtures/agent-answer"


class AgentAnswerTests(unittest.TestCase):
    def call(self, case, source, value):
        return subprocess.run([SCRIPT, source, value, "--fixture", FIXTURES / f"{case}.json", "--quiet"], text=True, capture_output=True)

    def test_pi_answer(self):
        result = self.call("pi_answer", "--pane", "p1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines()[0], "final answer")
        self.assertEqual(json.loads(result.stdout.splitlines()[-1])["event"], "answer")

    def test_claude_answer(self):
        result = self.call("claude_answer", "--session", "/claude.jsonl")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("claude answer", result.stdout)

    def test_truncated(self):
        result = self.call("truncated", "--session", "/truncated.jsonl")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout.splitlines()[-1])["event"], "truncated")


if __name__ == "__main__":
    unittest.main()
