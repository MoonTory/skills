#!/usr/bin/env python3
"""Shared command, clock, output, and API helpers for agent-scripts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shlex
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path
from typing import Any, NoReturn

EXIT_OK = 0
EXIT_GONE = 2
EXIT_TIMEOUT = 3
EXIT_TOOL = 4


def backoff(failures: int, interval: float) -> float:
    return min(interval * 2 ** (failures - 1), 300)


class Clock:
    def __init__(self, fixture: bool = False):
        self.fixture = fixture
        self._value = 0.0 if fixture else time.monotonic()
        self._wall = dt.datetime(2000, 1, 1, tzinfo=dt.timezone.utc) if fixture else None

    def now(self) -> float:
        return self._value if self.fixture else time.monotonic()

    def sleep(self, seconds: float) -> None:
        if self.fixture:
            self._value += seconds
        else:
            time.sleep(seconds)

    def timestamp(self) -> str:
        instant = self._wall + dt.timedelta(seconds=self._value) if self._wall else dt.datetime.now(dt.timezone.utc)
        return instant.isoformat(timespec="seconds").replace("+00:00", "Z")


class FixtureProcess:
    def __init__(self, response: dict[str, Any]):
        self.response = response
        self.returncode: int | None = None
        self._polls = int(response.get("polls", 0))
        self._count = 0
        self.terminated = False

    def poll(self) -> int | None:
        if self.terminated:
            return self.returncode
        if self._count < self._polls:
            self._count += 1
            return None
        self.returncode = int(self.response.get("exit", 0))
        return self.returncode

    def communicate(self) -> tuple[str, str]:
        return str(self.response.get("stdout", "")), str(self.response.get("stderr", ""))

    def terminate(self) -> None:
        self.terminated = True
        self.returncode = -15


class Runner:
    def __init__(self, fixture: str | None = None):
        self.fixture_path = fixture
        self.fixture: dict[str, Any] = {}
        self._responses: list[dict[str, Any]] = []
        self._index = 0
        if fixture:
            with open(fixture, encoding="utf-8") as handle:
                self.fixture = json.load(handle)
            self._responses = self.fixture.get("responses", [])

    @property
    def is_fixture(self) -> bool:
        return self.fixture_path is not None

    def _next(self, argv: list[str]) -> dict[str, Any]:
        if self._index >= len(self._responses):
            raise AssertionError(f"no fixture response left for: {shlex.join(argv)}")
        response = self._responses[self._index]
        self._index += 1
        built = shlex.join(argv)
        recorded = str(response.get("cmd", ""))
        if not recorded.startswith(built):
            raise AssertionError(f"fixture command mismatch\nbuilt: {built}\nrecorded: {recorded}")
        return response

    def run(self, argv: list[str], timeout: float = 30) -> tuple[int, str, str]:
        if self.is_fixture:
            response = self._next(argv)
            return int(response.get("exit", 0)), str(response.get("stdout", "")), str(response.get("stderr", ""))
        try:
            completed = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, check=False)
            return completed.returncode, completed.stdout, completed.stderr
        except (OSError, subprocess.TimeoutExpired) as error:
            return 127, "", str(error)

    def start(self, argv: list[str]) -> subprocess.Popen[str] | FixtureProcess:
        if self.is_fixture:
            return FixtureProcess(self._next(argv))
        return subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def _fixture_key(self, values: dict[str, Any], path: str) -> str | None:
        if path in values:
            return path
        home = str(Path.home())
        abbreviated = f"~{path[len(home):]}" if path.startswith(home) else path
        return abbreviated if abbreviated in values else None

    def text(self, path: str) -> str:
        files = self.fixture.get("files", {})
        key = self._fixture_key(files, path) if self.is_fixture else None
        if key is not None:
            value = files[key]
            return value if isinstance(value, str) else "\n".join(json.dumps(line) for line in value) + "\n"
        if self.is_fixture:
            raise FileNotFoundError(f"fixture has no file: {path}")
        return Path(path).read_text(encoding="utf-8")

    def mtime(self, path: str) -> float:
        mtimes = self.fixture.get("mtimes", {})
        key = self._fixture_key(mtimes, path) if self.is_fixture else None
        if key is not None:
            return float(mtimes[key])
        if self.is_fixture:
            raise FileNotFoundError(f"fixture has no mtime: {path}")
        return os.stat(path).st_mtime


class Script:
    def __init__(self, name: str, target: str = "", *, timeout: float = 60, interval: float = 2):
        self.name = name
        self.target = target
        self.parser = argparse.ArgumentParser(prog=name)
        self.parser.add_argument("--timeout", type=float, default=timeout)
        self.parser.add_argument("--interval", type=float, default=interval)
        self.parser.add_argument("--fixture")
        self.parser.add_argument("--quiet", action="store_true")
        self.parser.add_argument("--pretty", action="store_true")
        self.parser.add_argument("--brief")
        self.args: argparse.Namespace | None = None
        self.clock = Clock()
        self.started = self.clock.now()
        self.command = shlex.join(sys.argv)

    def parse(self, argv: list[str] | None = None) -> argparse.Namespace:
        self.args = self.parser.parse_args(argv)
        self.clock = Clock(bool(self.args.fixture))
        self.started = self.clock.now()
        return self.args

    def progress(self, message: str) -> None:
        if not self.args or not self.args.quiet:
            print(f"{self.name}: {message}", file=sys.stderr)

    def envelope(self, event: str, detail: Any) -> dict[str, Any]:
        elapsed = max(0, self.clock.now() - self.started)
        elapsed_value: int | float = int(elapsed) if elapsed.is_integer() else round(elapsed, 3)
        return {
            "script": self.name,
            "event": event,
            "target": self.target,
            "elapsed_s": elapsed_value,
            "at": self.clock.timestamp(),
            "detail": detail,
        }

    def emit(self, event: str, detail: Any) -> dict[str, Any]:
        envelope = self.envelope(event, detail)
        if self.args and self.args.pretty:
            print(f"{self.name}: {event} after {envelope['elapsed_s']} s")
        else:
            print(json.dumps(envelope, separators=(",", ":"), ensure_ascii=False))
        launch_log(self.args.brief if self.args else None, {
            "ts": envelope["at"], "script": self.name, "target": self.target,
            "event": event, "elapsed_s": envelope["elapsed_s"], "command": self.command,
        })
        return envelope

    def fail(self, code: int, event: str, detail: Any) -> NoReturn:
        self.emit(event, detail)
        raise SystemExit(code)


class Poller:
    """Apply one progress, backoff, and failure-cutoff policy to polling calls."""

    def __init__(self, script: Script, runner: Runner):
        self.script = script
        self.runner = runner
        self.failures = 0
        self.deadline = script.started + max(0, script.args.timeout)

    def progress(self, target: str) -> None:
        self.script.progress(f"poll {target}")

    def succeeded(self) -> None:
        self.failures = 0

    def failure(self, error: str) -> None:
        self.failures += 1
        detail = {"error": error.strip()}
        if self.failures >= 5 or self.script.args.timeout == 0:
            self.script.fail(EXIT_TOOL, "tool-failure", detail)
        delay = backoff(self.failures, self.script.args.interval)
        remaining = self.deadline - self.script.clock.now()
        if remaining <= 0 or delay >= remaining:
            self.script.fail(EXIT_TIMEOUT, "timeout", detail)
        self.script.progress(f"tool failure {self.failures}/5; retry in {delay:g} s: {error.strip()}")
        self.script.clock.sleep(min(delay, remaining))

    def run(
        self,
        argv: list[str],
        timeout: float = 30,
        accepted_codes: set[int] | None = None,
    ) -> tuple[int, str, str]:
        accepted = accepted_codes or {0}
        while True:
            self.progress(shlex.join(argv))
            code, stdout, stderr = self.runner.run(argv, timeout=timeout)
            if code in accepted:
                self.succeeded()
                return code, stdout, stderr
            if gone_error(stderr) or (code == 1 and timeout_error(stderr)):
                return code, stdout, stderr
            self.failure(stderr)

    def start(self, argv: list[str]) -> subprocess.Popen[str] | FixtureProcess:
        self.progress(shlex.join(argv))
        return self.runner.start(argv)


def timeout_error(stderr: str) -> bool:
    lowered = stderr.lower()
    return "timed out" in lowered or "timeout" in lowered


def pane_lines(poller: Poller, pane: str, source: str = "recent-unwrapped") -> tuple[int, list[str], str]:
    code, stdout, stderr = poller.run(["herdr", "pane", "read", pane, "--source", source])
    return code, stdout.splitlines(), stderr


def wait_for_output(
    script: Script,
    poller: Poller,
    pane: str,
    *,
    match: str | None = None,
    regex: str | None = None,
    source: str = "recent-unwrapped",
    timeout: float,
    baseline: list[str] | None = None,
) -> tuple[int, Any, str]:
    if baseline is None:
        code, baseline, stderr = pane_lines(poller, pane, source)
        if code != 0:
            return code, {}, stderr
    baseline_count = len(baseline)
    deadline = script.clock.now() + timeout
    argv = ["herdr", "pane", "wait-output", pane]
    argv += ["--regex", regex] if regex is not None else ["--match", str(match)]
    argv += ["--source", source, "--timeout", str(int(max(0, timeout) * 1000))]
    code, stdout, stderr = poller.run(argv, timeout=max(timeout + 5, 5))
    if code != 0:
        return code, {}, stderr
    try:
        detail = json_result(stdout)
    except (ValueError, TypeError) as error:
        poller.failure(str(error))
        return wait_for_output(
            script, poller, pane, match=match, regex=regex, source=source,
            timeout=max(0, deadline - script.clock.now()), baseline=baseline,
        )
    matched_line = detail.get("matched_line") if isinstance(detail, dict) else None
    read = detail.get("read", {}) if isinstance(detail, dict) else {}
    current = str(read.get("text", "")).splitlines()
    matcher = (lambda line: re.search(regex, line) is not None) if regex is not None else (lambda line: str(match) in line)
    if matched_line is None or any(matcher(line) for line in current[baseline_count:]):
        return 0, detail, ""
    script.progress("ignored match from output present before the wait")
    while script.clock.now() < deadline:
        script.clock.sleep(min(script.args.interval, max(0, deadline - script.clock.now())))
        code, current, stderr = pane_lines(poller, pane, source)
        if code != 0:
            return code, {}, stderr
        for line in current[baseline_count:]:
            if matcher(line):
                if isinstance(detail, dict):
                    detail["matched_line"] = line
                return 0, detail, ""
    return 1, {}, "timed out"


def launch_log(brief: str | None, row: dict[str, Any]) -> None:
    path = Path(f"{brief}.launch") if brief else Path(os.environ.get("TMPDIR", tempfile.gettempdir())) / "agent-scripts" / "waits.log"
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ("ts", "script", "target", "event", "elapsed_s", "command")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\t".join(str(row.get(field, "")) for field in fields) + "\n")


def json_result(stdout: str) -> Any:
    value = json.loads(stdout)
    return value.get("result", value) if isinstance(value, dict) else value


def gone_error(stderr: str) -> bool:
    lowered = stderr.lower()
    return "pane_not_found" in lowered or "not found" in lowered or "not_found" in lowered


class HerdrSocket:
    def __init__(self, path: str | None = None):
        self.path = os.path.expanduser(path or os.environ.get("HERDR_SOCKET_PATH", "~/.config/herdr/herdr.sock"))

    def request(self, method: str, params: dict[str, Any], timeout_ms: int = 30_000) -> Any:
        payload = json.dumps({"method": method, "params": params}).encode() + b"\n"
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.settimeout(timeout_ms / 1000)
            client.connect(self.path)
            client.sendall(payload)
            chunks = bytearray()
            while not chunks.endswith(b"\n"):
                part = client.recv(65536)
                if not part:
                    break
                chunks.extend(part)
        response = json.loads(chunks)
        if response.get("error"):
            error = response["error"]
            raise RuntimeError(f"{error.get('code')}: {error.get('message', '')}")
        return response.get("result")


class LinearApi:
    def __init__(self, key: str):
        self.key = key

    def query(self, gql: str, variables: dict[str, Any]) -> Any:
        body = json.dumps({"query": gql, "variables": variables}).encode()
        request = urllib.request.Request(
            "https://api.linear.app/graphql", data=body,
            headers={"Authorization": self.key, "Content-Type": "application/json"}, method="POST",
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
        if result.get("errors"):
            raise RuntimeError(json.dumps(result["errors"]))
        return result.get("data")
