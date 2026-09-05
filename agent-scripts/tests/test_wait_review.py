import contextlib
import io
import json
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/wait-review"
FIXTURES = ROOT / "fixtures/wait-review"
MAIN = runpy.run_path(str(SCRIPT))["main"]


def lines(result):
    return [json.loads(line) for line in result.stdout.splitlines()]


def events(result):
    return [line["event"] for line in lines(result)]


def run(case, *extra):
    argv = [
        str(SCRIPT), "--pr", "57", "--repo", "acme/widgets",
        "--fixture", str(FIXTURES / f"{case}.json"), "--quiet", *extra,
    ]
    stdout, stderr = io.StringIO(), io.StringIO()
    code = 0
    with patch.object(sys, "argv", argv), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try:
            MAIN()
        except SystemExit as error:
            code = error.code
    return SimpleNamespace(returncode=code, stdout=stdout.getvalue(), stderr=stderr.getvalue())


class WaitReviewTests(unittest.TestCase):
    def test_baseline(self):
        result = run("baseline", "--timeout", "0")
        output_lines = lines(result)
        self.assertEqual(len(output_lines), 1)
        output = output_lines[0]
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output["event"], "baseline")
        self.assertEqual(output["target"], "pr:57")
        self.assertEqual(output["detail"], {
            "threads": 1, "reviews": 1, "review_decision": "REVIEW_REQUIRED",
        })

    def test_new_threads(self):
        result = run("threads_new")
        output = lines(result)
        final = output[-1]
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(events(result), ["watching", "thread", "thread", "threads"])
        self.assertEqual(output[0]["detail"], {
            "threads": 0, "reviews": 0, "review_decision": "REVIEW_REQUIRED",
        })
        self.assertEqual([line["detail"] for line in output[1:3]], final["detail"]["threads"])
        self.assertEqual(final["detail"], {
            "threads": [
                {
                    "id": "t-gustavo", "author": "gustavo", "path": "src/main.py",
                    "line": 42, "body": "Please rename this.",
                    "url": "https://github.com/acme/widgets/pull/57#discussion-1",
                },
                {
                    "id": "t-copilot", "author": "copilot-pull-request-reviewer[bot]",
                    "path": "src/util.py", "line": None, "body": "Handle the empty case.",
                    "url": "https://github.com/acme/widgets/pull/57#discussion-2",
                },
            ],
            "review_decision": "REVIEW_REQUIRED",
        })

    def test_malformed_json_hits_tool_failure_cutoff(self):
        result = run("malformed_json")
        self.assertEqual(result.returncode, 4)
        self.assertEqual(lines(result)[-1]["event"], "tool-failure")

    def test_reopened_fixture_starts_with_the_thread_resolved(self):
        fixture = json.loads((FIXTURES / "threads_reopened.json").read_text())
        first = next(r for r in fixture["responses"] if r["cmd"].startswith("gh api graphql"))
        nodes = json.loads(first["stdout"])["data"]["repository"]["pullRequest"]["reviewThreads"]["nodes"]
        self.assertEqual([(n["id"], n["isResolved"]) for n in nodes], [("t-reopen", True)])

    def test_baseline_file_written_when_first_poll_is_merged(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "baseline.json"
            result = run("merged", "--baseline", str(path))
            self.assertEqual(result.returncode, 2)
            self.assertTrue(path.exists())

    def test_reopened_thread(self):
        result = run("threads_reopened")
        output = lines(result)[-1]
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output["event"], "threads")
        self.assertEqual(output["detail"]["threads"][0]["id"], "t-reopen")

    def test_thread_resolved_after_baseline(self):
        result = run("thread_resolved_after_baseline", "--timeout", "60")
        output = lines(result)
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertEqual(events(result), ["watching", "thread-resolved", "timeout"])
        self.assertEqual(output[1]["detail"], {"id": "t-existing"})

    def test_thread_resolved_between_polls_times_out(self):
        result = run("thread_resolved_between_polls", "--timeout", "60")
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertEqual(events(result), ["watching", "timeout"])

    def test_changes_requested(self):
        result = run("changes_requested")
        output = lines(result)[-1]
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(events(result), ["watching", "changes_requested"])
        self.assertEqual(output["detail"], {
            "review_id": "r-changes", "author": "carol",
            "review_decision": "CHANGES_REQUESTED",
        })

    def test_approved(self):
        result = run("approved")
        output = lines(result)[-1]
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(events(result), ["watching", "approved"])
        self.assertEqual(output["detail"], {
            "review_id": "r-approved", "author": "dana", "review_decision": "APPROVED",
        })

    def test_merged(self):
        result = run("merged")
        output = lines(result)[-1]
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(events(result), ["watching", "merged"])
        self.assertEqual(output["detail"], {"sha": "merge789"})

    def test_closed(self):
        result = run("closed")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(lines(result)[-1]["event"], "closed")

    def test_tool_failure_recovers(self):
        result = run("tool_recovered")
        output = lines(result)[-1]
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output["event"], "approved")
        self.assertEqual(output["elapsed_s"], 60)

    def test_baseline_file_is_written_once_and_read_back(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "review-baseline.json"
            first = run("baseline_file", "--baseline", str(path), "--timeout", "0")
            written = path.read_text(encoding="utf-8")
            path.chmod(0o444)
            second = run("baseline_file", "--baseline", str(path), "--timeout", "0")
            after = path.read_text(encoding="utf-8")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(written, after)
        self.assertEqual(written, (
            '{"review_decision": "REVIEW_REQUIRED", "reviews": ["r-existing"], '
            '"threads": {"t-existing": false}}\n'
        ))
        self.assertEqual(lines(second)[-1]["detail"], {
            "threads": 1, "reviews": 1, "review_decision": "REVIEW_REQUIRED",
        })


if __name__ == "__main__":
    unittest.main()
